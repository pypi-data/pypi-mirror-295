# container.py
# Copyright (C) 2022-2024 Red Hat, Inc.
#
# Authors:
#   Akira TAGOH  <tagoh@redhat.com>
#
# Permission is hereby granted, without written agreement and without
# license or royalty fees, to use, copy, modify, and distribute this
# software and its documentation for any purpose, provided that the
# above copyright notice and the following two paragraphs appear in
# all copies of this software.
#
# IN NO EVENT SHALL THE COPYRIGHT HOLDER BE LIABLE TO ANY PARTY FOR
# DIRECT, INDIRECT, SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES
# ARISING OUT OF THE USE OF THIS SOFTWARE AND ITS DOCUMENTATION, EVEN
# IF THE COPYRIGHT HOLDER HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH
# DAMAGE.
#
# THE COPYRIGHT HOLDER SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING,
# BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
# FITNESS FOR A PARTICULAR PURPOSE.  THE SOFTWARE PROVIDED HEREUNDER IS
# ON AN "AS IS" BASIS, AND THE COPYRIGHT HOLDER HAS NO OBLIGATION TO
# PROVIDE MAINTENANCE, SUPPORT, UPDATES, ENHANCEMENTS, OR MODIFICATIONS.
"""Module to build a container image for fontquery."""

import glob
import sys
import os
import importlib.metadata
import re
import subprocess
import shutil
import tempfile
from importlib.resources import files
from pathlib import Path

try:
    FQ_SCRIPT_PATH = files('fontquery.scripts')
except ModuleNotFoundError:
    FQ_SCRIPT_PATH = Path(__file__).parent / 'scripts'
try:
    FQ_DATA_PATH = files('fontquery.data')
except ModuleNotFoundError:
    FQ_DATA_PATH = Path(__file__).parent / 'data'
try:
    FQ_VERSION = importlib.metadata.version('fontquery')
except ModuleNotFoundError:
    import tomli
    tomlfile = Path(__file__).parent.parent / 'pyproject.toml'
    with open(tomlfile, 'rb', encoding='utf-8') as f:
        FQ_VERSION = tomli.load(f)['project']['version']


class ContainerImage:
    """Container helper"""

    def __init__(self, product: str, version: str, verbose: bool = False):
        self.__product = product
        self.__version = version
        self.__target = None
        self.__verbose = verbose
        if product == 'fedora':
            if version == 'eln':
                self.__registry = 'quay.io/fedoraci/fedora'
            else:
                self.__registry = 'quay.io/fedora/fedora'
        elif product == 'centos':
            self.__registry = 'quay.io/centos/centos'
            if re.match(r'\d+(\-development)?$', version):
                self.__version = 'stream' + version
        else:
            raise RuntimeError('Unknown product')

    def _get_namespace(self) -> str:
        if not self.__target:
            raise RuntimeError('No target is set')
        return f'fontquery/{self.__product}/{self.__target}:{self.__version}'

    def _get_fullnamespace(self) -> str:
        return f'ghcr.io/fedora-i18n/{self._get_namespace()}'

    @property
    def target(self) -> str:
        return self.__target

    @target.setter
    def target(self, v: str) -> None:
        self.__target = v

    def exists(self, remote=True) -> bool:
        """Whether the image is available or not"""
        if not remote:
            cmdline = [
                'buildah', 'images', self._get_fullnamespace()
            ]
        else:
            cmdline = [
                'buildah', 'pull', self._get_fullnamespace()
            ]
        if self.__verbose:
            print('# ' + ' '.join(cmdline), file=sys.stderr)
        try:
            subprocess.run(cmdline, check=True)
        except subprocess.CalledProcessError:
            return False
        return True

    def pull(self, *args, **kwargs) -> bool:
        cmdline = [
            'podman', 'pull', self._get_fullnamespace()
        ]
        if self.__verbose:
            print('# ' + ' '.join(cmdline))
        if not ('try_run' in kwargs and kwargs['try_run']):
            ret = subprocess.run(cmdline, check=False)
            return ret.returncode == 0

        return True

    def build(self, *args, **kwargs) -> bool:
        """Build an image"""
        retval = True
        if self.exists(remote=False):
            print(f'Warning: {self._get_namespace()} is already'
                  ' available on local. '
                  'You may want to remove older images manually.',
                  file=sys.stderr)
        with tempfile.TemporaryDirectory() as tmpdir:
            abssetup = FQ_SCRIPT_PATH.joinpath('fontquery-setup.sh')
            setup = str(abssetup.name)
            devpath = Path(__file__).parents[1]
            sdist = str(devpath / 'dist' / f'fontquery-{FQ_VERSION}*.whl')
            dist = '' if 'debug' not in kwargs or not kwargs['debug']\
                else glob.glob(sdist)[0]
            containerfile = str(FQ_DATA_PATH.joinpath('Containerfile'))
            if dist:
                # Use all files from development
                containerfile = str(devpath / 'fontquery' / 'data' /
                                    'Containerfile')
                abssetup = str(devpath / 'fontquery' / 'scripts' /
                               'fontquery-setup.sh')
                shutil.copy2(dist, tmpdir)
            shutil.copy2(abssetup, tmpdir)
            cmdline = [
                'buildah', 'build', '-f', containerfile,
                '--build-arg', f'registry={self.__registry}',
                '--build-arg', f'release={self.__version}',
                '--build-arg', f'setup={setup}',
                '--build-arg', f'dist={Path(dist).name}',
                '--target', self.target, '-t',
                f'ghcr.io/fedora-i18n/{self._get_namespace()}',
                tmpdir
            ]
            if self.__verbose:
                print('# ' + ' '.join(cmdline))
            if not ('try_run' in kwargs and kwargs['try_run']):
                ret = subprocess.run(cmdline, cwd=tmpdir, check=False)
                retval = ret.returncode == 0

        return retval

    def update(self, *args, **kwargs) -> bool:
        """Update an image"""
        if not self.exists(remote=True):
            raise RuntimeError("Image isn't yet available. "
                               f"try build first: {self._get_namespace()}")
        cname = f'fontquery-{os.getpid()}'
        cmdline = [
            'podman', 'run', '-ti', '--name', cname,
            self._get_fullnamespace(),
            '-m', 'checkupdate'
        ]
        cleancmdline = [
            'podman', 'rm', cname
        ]
        if self.__verbose:
            print('# ' + ' '.join(cmdline))
        if not ('try_run' in kwargs and kwargs['try_run']):
            try:
                res = subprocess.run(cmdline, check=False)
                if res.returncode != 0:
                    subprocess.run(cleancmdline, check=False)
                    cmdline[-1] = 'update'
                    if self.__verbose:
                        print('# ' + ' '.join(cmdline))
                    res = subprocess.run(cmdline, check=False)
                    if res.returncode == 0:
                        cmdline = [
                            'podman', 'commit', cname,
                            self._get_fullnamespace()
                        ]
                        res = subprocess.run(cmdline, check=False)
                        if res.returncode == 0:
                            print('** Image has been changed.')
                        else:
                            print('** Failed to change image.')
                            return False
                    else:
                        print('** Updating image failed.')
                        return False
                else:
                    print('** No updates available')
            finally:
                if self.__verbose:
                    print('# ' + ' '.join(cleancmdline))
                subprocess.run(cleancmdline, check=False)

        return True

    def clean(self, *args, **kwargs) -> None:
        """Clean up an image"""
        if not self.exists(remote=False):
            print(f"Warning: {self._get_namespace()} isn't available on local. "
                  "You don't need to clean up.",
                  file=sys.stderr)
            return
        cmdline = [
            'buildah', 'rmi',
            f'ghcr.io/fedora-i18n/{self._get_namespace()}'
        ]
        if self.__verbose:
            print('# ' + ' '.join(cmdline))
        if not ('try_run' in kwargs and kwargs['try_run']):
            subprocess.run(cmdline, check=False)

    def push(self, *args, **kwargs) -> bool:
        """Publish an image to registry"""
        if not self.exists(remote=False):
            print(f"Warning: {self._get_namespace()} isn't"
                  " available on local.")
            return False
        cmdline = [
            'buildah', 'push',
            f'ghcr.io/fedora-i18n/{self._get_namespace()}'
        ]
        if self.__verbose:
            print('# ' + ' '.join(cmdline))
        if not ('try_run' in kwargs and kwargs['try_run']):
            ret = subprocess.run(cmdline, check=False)
            return ret.returncode == 0

        return True

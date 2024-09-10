#!/usr/bin/env python3

import os
import sys
import pathlib
import json
import yaml
from six import StringIO  # Python 2 and 3 compatible

from conans.client.userio import UserIO
from conans.client.output import ConanOutput
from conans.client.conan_api import Conan
from conans.client.command import Command
from conans.client.cache.remote_registry import CONAN_CENTER_REMOTE_NAME
from conans.util.files import save
from conans.model.ref import ConanFileReference, get_reference_fields
from conan.tools.scm import Version


def in_docker():
    return os.path.exists("/.dockerenv")


def yaml_load(f):
    if (Version(yaml.__version__) < Version("5.1")):
        return yaml.load(f)
    else:
        return yaml.full_load(f)


class Niobuild:
    remote_name = "zhihe"
    conan_artifactory = 'http://10.0.11.10:8081/artifactory/api/conan/conan-local'
    conan_user = 'riscv.sdk'
    conan_api_key = 'cmVmdGtuOjAxOjE3NTU3NDQ4OTU6M0VtZmRVZGxjOEpMcWdmVE9xYlhQR0ZySzFH'

    def __init__(self):
        self.conan_api = Conan(output=ConanOutput(StringIO()))
        self.command = Command(self.conan_api)
        self.conan_api.create_app()
        if not in_docker():
            self.conan_api.config_init()
            for remote in self.conan_api.remote_list():
                if remote.name == CONAN_CENTER_REMOTE_NAME:
                    self.conan_api.remote_remove(CONAN_CENTER_REMOTE_NAME)
                    break
            self.update_remote(self.remote_name, self.conan_artifactory, self.conan_user, self.conan_api_key)
            self.gen_hook()
        try:
            split_char = '/'
            try:
                idx = sys.argv.index("version")
                version = sys.argv[idx + 1]
                sel4_sdk_version, release_candidate = version.split(split_char)
                self.set_version(sel4_sdk_version, release_candidate)
            except:
                pass
            self.user = self.conan_api.app.cache.config.get_item('sel4sdk.version')
            self.channel = self.conan_api.app.cache.config.get_item('sel4sdk.channel')
        except:
            self.user, self.channel = None, None
        self.install_zbuild()

    def update_remote(self, remote_name, remote_url, user_name, user_api_key):
        try:
            info = self.conan_api.users_list(remote_name)
        except:
            self.conan_api.remote_add(remote_name, remote_url)
            self.conan_api.user_set(user_name, remote_name)
            info = self.conan_api.users_list(remote_name)
        for remote in info['remotes']:
            if remote['name'] == remote_name and not remote['authenticated']:
                self.conan_api.authenticate(user_name, user_api_key, remote_name)
                break
        self.conan_api.users_list(remote_name)['remotes'][0]['authenticated']

    def set_version(self, user, channel):
        if user == '_' or channel == '_' or not user or not channel:
            if self.conan_api.app.cache.config.has_section('sel4sdk'):
                self.conan_api.app.cache.config.rm_item('sel4sdk')
        else:
            self.conan_api.app.cache.config.set_item('sel4sdk.version', user)
            self.conan_api.app.cache.config.set_item('sel4sdk.channel', channel)

    def new_reference(self, text) -> ConanFileReference:
        name, version, user, channel, revision = get_reference_fields(text)
        version = version or '*'
        user = user or self.user
        channel = channel or self.channel
        return ConanFileReference(name, version, user, channel, revision)

    def gen_hook(self):
        complete_hook = """
import os

def pre_source(output, conanfile, conanfile_path, **kwargs):
    conanfile = os.path.join(conanfile.source_folder, "conanfile.py")
    if os.path.exists(conanfile):
        os.rename(conanfile, conanfile + '.bak')

def post_source(output, conanfile, conanfile_path, **kwargs):
    conanfile1 = os.path.join(conanfile.source_folder, "conanfile.py.bak")
    conanfile2 = os.path.join(conanfile.source_folder, "conanfile.py")
    if os.path.exists(conanfile1):
        os.rename(conanfile1, conanfile2)
"""
        hook_path = os.path.join(self.conan_api.app.cache.hooks_path, "hook_source.py")
        save(hook_path, complete_hook, only_if_modified=True)
        self.conan_api.app.cache.config.set_item('hooks.hook_source', None)

    def install_module(self, ref):
        try:
            info = self.conan_api.install_reference(ref, remote_name=self.remote_name, update=True, build=['missing'])
        except:
            try:
                info = self.conan_api.install_reference(ref, remote_name=self.remote_name, update=False, build=['missing'])
            except:
                return False
        if not info['error'] and 'installed' in info:
            zbuild_recipe_path = info['installed'][0]['packages'][0]['cpp_info']['rootpath']
            zbuild_recipe_path = os.path.join(zbuild_recipe_path, 'zbuild')
            if os.path.exists(zbuild_recipe_path):
                sys.path.insert(0, zbuild_recipe_path)
                from conanex import Version
                print(f"Niobuild directory: {zbuild_recipe_path}, version is {Version}\n")
                return True
        return False

    def get_output_yml(self):
        build_path = pathlib.Path('build')
        conanbuildinfo_file = build_path.joinpath('conanbuildinfo.json')
        if conanbuildinfo_file.exists():
            self.conandata_info = json.loads(conanbuildinfo_file.read_text())
            build_type = self.conandata_info['settings']['build_type']
            output_file = build_path.joinpath(build_type, 'output.yml')
            if output_file.exists():
                return output_file
        output_file = pathlib.Path('build/output.yml')
        if output_file.exists():
            return output_file
        return None

    def get_existed_build_version(self):
        output_file = self.get_output_yml()
        if output_file:
            with output_file.open() as f:
                data = yaml_load(f)
                version = data.get('sel4sdk_version', '_')
                channel = data.get('sel4sdk_channel', '_')
                return version, channel
        return None, None

    def install_zbuild(self):
        zbuild_ref_str = 'zbuild/p100@'
        # for sel4flash cmd, need to check sdk version in output.yml in build dir
        if pathlib.Path(sys.argv[0]).name in ['sel4flash']:
            user, channel = self.get_existed_build_version()
            if user == '_' or channel == '_' or (user and channel):
                self.user = user
                self.channel = channel
        zbuild_ref = self.new_reference(zbuild_ref_str)
        if not self.install_module(zbuild_ref):
            ref = ConanFileReference.loads(zbuild_ref_str, validate=False)
            self.install_module(ref)


zbuild = Niobuild()


def zbuild_main():
    from conanex import build
    build.main()


def tb_main():
    from conanex import build
    argv = ['build']
    argv.extend(sys.argv[1:])
    build.main(argv)


def sel4run_main():
    from conanex import sel4run
    sel4run.main()


def sel4flash_main():
    from conanex import sel4flash
    sel4flash.main()


def ndb_main():
    from adb import adb_debug
    adb_debug.main()


def tapnet_main():
    from conanex import tap
    tap.main()


def mkuenv_main():
    from uboot import mkimg
    mkimg.main()


def board_main():
    from conanex import board
    board.main()


def buildserver_main():
    from server import buildserver
    buildserver.main()


def mainserver_main():
    from server import mainserver
    mainserver.main()


if __name__ == '__main__':
    zbuild_main()

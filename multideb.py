# -*- coding: utf-8 -*-
"""Generate Debian packages for all installed packages

python multideb.py

You should use a `stdeb.cfg` configuration file
"""
from __future__ import unicode_literals, print_function
import argparse
import glob
from importlib import import_module
import os
import shutil
from tempfile import NamedTemporaryFile, mkdtemp

# noinspection PyPackageRequirements
from pip import get_installed_distributions
# noinspection PyPackageRequirements,PyProtectedMember
from pip._vendor.pkg_resources import Distribution
# noinspection PyPackageRequirements
from stdeb.downloader import get_source_tarball
# noinspection PyPackageRequirements
from stdeb.util import check_call

try:
    import configparser
except ImportError:
    # noinspection PyUnresolvedReferences,PyPep8Naming
    import ConfigParser as configparser

__author__ = 'Matthieu Gallet'


def normalize_package_name(name):
    return name.lower().replace('_', '-').strip()


def import_string(dotted_path):
    """
    Import a dotted module path and return the attribute/class designated by the
    last name in the path. Raise ImportError if the import failed.
    """
    module_path, sep, class_name = dotted_path.rpartition('.')
    if sep != '.':
        raise ImportError("%s doesn't look like a module path" % dotted_path)
    module = import_module(module_path)
    try:
        return getattr(module, class_name)
    except AttributeError:
        raise ImportError('Module "%s" does not define a "%s" attribute/class' % (module_path, class_name))


class TemporaryDirectory(object):
    """Create and return a temporary directory.  This has the same
    behavior as mkdtemp but can be used as a context manager.  For
    example:

        with TemporaryDirectory() as tmpdir:
            ...

    Upon exiting the context, the directory and everything contained
    in it are removed.
    """

    # noinspection PyShadowingBuiltins
    def __init__(self, suffix="", prefix='tmp', dir=None, delete=True):
        self.name = mkdtemp(suffix, prefix, dir)
        self.delete = delete

    def __repr__(self):
        return "<{} {!r}>".format(self.__class__.__name__, self.name)

    def __enter__(self):
        return self.name

    # noinspection PyUnusedLocal
    def __exit__(self, exc, value, tb):
        if self.delete:
            shutil.rmtree(self.name)


def main():
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument('--config', '-f', action='store', help='Configuration file', default='stdeb.cfg')
    args_parser.add_argument('--ignore-freeze', '-I', action='store_true', help='Add packages listed in `pip freeze`', default=False)
    args_parser.add_argument('--allow-unsafe-download', action='store_true', help='Allow unsafe downloads', default=False)
    args_parser.add_argument('--dest-dir', help='Destination dir', default='deb')
    args_parser.add_argument('--keep-temp', help='Do not remove temporary dir', default=False, action='store_true')

    args = args_parser.parse_args()
    config_parser = configparser.ConfigParser()
    config_parser.read([args.config])
    allow_unsafe_download = args.allow_unsafe_download
    ignore_freeze = args.ignore_freeze
    destination_dir = args.dest_dir

    distribution_list = {}

    if not ignore_freeze:
        installed_distributions = get_installed_distributions(local_only=True)
        for distrib in installed_distributions:
            assert isinstance(distrib, Distribution)
            distribution_list[distrib.project_name] = distrib.version

    if config_parser.has_option('multideb', 'exclude'):
        excluded_packages = {x for x in config_parser.get('multideb', 'exclude').splitlines() if x.strip()}
    else:
        excluded_packages = set()

    if config_parser.has_section('multideb-packages'):
        for option_name in config_parser.options('multideb-packages'):
            option_value = config_parser.get('multideb-packages', option_name)
            package_name, sep, package_version = option_value.partition('==')
            distribution_list[package_name] = package_version

    deb_dest_dir = os.path.abspath(destination_dir)
    if not os.path.isdir(deb_dest_dir):
        os.makedirs(deb_dest_dir)
    if excluded_packages:
        print('List of packages excluded from deb. generation:')
        for package_name in excluded_packages:
            print(package_name)
    excluded_packages = {normalize_package_name(x) for x in excluded_packages}

    # create a temp dir and do the work
    cwd = os.getcwd()
    with TemporaryDirectory(delete=not args.keep_temp) as temp_dir:
        # simplest way for storing .tar.gz files in a temp dir
        os.chdir(temp_dir)
        for package_name, package_version in distribution_list.items():
            if normalize_package_name(package_name) in excluded_packages:
                continue
            prepare_package(package_name, package_version, deb_dest_dir, config_parser, allow_unsafe_download)
    os.chdir(cwd)
    if args.keep_temp:
        print('Temporary directory: %s' % temp_dir)


def prepare_package(package_name, package_version, deb_dest_dir, multideb_config_parser, allow_unsafe_download):
    """
    :param package_name: name of the package to prepare
    :type package_name: :class:`str`
    :param package_version: version of the package to prepare
    :type package_version: :class:`str`
    :param deb_dest_dir: directory where to put created Debian packages
    :type deb_dest_dir: :class:`str`
    :param multideb_config_parser: multideb configuration file
    :type multideb_config_parser: :class:`configparser.ConfigParser`
    :param allow_unsafe_download:  allow unsafe downloads?  (see pip documentation)
    :type allow_unsafe_download: :class:`bool`
    """
    assert isinstance(multideb_config_parser, configparser.ConfigParser)
    print('downloading %s %s' % (package_name, package_version))
    filename = get_source_tarball(package_name, verbose=False, release=package_version, allow_unsafe_download=allow_unsafe_download)
    # create a Debian source
    with NamedTemporaryFile() as temp_config_file:
        # config file for each package?
        if multideb_config_parser.has_section(package_name):
            new_config_parser = configparser.ConfigParser()
            new_config_parser.add_section('DEFAULT')
            for option_name in multideb_config_parser.options(package_name):
                option_value = multideb_config_parser.get(package_name, option_name)
                new_config_parser.set('DEFAULT', option_name, option_value)
            new_config_parser.write(temp_config_file)
        temp_config_file.flush()
        if os.path.isdir('deb_dist'):
            shutil.rmtree('deb_dist')
        check_call(['py2dsc', '-x', temp_config_file.name, filename])
    # find the actual debian source dir
    directories = [x for x in os.listdir('deb_dist') if x != 'tmp_py2dsc']
    if len(directories) != 1:
        raise ValueError('Require a single directory in %s/deb_dist' % os.getcwd())
    debian_source_dir = os.path.abspath(os.path.join('deb_dist', directories[0]))
    # check if we have a post-source to execute
    if multideb_config_parser.has_option(package_name, 'post_source'):
        post_source_hook = import_string(multideb_config_parser.get(package_name, 'post_source'))
        post_source_hook(package_name, package_version, debian_source_dir)

    # build .deb from the source
    check_call(['dpkg-buildpackage', '-rfakeroot', '-uc', '-b'], cwd=debian_source_dir)

    # move the .deb to destination dir
    packages = glob.glob('deb_dist/*.deb')
    if not packages:
        raise ValueError('Unable to create %s-%s' % (package_name, package_version))
    os.rename(packages[0], os.path.join(deb_dest_dir, os.path.basename(packages[0])))


# noinspection PyUnusedLocal
def remove_tests_dir(package_name, package_version, deb_src_dir):
    """ Post source hook for removing `tests` dir """
    test_dir = os.path.join(deb_src_dir, 'tests')
    if os.path.isdir(test_dir):
        shutil.rmtree(test_dir)


if __name__ == '__main__':
    main()
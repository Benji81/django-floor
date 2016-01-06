# coding=utf-8
"""Display the current config
==========================

Display the current loaded config.
Can also generate settings.py (with `-m`) or settings.ini config files (with `--ini`).

"""
from __future__ import unicode_literals
try:
    # noinspection PyCompatibility
    from configparser import ConfigParser
except ImportError:
    # noinspection PyUnresolvedReferences,PyCompatibility
    from ConfigParser import ConfigParser
import os
import sys

from django.conf import settings
from django.core.management import BaseCommand
from django.utils.functional import cached_property
from django.utils.six import text_type, StringIO
from django.utils.translation import ugettext as _, ugettext_lazy

from djangofloor import __version__ as version
from djangofloor.iniconf import OptionParser
from djangofloor.settings import merger

__author__ = 'Matthieu Gallet'


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--merged', '-m', action='store_true', default=False,
                            help='Output a merged settings file.')
        parser.add_argument('--ini', action='store_true', default=False,
                            help='Output a sample config file.')

    def show_config(self, kind, env_variable, path):
        values = {'kind': kind, 'var': env_variable, 'path': path, }
        msg = _('%(kind)s: %(path)s') % values
        if env_variable:
            msg += _(' (defined in environment by %(var)s)') % values
        if not path:
            self.stdout.write(self.style.WARNING(msg))
        elif os.path.isfile(path):
            self.stdout.write(self.style.MIGRATE_HEADING(msg))
        else:
            self.stdout.write(self.style.ERROR(msg))

    def handle(self, *args, **options):
        project_default_conf = merger.project_settings_module.__file__
        if project_default_conf.endswith('.pyc'):
            project_default_conf = project_default_conf[:-1]
        djangofloor_default_conf = merger.default_settings_module.__file__
        if djangofloor_default_conf.endswith('.pyc'):
            djangofloor_default_conf = djangofloor_default_conf[:-1]
        all_keys = merger.default_settings_module.__dict__.copy()
        all_keys.update(merger.project_settings_module.__dict__)

        if options['ini']:
            self.config_file()
        elif options['merged']:
            self.merge(djangofloor_default_conf, project_default_conf)
        else:
            self.display_header(djangofloor_default_conf, project_default_conf)
            self.display(all_keys)

    def display_header(self, djangofloor_default_conf, project_default_conf):
        self.stdout.write('-' * 80)
        self.stdout.write(self.style.WARNING(_('Djangofloor version %(version)s') % {'version': version, }))
        self.show_config(_('Python local configuration'), 'DJANGOFLOOR_PYTHON_SETTINGS', settings.USER_SETTINGS_PATH)
        self.show_config(_('INI local configuration'), 'DJANGOFLOOR_INI_SETTINGS', settings.DJANGOFLOOR_CONFIG_PATH)
        self.show_config(_('Default project settings'), 'DJANGOFLOOR_PROJECT_DEFAULTS', project_default_conf)
        self.show_config(_('Other default settings'), None, djangofloor_default_conf)
        self.stdout.write('-' * 80)
        self.stdout.write(self.style.MIGRATE_LABEL(_('List of available settings:')))

    def merge(self, djangofloor_default_conf, project_default_conf):
        keys = [key for key in merger.settings if
                (key == key.upper() and key not in ('_', '__') and not key.endswith('_HELP'))]
        keys.sort()
        self.stdout.write('# -*- coding: utf-8 -*-\n')
        self.stdout.write('"""\n')
        self.stdout.write('Automatically generated by %s config -m \n' % sys.argv[0])
        self.stdout.write('/!\ This file should only used in development mode\n')
        self.stdout.write('Python local configuration (os.environ["%s"]) = %s' %
                          ('DJANGOFLOOR_PYTHON_SETTINGS', settings.USER_SETTINGS_PATH))
        self.stdout.write('INI local configuration (os.environ["%s"]) = %s' %
                          ('DJANGOFLOOR_INI_SETTINGS', settings.DJANGOFLOOR_CONFIG_PATH))
        self.stdout.write('Default project settings (os.environ["%s"]) = %s' %
                          ('DJANGOFLOOR_PROJECT_DEFAULTS', project_default_conf))
        self.stdout.write('Other default settings = %s' % djangofloor_default_conf)
        self.stdout.write('"""\n')
        self.stdout.write('from __future__ import unicode_literals\n')
        self.stdout.write('# This line allows to add values only in %s' % merger.project_settings_module.__file__[:-1])
        self.stdout.write('from %s import *\n' % merger.project_settings_module_name)
        lazy_cls = ugettext_lazy('').__class__
        for key in keys:
            value = merger.settings[key]
            if isinstance(value, lazy_cls):
                value = text_type(value)
            self.stdout.write('%(key)s = %(value)r\n' % {'key': key, 'value': value, })

    def config_file(self):
        parser = ConfigParser()
        for option_parser in merger.option_parsers:
            assert isinstance(option_parser, OptionParser)
            if not parser.has_section(option_parser.section):
                parser.add_section(option_parser.section)
            if option_parser.setting_name not in merger.settings:
                continue
            value = merger.settings[option_parser.setting_name]
            str_value = option_parser.to_str(value)
            parser.set(option_parser.section, option_parser.key, str_value)
        fd = StringIO()
        parser.write(fd)
        content = fd.getvalue()
        self.stderr.write('%s' % settings.DJANGOFLOOR_CONFIG_PATH)
        self.stdout.write(content)

    def force_text(self, value):
        if isinstance(value, self.lazy_cls):
            return text_type(value)
        return value

    @cached_property
    def lazy_cls(self):
        return ugettext_lazy('').__class__

    def display(self, all_keys):
        """
        :param all_keys: dictionnary of all default settings (djangofloor's and project's ones), without local settings
        :type all_keys: :class:`dict`
        """
        # keys defined in DjangoFloor defaults
        keys = set([key for key in merger.default_settings_module.__dict__
                    if key == key.upper() and key + '_HELP' in all_keys])
        # keys defined in project defaults
        keys |= set([key for key in merger.project_settings_module.__dict__
                     if key == key.upper() and key + '_HELP' in all_keys])
        # and we sort them
        keys = list(keys)
        keys.sort()

        for key in keys:
            if not all_keys[key + '_HELP']:
                continue
            default_value = self.force_text(all_keys[key])  # default value
            actual_value = self.force_text(getattr(settings, key))
            is_redefined = key in merger.user_settings_module.__dict__ or key in merger.ini_config_mapping
            is_changed = actual_value != default_value
            values = {'key': key, 'help': all_keys[key + '_HELP'], 'default': default_value, 'actual': actual_value,
                      'origin': merger.settings_origin[key], }
            if is_changed:
                self.stdout.write(self.style.WARNING('%(key)s = %(actual)r, from %(origin)s:') % values)
            elif is_redefined:
                self.stdout.write(self.style.MIGRATE_LABEL('%(key)s = %(actual)r, from %(origin)s:') % values)
            else:
                self.stdout.write(_('%(key)s = %(default)r, from %(origin)s:\n') % values)
            if default_value != actual_value:
                self.stdout.write(_('     (default value: %(default)r)') % values)
            self.stdout.write('     %(help)s\n\n' % values)
        self.stdout.write(self.style.MIGRATE_HEADING(_('Use djangofloor.utils.[DirectoryPath|FilePath]'
                                                       '("/{directory}/path") instead of "/{directory}/path"'
                                                       ' to automatically create required directories.')))

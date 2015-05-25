# coding=utf-8
from __future__ import unicode_literals
from django.conf import settings
from django.core.management import BaseCommand
from django.utils.six import u
from django.utils.translation import ugettext as _, ugettext_lazy

from djangofloor import defaults
from djangofloor.settings import project_settings as project, user_settings, ini_config_mapping


__author__ = 'flanker'


class Command(BaseCommand):
    def handle(self, *args, **options):
        lazy_cls = ugettext_lazy('').__class__
        self.stdout.write(self.style.MIGRATE_HEADING(_('Configuration file: %(path)s') % {'path': settings.USER_SETTINGS_PATH, }))
        self.stdout.write(self.style.MIGRATE_HEADING(_('.ini configuration file: %(path)s') % {'path': settings.DJANGOFLOOR_CONFIG}))
        default_conf = project.__file__
        if default_conf.endswith('.pyc'):
            default_conf = default_conf[:-1]
        self.stdout.write(self.style.MIGRATE_HEADING(_('Default values: %(path)s') % {'path': default_conf}))
        self.stdout.write('-' * 80)
        self.stdout.write(self.style.MIGRATE_LABEL(_('List of available settings:')))
        all_keys = defaults.__dict__.copy()
        all_keys.update(project.__dict__)
        keys = set([key for key in defaults.__dict__ if key == key.upper() and key + '_HELP' in all_keys])
        keys |= set([key for key in project.__dict__ if key == key.upper() and key + '_HELP' in all_keys])
        keys = list(keys)
        keys.sort()
        for key in keys:
            if not all_keys[key + '_HELP']:
                continue
            value = all_keys[key]
            is_redefined = key in user_settings.__dict__
            is_changed = is_redefined and user_settings.__dict__[key] != defaults.__dict__[key]
            if isinstance(value, lazy_cls):
                value = u(value)
            actual_value = (getattr(settings, key))
            values = {'key': key, 'help': all_keys[key + '_HELP'], 'default': value, 'actual': actual_value}
            if is_changed:
                self.stdout.write(self.style.WARNING('%(key)s = %(default)r:') % values)
            elif is_redefined:
                self.stdout.write(self.style.MIGRATE_LABEL('%(key)s = %(default)r:') % values)
            else:
                self.stdout.write(_('%(key)s = %(default)r:\n') % values)
            if value != actual_value:
                self.stdout.write(_('     (actual value: %(actual)r)') % values)
            self.stdout.write('     %(help)s\n\n' % values)

        self.stdout.write(self.style.MIGRATE_HEADING(_('Use djangofloor.utils.[DirectoryPath|FilePath]("/{directory}/path") instead of "/{directory}/path"'
                          ' to automatically create required directories.')))


if __name__ == '__main__':
    import doctest

    doctest.testmod()
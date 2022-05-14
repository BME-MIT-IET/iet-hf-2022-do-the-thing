import os
import json
import datetime
import sys
from namanager.core import Namanager
from namanager.archieve_manager import ArchieveManager
from namanager.logger import logger
import namanager.enums as enums
import namanager.util as util


def raiser(condition, msg):
    if not condition:
        raise Exception(msg)  # pragma: no cover


def test_writing_permission(**kwargs):
    """
    param dirname:
    type dirname: str
    param required: default True
    type required: True, False
    param error_msg:
    type error_msg: str
    """

    try:
        dirname = kwargs.get('dirname', os.getcwd())
        if dirname[-1] != os.sep:
            dirname += os.sep
        # test directory is exists or not and raise
        os.path.realpath(dirname)
        logger().info('dirname: {0}'.format(dirname))

        filename = ''.join([dirname, 'test_file'])
        while os.path.exists(filename):
            filename += '_'

        with open(filename, 'w') as f:
            f.write('test...')
            logger().info('successfully wrote: {0}.'.format(filename))

        with open(filename, 'r') as f:
            f.read()
            logger().info('successfully read: {0}.'.format(filename))

        os.remove(filename)

    except Exception as e:
        print(kwargs.get('error_msg', ''))
        required = kwargs.get('required', True)
        if required:
            raise e


class Driver():
    def __init__(self):
        self._result = {'errors': []}
        self._exit_code = 0

    @property
    def result(self):
        return self._result

    @property
    def exit_code(self):
        return self._exit_code

    def import_settings(self, settings_file):
        settings_json = {}
        try:
            with open(settings_file, 'r') as s:
                settings_json = json.loads(s.read())
        except Exception as e:
            file_not_found = False
            if sys.version_info[0] >= 3:
                if isinstance(e, FileNotFoundError):  # noqa: F821
                    file_not_found = True
            elif isinstance(e, IOError):  # noqa: F821
                file_not_found = True
            if file_not_found:
                self._result['errors'].append(
                    'File: {0} not found'.format(settings_file))
            else:
                raise e

        raiser(isinstance(settings_json, dict), 'settings must be dict.')

        return settings_json

    def get_src_dst_pair(self, error_info):
        # we need to move this function to/into a better place
        src_dst_pair = []

        for e in error_info:
            src_dst_pair.append([e['actual'], e['expect']])

        return src_dst_pair

    def get_bak_filename(self, **kwargs):
        prefix = kwargs.get('prefix', '')
        when = kwargs.get('when', '{:%Y%m%d%H%M%S}'.format(
            datetime.datetime.now()))

        return prefix + when + '.bak'

    def find_recent_backup_files(self, **kwargs):
        dirname = kwargs.get('dirname', os.getcwd())
        backup_files = []
        for dirpath, dirs, files in os.walk(dirname):
            for f in files:
                if f.startswith('namanager_rename_'):
                    backup_files.append(f)
            break

        return backup_files

    def revert(self, **kwargs):
        REVERT_FILE = kwargs.get('revert_file', None)
        REVERT_LAST = kwargs.get('revert_last', False)
        if REVERT_FILE is None or REVERT_LAST:
            backup_files = self.find_recent_backup_files()
            if len(backup_files) == 1:
                REVERT_FILE = backup_files[0]
            elif len(backup_files) > 1:
                if REVERT_LAST:
                    backup_files.sort(reverse=True)
                    REVERT_FILE = backup_files[0]
                else:
                    self._result['errors'].append(
                        'There are so many backup files, please specify file.')
            elif len(backup_files) == 0:
                self._result['errors'].append(
                    'No backup file are detected, please specify file.')

        try:
            am = ArchieveManager()
            with open(REVERT_FILE, 'r') as f:
                am.rename(json.loads(f.read()))
        except Exception as e:
            self._result['errors'].append(e)

    def generate_init_settings(self, **kwargs):
        INIT_PATH = kwargs.get('init_path', os.getcwd())
        settings = json.dumps(enums.SETTINGS, indent=4, sort_keys=True)
        settings_file = (os.path.join(INIT_PATH, 'settings.json')
                         if os.path.isdir(INIT_PATH)
                         else INIT_PATH)
        if os.path.exists(settings_file):
            self.result['errors'].append(
                'File existed. Cannot output settings file to {0}.\n'.format(
                    settings_file))
            return
        try:
            with open(settings_file, 'w') as f:
                f.write(settings)
        except Exception as e:
            self.result['errors'].append(
                'Cannot output settings file to {0}.\n'
                'Error: {1}'.format(
                    settings_file, e))

    def check(self, **kwargs):
        settings_json = kwargs.get('settings_json', enums.SETTINGS)
        COUNT = kwargs.get('count', False)
        FMT = kwargs.get('fmt', 'json')
        PRETTY_DUMP = kwargs.get('pretty_dump', False)
        self._result['unexpected_pairs'] = [] if FMT == 'nodump' else ''

        for d in settings_json['CHECK_DIRS']:
            if not util.isdir_casesensitive(d):
                continue

            checker = Namanager(settings_json)
            checker.check(d)

            if checker.error_info:
                unexpected_pairs = checker.error_info
                if COUNT:
                    self._result['errors'].append(
                        'In folder {0} :'.format(os.path.realpath(d)))
                    self._result['errors'].append(
                        'FAILED (error={0})'.format(checker.error_info_count))
            else:
                unexpected_pairs = []

            if FMT == 'readable':
                s = ""
                for pair in checker.get_dict(unexpected_pairs):
                    s += 'expect: {0}\n'.format(pair['expect'])
                    s += 'actual: {0}\n\n'.format(pair['actual'])
                self._result['unexpected_pairs'] += s
            elif FMT == 'json':
                self._result['unexpected_pairs'] += (
                    checker.get_json(unexpected_pairs, PRETTY_DUMP))
            elif FMT == 'xml':
                self._result['unexpected_pairs'] += (
                    checker.get_xml(unexpected_pairs, PRETTY_DUMP))
            elif FMT == 'nodump':
                self._result['unexpected_pairs'] += (
                    checker.get_dict(unexpected_pairs))

    def rename_backup(self, rename_pairs, **kwargs):
        am = ArchieveManager()
        RENAME_BACKUP = kwargs.get('rename_backup', True)
        logger().info('backup flag: {0}'.format(RENAME_BACKUP))

        if RENAME_BACKUP:
            RENAME_BACKUP_PATH = kwargs.get('rename_backup_path', os.getcwd())
            if os.path.isdir(RENAME_BACKUP_PATH):
                RENAME_BACKUP_PATH = os.sep.join([
                    RENAME_BACKUP_PATH,
                    self.get_bak_filename(prefix='namanager_rename_')])
            logger().info('backup path: {0}'.format(RENAME_BACKUP_PATH))
            test_writing_permission(
                dirname=os.path.dirname(RENAME_BACKUP_PATH))
            revert_pairs = am.gen_revert_path_pairs(rename_pairs)
            self._result['rename_backup_name'] = RENAME_BACKUP_PATH
            with open(RENAME_BACKUP_PATH, 'w') as f:
                f.write(json.dumps(revert_pairs, indent=4, sort_keys=True))
                logger().info('successfully wrote backup: {0}.'.format(
                    RENAME_BACKUP_PATH))

    def rename(self, rename_pairs, **kwargs):
        RENAME_RECOVER = kwargs.get('rename_recover', False)
        am = ArchieveManager()
        rename_pairs = self.get_src_dst_pair(rename_pairs)
        self.rename_backup(rename_pairs, **kwargs)

        error_pairs = am.rename(rename_pairs)

        if error_pairs:
            # TODO: output more information
            if RENAME_RECOVER:
                # try to directly revert all paths
                recover_pairs = am.gen_revert_path_pairs(rename_pairs)
                am.rename(recover_pairs)
                self._result['errors'].append("Failed to rename (Recovered).")

            else:
                self._result['errors'].append('Some paths can not be renamed.')

    def entry(self, **kwargs):
        REQUIRED = kwargs.get('required', False)
        VERSION = kwargs.get('version', False)
        INIT = kwargs.get('init', False)
        REVERT = kwargs.get('revert', False)
        RENAME = kwargs.get('rename', False)

        if VERSION:
            import namanager
            print(namanager.__version__)

        elif INIT:
            self.generate_init_settings(**kwargs)

        elif RENAME:
            SETTINGS = kwargs.get('settings', False)
            if SETTINGS:
                kwargs['settings_json'] = self.import_settings(SETTINGS)
            kwargs['fmt'] = 'nodump'
            self.check(**kwargs)
            self.rename(self._result['unexpected_pairs'], **kwargs)

        elif REVERT:
            self.revert(**kwargs)

        else:
            SETTINGS = kwargs.get('settings', False)
            if SETTINGS:
                kwargs['settings_json'] = self.import_settings(SETTINGS)
            self.check(**kwargs)
            print(self._result['unexpected_pairs'])

            if REQUIRED and self._result['unexpected_pairs']:
                self._exit_code = 1

        if self._result['errors']:
            for e in self._result['errors']:
                print(e)
            if REQUIRED:
                self._exit_code = 1

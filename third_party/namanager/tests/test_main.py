import os
import time
from namanager.logger import logger
import namanager.tests.helper as helper
import namanager.enums as enums
from namanager.main import Driver
# from filelock import FileLock


class TestMain():
    def __init__(self):
        self.TMPFILE_PREFIX = 'test_main_'
        self.RENAME_SUFFIX = '_*&^%$'

    def setUp(self):
        self.TMP_ROOT = helper.mkdtemp(
            root=os.path.realpath(os.path.dirname(__file__)))

    def tearDown(self):
        helper.rm_path(self.TMP_ROOT)

    def test_cli_version(self):
        driver = Driver()
        kwargs = {
            'version': True,
        }

        driver.entry(**kwargs)

        assert driver.result['errors'] == []

    def test_cli_settings(self):
        driver = Driver()
        kwargs = {
            'settings_json': {'CHECK_DIRS': ['../']},
        }

        driver.entry(**kwargs)

        assert driver.result['errors'] == []

    def temporarity_move_path(self, path):
        if os.path.exists(path):
            unique_path = path
            while os.path.exists(unique_path):
                unique_path += '-'
            os.rename(path, unique_path)
            return unique_path

    def test_cli_init_under_dir(self):
        driver = Driver()
        init_dir = helper.mkdtemps(1, root=self.TMP_ROOT,
                                   prefix=self.TMPFILE_PREFIX)[0]
        init_filename = os.sep.join([init_dir, 'settings.json'])
        recover_filename = None
        kwargs = {
            'init': True,
            'init_path': init_dir,
        }
        if os.path.exists(init_filename):
            recover_filename = self.temporarity_move_path(init_filename)

        driver.entry(**kwargs)

        assert os.path.exists(init_filename)
        assert driver.result['errors'] == []
        if recover_filename is not None:
            os.rename(recover_filename, init_filename)

    def test_cli_init_as_file(self):
        driver = Driver()
        dirs = helper.mkdtemps(1, root=self.TMP_ROOT,
                               prefix=self.TMPFILE_PREFIX)
        init_filename = os.path.join(dirs[0], '123.json')
        recover_filename = None
        kwargs = {
            'init': True,
            'init_path': init_filename,
        }
        if os.path.exists(init_filename):
            recover_filename = self.temporarity_move_path(init_filename)

        driver.entry(**kwargs)

        assert os.path.exists(init_filename)
        assert driver.result['errors'] == []
        if recover_filename is not None:
            os.rename(recover_filename, init_filename)

    def test_import_settings(self):
        driver = Driver()
        init_dir = helper.mkdtemps(1, root=self.TMP_ROOT,
                                   prefix=self.TMPFILE_PREFIX)[0]
        init_filename = os.sep.join([init_dir, 'settings.json'])
        recover_filename = None
        kwargs = {
            'init': True,
            'init_path': init_dir,
        }
        expect = enums.SETTINGS
        if os.path.exists(init_filename):
            recover_filename = self.temporarity_move_path(init_filename)

        driver.entry(**kwargs)
        actual = driver.import_settings(init_filename)

        assert helper.is_same_disorderly(expect, actual)
        assert driver.result['errors'] == []
        os.remove(init_filename)
        if recover_filename is not None:
            os.rename(recover_filename, init_filename)

    def test_cli_with_readable(self):
        driver = Driver()
        kwargs = {
            'settings_json': {'CHECK_DIRS': ['../']},
            'fmt': 'readable',
        }

        driver.entry(**kwargs)

        assert driver.result['errors'] == []

    def test_cli_with_xml(self):
        driver = Driver()
        kwargs = {
            'settings_json': {'CHECK_DIRS': ['../']},
            'fmt': 'xml',
        }

        driver.entry(**kwargs)

        assert driver.result['errors'] == []

    def test_cli_with_json(self):
        driver = Driver()
        kwargs = {
            'settings_json': {'CHECK_DIRS': ['../']},
            'fmt': 'json',
        }

        driver.entry(**kwargs)

        assert driver.result['errors'] == []

    def test_cli_xml_pretty_dump(self):
        driver = Driver()
        kwargs_xml = {
            'settings_json': {'CHECK_DIRS': ['../']},
            'fmt': 'xml',
            'pretty_dump': True,
        }

        driver.entry(**kwargs_xml)

        assert driver.result['errors'] == []

    def test_cli_json_pretty_dump(self):
        driver = Driver()
        kwargs_json = {
            'settings_json': {'CHECK_DIRS': ['../']},
            'fmt': 'json',
            'pretty_dump': True,
        }

        driver.entry(**kwargs_json)

        assert driver.result['errors'] == []

    def test_cli_rename(self):
        driver = Driver()
        dirs = helper.mkdtemps(1, root=self.TMP_ROOT,
                               prefix=self.TMPFILE_PREFIX)
        kwargs = {
            'settings_json': {
                'CHECK_DIRS': dirs,
                "DIR_FORMATS": {
                    "LETTER_CASE": "upper_case",
                    "SEP": ["dash_to_underscore"],
                },
            },
            'rename': True,
        }

        driver.entry(**kwargs)

        assert driver.result['errors'] == []

    def test_cli_rename_backup(self):
        driver = Driver()
        dirs = helper.mkdtemps(1, root=self.TMP_ROOT,
                               prefix=self.TMPFILE_PREFIX)
        kwargs = {
            'settings_json': {
                'CHECK_DIRS': dirs,
                "DIR_FORMATS": {
                    "LETTER_CASE": "upper_case",
                },
            },
            'rename': True,
            'rename_backup': True,
        }
        for backup_file in driver.find_recent_backup_files():
            os.remove(backup_file)
        assert driver.find_recent_backup_files() == []

        driver.entry(**kwargs)

        assert driver.result['errors'] == []

    def test_cli_rename_no_backup(self):
        driver = Driver()
        dirs = helper.mkdtemps(1, root=self.TMP_ROOT,
                               prefix=self.TMPFILE_PREFIX)
        kwargs = {
            'settings_json': {
                'CHECK_DIRS': dirs,
                "DIR_FORMATS": {
                    "LETTER_CASE": "upper_case",
                },
            },
            'rename': True,
            'rename_backup': False,
        }
        for backup_file in driver.find_recent_backup_files():
            os.remove(backup_file)
        assert driver.find_recent_backup_files() == []

        driver.entry(**kwargs)

        assert driver.find_recent_backup_files() == []
        assert driver.result['errors'] == []

    def test_cli_rename_backup_path(self):
        driver = Driver()
        dirs = helper.mkdtemps(1, root=self.TMP_ROOT,
                               prefix=self.TMPFILE_PREFIX)
        kwargs = {
            'settings_json': {
                'CHECK_DIRS': dirs,
                "DIR_FORMATS": {
                    "LETTER_CASE": "upper_case",
                },
            },
            'rename': True,
            'rename_backup': True,
            'rename_backup_path': dirs[0],
        }
        logger().debug('before')
        logger().info(os.listdir(dirs[0]))
        assert driver.find_recent_backup_files(dirname=dirs[0]) == []

        driver.entry(**kwargs)

        logger().debug('after')
        logger().info(driver.result['rename_backup_name'])
        if not os.path.isdir(dirs[0]):
            dirs[0] = os.sep.join(
                dirs[0].split(os.sep)[:-1] +
                [dirs[0].split(os.sep)[-1].upper()])
            assert os.path.isdir(dirs[0])
        assert driver.find_recent_backup_files(dirname=dirs[0]) != []
        assert driver.result['errors'] == []

    def test_cli_rename_backup_path_to_dir(self):
        driver = Driver()
        dirs = helper.mkdtemps(1, root=self.TMP_ROOT,
                               prefix=self.TMPFILE_PREFIX)
        kwargs = {
            'settings_json': {
                'CHECK_DIRS': dirs,
                "DIR_FORMATS": {
                    "LETTER_CASE": "upper_case",
                },
            },
            'rename': True,
            'rename_backup_path': dirs[0],
        }
        logger().debug('before')
        logger().info(os.listdir(dirs[0]))
        assert driver.find_recent_backup_files(dirname=dirs[0]) == []

        driver.entry(**kwargs)

        logger().debug('after')
        logger().info(driver.result['rename_backup_name'])
        if not os.path.isdir(dirs[0]):
            dirs[0] = os.sep.join(
                dirs[0].split(os.sep)[:-1] +
                [dirs[0].split(os.sep)[-1].upper()])
            assert os.path.isdir(dirs[0])
        assert driver.find_recent_backup_files(dirname=dirs[0]) != []
        assert driver.result['errors'] == []

    def test_cli_rename_backup_path_to_file(self):
        driver = Driver()
        dirs = helper.mkdtemps(1, root=self.TMP_ROOT,
                               prefix=self.TMPFILE_PREFIX)
        backup_filename = os.sep.join([dirs[0], '123'])
        kwargs = {
            'settings_json': {
                'CHECK_DIRS': dirs,
                "DIR_FORMATS": {
                    "LETTER_CASE": "upper_case",
                },
            },
            'rename': True,
            'rename_backup_path': backup_filename,
        }
        logger().debug('before')
        logger().info(os.listdir(dirs[0]))
        assert os.path.isdir(dirs[0])
        assert not os.path.isfile(backup_filename)

        driver.entry(**kwargs)

        logger().debug('after')
        logger().info(driver.result['rename_backup_name'])
        if not os.path.isdir(dirs[0]):
            dirs[0] = os.sep.join(
                dirs[0].split(os.sep)[:-1] +
                [dirs[0].split(os.sep)[-1].upper()])
            backup_filename = os.sep.join([dirs[0], '123'])
            assert os.path.isdir(dirs[0])
        assert os.path.isfile(backup_filename)
        assert driver.result['errors'] == []

    def _test_cli_rename_recover(self):
        return

        """
        Can not to create error for test recover mode
        tried:
            1. lock file
        """

        # driver = Driver()
        # dirs = helper.mkdtemps(1, root=self.TMP_ROOT,
        #                        prefix=self.TMPFILE_PREFIX)
        # files = helper.mktemps(3, root=dirs[0], prefix=self.TMPFILE_PREFIX)
        # kwargs = {
        #     'settings_json': {
        #         'CHECK_DIRS': dirs,
        #         "FILE_FORMATS": {"LETTER_CASE": "upper_case"}},
        #     'rename': True, 'rename_recover': True,
        # }
        # with FileLock(files[0]):
        #     driver.entry(**kwargs)

        # os.remove(driver.result['rename_backup_name'])
        # assert driver.result['errors'] != []

    def test_cli_revert(self):
        driver = Driver()
        dirs = helper.mkdtemps(1, root=self.TMP_ROOT,
                               prefix=self.TMPFILE_PREFIX)
        rename_kwargs = {
            'settings_json': {
                'CHECK_DIRS': dirs,
                "DIR_FORMATS": {"LETTER_CASE": "upper_case"}},
            'rename': True, 'rename_backup': True,
        }
        for backup_file in driver.find_recent_backup_files():
            os.remove(backup_file)
        assert driver.find_recent_backup_files() == []
        driver.entry(**rename_kwargs)
        assert driver.find_recent_backup_files() != []
        revert_kwargs = {
            'revert': True,
        }

        driver.entry(**revert_kwargs)

        assert driver.result['errors'] == []

    def test_cli_revert_last_existed(self):
        driver = Driver()
        dirs = helper.mkdtemps(1, root=self.TMP_ROOT,
                               prefix=self.TMPFILE_PREFIX)
        rename_kwargs = {
            'settings_json': {
                'CHECK_DIRS': dirs,
                "DIR_FORMATS": {"LETTER_CASE": "upper_case"}},
            'rename': True, 'rename_backup': True,
        }
        revert_kwargs = {'revert': True, 'revert_last': True}
        for backup_file in driver.find_recent_backup_files():
            os.remove(backup_file)
        assert driver.find_recent_backup_files() == []

        # rename 1
        driver.entry(**rename_kwargs)
        assert len(driver.find_recent_backup_files()) == 1
        first_backup = driver.result['rename_backup_name']

        # rename 2
        rename_kwargs['settings_json']['DIR_FORMATS']['LETTER_CASE'] = (
            'lower_case')
        # prevent write to same filename
        time.sleep(1)
        driver.entry(**rename_kwargs)
        assert len(driver.find_recent_backup_files()) == 2
        second_backup = driver.result['rename_backup_name']

        # revert 2
        driver.entry(**revert_kwargs)
        os.remove(second_backup)
        assert len(driver.find_recent_backup_files()) == 1

        # revert 1
        driver.entry(**revert_kwargs)

        os.remove(first_backup)
        assert driver.result['errors'] == []

    def test_cli_revert_last_not_existed(self):
        driver = Driver()
        revert_kwargs = {'revert': True, 'revert_last': True}
        for backup_file in driver.find_recent_backup_files():
            os.remove(backup_file)
        assert driver.find_recent_backup_files() == []

        driver.entry(**revert_kwargs)

        assert driver.result['errors'] != []

    def test_cli_revert_file(self):
        driver = Driver()
        dirs = helper.mkdtemps(1, root=self.TMP_ROOT,
                               prefix=self.TMPFILE_PREFIX)
        rename_kwargs = {
            'settings_json': {
                'CHECK_DIRS': dirs,
                "DIR_FORMATS": {"LETTER_CASE": "upper_case"}},
            'rename': True, 'rename_backup': True,
        }
        for backup_file in driver.find_recent_backup_files():
            os.remove(backup_file)
        assert driver.find_recent_backup_files() == []
        driver.entry(**rename_kwargs)
        assert driver.find_recent_backup_files() != []
        revert_kwargs = {
            'revert': True, 'revert_file': driver.result['rename_backup_name']
        }

        driver.entry(**revert_kwargs)

        assert driver.result['errors'] == []

    def test_required_success(self):
        driver = Driver()
        kwargs = {'required': True}
        for backup_file in driver.find_recent_backup_files():
            os.remove(backup_file)
        assert driver.find_recent_backup_files() == []

        driver.entry(**kwargs)

        assert driver.exit_code == 0

    def test_required_failed(self):
        driver = Driver()
        revert_kwargs = {'revert': True, 'revert_last': True, 'required': True}
        for backup_file in driver.find_recent_backup_files():
            os.remove(backup_file)
        assert driver.find_recent_backup_files() == []

        driver.entry(**revert_kwargs)

        assert driver.exit_code != 0

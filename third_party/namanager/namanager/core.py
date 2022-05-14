import os
import re
import json
import dicttoxml
from xml.dom.minidom import parseString
import namanager.util as util
import namanager.enums as enums


class Namanager():
    def __init__(self, settings={}):
        self.init_settings()
        self.load_settings(settings)
        self.verify_setting_type()

        self._error_info = []
        self._error_info_count = 0

    def init_settings(self):
        # Please update `enums` if you modified these attributes
        self._FILE_FORMATS = (
            enums.SETTINGS['FILE_FORMATS'])
        self._FILE_SEP = (
            enums.SETTINGS['FILE_FORMATS']['SEP'])
        self._FILE_LETTER_CASE = (
            enums.SETTINGS['FILE_FORMATS']['LETTER_CASE'])
        self._INCLUDE_FILES = (
            enums.SETTINGS['INCLUDE_FILES'])
        self._IGNORE_FILES = (
            enums.SETTINGS['IGNORE_FILES'])

        self._DIR_FORMATS = (
            enums.SETTINGS['DIR_FORMATS'])
        self._DIR_SEP = (
            enums.SETTINGS['DIR_FORMATS']['SEP'])
        self._DIR_LETTER_CASE = (
            enums.SETTINGS['DIR_FORMATS']['LETTER_CASE'])
        self._INCLUDE_DIRS = (
            enums.SETTINGS['INCLUDE_DIRS'])
        self._IGNORE_DIRS = (
            enums.SETTINGS['IGNORE_DIRS'])

    def _convert_os_sep_of_str_in_list(self, strlist):
        # needs to test
        converted_strlist = []
        for s in strlist:
            converted_strlist.append(s.replace('/', os.sep))
        return converted_strlist

    def verify_setting_type(self):
        errors = []
        settings = [
            {'s': self._FILE_FORMATS,
             't': type(enums.SETTINGS['FILE_FORMATS'])},
            {'s': self._FILE_SEP,
             't': type(enums.SETTINGS['FILE_FORMATS']['SEP'])},
            {'s': self._FILE_LETTER_CASE,
             't': type(enums.SETTINGS['FILE_FORMATS']['LETTER_CASE'])},
            {'s': self._INCLUDE_FILES,
             't': type(enums.SETTINGS['INCLUDE_FILES'])},
            {'s': self._IGNORE_FILES,
             't': type(enums.SETTINGS['IGNORE_FILES'])},
            {'s': self._DIR_FORMATS,
             't': type(enums.SETTINGS['DIR_FORMATS'])},
            {'s': self._DIR_SEP,
             't': type(enums.SETTINGS['DIR_FORMATS']['SEP'])},
            {'s': self._DIR_LETTER_CASE,
             't': type(enums.SETTINGS['DIR_FORMATS']['LETTER_CASE'])},
            {'s': self._INCLUDE_DIRS,
             't': type(enums.SETTINGS['INCLUDE_DIRS'])},
            {'s': self._IGNORE_DIRS,
             't': type(enums.SETTINGS['IGNORE_DIRS'])},
        ]

        for setting in settings:
            if not isinstance(setting['s'], setting['t']):
                errors.append("Type of {0} must be {1}.".format(
                    util.name(setting['s'], self.__dict__), setting['t']))

        if errors:
            err_str = '\n'
            for error in errors:
                err_str += error + '\n'
            raise TypeError(err_str)

    def load_settings(self, settings={}):
        # Please update `enums` if you modified these attributes
        self._FILE_FORMATS = settings.get(
            'FILE_FORMATS', enums.SETTINGS['FILE_FORMATS'])
        self._FILE_SEP = self._FILE_FORMATS.get(
            'SEP', enums.SETTINGS['FILE_FORMATS']['SEP'])
        self._FILE_LETTER_CASE = str(
            self._FILE_FORMATS.get(
                'LETTER_CASE', enums.SETTINGS['FILE_FORMATS']['LETTER_CASE']))
        self._INCLUDE_FILES = self._convert_os_sep_of_str_in_list(
            settings.get('INCLUDE_FILES', enums.SETTINGS['INCLUDE_FILES']))
        self._IGNORE_FILES = self._convert_os_sep_of_str_in_list(
            settings.get('IGNORE_FILES', enums.SETTINGS['IGNORE_FILES']))

        self._DIR_FORMATS = settings.get(
            'DIR_FORMATS', enums.SETTINGS['DIR_FORMATS'])
        self._DIR_SEP = self._DIR_FORMATS.get(
            'SEP', enums.SETTINGS['DIR_FORMATS']['SEP'])
        self._DIR_LETTER_CASE = str(
            self._DIR_FORMATS.get(
                'LETTER_CASE', enums.SETTINGS['DIR_FORMATS']['LETTER_CASE']))
        self._INCLUDE_DIRS = self._convert_os_sep_of_str_in_list(
            settings.get('INCLUDE_DIRS', enums.SETTINGS['INCLUDE_DIRS']))
        self._IGNORE_DIRS = self._convert_os_sep_of_str_in_list(
            settings.get('IGNORE_DIRS', enums.SETTINGS['IGNORE_DIRS']))

    @property
    def error_info(self):
        return self._error_info

    @property
    def error_info_count(self):
        return self._error_info_count

    @property
    def file_formats(self):
        return self._FILE_FORMATS

    @property
    def dir_formats(self):
        return self._DIR_FORMATS

    @property
    def include_files(self):
        return self._INCLUDE_FILES

    @property
    def include_dirs(self):
        return self._INCLUDE_DIRS

    @property
    def ignore_files(self):
        return self._IGNORE_FILES

    @property
    def ignore_dirs(self):
        return self._IGNORE_DIRS

    @property
    def file_sep(self):
        return self._FILE_SEP

    @property
    def file_letter_case(self):
        return self._FILE_LETTER_CASE

    @property
    def dir_sep(self):
        return self._DIR_SEP

    @property
    def dir_letter_case(self):
        return self._DIR_LETTER_CASE

    def _is_string_matching(self, string, re_match_list=[]):
        if string:
            for pattern in re_match_list:
                if re.search(pattern, string) is not None:
                    return True
        return False

    def _get_walk(self, root):
        return [path_info for path_info in os.walk(os.path.realpath(root))]

    def _get_root_in_walk(self, walk):
        root = ''
        if walk:
            root = walk[0][0]
            for (dirpath, dirs, files) in walk:
                if len(dirpath.split(os.sep)) < len(root.split(os.sep)):
                    root = dirpath
        return root

    def _divide_full_part_path_patterns(self, re_patterns):
        full_path_patterns = []
        part_path_patterns = []

        for pattern in re_patterns:
            if pattern.rfind(os.sep) == -1:
                part_path_patterns.append(pattern)
            else:
                full_path_patterns.append(pattern)

        return full_path_patterns, part_path_patterns

    def _divide_file_and_dir_name_of_patterns(self, re_patterns):
        separated_patterns = []

        for pattern in re_patterns:
            latest_sep_index = pattern.rfind(os.sep)
            dirname_pattern = pattern[:latest_sep_index] + '$'
            filename_pattern = '^' + pattern[latest_sep_index + 1:]

            separated_patterns.append({
                "dirname": dirname_pattern,
                "filename": filename_pattern
            })

        return separated_patterns

    def _include_re_patterns_of_files_in_walk(self, re_patterns, walk,
                                              root=None):
        if root is None:
            root = self._get_root_in_walk(walk)

        filtered_walk = []
        within, without = (
            self._divide_full_part_path_patterns(re_patterns))
        within = self._divide_file_and_dir_name_of_patterns(within)

        for (dirpath, dirs, files) in walk:
            filtered = []

            if without:
                for filename in files:
                    if self._is_string_matching(filename, without):
                        filtered.append(filename)

            if within:
                rel_dirpath = dirpath[len(root):] if dirpath != root else '/'
                for pattern in within:
                    if not self._is_string_matching(
                       rel_dirpath, [pattern['dirname']]):
                        continue

                    for filename in files:
                        if self._is_string_matching(
                           filename, [pattern['filename']]):
                            filtered.append(filename)

            # at least one file be included
            if filtered:
                filtered_walk.append((
                    dirpath, dirs, filtered))

        return filtered_walk

    def _ignore_re_patterns_of_files_in_walk(self, re_patterns, walk,
                                             root=None):
        include_walk = self._include_re_patterns_of_files_in_walk(
            re_patterns, walk, root)
        filtered_walk = []

        for (dirpath, dirs, files) in walk:
            include_dirpath = ()

            for (dp, dn, fn) in include_walk:
                if dp == dirpath:
                    include_dirpath = (dp, dn, fn)

            if include_dirpath:
                filtered_files = []
                for filename in files:
                    if filename not in include_dirpath[2]:
                        filtered_files.append(filename)
                if filtered_files:
                    filtered_walk.append((dirpath, dirs, filtered_files))
            else:
                filtered_walk.append((dirpath, dirs, files))

        return filtered_walk

    def _include_re_patterns_of_dirs_in_walk(self, re_patterns, walk,
                                             root=None):
        if root is None:
            root = self._get_root_in_walk(walk)

        filtered_walk = []
        for (dirpath, dirs, files) in walk:
            rel_dirpath = dirpath[len(root):]
            if rel_dirpath == '':
                rel_dirpath = '/'
            if self._is_string_matching(rel_dirpath, re_patterns):
                filtered_walk.append((dirpath, dirs, files))

        return filtered_walk

    def _ignore_re_patterns_of_dirs_in_walk(self, re_patterns, walk,
                                            root=None):
        include_walk = self._include_re_patterns_of_dirs_in_walk(
            re_patterns, walk, root)
        filtered_walk = []

        for (dirpath, dirs, files) in walk:
            include_dirpath = ()

            for (dp, dn, fn) in include_walk:
                if dp == dirpath:
                    include_dirpath = (dp, dn, fn)

            if not include_dirpath:
                filtered_walk.append((dirpath, dirs, files))

        return filtered_walk

    def _get_file_walk(self, walk):
        if self.include_files:
            walk = self._include_re_patterns_of_files_in_walk(
                self.include_files, walk)
        if self.ignore_files:
            walk = self._ignore_re_patterns_of_files_in_walk(
                self.ignore_files, walk)

        return walk

    def _get_dir_walk(self, walk):
        if self.include_dirs:
            walk = self._include_re_patterns_of_dirs_in_walk(
                self.include_dirs, walk)
        if self.ignore_dirs:
            walk = self._ignore_re_patterns_of_dirs_in_walk(
                self.ignore_dirs, walk)

        return walk

    def check_file(self, root):
        root = os.path.realpath(root)
        walk = self._get_walk(root)
        walk = self._get_file_walk(walk)
        for dirpath, dirs, files in walk:
            for f in files:
                actual = f
                expect = self.get_expect_filename(f)

                if expect != actual:
                    self._error_info.append({
                        'expect': os.sep.join([dirpath, expect]),
                        'actual': os.sep.join([dirpath, actual])
                    })
                    self._error_info_count += len(expect)

    def check_dir(self, root):
        """
        Only check dirs/files path under root (excluded)
            root:     /root/path/to/dir
            dirpath:  /root/path/to/dir/SUBDIR
            settings: dir_format['letter_case'] = 'upper_case'

            OK: any part path of /root/path/to/dir will be never checked
        """
        root = os.path.realpath(root)
        walk = self._get_walk(root)
        walk = self._get_dir_walk(walk)
        for dirpath, dirs, files in walk:
            dirpath_dirname = os.path.dirname(dirpath)
            actual = os.sep + dirpath.split(os.sep)[-1]
            expect = self.get_expect_dirname(actual)

            if expect != actual:
                self._error_info.append({
                    'expect': "".join([dirpath_dirname, expect]),
                    'actual': "".join([dirpath_dirname, actual])
                })
                self._error_info_count += 1

    def get_extension(self, filename):
        extension = (''
                     if filename.find(r'\.') == -1
                     else '.' + filename.split(r'\.')[-1])
        return extension

    def get_filename_without_extension(self, filename):
        extension = self.get_extension(filename)
        return filename[:filename.rfind(extension)]

    def get_expect_filename(self, filename):
        name = self.get_filename_without_extension(filename)
        extension = self.get_extension(filename)

        name = util.convert_sep(name, self.file_sep)
        if self.file_letter_case != 'ignore':
            name = util.convert_sentence_to_case(
                name, self.file_letter_case)

        return name + extension

    def get_expect_dirname(self, dirname):
        dirname = util.convert_sep(dirname, self.dir_sep)
        if self.dir_letter_case != 'ignore':
            dirname = util.convert_sentence_to_case(
                dirname, self.dir_letter_case)

        return dirname

    def check(self, root):
        self.check_dir(root)
        self.check_file(root)

    def get_dict(self, data={}):
        return data

    def get_json(self, data={}, pretty_dump=False):
        if pretty_dump:
            return json.dumps(data, indent=4, sort_keys=True)
        else:
            return json.dumps(data)

    def get_xml(self, data={}, pretty_dump=False):
        xml = dicttoxml.dicttoxml(data)
        if pretty_dump:
            return parseString(xml).toprettyxml()
        else:
            return parseString(xml).toxml()

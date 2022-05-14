import os
import json
import itertools
import namanager.tests.helper as helper
from namanager.archieve_manager import ArchieveManager


class TestArchieveManager():
    def __init__(self):
        self.TMPFILE_PREFIX = 'test_am_'
        self.RENAME_SUFFIX = '_*&^%$'

    def setUp(self):
        self.TMP_ROOT = helper.mkdtemp(
            root=os.path.realpath(os.path.dirname(__file__)))

    def tearDown(self):
        helper.rm_path(self.TMP_ROOT)

    def test_rename(self):
        # test files/directories both mixed
        am = ArchieveManager()
        paths = helper.mkdtemps_recur(1, 1, filecount=1, root=self.TMP_ROOT,
                                      prefix=self.TMPFILE_PREFIX)
        path_pairs = self._gen_src_dst_rename_pairs(paths)
        renamed_path_pairs = self._gen_src_dst_renamed_pairs(paths)
        revert_path_pairs = self._gen_src_dst_revert_pairs(paths)

        for pairs in itertools.permutations(path_pairs):
            self._test_rename_before(pairs)
            assert [] == am.rename(pairs)
            self._test_rename_after(renamed_path_pairs)
            assert [] == am.rename(revert_path_pairs)

    def test_rename_file(self):
        am = ArchieveManager()
        files = helper.mktemps(2, prefix=self.TMPFILE_PREFIX,
                               root=self.TMP_ROOT)
        file_pairs = self._gen_src_dst_rename_pairs(files)
        revert_file_pairs = self._gen_src_dst_revert_pairs(files)

        for pairs in itertools.permutations(file_pairs):
            self._test_rename_before(pairs)
            assert [] == am.rename(pairs)
            # no needs renamed pairs for files,
            # because direcotires would not be changed
            self._test_rename_after(pairs)
            assert [] == am.rename(revert_file_pairs)

    def test_rename_dir(self):
        am = ArchieveManager()
        dirs = helper.mkdtemps_recur(2, 1, prefix=self.TMPFILE_PREFIX,
                                     root=self.TMP_ROOT)
        dir_pairs = self._gen_src_dst_rename_pairs(dirs)
        renamed_dir_pairs = self._gen_src_dst_renamed_pairs(dirs)
        revert_dir_pairs = self._gen_src_dst_revert_pairs(dirs)

        for perm_pairs in itertools.permutations(dir_pairs):
            self._test_rename_before(perm_pairs)
            assert [] == am.rename(perm_pairs)
            self._test_rename_after(renamed_dir_pairs)
            assert [] == am.rename(revert_dir_pairs)

    def _test_rename_before(self, pairs):  # pragma: no cover
        # haven't been tested
        errors = []

        for src, dst in pairs:
            helper.append_to_error_if_not_expect_with_msg(
                errors,
                os.path.exists(src),
                "The path:{0} haven't existed before rename.".format(src))
            helper.append_to_error_if_not_expect_with_msg(
                errors,
                not os.path.exists(dst),
                "The path:{0} have existed.".format(dst))

        assert errors == [], Exception(helper.get_error_string(errors))

    def _test_rename_after(self, pairs):  # pragma: no cover
        # haven't been tested
        errors = []

        for src, dst in pairs:
            helper.append_to_error_if_not_expect_with_msg(
                errors,
                not os.path.exists(src),
                "The path:{0} is exists too even renamed.".format(src))
            helper.append_to_error_if_not_expect_with_msg(
                errors,
                os.path.exists(dst),
                "The path:{0} haven't been renamed.".format(dst))

        assert errors == [], Exception(helper.get_error_string(errors))

    def test_gen_revert_path_pairs(self):
        am = ArchieveManager()
        paths = helper.mkdtemps_recur(1, 2, file_count=1, root=self.TMP_ROOT,
                                      prefix=self.TMPFILE_PREFIX)
        rename_path_pairs = self._gen_src_dst_rename_pairs(paths)
        expt_revert_path_pairs = self._gen_src_dst_revert_pairs(paths)

        for pairs in itertools.permutations(rename_path_pairs):
            actl_revert_path_pairs = (am.gen_revert_path_pairs(pairs))

            is_same = (
                helper.is_same_disorderly(
                    [pair[0] for pair in expt_revert_path_pairs],
                    [pair[0] for pair in actl_revert_path_pairs]) and
                helper.is_same_disorderly(
                    [pair[1] for pair in expt_revert_path_pairs],
                    [pair[1] for pair in actl_revert_path_pairs]))

            assert is_same, Exception(
                    "revert pairs are wrong"
                    "\nExpect:\n{0}\nActual:\n{1}\n".format(
                        json.dumps(expt_revert_path_pairs,
                                   indent=4, sort_keys=True),
                        json.dumps(actl_revert_path_pairs,
                                   indent=4, sort_keys=True)))

    def test_separate_file_dir_from_path_pair(self):
        am = ArchieveManager()
        errors = []
        dirs = helper.mkdtemps_recur(2, 1, prefix=self.TMPFILE_PREFIX,
                                     root=self.TMP_ROOT)
        files = (
            helper.mktemps(1, prefix=self.TMPFILE_PREFIX, root=self.TMP_ROOT) +
            helper.mktemps(1, root=dirs[0], prefix=self.TMPFILE_PREFIX))
        dir_pairs = self._gen_src_dst_rename_pairs(dirs)
        file_pairs = self._gen_src_dst_rename_pairs(files)
        path_pairs = file_pairs + dir_pairs

        for perm_pair in itertools.permutations(path_pairs):
            actl_file_pairs, actl_dir_pairs = (
                am._separate_file_dir_from_path_pair(perm_pair))

            for expt, actl in ((file_pairs, actl_file_pairs),
                               (dir_pairs, actl_dir_pairs)):
                helper.append_to_error_if_not_expect_with_msg(
                    errors, helper.is_same_disorderly(expt, actl),
                    "The files haven't separated well"
                    "\nExpect:\n{0}\nActual:\n{1}".format(
                        json.dumps(expt, indent=4, sort_keys=True),
                        json.dumps(actl, indent=4, sort_keys=True)))

            assert errors == [], Exception(helper.get_error_string(errors))

    def test_sort_path_pair(self):
        # only tests for directories
        am = ArchieveManager()
        errors = []
        # create some temp directories under different hierarchy
        expt_hrchy1_paths = helper.mkdtemps(1, prefix=self.TMPFILE_PREFIX,
                                            root=self.TMP_ROOT)
        expt_hrchy2_paths = (
            helper.mkdtemps(2, root=expt_hrchy1_paths[0],
                            prefix=self.TMPFILE_PREFIX) +
            helper.mkdtemps(1, root=expt_hrchy1_paths[0],
                            prefix=self.TMPFILE_PREFIX))
        expt_hrchy3_paths = (
            helper.mkdtemps(1, root=expt_hrchy2_paths[0],
                            prefix=self.TMPFILE_PREFIX) +
            helper.mkdtemps(1, root=expt_hrchy2_paths[1],
                            prefix=self.TMPFILE_PREFIX) +
            helper.mkdtemps(1, root=expt_hrchy2_paths[1],
                            prefix=self.TMPFILE_PREFIX))
        src_dst_pairs = self._gen_src_dst_rename_pairs(expt_hrchy1_paths +
                                                       expt_hrchy2_paths +
                                                       expt_hrchy3_paths)

        for perm_pair in itertools.permutations(src_dst_pairs):
            actl_pairs = am._sort_path_pair(perm_pair, reverse=True)

            actl_hrchy1_pairs = actl_pairs[-len(expt_hrchy1_paths):]
            actl_hrchy2_pairs = actl_pairs[
                len(expt_hrchy3_paths):-len(expt_hrchy1_paths)]
            actl_hrchy3_pairs = actl_pairs[:len(expt_hrchy3_paths)]

            actl_hrchy1_paths = [path[0] for path in actl_hrchy1_pairs]
            actl_hrchy2_paths = [path[0] for path in actl_hrchy2_pairs]
            actl_hrchy3_paths = [path[0] for path in actl_hrchy3_pairs]

            for expt, actl in ((expt_hrchy1_paths, actl_hrchy1_paths),
                               (expt_hrchy2_paths, actl_hrchy2_paths),
                               (expt_hrchy3_paths, actl_hrchy3_paths)):
                helper.append_to_error_if_not_expect_with_msg(
                    errors, helper.is_same_disorderly(expt, actl),
                    "The path not sort by hrchy"
                    "\nExpect:\n{0}\nActual:\n{1}".format(
                        json.dumps(expt, indent=4, sort_keys=True),
                        json.dumps(actl, indent=4, sort_keys=True)))

            assert errors == [], Exception(helper.get_error_string(errors))

    def _gen_src_dst_rename_pairs(self, path):  # pragma: no cover
        # haven't been tested
        if isinstance(path, (list, tuple, set)):
            pairs = []
            for p in path:
                pairs.extend(self._gen_src_dst_rename_pairs(p))
        else:
            pairs = [(path, path + self.RENAME_SUFFIX)]

        return pairs

    def _gen_src_dst_renamed_pairs(self, path):  # pragma: no cover
        # haven't been tested
        """
        If directories have been renaming,
        then we must also change upper hierarchy between the directories.
        e.g.,
            /change/upper -> /change/new_upper
            /change/upper/lower
                WRONG -> /change/upper/new_lower
                RIGHT -> /change/new_upper/new_lower
        """
        if isinstance(path, (list, tuple, set)):
            pairs = []
            for p in path:
                pairs.extend(self._gen_src_dst_renamed_pairs(p))
        else:
            dst_parts = []
            for path_part in path.split(os.sep):
                dst_parts.append(path_part + self.RENAME_SUFFIX
                                 if path_part.startswith(self.TMPFILE_PREFIX)
                                 else path_part)
            pairs = [(path, os.sep.join(dst_parts))]

        return pairs

    def _gen_src_dst_revert_pairs(self, path):  # pragma: no cover
        # haven't been tested
        if isinstance(path, (list, tuple, set)):
            pairs = []
            for p in path:
                pairs.extend(self._gen_src_dst_revert_pairs(p))
        else:
            dst_parts = []
            for path_part in path.split(os.sep):
                dst_parts.append(path_part + self.RENAME_SUFFIX
                                 if path_part.startswith(self.TMPFILE_PREFIX)
                                 else path_part)
            src_parts = dst_parts[:-1] + [path.split(os.sep)[-1]]
            pairs = [(os.sep.join(dst_parts), os.sep.join(src_parts))]

        return pairs

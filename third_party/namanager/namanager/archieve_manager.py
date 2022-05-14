import os
import shutil


class ArchieveManager():
    """
    Strategy:
        1. file rename first
        2. deeper first

    :type path_pairs: list of tuple, e.g., [(src, dst)]
    """

    def rename(self, path_pairs):
        """
        :return: pairs which doesn't be renamed
        """
        error_pairs = []
        file_pairs, dir_pairs = (
            self._separate_file_dir_from_path_pair(path_pairs))

        error_pairs.extend(self._rename(file_pairs))
        error_pairs.extend(self._rename(dir_pairs))

        return error_pairs

    def _rename(self, path_pairs):
        """
        :return: pairs which doesn't be renamed
        """
        error_pairs = []
        path_pairs = self._sort_path_pair(path_pairs, reverse=True)

        for src, dst in path_pairs:
            try:
                shutil.move(src, dst)
            except Exception:
                error_pairs.append([src, dst])

        return error_pairs

    def gen_revert_path_pairs(self, path_pairs):
        # Only implement for file/dir under same original directory
        """
        TODO:
        Find more elegant and efficient way to convert files/directories
        which upper hierarchy path have been renamed.

        this function must be called before rename functions,
        because we need to separate files/directories first.

        When we want to rollback names,
        we need different strategy to rename those be renamed files.
        The deeper files/directories which have been renamed must be first.
        e.g.,
            rename:
                /change/upper -> /change/new_upper
                /change/upper/lower -> /change/new_upper/new_lower
            revert:
                /change/new_upper/new_lower -> /change/new_upper/lower
                /change/new_upper -> /change/upper
        """
        file_pairs, dir_pairs = (
            self._separate_file_dir_from_path_pair(path_pairs))
        file_pairs = self._sort_path_pair(file_pairs)
        dir_pairs = self._sort_path_pair(dir_pairs)
        revert_path_pairs = []
        renamed_mapping = {}

        for pairs in [dir_pairs, file_pairs]:
            for src, dst in pairs:
                # replace dirname
                # if any hierarchical dirname has changed
                renamed_dirname = os.path.dirname(dst)
                dirname_parts = renamed_dirname.split(os.sep)
                # ['/root/to/path', '/root/to', '/root']
                dirname_powerset = []
                for r in range(len(dirname_parts) + 1, 1, -1):
                    dirname_powerset.append(os.sep.join(dirname_parts[:r]))
                for dn in dirname_powerset:
                    if dn in renamed_mapping:
                        renamed_dn = renamed_mapping[dn]
                        renamed_dirname = (
                            renamed_dn + renamed_dirname[len(dn):])
                        break

                renamed_dst = os.sep.join(
                    [renamed_dirname, os.path.basename(dst)])
                renamed_src = os.sep.join(
                    [renamed_dirname, os.path.basename(src)])
                revert_path_pairs.append((renamed_dst, renamed_src))

                renamed_mapping[src] = renamed_dst

        return revert_path_pairs

    def _separate_file_dir_from_path_pair(self, path_pairs):
        file_pairs = []
        dir_pairs = []

        for pair in path_pairs:
            if os.path.isfile(pair[0]):
                file_pairs.append(pair)
            elif os.path.isdir(pair[0]):
                dir_pairs.append(pair)

        return file_pairs, dir_pairs

    def _sort_path_pair(self, path_pairs, **kwargs):
        reverse = kwargs.get('reverse', False)

        path_pairs = path_pairs[:]
        counted_path_pairs = []
        for pair in path_pairs:
            counted_path_pairs.append(
                [pair[0], pair[1], len(pair[0].split(os.sep))])
        counted_path_pairs.sort(
            key=lambda p: p[2] if os.path.isdir(p[0]) else p[2] - 1,
            reverse=reverse)

        sorted_ = []
        for pair in counted_path_pairs:
            sorted_.append((pair[0], pair[1]))

        return sorted_

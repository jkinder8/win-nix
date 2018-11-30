"""
find.py
Contains __main__ to use as stand-alone, but the class
Find can be imported and used in other python code.
---------------------------------------------------------
usage: find.py [-h] [-t SEARCH_TYPE] [-i] base_dir pattern

positional arguments:
  base_dir              Base directory to start from.
  pattern               Pattern to search for.

optional arguments:
  -h, --help            show this help message and exit
  -t SEARCH_TYPE, --type SEARCH_TYPE
                        f for files or d for directories. Default=f
  -i                    Turn on ignore case.
---------------------------------------------------------
class usage example:
find = Find()
(args.base_dir, args.pattern, args.search_type, args.ignore_case)
results = find.find('E:/python', '*.ipynb', 'f', True)
"""
import os
import re

class Find:
    """
    Find files or directories of matching pattern from the base
    directory given.
    """

    def find(self, base_dir, pattern, find_type='f', ignorecase=False):
        """
        The method called for this class.
        :param base_dir: ex - E:/python
        :param pattern: use '*' for wildcarding characters. ex - *.txt, Data*, etc
        :param find_type: -t [f = file | d = directory ]. Defaults to f if not given
        :param ignorecase: -i, Optional flag to ignore case
        :return: list
        """
        repattern = self._compile_re(pattern, ignorecase)
        result_list = []
        if find_type == 'f':
            result_list = self._find_files(base_dir, repattern)
        else:
            result_list = self._find_dirs(base_dir, repattern)
        return result_list

    def _compile_re(self, pattern, ignorecase):
        pattern = pattern.replace('.', '\.')
        pattern = pattern.replace('*', '.+')
        if ignorecase:
            return re.compile('{}'.format(pattern), re.IGNORECASE)
        return re.compile('{}'.format(pattern))


    def _find_files(self, find_dir, pattern):
        filelist = []
        for (root, subs, files) in os.walk(find_dir):
            for f in files:
                if pattern.match(f):
                    filelist.append('{}/{}'.format(root, f))
        return filelist


    def _find_dirs(self, find_dir, pattern):
        dirlist = []
        for (root, subs, files) in os.walk(find_dir):
            for d in subs:
                if pattern.match(d):
                    dirlist.append('{}/{}'.format(root, d))
        return dirlist


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("base_dir", help="Base directory to start from.")
    parser.add_argument('pattern', help='Pattern to search for.')
    parser.add_argument('-t', '--type', dest='search_type', help='f for files or d for directories. Default=f')
    parser.add_argument('-i', dest='ignore_case', action='store_true', help='Turn on ignore case.')

    args = parser.parse_args()

    # First check if the base directory exist
    if not os.path.isdir(args.base_dir):
        print('Base directory %s does not exist.' % args.base_dir)
        exit(1)

    # Check search type and set to f (file) if not given
    if not args.search_type:
        args.search_type = 'f'
    find = Find()
    results = find.find(args.base_dir, args.pattern, args.search_type, args.ignore_case)
    if len(results) > 0:
        for r in results:
            print(r)


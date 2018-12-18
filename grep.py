"""
usage: grep.py [-h] [-r] [-i] base_dir file_pattern word_pattern

positional arguments:
  base_dir         Base directory to start from.
  file_pattern     Pattern for file name match. Use * for all files
  word_pattern     Word pattern to search in files.

optional arguments:
  -h, --help       show this help message and exit
  -r, --recursive  Check for word patterns from base_dir in all directories
                   recursively.Defaults to files in base_dir only if not set.
  -i               Turn on ignore case for word search.
  NOTE: The file pattern given is case insensitive
"""
import os
from collections import defaultdict
from find import Find

class Grep:
    def __init__(self):
        self._word_dict = defaultdict(list)

    def _happy_powershell(self, line):
        """Powershell and cmd windows seem to get unhappy outside of standard
        ascii range... replacing those chars found with '*'"""
        mystr = []
        for c in line:
            if ord(c) > 127:
                mystr.append('*')
            else:
                mystr.append(c)
        return ''.join(x for x in mystr)

    def grep(self, word_pattern, file_list, ignorecase=False):
        word_pat = find._compile_re(word_pattern, ignorecase)
        for f in file_list:
            try:
                f_lines = [l.rstrip() for l in open(f, encoding='utf-8')]
                match_lines = []

                for line in f_lines:
                    line = self._happy_powershell(line)
                    if word_pat.search(line):
                        match_lines.append(line)

                if len(match_lines) > 0:
                    self._word_dict[f] = match_lines
            except UnicodeDecodeError:
                print('Non UTF-8 chars in file:', f)


    def get_results(self):
        return self._word_dict


    def print_results(self):
        for f in self._word_dict.keys():
            print(f)
            lines = self._word_dict[f]
            for line in lines:
                print('\t', line)



if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("base_dir", help="Base directory to start from.")
    parser.add_argument('file_pattern', help='Pattern for file name match. Use * for all files')
    parser.add_argument('word_pattern', help='Word pattern to search in files.')
    parser.add_argument('-r', '--recursive', dest='depth', action='store_true',
                        help='Check for word patterns from base_dir in all directories recursively.'
                        'Defaults to files in base_dir only if not set.')
    parser.add_argument('-i', dest='ignore_case', action='store_true', help='Turn on ignore case for word search.')

    args = parser.parse_args()

    # First check if the base directory exist
    if not os.path.isdir(args.base_dir):
        print('Base directory %s does not exist.' % args.base_dir)
        exit(1)

    if not args.depth:
        depth = 0
    else:
        depth = 100

    find = Find()
    # results = find.find(args.base_dir, args.pattern, args.search_type, args.ignore_case)
    file_list = find.find(args.base_dir, args.file_pattern, depth, 'f', True)
    grep = Grep()
    grep.grep(args.word_pattern, file_list, args.ignore_case)
    grep.print_results()
    # Test to just get the results as opposed to calling the class print_results()
    #results = grep.get_results()
    #print('\n\n', results)
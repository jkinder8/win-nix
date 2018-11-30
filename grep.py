"""
usage: grep.py [-h] [-i] base_dir file_pattern word_pattern

positional arguments:
  base_dir      Base directory to start from.
  file_pattern  Pattern for file name match. Use * for all files
  word_pattern  Word pattern to search in files.

optional arguments:
  -h, --help    show this help message and exit
  -i            Turn on ignore case for word search.
"""
import os
from collections import defaultdict
from find import Find

class Grep:
    def __init__(self):
        self._word_dict = defaultdict(list)


    def grep(self, word_pattern, file_list, ignorecase=False):
        word_pat = find._compile_re(word_pattern, ignorecase)
        for f in file_list:
            f_lines = [l.rstrip() for l in open(f)]
            match_lines = []
            for line in f_lines:
                if word_pat.search(line):
                    match_lines.append(line)

            if len(match_lines) > 0:
                self._word_dict[f] = match_lines

    def get_results(self):
        return self._word_dict


    def print_results(self):
        for f in self._word_dict.keys():
            print(f)
            words = self._word_dict[f]
            for w in words:
                print('\t', w)



if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("base_dir", help="Base directory to start from.")
    parser.add_argument('file_pattern', help='Pattern for file name match. Use * for all files')
    parser.add_argument('word_pattern', help='Word pattern to search in files.')
    parser.add_argument('-i', dest='ignore_case', action='store_true', help='Turn on ignore case for word search.')

    args = parser.parse_args()

    # First check if the base directory exist
    if not os.path.isdir(args.base_dir):
        print('Base directory %s does not exist.' % args.base_dir)
        exit(1)

    find = Find()
    # results = find.find(args.base_dir, args.pattern, args.search_type, args.ignore_case)
    file_list = find.find(args.base_dir, args.file_pattern, 'f', True)
    grep = Grep()
    grep.grep(args.word_pattern, file_list, args.ignore_case)
    grep.print_results()
    # Test to just get the results as opposed to calling the class print_results()
    #results = grep.get_results()
    #print('\n\n', results)
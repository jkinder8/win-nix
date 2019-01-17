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
    """
    Class to search files for given word / pattern.
    """
    def __init__(self):
        """
        Initialize the dictionary.
        Key = Filename -> str
        Value = Matched lines -> list
        """
        self.__word_dict = defaultdict(list)

    def __happy_powershell(self, line):
        """
        Powershell and cmd windows seem to get unhappy outside of standard
        ascii range... replacing those chars > 127 found with '*'
        """
        mystr = []
        for c in line:
            if ord(c) > 127:
                # Replace the character
                mystr.append('*')
            else:
                # Printable character - append to the list
                mystr.append(c)
        return ''.join(x for x in mystr)

    def grep(self, word_pattern, file_list, ignorecase=False):
        """
        :param word_pattern: Word to supply as shown with Grep.py -h
        :param file_list: List of files to be searched.
        :param ignorecase: True / False for ignoring case for the word pattern.
        :return: None
        """
        # compile the word pattern
        word_pat = find._compile_re(word_pattern, ignorecase)
        for f in file_list:
            # list to hold matching lines
            match_lines = []
            with open(f, 'r', encoding='utf-8') as fp:
                try:
                    while True:
                        line = fp.readline()
                        if line == '':
                            break

                        if word_pat.search(line):
                            # pattern match. strip newline and check ord for each char
                            line = line.rstrip()
                            line = self.__happy_powershell(line)
                            match_lines.append(line)

                except UnicodeDecodeError:
                    print('Cannot decode:', f)

            # put entry in the dictionary if word pattern found.
            if len(match_lines) > 0:
                self.__word_dict[f] = match_lines

    def get_results(self):
        """
        :return: Dictionary containing the file name and a list
        of matching lines
        """
        return self.__word_dict


    def print_results(self):
        """
        :return: None
        Print results to stdout
        """
        for f in self.__word_dict.keys():
            print(f)
            lines = self.__word_dict[f]
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
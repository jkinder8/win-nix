# win-nix

Using this project to create some 'nix' style python to use on 
my Windows desktop, starting with a find.py and a grep.py.

After originally creating a find.py as a normal python script
with __main__ and methods to be called, I decided to do as a
class with a test for __main__, so that I can import and use the
classes in other python scripts.

So I can call find.py directly to have __main__ run and also
I can import the class Find in to grep.py in order to re-use
the code.

Given my original intention of using these on Windows 
(meaning to be used in powershell or cmd), modified grep.py
to replace chars with ord > 127 with '*' so powershell
doesn't cry about it.

Also assuming a single user system. Not checking for 
permissions.

1/17/2019:
Grep.py
- Change file reading from gathering all lines in to a list
to using the with statement in case an extremely large file
is encountered.
- Refactor _happy_powershell to __happy_powershell
- Add better commenting.

Find.py
- Add depth check to directory search as done on file
search.
- Refactor get_depth to __get_depth
- Refactor __find_files to __find_files
- Refactor __find_dirs to __find_dirs
- Add better commenting.
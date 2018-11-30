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
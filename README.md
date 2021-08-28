# simple-rss
Simple RSS Reader with GUI.
Tested to work with Debian Buster and Bullseye.

# Installing
install system-level dependencies:

'''bash
apt install python3-tk python3-venv git
'''

clone repository with git:

'''bash
mkdir simplerss
cd simplerss
git clone https://github.com/SamuelKos/simple-rss .
chmod u+x mkvenv
./mkvenv env
'''

# Running
activate virtual environment and start python-console:
 
'''bash
source env/bin/activate
python
'''

in python-console create root-window and start program.

'''python
from tkinter import Tk
root=Tk().withdraw()
u=simple_rss.Browser(root)
'''

Exit program by closing its window and in python-console press
ctrl-d to exit. Deactivate virtual environment with:

''bash
deactivate
'''

# Uninstalling
Just remove the folder where program was installed.
Remove git and tkinter:

'''bash
apt remove python3-tk git
''' 

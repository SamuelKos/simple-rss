# simple-rss
Simple RSS Reader with GUI.
Tested to work with Debian Buster and Bullseye.

# Installing
install system-level dependencies:

```console
foo@bar:~$ apt install python3-tk python3-venv git
```

clone repository with git:

```console
foo@bar:~$ mkdir simplerss
foo@bar:~$ cd simplerss
foo@bar:~$ git clone https://github.com/SamuelKos/simple-rss .
foo@bar:~$ chmod u+x mkvenv
foo@bar:~$ ./mkvenv env
```

# Running
activate virtual environment and start python-console:
 
```console
foo@bar:~$ source env/bin/activate
foo@bar:~$ python
```

in python-console create root-window and start program.

```python
from tkinter import Tk
root=Tk().withdraw()
u=simple_rss.Browser(root)
```

Exit program by closing its window and in python-console press
ctrl-d to exit. Deactivate virtual environment with:

```console
foo@bar:~$ deactivate
```

# Uninstalling
Just remove the folder where program was installed.
Remove git and tkinter:

```console
foo@bar:~$ apt remove python3-tk git
```

# simple-rss
Simple RSS Reader with GUI.
Tested to work with Debian Buster and Bullseye.

# Installing
debian-packages required: python3-tk python3-venv
To install them:

```console
foo@bar:~$ sudo apt install python3-tk python3-venv
```

Then clone this repo and run install.sh.
Git will create directory named simple-rss under the current working directory.
 
```console
foo@bar:~$ git clone https://github.com/SamuelKos/simple-rss
foo@bar:~$ cd simple-rss
foo@bar:~/simple-rss$ ./install.sh
```

# About Python dependencies:
Only one library outside standard is used: [html2text](https://github.com/Alir3z4/html2text/)
which is installed with pip. Interesting fact is that it is forked from repo
owned by [Aaron Swartz](https://en.wikipedia.org/wiki/Aaron_Swartz),
who was involved in RSS-format developing and more. Check it out!
 

# Running 

```console
foo@bar:~/simple-rss$ source env/bin/activate
foo@bar:~/simple-rss$ python -i startup.py
```

Exit python-console with ctrl-d.

# Uninstalling
Just remove the folder where program was installed.
To remove git and tkinter:

```console
foo@bar:~$ sudo apt remove python3-tk git
```

# Licence
This project is licensed under the terms of the GNU General Public License v3.0.

# simple-rss
Simple RSS Reader with GUI.
Tested to work with Debian Buster and Bullseye.

# Installing
If you have git, clone this repo and then run install.sh.
It will create directory named simple-rss under the current working directory.
 
```console
foo@bar:~$ git clone https://github.com/SamuelKos/simple-rss
foo@bar:~$ cd simple-rss
foo@bar:~/simple-rss$ sudo ./install.sh
```

If you don't have git, then just install it first with: sudo apt install git.
Sudo is needed in case we need to install system level dependencies like python3-tk.

# About Python dependencies:
Only one library outside standard is used: [html2text](https://github.com/Alir3z4/html2text/)
which is installed with pip. Interesting fact is that it is forked from repo
owned by [Aaron Swartz](https://en.wikipedia.org/wiki/Aaron_Swartz),
who was involved in RSS-format developing and more. Check it out!
 

# Running 

```console
foo@bar:~/simple-rss$ ./reader.sh
```

Exit python-console with ctrl-d.
You can make starting program easier by copying it to your bin-directory. If you don't
have a bin-directory in your home directory, create it first.
 
```console
foo@bar:~/simple-rss$ cp reader.sh ~/bin/reader           
```

Now you can just:

```console
foo@bar:~$ reader           
```

# Uninstalling
Just remove the folder where program was installed.
To remove git and tkinter:

```console
foo@bar:~$ sudo apt remove python3-tk git
```

# Licence
This project is licensed under the terms of the GNU General Public License v3.0.

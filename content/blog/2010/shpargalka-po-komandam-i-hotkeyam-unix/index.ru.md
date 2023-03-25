---
title: Шпаргалка по командам и хоткеям Unix
date: 2010-02-03 13:08:57 +0300
draft: false
tags: [old-site, unix]
---
Стянуто отсюда: http://www.debian.org/doc/manuals/debian-reference/ch01.en.html
<!--main-->
## Хоткеи:

| key                                     | description of key binding                                      |
|-----------------------------------------|-----------------------------------------------------------------|
| `Ctrl-U`                                  | стереть тест перед курсором (erase line before cursor)          |
| `Ctrl-H`                                  | стереть символ перед курсром (erase a character before cursor)  |
| `Ctrl-D`                                  | terminate input (exit shell if you are using shell)             |
| `Ctrl-C`                                  | terminate a running program                                     |
| `Ctrl-Z`                                  | temporarily stop program by moving it to the background job     |
| `Ctrl-S`                                  | halt output to screen                                           |
| `Ctrl-Q`                                  | reactivate output to screen                                     |
| `Ctrl-Alt-D`el                            | reboot/halt the system, see `inittab(5)`                        |
| `Left-Alt-key (optionally, Windows-key)`  | meta-key for Emacs and the similar UI                           |
| `Up-arrow`                                | start command history search under `bash`                       |
| `Ctrl-R`                                  | start incremental command history search under `bash`           |
| `Tab`                                   | complete input of the filename to the command line under `bash` |
| `Ctrl-V` `Tab`                          | input `Tab` without expansion to the command line under `bash`  |

## Команды:
| command                       | description |
|-------------------------------|--------------------------------------------------------------------------|
 | `pwd`                         | выводит текущую директорию (display name of current/working directory)|
 | `whoami`                      | выводит имя текущего юзера (display current user name)|
 | `id`                          | выводит id текущего юзера (display current user identity (name, uid, gid, and associated groups))|
 | `file <foo>`            | выводит тип файла, переданного в качестве аргумента (display a type of file for the file `<foo>`)|
 | `type -p <commandname>` | выводит расположение файла, вызывающегося при вводе команды (display a file location of command `<commandname>`) |
 | `type <commandname>`    | выводит информацию о команде (display information on command `<commandname>`) |
| `apropos <key-word>` | находит команды, связанные с переданным аргумеентом find commands related to `<key-word>` |
| `whatis <commandname>` | display one line explanation on command `<commandname>` |
| `man -a <commandname>` | display explanation on command `<commandname>` (Unix style) |
| `info <commandname>` | display rather long explanation on command `<commandname>` (GNU style) |
| `ls` | list contents of directory (non-dot files and directories) |
| `ls -a` | list contents of directory (all files and directories) |
| `ls -A` | list contents of directory (almost all files and directories, i.e., skip `..` and `.`) |
| `ls -la` | list all contents of directory with detail information |
| `ls -lai` | list all contents of directory with inode number and detail information |
| `ls -d` | list all directories under the current directory |
| `tree` | display file tree contents |
| `lsof <foo>` | list open status of file `<foo>` |
| `lsof -p <pid>` | list files opened by the process ID: `<pid>` |
| `mkdir <foo>` | make a new directory `<foo>` in the current directory |
| `rmdir <foo>` | remove a directory `<foo>` in the current directory |
| `cd <foo>` | change directory to the directory `<foo>` in the current directory or in the directory listed in the variable `$CDPATH` |
| `cd /` | change directory to the root directory |
| `cd` | change directory to the current user's home directory |
| `cd /<foo>` | change directory to the absolute path directory `/<foo>` |
| `cd ..` | change directory to the parent directory |
| `cd ~<foo>` | change directory to the home directory of the user `<foo>` |
| `cd -` | change directory to the previous directory |
| `</etc/motd pager` | display contents of `/etc/motd` using the default pager |
| `touch <junkfile>` | create a empty file `<junkfile>` |
| `cp <foo> <bar>` | copy a existing file `<foo>` to a new file `<bar>` |
| `rm <junkfile>` | remove a file `<junkfile>` |
| `mv <foo> <bar>` | rename an existing file `<foo>` to a new name `<bar>` (`<bar>` must not exist) |
| `mv <foo> <bar>` | move an existing file `<foo>` to a new location `<bar>/<foo>` (the directory `<bar>` must exist) |
| `mv <foo> <bar>/<baz>` | move an existing file `<foo>` to a new location with a new name `<bar>/<baz>` (the directory `<bar>` must exist but the directory `<bar>/<baz>` must not exist) |
| `chmod 600 <foo>` | make an existing file `<foo>` to be non-readable and non-writable by the other people (non-executable for all) |
| `chmod 644 <foo>` | make an existing file `<foo>` to be readable but non-writable by the other people (non-executable for all) |
| `chmod 755 <foo>` | make an existing file `<foo>` to be readable but non-writable by the other people (executable for all) |
| `find . -name <pattern>` | find matching filenames using shell `<pattern>` (slower) |
| `locate -d . <pattern>` | find matching filenames using shell `<pattern>` (quicker using regularly generated database) |
| `grep -e "<pattern>" *.html` | find a "<pattern>" in all files ending with `.html` in current directory and display them all |
| `top` | display process information using full screen, type `q` to quit |
| `kill <1234>` | kill a process identified by the process ID: "<1234>" |
| `gzip <foo>` | compress `<foo>` to create `<foo>.gz` using the Lempel-Ziv coding (LZ77) |
| `gunzip <foo>.gz` | decompress `<foo>.gz` to create `<foo>` |
| `bzip2 <foo>` | compress `<foo>` to create `<foo>.bz2` using the Burrows-Wheeler block sorting text compression algorithm, and Huffman coding (better compression than `gzip`) |
| `bunzip2 <foo>.bz2` | decompress `<foo>.bz2` to create `<foo>` |
| `tar -xvf <foo>.tar` | extract files from `<foo>.tar` archive |
| `tar -xvzf <foo>.tar.gz` | extract files from gzipped `<foo>.tar.gz` archive |
| `tar -xvf -j <foo>.tar.bz2` | extract files from `<foo>.tar.bz2` archive |
| `tar -cvf <foo>.tar <bar>/` | archive contents of folder `<bar>/` in `<foo>.tar` archive |
| `tar -cvzf <foo>.tar.gz <bar>/` | archive contents of folder `<bar>/` in compressed `<foo>.tar.gz` archive |
| `tar -cvjf <foo>.tar.bz2 <bar>/` | archive contents of folder `<bar>/` in `<foo>.tar.bz2` archive |
| `zcat README.gz > foo` | create a file `foo` with the decompressed content of `README.gz` |
| `zcat README.gz >> foo` | append the decompressed content of `README.gz` to the end of the file `foo` (if it does not exist, create it first) |
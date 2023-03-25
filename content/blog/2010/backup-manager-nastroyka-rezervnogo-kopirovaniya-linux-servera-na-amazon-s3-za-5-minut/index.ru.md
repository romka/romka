---
title: Backup-manager — настройка резервного копирования Linux-сервера на Amazon S3 за 5 минут
date: 2010-03-13 17:45:37 +0300
draft: false
tags: [old-site, backup, linux, резервное копирование, amazon, s3]
deprecated: true
---
Настраиваю сейчас под свои веб-девелоперские нужды сервер на основе Debian lenny и когда дошел до настройки резервного копирования данных стало понятно, что задача эта хоть и простая, но очень уж муторная: нужно написать и отладить скрипты, которые будут архивировать нужные папки (причем желательно делать инкрементальные архивы), базы данных, хранилища subversion, а затем переносить эти архивы на удаленный сервер. Задача в общем-то посильная для любого опытного программиста, но минимум день-два написание этих скриптов отнимет.

Очень удачной находкой для решения этой задачи стал [backup-manager](http://www.backup-manager.org/about/) — это бесплатный набор bash-скриптов, позволяющих:
 - архивировать  любые папки, в том числе и создавать инкрементальные архивы. В конфиге просто указывается список директорий, которые должны быть скопированы, а также "черный список" файлов, которые копироваться не будут.
 - делать резервное копирование баз данных MySQL. В конфиге указываются логин и пароль mysql-юзера, имеющего доступ к базам, а всю остальную работу backup-manager делает сам.
 - делать резервное копирование svn-репозиториев, причем бэкап делается не копированием папки с хранилищем, а с помощью команды <em>svnadmin dump</em>.
 - копировать созданные архивы на удаленные сервера по FTP, SSH или (это самая важная для меня фича) в хранилище Amazon S3, а также записывать их на DVD.

Таким образом, один этот этот набор скриптов решил абсолютно все мои задачи, связанные с резервным копированием. Настраивается все это хозяйство не более чем за пять минут, так как в конфигурационном файле каждый параметр имеет подробные комментарии, так что проблем с настройкой возникнуть ни у кого не должно.

Правда запустить копирование архивов на Amazon S3  с ходу не получилось, описание и решение возникших трудностей под катом.
<!--more-->
При попытке скопировать данные в хранилище Amazon S3 backup-manager падал с ошибкой типа:
```
Error reported by backup-manager-upload for method "s3", check "/tmp/bmu-log.kRZndC"
```
В свою очередь в файле `/tmp/bmu-log.kRZndC` лежало абсолютно неинформативное сообщение:
```
The upload transfer "s3" failed.
```
Но вот в syslog записывались более полезные сообщения:
```
Mar 12 16:12:26 dom7 backup-manager[26326]: info * Using the upload method "S3".
Mar 12 16:12:26 dom7 backup-manager-upload[28932]: info  * Trying to upload files to s3 service - main::verbose (/usr/bin/backup-manager-upload l. 1000)
Mar 12 16:12:26 dom7 backup-manager-upload[28932]: error * Net::Amazon::S3 is not available, cannot use S3 service : Can't locate Net/Amazon/S3.pm in @INC (@INC contains: /etc/per$
Mar 12 16:12:26 dom7 backup-manager-upload[28932]: error * The upload transfer "s3" failed. - main::verbose_error (/usr/bin/backup-manager-upload l. 1007)
Mar 12 16:12:26 dom7 backup-manager[26326]: error * Error reported by backup-manager-upload for method "s3", check "/tmp/bmu-log.kRZndC".
Mar 12 16:12:26 dom7 backup-manager[26326]: debug * DEBUG: exec_post_command()
Mar 12 16:12:26 dom7 backup-manager[26326]: info * Releasing lock
Mar 12 16:12:26 dom7 backup-manager[26326]: debug * DEBUG: release_lock()
```
Эти ошибки были устранены после установки пакета `libnet-amazon-s3-perl`, но копирование на S3 опять работать не захотело, теперь уже с такими сообщениями об ошибках:
```
Mar 12 16:35:45 dom7 backup-manager[4800]: info * Using the upload method "S3".
Mar 12 16:35:45 dom7 backup-manager-upload[7272]: info  * Trying to upload files to s3 service - main::verbose (/usr/bin/backup-manager-upload l. 1000)
Mar 12 16:35:45 dom7 backup-manager-upload[7272]: error * File::Slurp is not available, cannot use S3 service - main::send_files_with_s3 (/usr/bin/backup-manager-upload l. 1001)
Mar 12 16:35:45 dom7 backup-manager-upload[7272]: error * The upload transfer "s3" failed. - main::verbose_error (/usr/bin/backup-manager-upload l. 1007)
Mar 12 16:35:45 dom7 backup-manager[4800]: error * Error reported by backup-manager-upload for method "s3", check "/tmp/bmu-log.uOcYNB".
Mar 12 16:35:45 dom7 backup-manager[4800]: debug * DEBUG: exec_post_command()
Mar 12 16:35:45 dom7 backup-manager[4800]: info * Releasing lock
Mar 12 16:35:45 dom7 backup-manager[4800]: debug * DEBUG: release_lock()
```
После установки пакета `libfile-slurp-perl` пропали и эти ошибки и данные стали корректно копироваться на S3. Ура! Теперь остается добавить запуск бэкап менеджера в cron и можно спать спокойно :)
---
title: HTTP/2 на этом сайте
date: 2015-10-25 15:45:53 +0300
draft: false
tags: [old-site, nginx, http/2]
---
Обновил на этом сайте nginx до версии  1.9.5 и включил поддержку HTTP/2. Для теста погонял сайт до и после на <a href="http://www.webpagetest.org/">WebPagetest</a>. Честно говоря, результат измерений не сильно впечатлил, вот результат до:

[![]({{< relref "nginx-195" >}}/b.png)](http://www.webpagetest.org/result/151022_YC_Q7C/)

а вот после:

[![]({{< relref "nginx-195" >}}/a.png)](http://www.webpagetest.org/result/151023_V7_AFT/)


Но визуально, возможно подсознательно, кажется что сайт стал грузиться шустрее.

Ниже информация о том, что нужно сделать для апгрейда nginx в Ubuntu.
<!--more-->
Сначала обязательно сделайте резервную копию директории с конфигами веб-сервера &mdash; скопировать стоит всю директорию ```/etc/nginx```.

Затем проверьте какая версия уже установлена и какая доступна:
```
sudo apt-cache policy nginx
nginx:
Installed: 1.4.6-1ubuntu3.1
Candidate: 1.4.6-1ubuntu3.1
Version table:
*** 1.4.6-1ubuntu3.1 0
500 http://mirrors.digitalocean.com/ubuntu/ trusty-updates/main amd64 Packages
500 http://security.ubuntu.com/ubuntu/ trusty-security/main amd64 Packages
100 /var/lib/dpkg/status
1.4.6-1ubuntu3 0
500 http://mirrors.digitalocean.com/ubuntu/ trusty/main amd64 Packages
```

В моем случае в официальном репозитории Ubuntu пока лежит nginx 1.4.6, но я знаю, что в репозитории разработчиков nginx доступен пакет с версией 1.9.5.  Для того чтобы добавить этот репозиторий создайте в директории ```/etc/apt/sources.list.d``` файл ```nginx.list``` с таким содержимым:
```
deb http://nginx.org/packages/mainline/ubuntu/ trusty nginx
deb-src http://nginx.org/packages/mainline/ubuntu/ trusty nginx
```

Далее, чтобы при установке не получить ошибку: ```W: GPG error: http://nginx.org trusty Release: The following signatures couldn't be verified because the public key is not available: NO_PUBKEY ABF5BD827BD9BF62``` скачайте с http://nginx.org/en/linux_packages.html ключ http://nginx.org/keys/nginx_signing.key и добавьте его в keyring:
```
wget http://nginx.org/keys/nginx_signing.key
sudo apt-key add nginx_signing.key
```

Теперь обновим информацию о репозиториях и еще раз посмотрим какие версии nginx доступны, должен получиться результат вида:
```
sudo apt-get update
sudo apt-cache policy nginx
nginx:
Installed: 1.4.6-1ubuntu3.1
Candidate: 1.9.5-1~trusty
Version table:
1.9.5-1~trusty 0
500 http://nginx.org/packages/mainline/ubuntu/ trusty/nginx amd64 Packages
1.4.6-1ubuntu3.3 0
500 http://mirrors.digitalocean.com/ubuntu/ trusty-updates/main amd64 Packages
*** 1.4.6-1ubuntu3.1 0
500 http://security.ubuntu.com/ubuntu/ trusty-security/main amd64 Packages
100 /var/lib/dpkg/status
1.4.6-1ubuntu3 0
500 http://mirrors.digitalocean.com/ubuntu/ trusty/main amd64 Packages
```
&nbsp;
Еще раз убедитесь, что забэкапили директорию ```/etc/nginx```. В моем случае пришлось удалить старую версию nginx, иначе я получал такую же ошибку <a href="https://www.digitalocean.com/community/questions/update-nginx-to-version-1-9-5">какая описана тут</a>, а удаление текущей версии программы удаляет существующие конфиги, поэтому критически важно иметь их резервную копию перед выполнением следующего шага. Удаляем текущую версию nginx:
```
sudo apt-get purge nginx nginx-common
```

И ставим новую версию:
```
sudo apt-get install nginx

nginx -v
nginx version: nginx/1.9.5
```

Готово.

Теперь осталось вернуть на место конфиги из бэкапа и активировать HTTP/2 для выбранных хостов. В моем случае я заменил в конфиге:
```
server {
listen       443 ssl;
server_name  romka.eu;
...
}
```

на:

```
server {
        listen       443 ssl http2;
        server_name  romka.eu;
        ...
}
```
&nbsp;
[Преимущества HTTP/2 я описал в предыдущем посте]({{< relref "nginx-ssl-http2" >}}).
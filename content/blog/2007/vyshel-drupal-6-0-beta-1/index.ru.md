---
title: "Вышел Drupal 6.0 beta 1"
date: 2007-09-17 09:37:09 +0400
draft: false
tags: [old-site, drupal-6, Работа, Новости OpenSource]
---
После 8 месяцев разработки вышла первая бета-версия мощной OpenSource [CMF](http://ru.wikipedia.org/wiki/CMF) [Drupal](http://drupal.org) семейства 6.х. Эта бета включает в себя огромное (просто ужасающее :)) количество новых фич как для пользователей, так и для программистов. Разработчики усовершенствовали механизмы работы с базами данных, систему журналирования (logging) и авторизации, для большей безопасности добавили в ядро модуль предупреждения об обновлениях.

Разработчики очень **_не рекомендуют_** использовать эту бета-версию на работающих сайтах.
<!--more--> 
**Краткий список нововведений:**

1. Усовершенствованный инсталлятор, позволяющий сделать установку еще более простой.
2. Поддержка Right to Left языков, а также возможность переводить интерфейс без установки дополнительных модулей.
3. Поддержка ядром Друпала протокола [OpenId](http://ru.wikipedia.org/wiki/OpenID).
4. Триггеры. Новая фича, позволяющая привязывать различные действия к событиям (например отправлять письмо по электронной почте при добавлении нового сообщения).
5. В ядро системы перенесен модуль Update status, информирующий администратора сайта о выходе новых патчей и апдейтов.
6. Значительно модифицированы система меню, темизации, а также модули Book и Forum.

Оригинальная новость лежит [здесь](http://drupal.org/drupal-6.0-beta1), полный список обновлений можно посмотреть [здесь](http://cvs.drupal.org/viewvc.py/drupal/drupal/CHANGELOG.txt?revision=1.223&amp;view=markup), а скачать бета-версию движка можно [отсюда](http://ftp.drupal.org/files/projects/drupal-6.0-beta1.tar.gz).
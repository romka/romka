---
title: Typo — Drupal-модуль для борьбы с опечатками на сайте
date: 2012-09-15 20:11:50 +0400
draft: false
tags: [old-site, Drupal, модуль, Работа, orphus]
---
Разработал новый модуль для Drupal 7, который позволяет пользователю выделить мышью найденную в тексте опечатку и нажатием Ctrl + Enter отправить сообщение о ней администратору сайта. Модуль не зависит от внешних сервисов типа Орфуса и тесно интегрирован с популярными модулями Друпала такими как Rules, Token, Views и Views bulk operations.

Интеграция с модулями Rules и Token, позволяет, например, настроить отправку сообщений о найденных ошибках по е-мейлу, в системный журнал или вызвать любое другое действие, доступное в модуле Rules. С помощью токенов `[typo:url]`, `[typo:text]` и `[typo:comment]` в текст сообщения можно включить информацию об опечатке.

Интеграция с Views позволяет сделать вывод списка ошибок на странице, в комплекте с модулем уже идет настроенное представление, а интеграция с Views bulk operations позволяет удалять из этого представления обработанные сообщения.

По умолчанию, все сообщения старше 3 дней автоматически удаляются, но это действие можно отключить в настройках модуля.

Popup-окно с формой отправки опечатки выводится модулем Ctools и его вид может быть изменён как правкой CSS-файла, так и правкой соответствующего tpl-файла. Ctools — это единственная зависимость модуля, остальные модули (Rules, Views, etc) нужны только если вы хотите использовать соответствующий функционал.

Скачать модуль можно на странице проекта: http://drupal.org/project/typo.

Испытать этот модуль вы можете прямо на этом сайте, список отправленных отчетов об опечатках доступен всем посетителям здесь: [http://romka.eu/typo-reports](http://d7.romka.eu/typo-reports) (на реальном сайте к этому представлению анонимам лучше не давать).

**upd**
Модуль упомянули в [обзоре в блоге Cocomore](http://drupal.cocomore.com/blog/modules-month-september-more-interesting-new-drupal-modules), жду наплыва установок на агнлоязычных сайтах :)
<!--more-->
---
title: Несколько статей о Друпале
date: 2010-01-03 22:16:18 +0300
draft: false
tags: [old-site, Drupal, статья, Работа]
---
В течение последнего года я написал три статьи о [CMS Drupal](http://drupal.org), которые были опубликованы в бумажной и [электронной версии журнала PC Magazine/RE](http://pcmag.ru). Сейчас я публикую "авторские" **[^1]** версии этих статей. Каждая статья разбита на несколько разделов и ниже я привожу ссылки и описания каждого из них.

## Первая статья "[Разработка сайта на Drupal](http://pcmag.ru/solutions/detail.php?ID=32535)"

 - "[Часть 1. Введение]({{< relref "drupal-article-1-part-1-vvedenie" >}})". В этой части рассказывается о возможностях Друпала "из коробки", а также об основных дополнительных модулях. Таксономия, ревизии, мультисайтинг — это совсем не страшно.
 - "[Часть 2. Архитектура Друпала]({{< relref "drupal-article-1-part-2-drupal-architecture" >}})". Здесь сказаны общие слова о модульной системе Друпала, механизмах работы с формами, базой данных и кешем. Подробнее эти вопросы будут рассмотрены в следующих разделах и статьях.

После прочтения первых двух частей этой статьи новичок, задающийся вопросом "подойдет ли Друпал для моего нового суперстартапа", должен на 100% определиться с ответом на этот вопрос. Вообще, в 95% случаев на этот вопрос можно ответить утвердительно, с оговоркой, что работать над проектом будет профессионал хорошо знакомый с Друпалом.
 - "[Часть 3. Модули Drupal]({{< relref "drupal-article-1-part-3-drupal-modules" >}})". CCK, Views, Imagecache, Panels, Ubercart — модули Друпала покрывающие 90% возникающих задач. В этой части статьи даны краткие описания каждого из перечисленных модулей.
 - [Часть 4. Интранет-сайт на Друпале]({{< relref "drupal-article-1-part-4-intranet-site" >}}). Первый практический пример, в нем разрабатывается интранет-сайт для большой компании. Цель этого раздела — показать возможности, которыми обладает Друпал без доработки напильником. При разработке используются только существующие модули и не написано ни единой строчки программного кода. Аналогичное, только значительно более "кастомное" решение я успешно внедрил в одной из компаний со штатом в несколько сотен человек.
 - "[Часть 5. Социальная сеть на Друпале]({{< relref "drupal-article-1-part-5-social-network" >}})". Точнее не социальная сеть, а коллективный блог с элементами социальной сети. Описание более новой версии примера описанного в этом раздедле можно найти на [Швабрешвабр](http://shvabrashvabr.ru).
 - "[Часть 6. Оптимизация Друпал]({{< relref "drupal-article-1-part-6-drupal-optimization" >}})". Этот раздел написал Александр Графов, он же [axel](mailto:axel@drupal.ru). Друпал часто критикуют за низкую производительность. В этом разделе рассказано о приемах, позволяющих "разогнать" движок.


## Вторая статья "[Пример разработки модуля для Drupal](http://pcmag.ru/solutions/detail.php?ID=36589)"

 - "[Часть 1. Основы модульной системы Друпала]({{< relref "drupal-article-2-part-1-drupal-develop-module-vvedenie" >}})". Что такое хуки? Где и какие файлы с программным кодом должны быть созданы, чтобы Друпал посчитал их "модулем"? Где найти дополнительную информацию? Ответы на перечисленные вопросы в первой части второй статьи.
 - "[Часть 2. Разработка простейшего модуля]({{< relref "drupal-article-2-part-2-drupal-develop-module" >}})". Первые шаги при разработке любого модуля: описание *.info-файла модуля и хуков hook_perm, hook_menu.
 - "[Часть 3. Введение в темизацию Друпала (для программистов, а не дизайнеров)]({{< relref "drupal-article-2-part-3-drupal-develop-module-cron-and-themeing" >}})". В этом разделе рассказано о том, как правильно разрабатывать модули, чтобы сторонние разработчики могли без проблем (читай "без правки исходного кода модуля") изменять внешний вид данных, возвращаемых модулем.


## Третья статья "[Темизация Друпал](http://pcmag.ru/solutions/detail.php?ID=37518)"

 - "[Часть 1. Введение]({{< relref "drupal-article-3-part-1-drupal-themeing">}})". Во введении рассказано о шаблонных движках, которые могут быть использованы в Друпале, даны определения основных терминов, использованных в тексте (тема оформления, регион, блок), а также приведено несколько полезных ссылок.
 - "[Часть 2. Анатомия темы оформления]({{< relref "drupal-article-3-part-2-drupal-themeing-anatomy" >}})". Здесь дано подробное описание каждого из файлов-шаблонов, использующихся в темах оформления, а также рассказано о том, как определить отдельный шаблон для каждой страницы или группы страниц.
 - "[Часть 3. Forms API и темизация]({{< relref "drupal-article-3-part-3-drupal-forms-api" >}})". В этом разделе приводится пример разработки новой и изменения существующей формы с помощью Forms API Друпала, а также о изменении внешнего вида любого элемента формы в отдельности или формы целиком.
 - "[Часть 4. Темизация Views]({{< relref "drupal-article-3-part-4-drupal-themeing-views" >}})". Небольшой раздел, рассказывающий о том, как изменить внещний вид данных, возвращаемых модулем Views.


[^1]: Отличий от "редакторской" версии немного, но они есть. В основном эти отличия касаются форматирования текста (например, в журнальной версии просили не использовать маркированные списки), а также трактования написания и произношения тех или иных заимствованных из английского языка технических терминов. Кроме того, я немного поменял разделение статей на разделы и сделал более читабельную подсветку программного кода.
<!--more-->

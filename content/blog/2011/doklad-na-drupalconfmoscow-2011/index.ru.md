---
title: Доклад на DrupalConfMoscow 2011
date: 2011-04-25 01:18:39 +0400
draft: false
tags: [old-site, Работа, Друпал, доклад, конференция]
---
_23 апреля 2011 года принял участие в конференции <a href="http://drupalconf.ru/">DrupalConfMoscow 2011</a>. Вместе с Тарасом Савчуком рассказал о том, как мы настраивали Друпал и системное окружение, чтобы сайт <a href="http://forbes.ru">forbes.ru</a> мог выдержать нагрузку 250 тысяч уников в сутки. Ниже видео и текстовая версия моей части доклада._

<object width="450" height="330"><param name="video" value="http://static.video.yandex.ru/lite/vaspi/4zk6epousu.2914/"/><param name="allowFullScreen" value="true"/><param name="scale" value="noscale"/><embed src="http://static.video.yandex.ru/lite/vaspi/4zk6epousu.2914/" type="application/x-shockwave-flash" width="450" height="330" allowFullScreen="true" scale="noscale"> </embed></object>
<!--more-->
## Вступление

Моя часть доклада посвящена тому, какие мы использовали модули, для оптимизации Друпала под нашу нагрузку, о том как они настроены, с какими мы сталкивались проблемами и какие видим решения.

Посещаемость сайта [forbes.ru](http://forbes.ru) (с ноября 2009 по август 2010 известного как forbesrussia.ru):

 - в ноябре 2009 года составляла примерно 45 тысяч уников и 200 тысяч просмотров в день,
 - летом 2010 — 80-90 тысяч уников и 400 тысяч просмотров в день,
 - сейчас, весной 2011 — 120-130 тысяч уников, 600 тысяч просмотров в обычный день и в моменты пиковой нагрузки свыше 250 тысяч уников и 1,5 млн просмотров в день.

## Пара слов о текущем положении дел

90% посетителей сайта являются анонимами, это означает что таким пользователям не нужно создавать персонифицированные страницы, а это в свою очередь значительно упрощает систему кеширования.

Для ускорения генерации страниц зарегистрированным пользователям у нас используется memcache с Друпальским модулем memcache (`memcache.db.inc`, а не `memcache.inc`).

Для кеширования страниц, отдаваемых анонимам используется модуль [Boost](http://drupal.org/project/boost).

## Что такое Boost и какими фичами он обладает?

Суть  модуль Boost заключается в том, что сгенерированные для анонимов страницы складываются в файловый кеш.

Когда на сайт приходит очередной аноним, то Apache, руководствуясь специальными правилами, прописанными в .htaccess, пытается найти закешированную страницу на жестком диске. Если ему это удается, то он отдает эту страницу пользователю не дергая связку PHP+Drupal, таким образом сильно увеличивается скорость отдачи контента и значительно снижается нагрузка сервер.

В случае если страница в кеше не найдена, то управление передается Друпалу, он генерирует страницу и кладет ее в кеш.

Фактически, задачей Буста является только сохранить страницу в кеш, если её запросил аноним и вовремя этот кеш очистить. Отдача кеша полностью осуществляется веб-сервером.

**Важный момент**. Буст хранит в базе данных информацию о закешированных страницах. Это позволяет:

 - при изменении одной страницы очищать кеш всех связанных с ней страниц, например страниц, созданных модулем Views;
 - не очищать кеш страниц, которые не были изменены с момента создания кеша.


При настройке Буста разработчику нужно ответить на два вопроса:

 - как часто будет чиститься кеш?
 - по какому принципу должен создаваться/очищаться кеш? 


## Как часто очищается кеш?

Ответ на этот вопрос получить проще всего, все зависит от частоты обновления контента на сайте и критичности того факта, что пользователь не увидит обновления до истечения срока жизни кеша. В нашем случае время жизни кеша равно 10 минутам.

## По какому принципу создается/очищается кеш?

Вопрос очистки кеша достаточно тонкий:

 - кеш может создаваться на определенное время, например на 10 минут, очищаться по Крону, и пересоздаваться по запросу пользователя.
 - кеш может создаваться на определенное время и пересоздаваться в фоне, вне зависимости от действий посетителя.
 - кеш может создаваться навечно и перегенерироваться только в случае изменения ноды.


Давайте по очереди рассмотрим преимущества и недостатки каждого варианта.

## Временный кеш, генерация по запросу пользователя

На первый взгляд этот вариант кеширования может показаться самым оптимальным. Если задать время жизни кеша равное, например, 10 минутам, то анонимы всегда будут видеть практически самую актуальную версию контента.

Недостаток метода состоит в том, что на сайте, как в нашем случае, может быть несколько десятков тысяч документов, при этом только малая часть из них просматривается в данный конкретный десятиминутный диапазон времени. Старые материалы, которые были созданы несколько месяцев или лет назад могут просматриваться раз в час или того реже, а так как кеш чистится раз в 10 минут, то практически всегда такие страницы будут генерироваться заново, а не отдаваться из кеша.

## Вечный кеш

Логичным решением проблемы предыдущего способа кеширования является создание вечного кеша. То есть кеш создается при первом просмотре материала и удаляется только при его изменении. Но такой подход не применим на сайтах, которые выводят на страницах блоки с динамически обновляемой информацией, например, последние новости, посты на форуме или курсы валют. Если использовать этот метод работы с кешем, то на закешированых год назад страницах будут выводиться блоки с новостями годовалой давности.

Решений у проблемы два:

 - использования ESI/SSI или java-script для отображения блоков
 - генерация кеша в фоне

Вариант с java-скрипт не подходит для сайтов, которые хотят, чтобы их полюбили поисковые системы, так как поисковики не увидят содержимое блоков.

Использование ESI/SSI — один из шагов, который мы собираемся применить в ближайшее время. Можно копнуть в сторону модуля http://drupal.org/project/ssi (хотя пугает количество его использований) или создавать собственное решение.

Суть решения в том, что также как модуль Буст кеширует в файловую систему страницы, должны в виде отдельных html-файлов кешироваться и отдельные блоки. В шаблонах вместо вставки блоков должны вставляться SSI-инструкции, внедряющие в шаблоны страниц html-код блоков.

Такое решение мне видится идеальным, но оно пока не реализовано.

Преимущество ESI перед SSI показывает вот такая строка:
```
<esi:include src="http://example.com/1.html" alt="http://bak.example.com/2.html" onerror="continue"/>
```

А это SSI:
```
<!--#include file="footer.html" -->
```

## Использование краулера (генерация кеша в фоне)

Этот способ кажется мне наименее удобным и эффективным, он предполагает, что кеш будет жить ограниченное время, например 10 минут, после очистки кеша будет запускаться специальный скрипт-краулер, который будет генерировать кеш для всех страниц.

Использование этого метода приемлемо только для небольших сайтов, в нашем случае перегенерирование кеша более чем 60 тысяч нод раз в 10 минут — это недопустимо большая нагрузка на сервер.

## Проблема Буста на очень нагруженных проектах

У Буста есть одна проблема. Он не умеет работать в системах, в которых два фронтенда с Друпалом работают с одним бэкендом с БД.

Если настроить такую схему, то каждый Буст будет создавать собственную копию кеша, причем структура директорий кеша и записи, оставляемые Бустом в БД будут полностью идентичными. Буст не пишет в БД имя сервера, который сделал запись о кеше. Таким образом, возможна следующая ситуация:

 - первый сервер закешировал страницу node/123 и сделал в БД запись об этом;
 - второй сервер закешировал эту же страницу node/123 и обновил запись в БД, созданную первым сервером;;
 - на первом сервере запустился крон, удалил из своей файловой системы закешированную версию страницы node/123 и удалил из БД все записи, связанные с этой страницей;
 - на втором сервере запустился крон, увидел что в БД нет записи о том, что в кеше лежит устаревшая версия страницы node/123 и ничего не сделал. При этом Апач на втором сервере по прежнему продолжает отдавать старую версию страницы node/123.


Способы решения проблемы:

 - научить Буст писать некий id сервера в БД и при очистке кеша каждый сервер будет удалять из БД только те записи, которые созданы этим сервером.
 - вынести таблицы, с которыми работает в Буст, в отдельную БД и научить Буст работать с этой БД. У каждого сервера должна быть отдельная БД.
 - Синхронизировать директории с кешем rsync’ом/csync'ом.

Небольшой вывод, основанный на собственном опыте. Boost — модуль который <u>должен</u> быть использован на 99% Друпал-сайтов. Он не требует установки на сервере дополнительного софта, он дает сайту некоторый прирост в скорости отдачи контента и при этом не имеет серьезных недостатков.

## Memcache
Для Друпала есть как минимум 2 модуля, позволяющих использовать Мемкеш: [cacherouter](http://drupal.org/project/cacherouter) и [memcache](http://drupal.org/project/memcache). Мы на forbes.ru используем модуль memcache. Кэшроутер хорош тем, чем предоставляет доступ сразу к нескольким бэкендам для хранения кеша, но в случае с мемкешом он имеет меньше возможностей (по крайней мере имел на момент старта проекта) чем модуль мемкеш. Например, он не позволял кешировать в памяти сессии и алиасы путей.

## Пара слов о том, как устроена система кеширования в Друпале

Ядро Друпала содержит файл includes/cache.inc, в котором определены функции cache_get, cache_set и cache_clear_all, из их названий нетрудно догадаться для чего они предназначены. Кеш в Друпале, по умолчанию, хранится в БД. Разработчик, который хочет переопределить друпальские функции работы с кешем должен создать свой собственный файл, содержащий одноименные функции, и задать специальный параметр в файле settings.php ($conf['cache_inc'] ='sites/all/modules/memcache/memcache.db.inc';), который скажет Друпалу, что вместо родного cache.inc нужно использовать альтернативный файл.

Аналогичная ситуация и с файлом ядра includes/session.inc, он определяет ряд функций для работы с сессиями и любой разработчик может переопределить их в своем модуле.

Также, при желании можно заменить и инструменты для работы с алиасами путей, добавив им кеширование в мемкеше, но здесь в шестом Друпале не обойтись без патча файла ядра includes/path.inc (как дела обстоят в седьмом не знаю). Эта задача решается модулем pathcache.

Модуль memcache предлагает замену для стандартных друпальских механизмов работы с кешем и с сессиями.

В случае с сессиями нет почти ничего интересного, как я уже говорил, необходимо в settings.php прописать путь к файлу memcace-session.inc, который идет в комплекте с модулем memcache, для того чтобы заменить стандартные функции Друпала для работы с сессиями на новые.

В случае с кешем модуль memcache предоставляет два файла, переопределяющих друпальские функции для работы с кешем: memcache.inc и memcache.db.inc. Из названий можно догадаться, что первый в своей работе никак не использует БД, а второй использует. Разработчику нужно понимать их отличия для того чтобы решить, который из них выбрать.

Вообще, в комментариях к последним релизам модуля memcache сказано, что memcache.db.inc является устаревшим и в следующих релизах модуля он будет удален. Отличие его от memcache.inc состоит в том, что весь кеш одновременно записывается и в мемкеш, и в базу данных. При попытке прочитать кеш сначала идет запрос в мемкеш, если в нем кеш не найден, то он отправляется запрос в БД. Если кеш не найден и в БД то возвращается FALSE.

Логично предположить, что функции из memcache.inc должны работать шустрее, чем функции из memcache.db.inc, но на практике это не так (хотя [профессионалы](http://prodrupal.ru) рекомендуют обновиться до последней dev-версии модуля, там эта проблема должна быть решена). По этой причине мы используем memcache.db.inc.
## Проблемы и их решения

Исходя из своего опыта я могу сказать, что и ядро Друпала, и большинство контриб модулей написано очень грамотно и в работе сайта не возникает проблем по их вине. Практически все проблемы, с которыми мы сталкивались возникали из-за кривизны собственных рук.

В таких ситуациях на помощь приходили логи медленных запросов MySQL и утилиты для дебага и профилирования кода, мы, например, используем [xdebug](http://xdebug.com).

Xdebug — это расширение для PHP, которое позволяет вести лог выполнения php-скрипта. Лог сохраняется в формате cachegrind и может быть скормлен специальной утилите, в которой с помощью понятного интерфейса можно будет найти “бутылочные горлышки” в потоке выполнения скрипта.

Из проблем, с которыми могут столкнуться все высоконагруженные сайты на Друпале, мы столкнулись с такими бутылочными горлышками:

 - сообщение об ошибке 404. Эта страница генерируется заново для каждого ошибочного запроса, а это не нужно в большинстве случаев, поэтому мы заменили её статичной. Эта проблема в основном, появлялась по нашей собственной вине: модуль Pathauto был настроен так, что он генерировал УРЛы на основе заголовков статей и при изменении заголовка удалял старый УРЛ и создавал новый. Если статью со старым УРЛом успевал подхватить сервис Яндекс.Новости, то можно было получить несколько тысяч ошибок 404 за короткий промежуток времени.
 - Хлебные крошки — до 10% времени генерации страницы работала функция drupal_get_breadcrumbs, создающая хлебные крошки. С учетом того что они у нас не используются это была лишняя трата времени. Пропатчили функцию, которая их создает.
 - Был еще ряд проблем, но они характерны только нашему проекту.

В общем, если ваш сайт тормозит, то включить xdebug и проанализировать его логи — это первое действие, которое вы должны сделать перед тем как обвинить Друпал в тормознутости. Только надо понимать, что логи иксдебага имеют большой объем, до нескольких мегабайт на лог действий, которые выполняет Друпал при генерации одной страницы. На forbes.ru ночью мы собираем несколько гигабайт логов за 2-3 минуты. По этому включать его надолго нельзя и для поиска редковозникающих проблем он не подходит.
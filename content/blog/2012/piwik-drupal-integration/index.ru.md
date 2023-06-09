---
title: Интеграция системы статистики Piwik с Drupal 6
date: 2012-10-21 13:48:03 +0400
draft: false
tags: [old-site, Drupal, Работа, Piwik, статистика]
---
При работе над Drupal-проектом у меня возникла необходимость сбора детальной статистики о просмотрах материалов и вывода этой статистики в виде блоков, отображающих самые просматриваемые материалы за последние день, неделю и месяц. Стандартный друпальский модуль Statistics (и в шестом, и в седьмом Друпале) для решения такой задачи абсолютно неприменим:

 - во-первых он осуществляет сбор статистики на `hook_exit()` и не будет работать корректно со сколько-нибудь серьезными системами кеширования, например при использовании [Varnish или модуля Boost]({{< relref "keshirovanie-na-drupal-sayte-sravnenie-effektivnosti-vstroennogo-v-drupal-kesha-staticheskogo" >}}).
 - во-вторых модуль Statistics собирает статистику за всё время существования материала, сделать выборку вида: "сколько раз был просмотрен материал за последний день" с этим модулем невозможно. По этому при использовании этого модуля исходную задачу пришлось бы модифицировать к виду: вывести список самых просматриваемых материалов созданных за последние день, неделю или месяц, но этот подход неприемлем, так как на сайте существуют материалы старше месяца, способные попасть в топ по просмотрам.


Таким образом,  возникла необходимость внедрить полноценную систему статистики и интегрировать ее с Друпалом. Под полноценными системами я понимаю сервисы типа Google Analytics или Яндекс.Метрика, используя API которых можно запросить статистику просмотров материалов за любой диапазон дат. Достоинством этих сервисов является то, что они у себя хранят всю статистику, а она на посещаемом ресурсе может занимать немало места, их недостаток — все таки это внешние сервисы и неизвестно, что с ними случится завтра: сломаются, станут платными, не захотят внедрять нужную пользователю фичу и т.д.

В итоге я решил установить на собственном сервере open source систему статистики [Piwik](http://piwik.org/) и интегрировать ее с Друпалом. Да, Пивик пока местами уступает GA и Я.М в гибкости отчетов (хотя есть в нем и отчеты, которых нет ни в ГА, ни в Я.М), но, во-первых, нужную мне задачу он решает, во-вторых он постоянно развивается своими разработчиками и может быть расширен с помощью [самописных плагинов](http://dev.piwik.org/trac).

Для седьмого Друпала есть замечательный модуль [Piwik stats](http://drupal.org/project/piwik_stats), интегрирующий Друпал с Пивиком. Суть модуля состоит в том, что он создает специальное поле, которое может быть прикреплено к любой entity (материалу, пользователю). В настройках поля задается параметр, отвечающий за то, статистика за сколько дней должна быть в этом поле. Одна entity может содержать несколько полей с разными настройками, то есть, например, каждый материал может содержать три поля с информацией о просмотрах за последние день, неделю, месяц, как раз то что мне и требовалось.

Заполнение полей данными осуществляется через [Drupal Queue API](http://api.drupal.org/api/drupal/modules%21system%21system.queue.inc/group/queue/7) по крону, но при желании стандартный механизм обработки очереди может быть заменен чем угодно, например [Rabbit MQ](http://drupal.org/project/rabbitmq).

Плюсом хранения статистики в полях является то, что статистика становится прозрачно интегрированной со всем модулями Друпала, например с Views, с помощью которого, в том числе, можно строить блоки с контексто-зависимой статистикой. То есть, например, на главной странице сайта выводить список самых популярных статей со всего сайта, а на странице статьи или раздела — выводить самые популярные статьи текущего раздела.

Основная проблема для меня состояла в том, что модуль Piwik stats работает только под седьмым Друпалом и его разработчик не планировал делать бэкпорт под шестерку, а проект, в котором мне понадобился этот функционал, работает как раз на древней шестой версии Друпала. По этому я сам сделал бэкпорт этого модуля под шестерку. Забрать мою версию модуля можно из [sandbox-проекта Piwik_stats](http://drupal.org/sandbox/romka/1794242), обсуждение этого бэкпорта с автором основного модуля тут: http://drupal.org/node/1736398.

Пока мейнтейнер модуля не хочет делать мою версию модуля официальной, из-за того, что требуется сделать детальный code review. Тем не менее, мой модуль без нареканий больше месяца работает в бою на двух Друпал 6 проектах.
<!--more-->
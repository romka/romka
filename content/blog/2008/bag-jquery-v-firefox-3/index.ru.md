---
title: Баг jQuery в Firefox 3 и WebKit
date: 2008-10-12 13:19:45 +0400
draft: false
tags: [old-site, firefox, jquery, bug, ошибка, webkit, safari, chrome, сафари, хром]
---
Работая над очередной задачей, столкнулся с проблемой, решить которую помог [Гугл](http://groups.google.com/group/jquery-en/browse_thread/thread/95465c4025cfd73d). Суть проблемы заключается в том, что в библиотеке [jQuery](http://jquery.com) 1.2.6 некорректно работают функции `width()` и `height()` в третьем Firefox'е, а также браузерах, работающих на движке [WebKit](http://ru.wikipedia.org/wiki/WebKit) — [Safari](http://ru.wikipedia.org/wiki/Safari) и [Google Chrome](http://ru.wikipedia.org/wiki/Google_Chrome). Удивительно, но даже в шестом IE, с которым обычно больше всего проблем, этого глюка нет. Природа проблемы осталась мне неясной, но известно, что она проявляется только тогда, когда в html-коде подключены сначала JS-файлы, а затем CSS-файлы и пропадает если сделать наоборот — сначала подключить все CSS-файлы, а затем все JS-файлы. В новом релизе jQuery этот баг [обещают](http://groups.google.com/group/jquery-dev/browse_thread/thread/4633136bb957660a?hl=en) исправить.
<!--more-->

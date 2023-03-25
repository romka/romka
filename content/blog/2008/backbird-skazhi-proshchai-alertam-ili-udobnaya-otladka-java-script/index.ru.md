---
title: Backbird — скажи "прощай" алертам или удобная отладка java-script.
date: 2008-10-16 12:23:40 +0400
draft: false
tags: [old-site, java-script, Blackbird, отладка]
deprecated: true
---
Нашел очень удобный инструмент для отладки ява-скриптов — библиотеку [Blackbird](http://www.gscottolson.com/blackbirdjs/). Её необходимо скачать и подключить к необходимой странице, после чего на странице появится удобная консоль, в которую можно будет выводить отладочные сообщения. Сообщения делятся на типы — debug, info, warning, error, а в консоли предусмотрены фильтры по типам.

Любимый многими разработчиками, в том числе и мной, [Firebug](http://getfirebug.com) обладает значительно более широким функционалом, но у Blackbird есть одно преимущество — он совместим с браузерами Firefox 2+, Inernet Explorer 6+, Opera 9+, Safari 2+ и Google Chrome. [Firebug Lite](http://getfirebug.com/lite.html), который также как и Blackbird работает со всеми перечисленными бразуерами, уступает ему по возможностям.
<!--more-->
Вывод данных в консоль делается просто:
```
log.debug( 'this is a debug message' );
log.info( 'this is an info message' );
log.warn( 'this is a warning message' );
log.error( 'this is an error message' );
```

Кроме вывода отладочных сообщений Blackbird позволяет измерять скорость работы скриптов, для этого в библиотеке реализован метод profile:
```
// запускаем таймер с именем some name
log.profile("some name")
/*
А здесь ява-скрипт, скорость работы которого необходимо измерить
*/
// останавливаем таймер с именем some name
log.profile("some name")
```

Примеры использования, а также описание горячих клавиш можно найти на [официальной странице проекта](http://www.gscottolson.com/blackbirdjs/).
---
title: Вращение изображений при помощи Javascript
date: 2009-03-04 13:45:01 +0300
draft: false
tags: [old-site, jquery, Javascript, изображение, вращение, поворот, wilq32, mootools]
deprecated: true
---
Довольно давно я задумался о решении такой задачки: необходимо при помощи ява-скрипта поворачивать картинку на заданный угол. Сейчас нашел её решение — плагин <a href="http://wilq32.googlepages.com/wilq32.rollimage222">wilq32</a> для <a href="http://jquery.com">jQuery</a>, позволяющий как просто поворачивать картинки, так и создавать анимированное вращение:
```
<div>
  <img src="/old-site/examples/rotate/eye-small.jpg" id="image">
  <img src="/old-site/examples/rotate/eye-small.jpg" id="image2">
  <img src="/old-site/examples/rotate/eye-small.jpg" id="image3">
</div>
```

Использовать плагин предельно просто, он реализует две функции rotate и rotateAnimation, которые принимают ряд параметров, детально описанных в документации.

Например, для поворота изображения достаточно использовать код:
```
$('#image').rotate(-25);
```
где "#image" — id изображения, которое мы хотим повернуть, а -25 — угол поворота.

Немного более сложный пример. Поворачиваем изображение при наведении на него курсора мышки и возвращаем его в исходное состояние, когда курсор не находится над изображением:
```
var rot=$('#image3').rotate({
    bind:
        [
            {
                "mouseover":
                    function() {
                        rot.rotateAnimation(35);
                    }
            },
            {
                "mouseout":
                    function() {
                        rot.rotateAnimation(0);
                    }
            }
        ]
});
```

Скачать плагин можно [на сайте автора](http://wilq32.googlepages.com/wilq32.rollimage222). В комментариях к плагину приведены примеры его использования.

К сожалению, на данный момент, плагин может глючить в IE, но автор обещает исправить эту недоработку к релизу плагина (пока доступна версия 0.5).

Версию этого плагина для библиотеки mootools можно найти тут: [http://www.piksite.com/mRotate/](http://www.piksite.com/mRotate/).

**Обновление.** Несколько дней назад [стала доступна](http://wilq32.blogspot.com/2009/06/jqueryplugin-update.html) версия 0.7 плагина. В ней немного изменился метод вызова анимации, а также исправлены глюки из-за которых плагин не работал в Internet Explorer.
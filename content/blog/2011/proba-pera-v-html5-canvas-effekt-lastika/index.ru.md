---
title: Проба пера в HTML5 + canvas. Эффект ластика
date: 2011-07-06 15:42:34 +0400
draft: false
tags: [old-site, canvas, html5, ластик]
---
## Задача

Создать эффект "ластика" с помощью html5 тэга canvas. Суть эффекта простая: выводится картинка, поверх картинки выводится полупрозрачный фон, если пользователь нажимает на левую кнопку мыши и начинает двигать курсор по холсту, то полупрозрачный фон должен стираться. Конечный результат [можно увидеть тут](/old-site/examples/canvas/canvas3-7.html).

Задача будет разбита на 3 части:
1. сначала мы зальем картинку равномерным фоном и научимся стирать этот фон ластиком квадратной формы.
2. Затем мы зальем картинку равномерным фоном и научимся стирать фон ластиком круглой формы.
3. И в конце мы зальем картинку полупрозрачной текстурой и научимся стирать эту текстуру.

Прежде чем читать дальше, рекомендую ознакомиться вот с этой документацией: [Обучение Canvas](https://developer.mozilla.org/ru/%D0%9E%D0%B1%D1%83%D1%87%D0%B5%D0%BD%D0%B8%D0%B5_canvas). Думаю, задачу проще было бы решить с использованием библиотек типа [Libcanvas](https://github.com/theshock/libcanvas), но мне сначала интересно было поразбираться с голым канвасом.

## Этап первый

Создаем html-страницу с холстом размером 800 на 600 и подключаем к ней файлы со стилями и скриптами ([canvas3-1.html](/old-site/examples/canvas/canvas3-1.html)). На холсте с id "working-canvas" мы будем рисовать, холст с id "fog-canvas" будет выводиться поверх рабочего холста, на нем мы будем выводить полупрозрачный фон. Working-canvas я далее буду называть нижним холстом, а fog-canvas — верхним холстом.

canvas3-1.html:
```
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="ru">
<head>
  <meta http-equiv="content-type" content="text/html; charset=utf-8" />
  <title>Эксперименты с канвасом</title>
  <link type="text/css" rel="stylesheet" media="all" href="./styles.css" />
  <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.5/jquery.min.js"></script>
  <script type="text/javascript" src="./script.js"></script>
</head>
<body>
  <div id="wrapper">
    <canvas id="working-canvas" width="800" height="600">
      Вы должны обновить ваш браузер
    </canvas>

    <canvas id="fog-canvas" width="800" height="600">
      Вы должны обновить ваш браузер
    </canvas>
  </div>  
</body>
</html>
```

На событие _document.ready_ ([canvas3-3.html](/old-site/examples/canvas/canvas3-3.html)) мы:

1. создаем 2 канваса,
2. для каждого канваса создаем по контексту,
3. вызываем функцию draw(),
4. на событие mouseDown "включаем" ластик, за работу которого отвечает функция eraser(),
5. на событие mouseUp "выключаем" ластик.

Событие _document.ready_:
```
$(document).ready(function() {
  // Создаем холсты и контексты
  var canvas = document.getElementById('working-canvas');
  var fog_canvas = document.getElementById('fog-canvas');

  var context = canvas.getContext('2d');
    var fog_context = fog_canvas.getContext('2d');
    
    if (canvas.getContext && fog_canvas.getContext){
    // если все успешно создано, выводим изображения на холсты
    draw(context, fog_context);
  }

  // Биндим эффект квадратного ластика на маусдаун
  $(fog_canvas).bind('mousedown', function(e) {
    eraser(e, context, 40);
    $(fog_canvas).bind('mousemove', function(e) {
      eraser(e, context, 40);
    });
  });

  // при маусапе отключаем ластик
  $(fog_canvas).bind('mouseup', function() {
    $(fog_canvas).unbind('mousemove');
  });
});
```

Функция draw():

1. на нижнем холсте выводит картинку,
2. верхний холст заливает полупрозрачным фоном.

```
function draw(context, fog_context) {
  // Загружаем картинку, после ее загрузки выводим её на нижний холст, верхний холст заливаем полупрозрачным фоном
  var img = new Image();
  img.src = 'ya.jpg';
  img.onload = function() {
    // когда изображение загружено, выводим его на холст
    context.drawImage(img, 200, 200);

    // заливаем изображение полупрозрачным фоном
    fog_context.fillStyle = "rgba(0, 200, 200, 0.5)";
    fog_context.fillRect (200, 200, 430, 400);
  }
}
```

Ход работы над этой задачей вы можете увидеть по ссылкам: [canvas3-1.html](/old-site/examples/canvas/canvas3-1.html), [canvas3-2.html](/old-site/examples/canvas/canvas3-2.html), [canvas3-3.html](/old-site/examples/canvas/canvas3-3.html), [canvas3-4.html](/old-site/examples/canvas/canvas3-4.html), [canvas3-5.html](/old-site/examples/canvas/canvas3-5.html), [canvas3-6.html](/old-site/examples/canvas/canvas3-6.html) (тупиковая ветвь), [canvas3-7.html](/old-site/examples/canvas/canvas3-7.html) (окончательная версия). На протяжении всей работы заметно будет меняться только содержимое функции eraser().

Нижний холст будет использоваться в качестве эталона: когда нам понадобится "стереть" определенную область на верхнем холсте мы скопируем нужные пикселы с нижнего холста и заменим ими ту же область верхнего холста.

Сначала мы реализуем простейший эффект стирания, с помощью метода clearRect. Для этого создаем функцию eraser() и вешаем её работу на событие onMouseDown. На OnMouseUp делаем анбинд:
```
function eraser(e, context, fog_context, radius) {
  /**
  * Пока в эту функцию передаются только рабочий контекст, радиус (пока он используется для задания стороны квадрата ластика) и объект event.
  * Позже, нам понадобится добавить сюда передачу второго контекста
    */
  var mouseX, mouseY;

  if(e.offsetX) {
    mouseX = e.offsetX;
    mouseY = e.offsetY;
  }
  else if(e.layerX) {
    mouseX = e.layerX;
    mouseY = e.layerY;
  } else {
    mouseX = -1000;
    mouseY = -1000;
  }
  
  // вот это и есть ластик:
  fog_context.clearRect(mouseX, mouseY, radius, radius);
}
```
Эффект ластика в таком виде не очень удобен ([пример](/old-site/examples/canvas/canvas3-3.html)), так как невозможно изменить его форму. Для того, чтобы исправить этот недостаток, как я уже писал выше, необходимо скопировать нужную область из нижнего холста и заменить ею ту же область верхнего холста, а для этого нужно воспользоваться методами getImageData и putImageData. Из названий не трудно догадаться, что первый метод получает информацию о цветах пикселов области, воторой позволяет изменить заданную область холста.

Новая версия функции eraser():
```
function eraser(e, context, fog_context, radius) {
  /**
  * Пока в эту функцию передаются только рабочий контекст, радиус (пока он используется для задания стороны квадрата ластика) и объект event.
  * Позже, нам понадобится добавить сюда передачу второго контекста
  */
  var mouseX, mouseY;

  var diameter = radius * 2;
  
  if(e.offsetX) {
    mouseX = e.offsetX;
    mouseY = e.offsetY;
  }
  else if(e.layerX) {
    mouseX = e.layerX;
    mouseY = e.layerY;
  } else {
    mouseX = -1000;
    mouseY = -1000;
  }
  
  // Этот вариант ластика нам не подходит:
  //context.clearRect(mouseX, mouseY, radius, radius);
  // вместо него используем такой: сначала из нижнего холста получаем значения цветов пикселов, попавших под ластик
  imagedata = context.getImageData(mouseX - radius, mouseY - radius, diameter, diameter);
  // Затем заменяем этими пикселами пикселы на верхнем холсте:
  fog_context.putImageData(imagedata, mouseX - radius, mouseY - radius);
}
```
[Рабочий пример квадратного ластика на html5 + canvas](/old-site/examples/canvas/canvas3-4.html).

## Этап второй. Учимся стирать ластиком круглой формы

Для того чтобы изменить форму ластика, необходимо преобразовать содержимое объекта, возвращаемого методом getImageData. Этот объект содержит 3 свойства: width, height и data. Первые два элемента в посянении не нуждаются, последний элемент — это массив, содержащий информацию о цветах пикселов, входящих в выделенную область.

Формат этого массива имеет не очень удобную форму, это одномерный массив такого вида: [r1, g1, b1, a1, r2, g2, b2, a2, ... rN, gN, bN, aN], другими словами, за цвет пиксела M отвечают элементы массива от (M - 1) * 4 до (M - 1) * 4 + 3:
(M - 1) * 4       — красный
(M - 1) * 4 + 1 — зеленый
(M - 1) * 4 + 2 — синий
(M - 1) * 4 + 3 — альфа

При этом видно, что в этом массиве нет разбиения на строки, то есть массив, содержащий 1600 элементов, то есть информацию о 400 пикселах, может описывать как прямоугольник 10 на 40, так и квадрат 20 на 20.

Дальше немного тригонометрии:

1. нам необходимо получить (x, y) координаты курсора мыши, 
2. те пикселы на верхнем холсте, которые попадают в круг определенного радиуса с центром (x, y) заменить пикселами с нижнего холста с теми же координатами,
3. те пикселы на верхнем холсте, которые не попадают в круг, оставить без изменений.

[Рабочий пример круглого ластика можно увидеть тут](/old-site/examples/canvas/canvas3-5.html). А вот измененная часть функции eraser():
```
  // Этот вариант ластика нам не подходит:
  //context.clearRect(mouseX, mouseY, radius, radius);
  // вместо него используем такой: сначала из нижнего холста получаем значения цветов пикселов, попавших под ластик
  imagedata = context.getImageData(mouseX - radius, mouseY - radius, diameter, diameter);
  fog_imagedata = fog_context.getImageData(mouseX - radius, mouseY - radius, diameter, diameter);

  //for(elem in imagedata) {
  //  console.log(elem);
  //}
  
  elem_count = diameter * diameter * 4;
  
  // Затем, воспользовавшись знаниями из геометрии за 7 класс, преобразовываем массив пикселов
  i = 0;
  while(i <= elem_count) {
    /*
    каждый элемент массива это не массив ргба, а отдельная компонетна цвета, то есть для нулевого элемента
    0 - р
    1 - г
    2 - б
    3 - а
    
       для m = i / 4 элемента:
       i     - р
       i + 1 - г
       i + 2 - б
       i + 3 - а
       
       
       c
       |
       |\
       | \
       |  \
       |   \
       |____\
       b     a
       
       ac должно быть меньше radius
       
       a — центр круга
      
       */
  
      // определяю координаты точки в матрице. m — номер в строке, n — номер строки
      m = i / 4;
      if (m < diameter) {
        n = 0;
      } else {
        n = 0;
        while(m >= diameter) {
          m -= diameter;
          n++;
        }
      }
      
      bc = radius - m;
      if(bc < 0) {
        bc = -bc;
      }
      
      ab = radius - n;
      if(ab < 0) {
        ab = -ab;
      }
      
      if(Math.sqrt(bc * bc + ab * ab) < radius) {
        // Если пиксел попал в круг, то меняю его цвет как на нижнем холсте, иначе оставляю цвет на такой как на верхнем холсте
        fog_imagedata['data'][i]     = imagedata['data'][i];     // r
        fog_imagedata['data'][i + 1] = imagedata['data'][i + 1]; // g
        fog_imagedata['data'][i + 2] = imagedata['data'][i + 2]; // b
        fog_imagedata['data'][i + 3] = imagedata['data'][i + 3]; // a
      }
      
      i += 4;
  }
  
  // Затем заменяем этими пикселами пикселы на рабочем холсте:
  fog_context.putImageData(fog_imagedata, mouseX - radius, mouseY - radius);
```

## Этап третий. Теперь заменим однотонную заливку на заливку текстурой

Небольшая проблема вывода полупрозрачной текстуры состоит в том, что метод drawImage(), который мы используем для вывода изображения не позволяет сделать картинку полупрозрачной:

1. метод globalAlpha() эту задачу не решает,
2. эксперименты с createPattern() тоже ни к чему интересному не привели (пример [canvas3-6.html](/old-site/examples/canvas/canvas3-6.html)), хотя во время этих экспериментов, я наткнулся на интересный пример: http://jsfiddle.net/UxDVR/7/.

Чтобы решить эту проблему мы прежде чем выводить картинку на верхний холст получим информацию об изображении с помощтю getImageData, каждый четвертый элемент массива data заменим, например, на 192 (это значение альфа-канала), а затем содержимое полученного массива перенесем на верхний холст ([canvas3-7.html](/old-site/examples/canvas/canvas3-7.html)).

Ниже измененная версия функции draw():
```
function draw(context, fog_context) {
  // загружаем содержимое для верхнего слоя
  var img_moroz = new Image();
  img_moroz.src = 'moroz-small-2.png';
  img_moroz.onload = function() {
  
      // загружаем содержимое нижнего слоя
      var img = new Image();
      img.src = 'ya.jpg';
      img.onload = function() {
        // когда нижнее изображение загружено, выводим его на холст
        context.drawImage(img, 200, 200, 400, 400);
        
        // заливаем изображение полупрозрачным фоном
        //fog_context.fillStyle = "rgba(0, 200, 200, 0.5)";
        //fog_context.fillRect (200, 200, 430, 400);
        
        // выводим верхнее изображение, считываем его при помощи imageGetData и меняем альфу для всех пикселов
        fog_context.drawImage(img_moroz, 200, 200);
        
        fog_imagedata = fog_context.getImageData(200, 200, 400, 400);
        
        elem_count = 429 * 400 * 4;
        i = 3;
        while(i <= elem_count) {
          fog_imagedata['data'][i] = 192;
          i += 4;
        }
  
        // заменяем содержимое верхнего холста измененным содержимым
        fog_context.putImageData(fog_imagedata, 200, 200);
      }
  }
}
```

Конечный результат [можно увидеть тут](/old-site/examples/canvas/canvas3-7.html).
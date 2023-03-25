---
title: Перетаскивание строк таблицы. Table drag and drop — плагин для jQuery
date: 2008-09-01 23:31:41 +0400
draft: false
tags: [old-site, jquery, Штуки-дрюки, drag and drop]
deprecated: true
---
В своем модуле "[Адаптивное меню]({{< relref "razrabotal-modul-adaptivnoe-menyu-dlya-drupal-6" >}})" я использовал очень удобный плагин для библиотеки [jQuery](http://jquery.com), который позволяет  сортировать ячейки таблиц, перетаскивая их мышью. Сейчас я хочу подробнее рассказать о возможностях этого плагина.

Для работы необходимо скачать последнюю версию библиотеки [jQuery](http://docs.jquery.com/Downloading_jQuery), последнюю версию плагина [Table DnD](http://plugins.jquery.com/project/TableDnD). Также можно ознакомиться с [официальной документацией к плагину](http://www.isocra.com/2008/02/table-drag-and-drop-jquery-plugin/).
<!--more-->
<?php
drupal_add_js("examples/table-dnd/jquery.tablednd_0_5.js");
drupal_add_css("examples/table-dnd/table-dnd-example.css");
drupal_add_js("examples/table-dnd/table-dnd-example-blog.js");
?>
## Свойства "Table drag and drop"
После подключения, плагин добавляет к функционалу jQuery возможность использовать функцию tableDnD(), принимающую следующие параметры :

- onDragStyle — CSS-стиль перетаскиваемой строки;
- onDropStyle — стиль строки, после того как ее перетащили;
- onDragClass — по сути то же что и onDragStyle, но вместо стилей указывается класс, содержащий необходимые стили;
- onDrop — функция, выполняемая после того как строчку "бросили";
- onDragStart — функция, выполняемая после того как строчку начали перетаскивать;
- dragHandle — здесь определяется класс ячейки, за которую можно будет перетаскивать строчку. Если параметр не определен, то хватать строку можно будет за любую ячейку;
- scrollAmount — число пикселей, на которое проскроллится страница, в случае если во время перетаскивания курсор дойдет до верхней или нижней границы страницы.

## Простой пример работы
```
<table cellspacing="0" cellpadding="2" id="table-1">
<tbody>

<tr id="1" style="cursor: move;" class="even-dnd">
<td>1</td>
<td>One</td>
<td>some text</td>
</tr>
<tr id="2" style="cursor: move;" class="odd-dnd">
<td>2</td>
<td>Two</td>
<td>some text</td>
</tr><tr id="3" style="cursor: move;" class="even-dnd">
<td>3</td>
<td>Three</td>
<td>some text</td>
</tr><tr id="4" style="cursor: move;" class="odd-dnd">
<td>4</td>
<td>Four</td>
<td>some text</td>
</tr>

<tr id="5" style="cursor: move;" class="even-dnd">
<td>5</td>
<td>Five</td>
<td>some text</td>
</tr><tr id="6" style="cursor: move;" class="odd-dnd">
<td>6</td>
<td>Six</td>
<td>some text</td>
</tr>
</tbody></table>
```

В этом примере включается перетаскивание строк для таблицы с id="table-1" и перетаскиваемым ячейкам назначается класс "myDragClass". Для работы примера необходимо подключить jQuery, плагин "Table drag and drop", файл со скриптом реализующим логику и файл со стилями:
```
<script type="text/javascript" src="jquery.js"></script>
<script type="text/javascript" src="jquery.tablednd_0_5.js"></script>
<script type="text/javascript" src="table-dnd-example.js"></script>
<link type="text/css" rel="stylesheet" href="table-dnd-example.css" />
```

Исходник файла table-dnd-example.js для этого примера:
```
$(document).ready(function() {
    $("#table-1").tableDnD({
      onDragClass: "myDragClass"
    });
});
```

Таблица из примера выглядит так:
```
<table cellspacing="0" cellpadding="2" id="table-1"><tbody>
<tr id="1" style="cursor: move;" class="even-dnd"><td>1</td><td>One</td><td>some text</td></tr>
<tr id="2" style="cursor: move;" class="odd-dnd"><td>2</td><td>Two</td><td>some text</td></tr>
<tr id="3" style="cursor: move;" class="even-dnd"><td>3</td><td>Three</td><td>some text</td></tr>
<tr id="4" style="cursor: move;" class="odd-dnd"><td>4</td><td>Four</td><td>some text</td></tr>
<tr id="5" style="cursor: move;" class="even-dnd"><td>5</td><td>Five</td><td>some text</td></tr>
<tr id="6" style="cursor: move;" class="odd-dnd"><td>6</td><td>Six</td><td>some text</td></tr>
</tbody></table>
```

Теперь немного более сложный пример — разрешаем перетаскивать строки только за крайнюю ячейку, в которой при наведении курсора выводится иконка-подсказка:

```
<table cellspacing="0" cellpadding="2" id="table-2">
<tbody><tr class="even-dnd">
<td class="dragHandle"> </td>
<td>6</td>
<td>Six</td>
<td>some text</td>
</tr><tr class="odd-dnd">
<td class="dragHandle"> </td>
<td>1</td>
<td>One</td>
<td>some text</td>
</tr>

<tr class="even-dnd">
<td class="dragHandle"> </td>
<td>2</td>
<td>Two</td>
<td>some text</td>
</tr><tr class="odd-dnd">
<td class="dragHandle"> </td>
<td>3</td>
<td>Three</td>
<td>some text</td>
</tr>
<tr class="even-dnd">
<td class="dragHandle"> </td>
<td>4</td>
<td>Four</td>
<td>some text</td>
</tr>
<tr class="odd-dnd">
<td class="dragHandle"> </td>
<td>5</td>
<td>Five</td>
<td>some text</td>
</tr>

</tbody></table>
```


Таблица из второго примера, обратите внимание на то, что первой ячейке каждой строки присвоен класс dragHandle:
```
<table cellspacing="0" cellpadding="2" id="table-2"><tbody>
<tr class="even-dnd"><td class="dragHandle"> </td><td>6</td><td>Six</td><td>some text</td></tr>
<tr class="odd-dnd"><td class="dragHandle"> </td><td>1</td><td>One</td><td>some text</td></tr>
<tr class="even-dnd"><td class="dragHandle"> </td><td>2</td><td>Two</td><td>some text</td></tr>
<tr class="odd-dnd"><td class="dragHandle"> </td><td>3</td><td>Three</td><td>some text</td></tr>
<tr class="even-dnd"><td class="dragHandle"> </td><td>4</td><td>Four</td><td>some text</td></tr>
<tr class="odd-dnd"><td class="dragHandle"> </td><td>5</td><td>Five</td><td>some text</td></tr>
</tbody></table>
```

Этим скриптом разрешаем таскать строки только за ячейку с классом dragHandle, а также при наведении курсора на строчку выводим в первой ячейке иконку-подсказку (для этого добавляем/удаляем класс showDragHandle):
```
$(document).ready(function() {
    // Initialise the table
    $("#table-2").tableDnD({
      onDragClass: "myDragClass",
      dragHandle: "dragHandle"
    });

    $("#table-2 tr").hover(function() {
          $(this.cells[0]).addClass('showDragHandle');
    }, function() {
          $(this.cells[0]).removeClass('showDragHandle');
    });

});
```

## Передача данных на сервер
Без возможности сохранить сделанные пользователем изменения плагин был бы простой игрушкой. В этом примере клиентский скрипт передаст серверному информацию о последовательности строк и выведет на экран ответ сервера.
```
<div id="upd-dnd" style="position: relative; border: 1px solid #ccc; width: 300px; float: right; margin: 20px 10px 20px 20px; padding: 10px;">Тут будет ответ от сервера</div>
<table id="table-3"><tbody>
<tr id="table-3-row-1" class="even-dnd"><td>1</td><td>One</td><td>some text</td></tr>
<tr id="table-3-row-2" class="odd-dnd"><td>2</td><td>Two</td><td>some text</td></tr>
<tr id="table-3-row-3" class="even-dnd"><td>3</td><td>Three</td><td>some text</td></tr>
<tr id="table-3-row-4" class="odd-dnd"><td>4</td><td>Four</td><td>some text</td></tr>
<tr id="table-3-row-5" class="even-dnd"><td>5</td><td>Five</td><td>some text</td></tr>
<tr id="table-3-row-6" class="odd-dnd"><td>6</td><td>Six</td><td>some text</td></tr>
</tbody></table>
```

Для работы примера необходимо каждой строке присвоить уникальный id. В слое upd-dnd будет выводиться ответ сервера:
```
<div id="upd-dnd" style="position: relative; border: 1px solid #ccc; width: 300px; float: right; margin: 20px 10px 20px 20px; padding: 10px;">Тут будет ответ от сервера</div>
<table id="table-3"><tbody>
<tr id="table-3-row-1" class="even-dnd"><td>1</td><td>One</td><td>some text</td></tr>
<tr id="table-3-row-2" class="odd-dnd"><td>2</td><td>Two</td><td>some text</td></tr>
<tr id="table-3-row-3" class="even-dnd"><td>3</td><td>Three</td><td>some text</td></tr>
<tr id="table-3-row-4" class="odd-dnd"><td>4</td><td>Four</td><td>some text</td></tr>
<tr id="table-3-row-5" class="even-dnd"><td>5</td><td>Five</td><td>some text</td></tr>
<tr id="table-3-row-6" class="odd-dnd"><td>6</td><td>Six</td><td>some text</td></tr>
</tbody></table>
```

Чтобы получить возможность обработать массив строк необходимо повесить свою функцию на событие onDrop, делается это так:
```$(document).ready(function() {
  // Initialise the table 3    
  $("#table-3").tableDnD({
    onDragClass: "myDragClass",
    onDrop: function(table, row) {
      var rows = table.tBodies[0].rows;
      var w = "";
      // В цикле создаем разделенный символом ";" список, в котором последовательно размещены id строк
      for (var i = 0; i < rows.length; i++) {
        w += rows[i].id + ";";
      }
      // Передаем данные на сервер
      $.ajax({
    		type: "POST",
     		url: "table-dnd-example.php",
     		timeout: 5000,
     		data: "w=" + w,
     		success: function(data){$("div#upd-dnd").html(data);},
     		error: function(data){$("div#upd-dnd").html("Error");}
     	});
    }
  });
});
```

PHP-backend здесь простой, он просто отдает клиентской части строку, которую получил, предварительно ее отформатировав. В реальном случае входной массив придется сохранить.
```
<?php
print "Rows:
" . str_replace(";", "
", $_POST['w']);
?>
```

[Все примеры на одной странице тут](/old-site/examples/table-dnd/index.html).

[Архив с примерами использования Table DnD](/old-site/examples/table-dnd/table-dnd.zip).


---
title: Динамическое добавление элементов к форме
date: 2008-09-17 17:02:34 +0400
draft: false
tags: [old-site, jquery, Штуки-дрюки, Javascript, форма]
---
При разработке модуля [Inner poll]({{< relref "inner-poll" >}}) возникла задача динамического добавления элементов к форме. С помощью библиотеки jQuery эта задача решается в два счета.

Для начала пишем функцию:
```
function addInput() {
    /* default-id — скрытый элемент формы, из которого берется id для первого создаваемого элемента */
    var id = document.getElementById("default-id").value;
    id++;
    /* в форму с именем testform добавляем новый элемент */
    $("form[name=testform]").append('<div id="div-' + id + '"><input name="input-' + id + '" id="input-' + id + '" value="' + id + '"><a href="javascript:{}" onclick="removeInput(\'' + id + '\')">Удалить</a></div>');
    /* увеличиваем счетчик элементов */
    document.getElementById("default-id").value = id;
}
```

Затем создаем форму:
```
<form name="testform" action="test.php" method="POST">
      <input type="hidden" id="default-id" value="0">
      <input type="submit" value="Отправить!">
</form>
<a href="javascript:{}" onclick="addInput()">Добавить текстовое поле</a><br>
```

Вот и всё. [Здесь](/old-site/examples/addelements/index.html) размещен работающий пример. Кроме добавления элементов, также приведен пример их удаления.
<!--more-->

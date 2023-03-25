---
title: Темизация Drupal. Часть 4. Темизация Views
date: 2010-01-03 22:09:43 +0300
draft: false
tags: [old-site, Drupal, статья, темизация, Views]
---
[Views](http://drupal.org/project/views) — один из самых востребованных модулей для [Drupal](http://drupal.org) — позволяет создавать списки документов (представления, _view_), отфильтрованные по любому сложному алгоритму. На выходе модуль возвращает массив данных, который выводится в шаблоне, соответствующем выбранному администратором типу отображения (display) данных. Каждое представление может быть отображено в виде таблицы, маркированного списка, решетки (grid) и т. п. Чтобы переопределить используемый для отображения представления шаблон, нужно в свойствах представления в блоке Basic settings найти параметр Theme information и посмотреть в нем имена шаблонов, которые могут быть использованы модулем для отображения текущего представления. Затем нужно в подпапке _theme_ модуля Views найти шаблон, соответствующий выбранному типу отображения (например, _views-view-table.tpl.php_ для табличного варианта отображения или _views-view-list.tpl.php_ для списка), скопировать его в папку с текущей темой оформления и присвоить ему одно из имен, перечисленных в Theme information. Теперь созданный шаблон можно настроить для своих нужд.

Например, вот так выглядит шаблон _views-view-table.tpl.php_:
```
<table class="<?php print $class; ?>">
  <?php if (!empty($title)) : ?>
    <caption><?php print $title; ?></caption>
  <?php endif; ?>
  <thead>
    <tr>
      <?php foreach ($header as $field => $label): ?>
        <th class="views-field views-field-<?php print $fields[$field]; ?>">
          <?php print $label; ?>
        </th>
      <?php endforeach; ?>
    </tr>
  </thead>
  <tbody>
    <?php foreach ($rows as $count => $row): ?>
      <tr class="<?php print implode(' ', $row_classes[$count]); ?>">
        <?php foreach ($row as $field => $content): ?>
          <td class="views-field views-field-<?php print $fields[$field]; ?>">
            <?php print $content; ?>
          </td>
        <?php endforeach; ?>
      </tr>
    <?php endforeach; ?>
  </tbody>
</table>
```

Первые 14 строк этого шаблона выводят заголовок страницы и таблицы с данными, а самая интересная и важная часть шаблона сосредоточена в строках с 15 по 23 — здесь в цикле выводятся данные, выбранные запросом, заданным в настройках представления. Данные возвращаются в виде рекордсета, то есть структуры данных, которую можно представить как таблицу, строками которой являются выбранные объекты (например ноды), а ячейками — значения полей объекта (например поля "заголовок" или "автор" ноды).

Вот этот же кусок шаблона с комментариями:
```
// Цикл по объекту $rows, содержащему все возвращенные данные
// $row — одна строка
<?php foreach ($rows as $count => $row): ?>
  <tr class="<?php print implode(' ', $row_classes[$count]); ?>">
    // Цикл по всем ячейкам внутри строки
    // $field — имя поля, например nid, title и т.д.
    // $content — значение поля
    <?php foreach ($row as $field => $content): ?>
      <td class="views-field views-field-<?php print $fields[$field]; ?>">
        <?php print $content; ?>
      </td>
    <?php endforeach; ?>
  </tr>
<?php endforeach; ?>
```

Это достаточно универсальный и не очень удобный шаблон, так как он оборачивает одним и тем же html-кодом каждый элемент данных, в частном случае, когда вы заранее знаете имена всех полей, которые будете выводить, этот шаблон можно сильно упростить:
```
<?php
    foreach ($rows as $count => $row) {
        print $row['field_name_1'] . "; " . $row['field_name_2'];
    }
```
Здесь нужно учитывать, что в качестве ключей массива $row нужно использовать имена соответствующих колонок с данными в БД, в случае с дефолтными полями это будут ключи типа _nid_, _title_, _created_, а в случае с данными, выбранными из CCK-полей нужно не забывать добавлять к именам приставку _field__.

Список всех доступных в шаблоне полей можно вывести на экран вот так:
```
    foreach ($rows as $count => $row) {
     $fields = array();
     foreach ($row as $field => $content) {
        $fields[] = $field;
     }
    }
    print implode(", ", $fields);
```

Ссылки на другие части этой статьи:
- [Часть 1. Введение]({{< relref "drupal-article-3-part-1-drupal-themeing" >}})
- [Часть 2. Анатомия темы оформления]({{< relref "drupal-article-3-part-2-drupal-themeing-anatomy" >}})
- [Часть 3. Forms API и темизация]({{< relref "drupal-article-3-part-3-drupal-forms-api" >}})
- **Часть 4. Темизация Views**

Содержание всех статей: [/blog/2010/my-drupal-articles]({{< relref "my-drupal-articles" >}})
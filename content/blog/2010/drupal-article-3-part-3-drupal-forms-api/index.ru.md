---
title: Темизация Drupal. Часть 3. Основы Drupal Forms API и темизация форм
date: 2010-01-03 21:58:46 +0300
draft: false
tags: [old-site, Drupal, статья, темизация, формы Forms API]
---
Прежде чем говорить об изменении внешнего вида форм, ознакомимся с основами Drupal Forms API — программного интерфейса, используемого для генерации форм. Применение Forms API несколько сложнее создания HTML-форм вручную, так как требует изучения логики его работы, однако его использование обязательно, поскольку Forms API решает ряд важных задач:

 - любой разработчик может добавить или удалить элементы в форме, созданной другим разработчиком, не меняя ее исходного кода;
 - любой разработчик может добавить дополнительные функции проверки и обработки введенных пользователем данных без изменения исходной формы;
 - формы, созданные с использованием Forms API, защищены от атак, связанных с отправкой пользователем модифицированной формы;
 - любой разработчик может изменить внешний вид формы, не изменяя ее исходного кода. 
 
Каждая форма в Drupal представляет собой функцию, возвращающую ассоциативный массив. Этот массив должен содержать информацию обо всех элементах формы, функциях проверки (валидаторы, validators) и обработки (сабмиттеры, submitters) введенных данных. Данная функция должна быть расположена в файле модуля, о разработке модуля говорилось в [предыдущей статье]({{< relref "drupal-article-2-part-1-drupal-develop-module-vvedenie" >}}).
<!--more-->
### На заметку: готовые решения

 - Темы оформления, позволяющие менять цветовую схему через интерфейс администратора: [Pixture Reloaded](http://drupal.org/project/pixture_reloaded), [Dropshadow](http://drupal.org/project/dropshadow), [Wabi](http://drupal.org/project/wabi), Garland (стандартная тема Drupal).
 - Темы оформления, обладающие множеством настроек и регионов: [Deco](http://drupal.org/project/deco), [Acquia Marina](http://drupal.org/project/acquia_marina).

Рассмотрим простой пример.
```
function test_form($form_state) {
  $form["example_text_field"] = array(
    '#type' => 'textfield',
    '#title' => 'Example text field',
  );
  $options = array(
    0 => 'zero',
    1 => 'one',
    2 => 'two',
  );
  $form["example_select"] = array(
    '#type' => 'select',
    '#title' => 'Example select list',
    '#options' => $options,
    '#description' => t('You can select only value "one" in this
      form'),
  );
  $form["submit"] = array(
    '#type' => 'submit',
    '#value' => t('Submit'),
  );
  return $form;
}
```
Приведенная выше функция генерирует форму, состоящую из текстового поля, выпадающего списка с тремя элементами и кнопкой для отправки данных. Имя этой функции — ее уникальный идентификатор (_$form_id_), который будет использоваться для отображения и изменения данной формы сторонними модулями. Чтобы вывести форму на экран, нужно через [hook_menu](http://api.drupal.org/api/function/hook_menu/6) создать страницу, где будет вызвана функция [drupal_get_form](http://api.drupal.org/api/function/drupal_get_form/6), принимающая в качестве параметра _$form_id_ формы, которая должна быть отображена на экране:
```
function имя_модуля_menu() {
  $items = array();
  $items['test-form'] = array(
    'title' => 'Test form',
    'page callback' => 'test_form_page',
    'access arguments' => array('access content'),
    'type' => MENU_NORMAL_ITEM,
  );
  return $items;
}
function test_form_page() {
  return drupal_get_form('test_form');
}
```
В массиве, возвращаемом функцией _test_form($form_state)_, не определены процедуры проверки значений и заполнения полей (структур), поэтому ядро Drupal после нажатия на форме кнопки Submit попробует найти и выполнить функции _form_id_validate_ и _form_id_submit_. В нашем случае, как легко догадаться, это будут функции с именами _test_form_validate_ и _test_form_submit_:
```
function test_form_validate($form, &$form_state) {
  if($form_state['values']['example_select'] != 1) {
    form_set_error('example_select', t('You must select value
      "one" in select list :)'));
  }
}
function test_form_submit($form, &$form_state) {
  drupal_set_message('Form sumitted! Values:');
  drupal_set_message("textbox: " .
    $form_state['values']['example_text']);
  drupal_set_message("selectlist: " .
    $form_state['values']['example_select']); 
}
```
Функция-валидатор проверяет выбранное в выпадающем списке значение и, если оно не one, посылает сообщение об ошибке с указанием, какой элемент формы вызвал ошибку. Функция-сабмиттер выводит на экран введенные пользователем значения. В реальном случае эта функция должна будет сохранить данные в базе данных.

При желании программист может в массиве _$form функции test_form_ задать свойство _#submit_, содержащее массив обработчиков значений и свойство _#validate_ с массивом валидаторов (см. листинг 4). Оранжевыми комментариями выделены строки, добавленные к ранее описанным функциям.

**Листинг 4**
```
function test_form($form_state) {
    $form["example_text_field"] = array(
        '#type' => 'textfield',
        '#title' => 'Example text field',
        '#description' => 'Text must contain more then
        3 symbols',
    );
    $options = array(
        0 => 'zero',
        1 => 'one',
        2 => 'two',
    );
    $form["example_select"] = array(
        '#type' => 'select',
        '#title' => 'Example select list',
        '#options' => $options,
        '#description' => t('You can select only value "one" in this form'),
    );
    $form["submit"] = array(
        '#type' => 'submit',
        '#value' => t('Submit'),
    );
    //Добавлено
    $form["#validate"] = array('test_validate_first', 'test_validate_second');
    $form["#submit"] = array('test_submit_first', 'test_submit_second');
    //Конец добавления
    return $form;
}
```
Код модуля также дополнится функциями из листинга 5.

**Листинг 5**
```
function test_validate_first($form, &$form_state) {
    if(mb_strlen($form_state['values']['example_text_field']) < 3) {
        form_set_error('example_text_field', t('Text must contain more then 3 symbols'));
    }
}
function test_validate_second($form, &$form_state) {
    if($form_state['values']['example_select'] != 1) {
        form_set_error('example_select', t('You must select value "one" in select list :)'));
    }
}
function test_submit_first($form, &$form_state) {
    drupal_set_message('First submitter');
    drupal_set_message("textbox: " . $form_state['values']['example_text']);
}
function test_submit_second($form, &$form_state) {
    drupal_set_message('Second submitter');
    drupal_set_message("selectlist: " . $form_state['values']['example_select']);
}
```
Здесь добавлен валидатор, который проверяет текст, введенный в текстовое поле; если его длина оказывается меньше трех символов, то генерируется сообщение об ошибке.

При создании форм всегда рекомендуется использовать не стандартные валидаторы и сабмиттеры, а объявлять их явно, так как в этом случае сторонние программисты смогут дополнить массивы _#submit_ и _#validate_ своими функциями. Если используются стандартные валидаторы и сабмиттеры, то сторонние программисты смогут только заменить существующие функции своими, а это не всегда удобно.

Теперь вернемся к основной теме статьи — темизации Drupal. Функция _drupal_get_form_, получив на вход _$form_id_, идентификатор формы, которую нужно вывести на экран, вызывает функцию [form_builder](http://api.drupal.org/api/function/form_builder/6), проверяющую права доступа текущего пользователя к каждому из полей формы, и при наличии этих прав выводит стандартный HTML-код для каждого элемента формы. Каждый созданный элемент формы имеет уникальный атрибут id. Самый простой способ переопределения внешнего вида элементов формы — создание CSS-файла с описанием стилей нужных элементов формы. Если этого недостаточно, элементам формы можно добавить параметры _#prefix_ и _#suffix_, которые будут содержать HTML-код, выводимый до и после созданного элемента. Если и этого мало, можно определить параметр _#theme_, который должен содержать используемое имя функции темизации.

Персональные функции темизации можно задать для всей формы целиком или для каждого ее элемента. По умолчанию Drupal для темизации формы пробует найти функцию _theme_form_id_, поэтому использование параметра _#theme_ не обязательно.

Все функции, определенные параметром _#theme_, должны быть также объявлены через [hook_theme](http://api.drupal.org/api/function/hook_theme/6) (описание этого хука было дано в [предыдущей статье]({{< relref "drupal-article-2-part-3-drupal-develop-module-cron-and-themeing" >}})).

Давайте изменим внешний вид созданного текстового поля. Для этого сначала создадим реализацию хука hook_theme:
```
function название_модуля_theme() {
    return array(
        'example_text_field_theme_function' => array(
            'arguments' => array('form' => NULL),
        ),
    );
}
```
Затем модифицируем массив _$form["example_text_field"]_, который создается в функции _test_form_, добавив в него параметр _#theme_:
```
$form["example_text_field"] = array(
    '#type' => 'textfield',
    '#title' => 'Example text field',
    '#description' => 'Text must contain more then 3 symbols',
    '#theme' => 'example_text_field_theme_function',
);
```
Теперь мы можем объявить функцию _theme_example_text_field_theme_function_ и задать в ней любой HTML-код для отображения выбранного элемента:
```
function theme_example_text_field_theme_function($element) {
    $class = "";
    if(isset($element["#needs_validation"])) {
        $class = " error";
    }
    $output = '<div id="' . $element["#id"] . '"
        class="form-item"><input id="edit-example-text-field"
        class="form-text' . $class . '" name="' . $element["#name"]
        . '"></div>';
    return $output;
}
```
Кроме того, эту функцию можно переопределить, не изменяя кода модуля. Для этого в файле _template.php_, который находится в папке с текущей темой оформления, нужно создать копию этой функции, заменив в ней префикс _theme _на _имя текущей темы_.

Если в реализации _hook_theme_ использовать параметр _template_, например, так:
```
function название_модуля_theme() {
    return array(
        'example_text_field_theme_function' => array(
        'arguments' => array('form' => NULL),
            'template' => 'example-text-field',
        ),
    );
}
```
то HTML-код, ответственный за отображение элемента Web-страницы в браузере, можно будет задавать не в исходном тексте функции темизации, а в отдельном файле-шаблоне с соответствующим именем; в нашем примере это _example-text-field.tpl.php_. Такой подход удобен, если с сайтом должны работать дизайнеры, не имеющие опыта Web-программирования.

Если же возникла необходимость изменить внешний вид всей формы, а не только отдельных ее элементов, нужно проделать то же самое: указать значение параметра _#theme_ формы, объявить в _hook_theme_ функцию темизации и, наконец, реализовать ее. Давайте внесем необходимые изменения в наш код. Функция _hook_theme_ будет выглядеть следующим образом:
```
function название_модуля_theme() {
    return array(
        'test_form_theme_function' => array(
            'arguments' => array('form' => NULL),
        ),
        'example_text_field_theme_function' => array(
            'arguments' => array('form' => NULL),
       ),
    );
}
```
Исходный текст обновленной функции test_form приводится в листинге 6.

**Листинг 6**
```
function test_form($form_state) {
    $form['#theme'] = 'test_form_theme_function';
    $form["example_text_field"] = array(
        '#type' => 'textfield',
        '#title' => 'Example text field',
        '#description' => 'Text must contain more then 3 symbols',
        '#theme' => 'example_text_field_theme_function',//*/
    );
    $options = array(
        0 => 'zero',
        1 => 'one',
        2 => 'two',
    );
    $form["example_select"] = array(
        '#type' => 'select',
        '#title' => 'Example select list',
        '#options' => $options,
        '#description' => t('You can select only value "one" in this form'),
    );
    $form["submit"] = array(
        '#type' => 'submit',
        '#value' => t('Submit'),
    );
    $form["#validate"] = array('test_validate_first', 'test_validate_second');
    $form["#submit"] = array('test_submit_first', 'test_submit_second');
    return $form;
}
```
Также нам потребуется и сама функция темизации формы. Определим ее:
```
function theme_test_form_theme_function($form) {
    $output = "Some additional text";
    // Выводим некоторые элменты отдельно с дополнительным
    // форматированием
    $output .= '<div style="background-color: #ccc; padding: 3px;">';
    $output .= drupal_render($form['example_text_field']);
    $output .= "</div>";
    // Выводим остальные элементы, которые не были выведены
    // ранее
    $output .= drupal_render($form);
    return $output;
}
```
Как и с любой другой функцией темизации, ее содержимое можно вынести во внешний шаблон.

Ну а теперь осталось научиться модифицировать из внешнего модуля существующую форму. Для решения этой задачи нужно воспользоваться одним из двух хуков: или [hook_form_alter](http://api.drupal.org/api/function/hook_form_alter/6), через который проходят массивы всех обрабатываемых форм и в котором каждый массив можно отредактировать, или [hook_form_FORM_ID_alter](http://api.drupal.org/api/function/hook_form_FORM_ID_alter/6), где _FORM_ID_ должен быть заменен на идентификатор нужной формы. Через этот хук проходит только выбранная форма. На вход оба этих хука получают массив формы (в нашем примере это массив, который генерируется функцией _test_form_), и в этот массив могут быть добавлены или из него могут быть удалены любые параметры: _#theme_, _#prefix_, _#suffix_, _#submit_, _#validate_ и другие.

Для примера добавим к форме контейнер, который может содержать в себе несколько полей. Переместим в него два поля и сменим заголовок одного из них:
```
function название_модуля_form_test_form_alter(&$form, &$form_state) {
    $form["example_text_field"]["#title"] = "New title";
    $form["example_add_field"] = array(
        '#type' => 'fieldset',
        '#title' => 'new fieldset',
        '#collapsible' => TRUE,
        '#collapsed' => FALSE,
        '#weight' => 0,
    );
    foreach ($form as $name => $element) {
        if($element["#type"] == "select" || $element["#type"] == "textfield") {
            $form["example_add_field"][$name] = $element;
            unset($form[$name]);
        }
    }
    $form["submit"]["#weight"] = 5;
}
```
Вот и все.

Ссылки на другие части этой статьи:
- [Часть 1. Введение]({{< relref "drupal-article-3-part-1-drupal-themeing" >}})
- [Часть 2. Анатомия темы оформления]({{< relref "drupal-article-3-part-2-drupal-themeing-anatomy" >}})
- **Часть 3. Forms API и темизация**
- [Часть 4. Темизация Views]({{< relref "drupal-article-3-part-4-drupal-themeing-views" >}})

Содержание всех статей: [/blog/2010/my-drupal-articles]({{< relref "my-drupal-articles" >}})
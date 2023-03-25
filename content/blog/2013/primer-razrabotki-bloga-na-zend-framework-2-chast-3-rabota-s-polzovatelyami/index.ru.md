---
title: Пример разработки блога на Zend Framework 2. Часть 3. Работа с пользователями
date: 2013-09-03 17:17:56 +0400
draft: false
tags: [old-site, Zend Framework, Работа]
---
Это третья (последняя) часть статьи, посвященной разработке простого приложения при помощи Zend Framework 2. [В первой статье]({{< relref "primer-razrabotki-bloga-na-zend-framework-2-chast-1" >}}) я рассмотрел структуру ZendSkeletonApplication, [во второй части]({{< relref "primer-razrabotki-bloga-na-zend-framework-2-chast-2-modul-myblog" >}}) привел пример разработки простого модуля. Эта часть посвящена работе с пользователями.

## Работа с пользователями
Код написанный в предыдущих частях, позволяет создавать, редактировать и удалять блогпосты всем посетителям сайта. Такой подход неприемлем для любого рабочего сайта, по этому сейчас настало время решить вопросы регистрации/авторизации и распределения прав доступа к различным возможностям приложения.

### Zf Commons
Для Zend фреймворка написано достаточно много модулей, решающих стандартные задачи, найти их можно на специальном сайте: http://modules.zendframework.com/. Вместо разработки своих велосипедов для решения стандартных задач я считаю более правильным использовать/адаптировать под себя готовые решения (по крайней мере готовые решения нужно изучить прежде чем браться за разработку велосипеда).

Среди множества разработчиков модулей выделяется команда ZF Commons, ребятами из этой команды разработан ряд очень полезных модулей, которые мы будем использовать в этом проекте: https://github.com/ZF-Commons. Рассмотрим некоторые из них, которые необходимы нам на данном этапе.
<!--more-->
#### ZfcBase
Ядро, от которого зависят другие модули ZF Commons (https://github.com/ZF-Commons/ZfcBase).

#### ZfcUser
Модуль, реализующий механизмы регистрации/авторизации пользователей, профиль пользователя и View хелперы для использования в шаблонах (https://github.com/ZF-Commons/ZfcUser).

#### ZfcUserDoctrineORM
По умолчанию, ZfcUser работает со стандартным для фреймворка механизмом работы с БД, так как в нашем проекте используется Doctrine ORM, также нужен модуль ZfcUserDoctrineORM (https://github.com/ZF-Commons/ZfcUserDoctrineORM).

#### ZfcTwig
Модуль для интеграции с шаблонизатором Twig (https://github.com/ZF-Commons/ZfcTwig).

### BjyAuthorize
Кроме модулей от ZfCommons я буду использовать модуль BjyAuthorize, который предоставляет удобный механизм для распределения прав доступа. Логика работы модуля простая и распространенная среди других фреймворков. Модуль оперирует понятиями: пользователь, роль и guard.

Пользователь может быть авторизованным и не авторизованным. Авторизованный пользователь может иметь одну или несколько ролей. Guard в данном контексте — это контроллер/действие, к которому мы настраиваем права доступа для разных ролей.

### Подготовка к настройке пользователей
Прежде чем настраивать работу с пользователями необходимо создать entity для пользователя и роли, которые будут использоваться Доктриной. В комплекте с модулем BjyAuthorize идут примеры таких сущностей, на их основе я создал модуль MyUser.

Модуль не содержит ничего оригинального, посмотреть его код можно тут: https://github.com/romka/zend-blog-example/tree/master/module/MyUser, по своей структуре он не отличается от рассмотренных выше модулей Application и MyBlog: содержит конфиг и 2 entity.

Следует обратить внимание только на его конфиг (https://github.com/romka/zend-blog-example/blob/master/module/MyUser/config/module.config.php):
```
return array(
    'doctrine' => array(
        'driver' => array(
            'zfcuser_entity' => array(
                'class' =>'Doctrine\ORM\Mapping\Driver\AnnotationDriver',
                'paths' => array(__DIR__ . '/../src/MyUser/Entity')
            ),
            'orm_default' => array(
                'drivers' => array(
                    'MyUser\Entity' => 'zfcuser_entity',
                )
            )
        )
    ),

    'zfcuser' => array(
        // telling ZfcUser to use our own class
        'user_entity_class'       => 'MyUser\Entity\User',
        // telling ZfcUserDoctrineORM to skip the entities it defines
        'enable_default_entities' => false,
    ),

    'bjyauthorize' => array(
        // Using the authentication identity provider, which basically reads the roles from the auth service's identity
        'identity_provider' => 'BjyAuthorize\Provider\Identity\AuthenticationIdentityProvider',

        'role_providers'        => array(
            // using an object repository (entity repository) to load all roles into our ACL
            'BjyAuthorize\Provider\Role\ObjectRepositoryProvider' => array(
                'object_manager'    => 'doctrine.entity_manager.orm_default',
                'role_entity_class' => 'MyUser\Entity\Role',
            ),
        ),
    ),
);
```

В этом конфиге мы заменяем сущность zfcuser на нашу собственную, которая отвечает за работу с пользователем и указываем модулю BjyAuthorize сущность, отвечающую за работу с ролями.

Модуль MyUser нужно добавить в `application.config.php` и затем в консоли выполнить команды:
```
./vendor/bin/doctrine-module orm:schema-tool:update --force
./vendor/bin/doctrine-module orm:validate-schema
```

Первую — чтобы создать в БД таблицы для сущностей, созданных модулем MyUser, вторую — чтобы убедиться, что первая команда отработала корректно.

Последним подготовительным действием будет выполнение запроса:
```
INSERT INTO `role`
(`id`, `parent_id`, `roleId`)
VALUES
(1, NULL, 'guest'),
(2, 1, 'user'),
(3, 2, 'moderator'),
(4, 3, 'administrator');
```

который создаст соответствующие роли.

### Настройка ZfcUser, ZfcUserDoctrineORM и BjyAuthorize
Первым делом необходимо прописать новые модули в настройках Композера:
```
"zf-commons/zfc-base": "v0.1.2",
"zf-commons/zfc-user": "dev-master",
"zf-commons/zfc-user-doctrine-orm": "dev-master",
"doctrine/doctrine-orm-module": "0.7.*",
"bjyoungblood/bjy-authorize": "1.4.*"
```

выполнить апдейт `php composer.phar update` и добавить новые модули в `application.config.php`:
```
'ZfcBase',
'ZfcUser',
'ZfcUserDoctrineORM',
'BjyAuthorize',
```

Внимание! Настройки некоторых из этих модулей будут переопределены настройками самописных модулей, по этому эти модули необходимо добавить вверх списка.

Теперь нужно скопировать файл `zfcuser.global.php.dist` из директории `vendor/zf-commons/zfc-user/config` в `config/autoload` и переименовать его в `zfcuser.global.php`. В этом конфигурационном файле нужно задать значение:
```
'table_name' => 'users',
```

так как по умолчанию для работы с пользователями используется таблица user.

Еще в этой же директории нужно создать конфигурационный файл `bjyauth.global.php` содержащий настройки прав доступа для различных ролей. Полную версию этого файла вы можете посмотреть на Гитхабе https://github.com/romka/zend-blog-example/blob/master/config/autoload/bjyauth.global.php, самая интересная его часть, которая отвечает за распределение прав доступа к различным контроллерам, приведена ниже:
```
'guards' => array(
    /* If this guard is specified here (i.e. it is enabled), it will block
    * access to all controllers and actions unless they are specified here.
    * You may omit the 'action' index to allow access to the entire controller
    */
    'BjyAuthorize\Guard\Controller' => array(
        array(
            'controller' => 'zfcuser',
            'action' => array('index', 'login', 'authenticate', 'register'),
            'roles' => array('guest'),
        ),

        array(
            'controller' => 'zfcuser',
            'action' => array('logout'),
            'roles' => array('user'),
        ),

        array('controller' => 'Application\Controller\Index', 'roles' => array()),

        array(
            'controller' => 'MyBlog\Controller\BlogPost',
            'action' => array('index', 'view'),
            'roles' => array('guest', 'user'),
        ),

        array(
            'controller' => 'MyBlog\Controller\BlogPost',
            'action' => array('add', 'edit', 'delete'),
            'roles' => array('administrator'),
        ),
    ),
),
```

Из конфига видно, что доступ к экшенам index и view мы сделали для всех пользователей, а к экшенам `add/edit/delete` — только пользователям с ролью administrator. Сейчас в этом легко убедиться перейдя по ссылке `/blog/add` — будет возвращена ошибка 403.

Сейчас мы можем зарегистрироваться по ссылке /user/register и присвоить своему пользователю права администратора SQL-запросом:
```
INSERT INTO user_role_linker (user_id, role_id) VALUES (1, 4);
```

(да, админку для управления ролями пользователя модуль ZfcUser не предоставляет).

После авторизации внизу страницы в девелопер тулбаре будет выведена информация о роли текущего пользователя и действия `add/edit/delete` больше не будут возвращать ошибку 403.

Заметным недостатком текущего состояния проекта является то, что ссылки на редактирования/удаление блогпостов выводятся всем пользователям, несмотря на то, что у анонимов прав на выполнение таких действий нет. Модуль `BjyAuthorize` содержит View-плагин `isAllowed`, который позволяет легко исправить проблему. Добавим в шаблоны строчки такого вида:
```
if ($this->isAllowed('controller/MyBlog\Controller\BlogPost:edit')) {
// some code here
}
```

там где нужно проверить наличие прав доступа к соответствующим контроллеру/действию, это позволит не выводить в шаблоне ссылки, просмотр которых недоступен текущему пользователю.

Аналогичным методом можно в экшене indexAction() для админов выводить полный список блогпостов, а не только опубликованные:
```
if ($this->isAllowed('controller/MyBlog\Controller\BlogPost:edit')) {
    $posts = $objectManager
        ->getRepository('\MyBlog\Entity\BlogPost')
        ->findBy(array(), array('created' => 'DESC'));
}
else {
    $posts = $objectManager
        ->getRepository('\MyBlog\Entity\BlogPost')
        ->findBy(array('state' => 1), array('created' => 'DESC'));
}
```

Проект в текущем виде доступен в репозитории на Гитхабе с тэгом `configured_user`: https://github.com/romka/zend-blog-example/tree/configured_user.

## Twig
На своей практике я использовал несколько различных шаблонизаторов и считаю питоновский [Jinja 2](http://jinja.pocoo.org/docs/) самым удобным из тех, с которыми мне приходилось работать. PHP-шаблонизатор [Twig](http://twig.sensiolabs.org/) изначально был разработан Armin’ом Ronacher’ом — автором Jinja 2, а затем за его поддержку и развитие взялся Fabien Potencier — разработчик фреймворка [Symfony](http://symfony.com/).

Одним из ключевых отличий Твига от встроенного в Zend Framework шаблонизатора является то, что в Twig-шаблонах нельзя использовать PHP-код, вместо этого в шаблонизаторе реализован собственный синтаксис для реализации циклов, условных операторов и т.п. Twig-шаблоны компилируются в PHP-код и как следствие не проигрывают в производительности PHP-коду.

Благодаря таким особенностям как наследование шаблонов, макросы, система фильтров и т.п. Twig-шаблоны получаются компактными и легко читаемыми.

### Установка
Для установки Твига достаточно выполнить стандартные действия: добавить строчку в `composer.json`, запустить `php composer.phar update` и добавить модуль в `application.config.php`.

Теперь к модулям, которые будут использовать этот шаблонизатор, в конфигурационный файл в секцию view_manager нужно добавить строчки:
```
'strategies' => array(
    'ZfcTwigViewStrategy',
),
```

и Твиг будет готов к использованию. Причем оба шаблонизатора (Твиг и дефолтный) могут использоваться вместе, то есть часть шаблонов может быть реализована на одном шаблонизаторе, часть на другом.

### Twig-шаблоны
Упомянутое выше наследование шаблонов означает, что мы можем создать дефолтный шаблон `layout.twig` примерно с таким содержимым:
```
<html>
<head>
    <title>
        {% block title %}Default title{% endblock title %}
    </title>

    {% block script %}
    <script type="text/javascript" src="/js/jquery.min.js"></script>
    {% endblock script %}
</head>
<body>
<div class="content">
    {% block content %}{{ content|raw }}{% endblock content %}
</div>
<div class="sidebar">
    {% block sidebar %}{{ sidebar|raw }}{% endblock sidebar %}
</div>
</body>
</html>
```

Далее мы можем создать шаблон, который будет наследоваться от layout.twig, в котором переопределим только изменившиеся части шаблона:
```
{% extends 'layout/layout.twig' %}

{% block script %}
    {{ parent() }}
    <script type="text/javascript" src="some-additional-file.js"></script>
{% endblock script %}


{% block content %}
    Custom content
{% endblock content %}
```

По умолчанию, блок переопределенный в шаблоне-наследнике заменяет собой блок в родительском шаблоне, но обратите внимание на строчку `{{ parent() }}` в блоке script, её использование означает, что в этот блок будет подгружено содержимое содержимое из аналогичного блока родительского шаблона.

Теперь давайте перепишем шаблоны с использованием нового шаблонизатора. Я начал со стандартного шаблона `layout.phtml` из Zend Skeleton Application, найти его можно в модуле MyBlog в директории view/layout https://github.com/romka/zend-blog-example/blob/master/module/MyBlog/view/layout/layout.twig.

Обратите внимание на то, насколько компактнее стало, например, использование view-хелперов, теперь вместо:
```
<?php
    echo $this->url('blog', array('action' => 'edit'));
?>
```

можно вызвать:
```
{{ url('blog', {'action': 'edit'}) }}
```

а вместо:
```
<?php
    echo $this->showMessages();
?>
```

просто:
```
{{ showMessages() }}
```

После переработки основного шаблона займемся формами. Первым делом в директории `view` модуля создадим поддиректорию `macros` и в ней файл [forms.twig](https://github.com/romka/zend-blog-example/blob/master/module/MyBlog/view/macros/forms.twig) с таким содержимым:
```
{% macro input(name, value, type, label, size, messages) %}
{% if type != 'hidden' %}
<div class="form-element-{{ name }}">
{% endif %}

    {% if label %}
        {{ label }}:
    {% endif %}

    {% if type == 'textarea' %}
        <textarea name="{{ name }}" size="{{ size|default(20) }}" {% if messages|length > 0 %}class="error"{% endif %}/>{{ value|e }}</textarea>
    {% elseif type == 'checkbox' %}
        <input type="{{ type }}" name="{{ name }}" value="1"{% if value == true %} checked="checked"{% endif %} {% if messages|length > 0 %}class="error"{% endif %}/>
    {% else %}
        <input type="{{ type|default('text') }}" name="{{ name }}" value="{{ value|e }}" size="{{ size|default(20) }}" {% if messages|length > 0 %}class="error"{% endif %}/>
    {% endif %}

    {% if type != 'hidden' %}
        </div>
    {%  endif %}
    {% if messages|length > 0 %}
        <ul>
            {% for m in messages %}
                <li>{{ m }}</li>
            {% endfor %}
        </ul>
    {% endif %}
{% endmacro %}
```

Этот макрос будет использоваться для отображения полей форм. На вход он получает параметры поля, на выходе возвращает html-разметку.

Сейчас можно удалить существующий шаблон `add.phtml` и заменить новым `add.twig` с таким содержимым:
```
{% extends 'layout/layout.twig' %}
{% import 'macros/forms.twig' as forms %}

{% block content %}
<h1>{{ title }}</h1>

    <form method="{{ form.attributes.method }}" action="{{ url('blog', {'action': 'add'}) }}">
        {% for element in form %}
            {{ forms.input(element.attributes.name, element.value, element.attributes.type, element.label, 20, element.messages) }}
        {% endfor %}
    </form>
{% endblock content %}
```

Аналогичным образом я переделал остальные шаблоны и поудалял теперь ставшие ненужными *.phtml-шаблоны модуля: https://github.com/romka/zend-blog-example/tree/master/module/MyBlog/view/my-blog/blog.

## Заключение
На этом я бы хотел закончить. Я не затронул массу важных моментов, таких как логгирование, кеширование, Dependency Injection, написание тестов и т.д и т.п, но все эти вопросы выходят за рамки ознакомительной статьи. Но я надеюсь, что для разработчиков начинающих изучать Zend Framework 2 эта статья поможет стать полезной отправной точкой.

_Я написал все 3 части этой статьи еще до публикации первой части и на момент завершения работы над текстом планировал на этом закончить. После прочтения комментариев к этой статье на Хабре (<a href="http://habrahabr.ru/post/192522/">1</a>, <a href="http://habrahabr.ru/post/192608/">2</a>, <a href="http://habrahabr.ru/post/192726/">3</a>) я решил немного усовершенствовать приложение:_

- использовать REST, вместо проверок на тип запроса GET/POST,
- перенести часть задач на хуки перед экшенами,
- перенести часть задач на хуки Доктрины,
- избавиться от магических констант,
- перенести конфиги в yaml,
- заменить часть вызовов на DI(?).


_На подготовку этих изменений уйдет некоторое время, надеюсь опубликовать четвертую часть статьи в скором времени._
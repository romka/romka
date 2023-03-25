---
title: Пример разработки блога на Zend Framework 2. Часть 2. Модуль MyBlog
date: 2013-09-03 16:33:40 +0400
draft: false
tags: [old-site, Zend Framework, Работа]
---
Это вторая из трех частей статьи, посвященной разработке простого приложения при помощи Zend Framework 2. [В первой статье]({{< relref "primer-razrabotki-bloga-na-zend-framework-2-chast-1" >}}) я рассмотрел структуру ZendSkeletonApplication, а в этой части приведу пример разработки простого модуля. [Третья часть]({{< relref "primer-razrabotki-bloga-na-zend-framework-2-chast-3-rabota-s-polzovatelyami" >}}) будет посвящена работе с пользователями.
## Установка и настройка дополнительных модулей
Первым делом хочу отметить, что установка стороннего модуля в Zend Framework обычно состоит из примерно таких четырех шагов:

1. добавляем соответствующую строчку в `composer.json`, чтобы сообщить Композеру о новом модуле,
2. выполняем команду `php composer.phar update`, чтобы Композер загрузил новый модуль и при необходимости перегенерировал автолоад файлы,
3. добавляем новый модуль в список modules в файле `config/application.config.php`,
4. при необходимости, размещаем конфигурационный файл модуля (обычно пример такого файла находится в папке `config` модуля) в `config/autoload` и делаем в нем необходимые правки.

Также, хочу подчеркнуть, что для всех модулей, перечисленных далее я задаю минимально необходимые для их работы настройки, более подробно о настройках и возможностях каждого из модулей можно узнать на их страницах документации.

Давайте начнем с установки простого, но полезного модуля Zend Developer Tools.
<!--more-->
### Zend Developer Tools
Zend Developer Tools — это удобный тулбар, содержащий полезную для разработчика информацию о созданной странице: число и список запросов к БД, список ролей текущего пользователя, использованные Entity, загруженная конфигурация сайта и т.д. Разумеется, тулбар может быть расширен любой другой вспомогательной информацией. Найти его можно тут: https://github.com/zendframework/ZendDeveloperTools.

Чтобы  установить тулбар сначала добавим строчку:
```
"zendframework/zend-developer-tools": "dev-master",
```
в файл `composer.json` в корне проекта и затем выполним команду `php composer.phar update` в корне проекта.

Затем в файл `config/application.config.php` в массив modules нужно добавить элемент ZendDeveloperTools:
```
'modules' => array(
    'Application',
    'ZendDeveloperTools',
),
```
Теперь осталось скопировать файл `vendor/zendframework/zend-developer-tools/config/zenddevelopertools.local.php.dist` в папку `config/autoload` нашего проекта и переименовать его, например, в `zenddevelopertools.local.php` (часть имени до local.php по большому счету значения не имеет).

Всё, теперь, по умолчанию, внизу всех страниц выводится информация о затраченных на генерацию страницы ресурсах, конфигурация проекта и т.п.

Хочу обратить внимание на то, что по умолчанию тулбар будет доступен всем посетителям сайта по этому в production окружении его использовать не стоит.

Текущая версия приложения доступна на Гитхабе в репозитории проекта с тэгом `zenddevelopertools`: https://github.com/romka/zend-blog-example/tree/zenddevelopertools

### Doctrine ORM
Для интеграции с Доктриной понадобятся модули DoctrineModule и DoctrineORMModule (https://github.com/doctrine/DoctrineModule и https://github.com/doctrine/DoctrineORMModule).

Добавим в секцию require файла composer.json строчки:
```
"doctrine/common": ">=2.1",
"doctrine/doctrine-orm-module": "0.7.*"
```
и выполним в консоли команду `php composer.phar update`.

Модуль DoctrineModule можно не указывать явно в нашем `composer.json`, так как эта зависимость прописана на уровне модуля DoctrineORMModule.

Теперь нужно в директории `config/autoload` разместить файл `doctrine.local.php` с параметрами доступа к БД, который будет использоваться Доктриной, его содержимое должно быть примерно таким:
```
<?php
return array(
    'doctrine' => array(
        'connection' => array(
            'orm_default' => array(
                'driverClass' =>'Doctrine\DBAL\Driver\PDOMySql\Driver',
                'params' => array(
                    'host'     => 'localhost',
                    'port'     => '3306',
                    'user'     => 'username',
                    'password' => 'pass',
                    'dbname'   => 'dbname',
                )
            )
        ),
    ),
);
```
Теперь если мы перезагрузим страницу нашего сайта, то внизу страницы в Zend девлопер тулбаре увидим два новых блока, показывающих число выполненных запросов и список маппингов к БД. Оба значения равны нулю, так как маппинги мы пока не сделали и, как следствие, запросов к базе нет.

В этом туториале я хочу разработать простейший блог и сейчас настало время написать первые строчки кода нового модуля.
## Модуль MyBlog
В каталоге `modules` создадим следующие директории и файлы:
```
MyBlog/
    config/
        module.config.php
    src/
        MyBlog/
            Entity/
                BlogPost.php
    Module.php
```
Содержимое файла `Module.php` должно быть таким:
```
<?php
namespace MyBlog;

class Module
{
  public function getAutoloaderConfig()
  {
    return array(
      'Zend\Loader\StandardAutoloader' => array(
        'namespaces' => array(
          __NAMESPACE__ => __DIR__ . '/src/' . __NAMESPACE__,
        ),
      ),
    );
  }

  public function getConfig()
  {
    return include __DIR__ . '/config/module.config.php';
  }
}
```
Файл аналогичен тому, что используется в модуле Application, мы говорим ядру фреймворка где искать конфигурационный файл модуля и файлы исходников.

Конфигурационный файл пока должен возвращать пустой массив, настройки нового модуля мы зададим чуть позже.

Файл `src/MyBlog/Entity/BlogPost.php` является связью (маппингом) между Доктриной и базой данных и о нем нужно поговорить подробнее.

### BlogPost.php
Каждый блогпост в моем примере будет содержать следующие поля:

- заголовок,
- тело блогпоста,
- id автора (0 для анонимов),
- статус (опубликовано/не опубликовано)
- дата публикации.

Для простоты я не стану в этом туториале заморачиваться с тэгами, комментариями и другими свойственными блогам фичами.

Этот файл объявляет класс BlogPost, который содержит описания полей блогпоста и методов доступа к ним. Полную версию файла вы можете посмотреть на Гитхабе (https://github.com/romka/zend-blog-example/blob/master/module/MyBlog/src/MyBlog/Entity/BlogPost.php), вот так выглядит его часть:
```
<?php
namespace MyBlog\Entity;

use Doctrine\Common\Collections\ArrayCollection;
use Doctrine\ORM\Mapping as ORM;

class BlogPost
{
  /**
   * @var int
   * @ORM\Id
   * @ORM\Column(type="integer")
   * @ORM\GeneratedValue(strategy="AUTO")
   */
  protected $id;

  /**
   * @var string
   * @ORM\Column(type="string", length=255, nullable=false)
   */
  protected $title;

  /**
   * Get id.
   *
   * @return int
   */
  public function getId()
  {
    return $this->id;
  }

  /**
   * Set id.
   *
   * @param int $id
   *
   * @return void
   */
  public function setId($id)
  {
    $this->id = (int) $id;
  }

  /**
   * Get title.
   *
   * @return string
   */
  public function getTitle()
  {
    return $this->title;
  }

  /**
   * Set title.
   *
   * @param string $title
   *
   * @return void
   */
  public function setTitle($title)
  {
    $this->title = $title;
  }

}
```
Каждая переменная в этом классе станет полем в БД, параметры полей задаются в аннотациях, которые будут прочитаны Доктриной (примерно вот так: http://php.net/manual/en/reflectionclass.getdoccomment.php, класс `Doctrine\Common\Annotations\AnnotationReader` метод `getClassAnnotations()`).

Теперь в конфигурационный файл модуля `config/module.config.php` можно добавить информацию о нашей новой Entity, которая будет использована Доктриной:
```
return array(
    'doctrine' => array(
        'driver' => array(
            'myblog_entity' => array(
                'class' =>'Doctrine\ORM\Mapping\Driver\AnnotationDriver',
                'paths' => array(__DIR__ . '/../src/MyBlog/Entity')
            ),
            'orm_default' => array(
                'drivers' => array(
                    'MyBlog\Entity' => 'myblog_entity',
                )
            )
        )
    ),
);
```
И осталось добавить модуль MyBlog в список активных модулей в `application.config.php`.

Мы закончили настройку сущности BlogPost и сейчас нужно создать соответствующую таблицу в базе данных, для этого воспользуемся консольной утилитой, поставляющейся в комплекте с Доктриной. В корне проекта выполним команду:
```
./vendor/bin/doctrine-module orm:info
```
И результатом должно быть сообщение вида:
```
Found 1 mapped entities:
[OK]   MyBlog\Entity\BlogPost
```
После того как мы убедились в том, что Доктрина видит наш объект BlogPost выполним команду:
```
./vendor/bin/doctrine-module orm:validate-schema
```
В результате должна вернуться ошибка вида:
```
[Mapping]  OK - The mapping files are correct.
[Database] FAIL - The database schema is not in sync with the current mapping file.
```
Это и логично, так как наша база данных все еще пуста и сейчас мы создадим нужную таблицу командой:
```
./vendor/bin/doctrine-module orm:schema-tool:update --force
```
Её результатом будет следующий вывод:
```
Updating database schema...
Database schema updated successfully! "1" queries were executed
```
И теперь вызов команды:
```
./vendor/bin/doctrine-module orm:validate-schema
```
вернет результат:
```
[Mapping]  OK - The mapping files are correct.
[Database] OK - The database schema is in sync with the mapping files.
```
Если сейчас обновить страницу нашего сайта, то в тулбаре внизу страницы мы увидим, что Доктрина видит один маппинг `Myblog\Entity\BlogPost`.

Исходные коды текущей версии проекта можно найти в репозитории проекта на Гитхабе с тэгом `blogpost_entity`: https://github.com/romka/zend-blog-example/tree/blogpost_entity.

Теперь, когда у нас есть сущность для работы с блогпостами можно перейти к написанию своего первого контроллера, реализующего форму добавления блогпоста.

### Добавление блогпоста
В директории src/MyBlog модуля создадим два новых каталога с файлами:
```
Controller/
    BlogController.php
Form/
    BlogPostForm.php
    BlogPostInputFilter.php
```
Далее в конфигурационный файл модуля нужно добавить элементы, объявляющие список контроллеров модуля, маршруты и путь к директории с шаблонами:
```
'controllers' => array(
    'invokables' => array(
        'MyBlog\Controller\BlogPost' => 'MyBlog\Controller\BlogController',
    ),
),

'router' => array(
    'routes' => array(
        ‘blog' => array(
            'type'    => 'segment',
            'options' => array(
                'route'    => '/blog[/][:action][/:id]',
                'constraints' => array(
                    'action' => '[a-zA-Z][a-zA-Z0-9_-]*',
                    'id'     => '[0-9]+',
                ),
                'defaults' => array(
                    'controller' => 'MyBlog\Controller\BlogPost',
                    'action'     => 'index',
                ),
            ),
        ),
    ),
),

'view_manager' => array(
    'template_path_stack' => array(
        __DIR__ . '/../view',
    ),
),
```

Исходя из заданных выше настроек, все страницы нашего блога будут иметь урлы вида `blog/[action]/[id]` (элементы пути в квадратных скобках не обязательны).

Файл `BlogPostForm.php` будет содержать форму, которая будет использоваться для добавления/редактирования блогпоста, давайте создадим эту форму.

### BlogPostForm.php
В самом простом случае код формы будет выглядеть вот так (это не полный исходный код формы, целиком его можно увидеть тут: https://github.com/romka/zend-blog-example/blob/master/module/MyBlog/src/MyBlog/Form/BlogPostForm.php):
```
class BlogPostForm extends Form
{
    public function __construct($name = null)
    {
        parent::__construct('blogpost');
        $this->setAttribute('method', 'post');
        $this->add(array(
            'name' => 'id',
            'type' => 'Hidden',
        ));
        $this->add(array(
            'name' => 'title',
            'type' => 'Text',
            'options' => array(
                'label' => 'Title',
            ),
            'options' => array(
                'min' => 3,
                'max' => 25
            ),
        ));
        $this->add(array(
            'name' => 'text',
            'type' => 'Textarea',
            'options' => array(
                'label' => 'Text',
            ),
        ));
        $this->add(array(
            'name' => 'state',
            'type' => 'Checkbox',
        ));
        $this->add(array(
            'name' => 'submit',
            'type' => 'Submit',
            'attributes' => array(
                'value' => 'Save',
                'id' => 'submitbutton',
            ),
        ));
    }
}
```
Очевидно, что этот код объявляет необходимые нам поля формы, но пока для них не заданы ни фильтры (позволяющие преобразовать входящие данные), ни валидаторы (которые не позволят ввести в форму данные в неправильном формате). Их мы зададим позже, а сейчас давайте напишем код контроллера, который будет выводить форму добавления блогпоста и сохранять введенные данные.

### BlogController.php
Полный код контроллера вы можете посмотреть в репозитории (https://github.com/romka/zend-blog-example/blob/master/module/MyBlog/src/MyBlog/Controller/BlogController.php), ниже его ключевая часть:
```
class BlogController extends AbstractActionController
{

    public function indexAction()
    {
        return new ViewModel();
    }

    public function addAction()
    {
        $form = new \MyBlog\Form\BlogPostForm();
        $form->get('submit')->setValue('Add');

        $request = $this->getRequest();
        if ($request->isPost()) {
            $form->setData($request->getPost());

            if ($form->isValid()) {
                $objectManager = $this->getServiceLocator()->get('Doctrine\ORM\EntityManager');

                $blogpost = new \MyBlog\Entity\BlogPost();

                $blogpost->exchangeArray($form->getData());

                $blogpost->setCreated(time());
                $blogpost->setUserId(0);

                $objectManager->persist($blogpost);
                $objectManager->flush();

                // Redirect to list of blogposts
                return $this->redirect()->toRoute('blog');
            }
        }
        return array('form' => $form);
    }
}
```
Значимым для нас является код экшена addAction (имена всех экшенов должны создаваться по маске nameAction()). В нем мы сначала создаем объект формы и заменяем текст кнопки submit на ней (у нас одна и та же форма будет использоваться и для создания, и для редактирования блогпостов, по этому тексты на этой кнопке удобно иметь разные):
```
$form = new \MyBlog\Form\BlogPostForm();
$form->get('submit')->setValue('Add');
```
Затем, в случае если форма прошла валидацию (а валидацию сейчас она пройдет в любом случае, так как валидаторов у нас пока нет) мы создаем экземпляр класса \MyBlog\Entity\BlogPost(), который является связью между нашим приложением и БД, наполняем созданный объект данными и сохраняем их в БД:
```
$blogpost->exchangeArray($form->getData());

$blogpost->setCreated(time());
$blogpost->setUserId(0);

$objectManager->persist($blogpost);
$objectManager->flush();
```
Текущую версию шаблона, отвечающего за отображение формы, можно увидеть по ссылке https://github.com/romka/zend-blog-example/blob/blogpost_form_1/module/MyBlog/view/my-blog/blog/add.phtml. 

Если cейчас попробовать сохранить пустую форму, то Доктрина вернет сообщение об ошибке вида:
```
An exception occurred while executing 'INSERT INTO blogposts (title, text, userId, created, state) VALUES (?, ?, ?, ?, ?)' with params [null, null, 0, 1377086855, null]:

SQLSTATE[23000]: Integrity constraint violation: 1048 Column 'title' cannot be null
```
Это правильно, ведь у нас есть только одно поле, помеченное как `nullable="true"` — это поле state, а все остальные должны быть заполнены. Давайте добавим к форме инпут фильтры и валидаторы, чтобы перехватывать подобные ошибки еще до попытки сохранить данные (на уровне нашего приложения, а не БД), чтобы у пользователя была возможность исправить ошибку.

### Валидация форм
В ранее созданном файле `BlogPostInputFilter.php` разместим такой код (полная версия на Гитхабе: https://github.com/romka/zend-blog-example/blob/master/module/MyBlog/src/MyBlog/Form/BlogPostInputFilter.php):
```
class BlogPostInputFilter extends InputFilter
{
    public function __construct()
    {
        $this->add(array(
            'name' => 'title',
            'required' => true,
            'validators' => array(
                array(
                    'name' => 'StringLength',
                    'options' => array(
                        'min' => 3,
                        'max' => 100,
                    ),
                ),
            ),
            'filters' => array(
                array('name' => 'StripTags'),
                array('name' => 'StringTrim'),
            ),

        ));

        $this->add(array(
            'name' => 'text',
            'required' => true,
            'validators' => array(
                array(
                    'name' => 'StringLength',
                    'options' => array(
                        'min' => 50,
                    ),
                ),
            ),
            'filters' => array(
                array('name' => 'StripTags'),
                array('name' => 'StringTrim'),
            ),
        ));

        $this->add(array(
            'name' => 'state',
            'required' => false,
        ));
    }
}
```
Предполагаю, что смысл этих строк должен быть интуитивно понятным: для полей title и text мы добавляем инпут фильтры, которые удалят из текстов все html тэги (фльтр StripTags) и обрежут пробелы по краям строк (StrinTrim), а также добавляем валидаторы, определяющие значения минимальной и максимальной длины полей (StringLength).

Осталось присоединить новый фильтр к форме, добавив в класс формы строчку:
```
$this->setInputFilter(new \MyBlog\Form\BlogPostInputFilter());
```
Теперь форма не пройдет валидацию, если в нее введены некорректные данные.
### View плагины
После того как блогпост успешно сохранен (или не сохранен) мы перенаправляем пользователя на страницу /blog, на которой в будущем у нас будет полный список блогпостов. Хотелось бы не просто сделать редирект, но и вывести на экран сообщение об успешно выполненном действии.

Добавить такие сообщения можно с помощью методов: 
```
$this->flashMessenger()->addMessage($message);
$this->flashMessenger()->addErrorMessage($message);
```
Извлечь сообщения, добавленные таким способом можно в контроллере или в phtml-шаблонах таким образом:
```
$object->flashMessenger()->getMessages();
$object->flashMessenger()->getErrorMessages();
```
Проблема в том, что неудобно (а в Twig-шаблонах, которые мы будем использовать позже, и вовсе невозможно) вызывать PHP-код для вывода сообщений. По этому мы напишем небольшой View-плагин, который сможет одной строчкой выводить на экран все сообщения.

Для этого в директории src\MyBlog модуля создадим такие директории и файлы:
```
View\
    Helper\
        ShowMessages.php
```
Содержимое `ShowMessages.php` можно посмотреть тут: https://github.com/romka/zend-blog-example/blob/master/module/MyBlog/src/MyBlog/View/Helper/ShowMessages.php, оно не очень интересно, я здесь просто получаю список сообщений, форматирую и возвращаю готовый html-код для их отображения.

Осталось сделать три действия:

1. зарегистрировать View-плагин,
2. добавить его использование в шаблон,
3. и вывести сообщения о успешном/неудачном сохранении формы.

Чтобы зарегистрировать плагин добавим в настройки модуля в сецкию view_helper => invokables строчку:
```
'view_helpers' => array(
    'invokables' => array(
        'showMessages' => 'MyBlog\View\Helper\ShowMessages',
    ),
),
```
В шаблоны добавим вывод сообщений:
```
print $this->showMessages();
```
Для вывода сообщений на экран добавим в контроллер такие строчки: 
```
$message = 'Blogpost succesfully saved!';
$this->flashMessenger()->addMessage($message);
```
Теперь у нас есть возможность выводить пользователю системные сообщения.

Эту версию приложения вы можете найти в гит-репозитории с тэгом `blogpost_form_1`: https://github.com/romka/zend-blog-example/tree/blogpost_form_1. 

На текущем этапе у нас есть:

1. сущность для связи приложения и БД, созданная при помощи Доктрины,
2. контроллер обслуживающий страницу добавления блогпоста,
3. форма добавления блогпоста с инпут фильтрами и валидаций,
4. свой кастомный View-плагин для вывода сообщений на экран.

Теперь давайте добавим страницы одного блогпоста, списка блогпостов и формы редактирования/удаления поста.

### Страница блогпоста
Добавим в контроллер BlogpostController новое действие view:
```
public function viewAction()
{
    $id = (int) $this->params()->fromRoute('id', 0);
    if (!$id) {
        $this->flashMessenger()->addErrorMessage('Blogpost id doesn\'t set');
        return $this->redirect()->toRoute('blog');
    }

    $objectManager = $this->getServiceLocator()->get('Doctrine\ORM\EntityManager');

    $post = $objectManager
        ->getRepository('\MyBlog\Entity\BlogPost')
        ->findOneBy(array('id' => $id));

    if (!$post) {
        $this->flashMessenger()->addErrorMessage(sprintf('Blogpost with id %s doesn\'t exists', $id));
        return $this->redirect()->toRoute('blog');
    }

    $view = new ViewModel(array(
        'post' => $post->getArrayCopy(),
    ));

    return $view;
}
```
Этот экшен доступен по адресу blog/view/ID. В нем мы сначала мы проверяем, что в URL’е задан id блогпоста, если это не так, то возвращаем ошибку и редиректим пользователя на страницу со списком блогпостов. Затем извлекаем пост из базы и передаем его в шаблон. 

В качестве имени шаблона по умолчанию используется имя контроллера, по этому теперь в директории модуля view/my-blog/blog нужно создать файл view.phtml с примерно вот таким содержимым:
```
<?php
    print $this->showMessages();
    print '<h1>' . $post['title'] . '</h1>';
    print '<div>' . $post['text'] . '</div>';
```

### Список блогпостов
Обновим код нашего indexAction до такого вида:
```
public function indexAction()
{
    $objectManager = $this->getServiceLocator()->get('Doctrine\ORM\EntityManager');

    $posts = $objectManager
        ->getRepository('\MyBlog\Entity\BlogPost')
        ->findBy(array('state' => 1), array('created' => 'DESC'));

    $view = new ViewModel(array(
        'posts' => $posts,
    ));

    return $view;
}
```
Здесь мы выбираем все опубликованные блогпосты (state == 1), сортируем их по дате публикации и передаем в шаблон `index.phtml` https://github.com/romka/zend-blog-example/blob/blogpost_form_2/module/MyBlog/view/my-blog/blog/index.phtml. В шаблоне выводятся заголовки блогпостов и ссылки на их редактирование и удаление.

### Небольшое отступление
Выше, при создании формы я забыл добавить поле userId, в котором хранится айдишник автора блогпоста. Так как сейчас регистрации/авторизации в нашем блоге нет, это поле по умолчанию заполняется нулем, но в будущем оно пригодится, по этому сейчас я добавил в форму hidden поле userId.

Кроме того, я добавил к форме Csrf-токен (поле security), который должен защитить форму от подделки. По умолчанию этот токен формируется на основании пользовательской сессии и соли и живет 300 секунд (`Zend\Form\Element\Csrf.php`), но может быть (и по хорошему должен быть) переопределен и к нему как минимум должна быть добавлена зависимость от ip посетителя.

### Редактирование блогпоста
Для редактирования поста мы будем использовать уже существующую форму. В контроллере необходимо создать действие `editAction()`, которое будет создавать форму, наполнять её существующими данными и отдавать пользователю. Этот экшен является смесью `addAction()`, в части работы с формой, и `viewAction()`, в части выборки данных https://github.com/romka/zend-blog-example/blob/blogpost_form_2/module/MyBlog/src/MyBlog/Controller/BlogController.php#L95.

Вот самая интересная часть этого контроллера:
```
if ($form->isValid()) {
    $objectManager = $this->getServiceLocator()->get('Doctrine\ORM\EntityManager');

    $data = $form->getData();
    $id = $data['id'];
    try {
        $blogpost = $objectManager->find('\MyBlog\Entity\BlogPost', $id);
    }
    catch (\Exception $ex) {
        return $this->redirect()->toRoute('blog', array(
            'action' => 'index'
        ));
    }

    $blogpost->exchangeArray($form->getData());

    $objectManager->persist($blogpost);
    $objectManager->flush();

    $message = 'Blogpost succesfully saved!';
    $this->flashMessenger()->addMessage($message);

    // Redirect to list of blogposts
    return $this->redirect()->toRoute('blog');
}
```
Здесь мы загружаем из БД блогпост, основываясь на id, который пришел в форме, обновляем данные:
```
$blogpost->exchangeArray($form->getData());
```
и кладем обновленный блогпост в базу:
```
$objectManager->persist($blogpost);
$objectManager->flush();
```

### Удаление блогпостов
Удаление блогпоста задача тривиальная, достаточно вывести пользователю форму с вопросом вида ”Действительно ли вы хотите удалить пост?” и в случае если пользователь нажмет кнопку “Да”, выполнить соответствующие действия.

Код соответствующего контроллера и шаблона можно посмотреть на Гитхабе: https://github.com/romka/zend-blog-example/blob/blogpost_form_2/module/MyBlog/src/MyBlog/Controller/BlogController.php#L161.

Исходники с тэгом `blogpost_form_2` (https://github.com/romka/zend-blog-example/tree/blogpost_form_2) содержат формы редактирования и удаления блогпоста, список постов и соответствующие шаблоны.

На этом я бы хотел завершить вторую часть статьи. [В третьей части]({{< relref "primer-razrabotki-bloga-na-zend-framework-2-chast-3-rabota-s-polzovatelyami" >}}) мы займёмся работой с пользователями.
---
title: Разработал модуль "Адаптивное меню" для Drupal 6
date: 2008-08-28 23:20:19 +0400
draft: false
tags: [old-site, Работа, Drupal, Drupal 6, модуль, Штуки-дрюки]
deprecated: true
---
{{< resource "sam_adaptive_menu.zip" "Модуль" >}} позволяет пользователям формировать меню, состоящее из любых ссылок, как внешних, так и внутренних.

## Фичи модуля

- достаточно добавить URL, заголовок страницы будет получен автоматически;
- сортировка элементов меню осуществляется простым перетаскиванием;
- все действия пользователя обрабатываются при помощи технологии AJAX, по этому интерфейс не усложнен лишними вопросами или перезагрузками страницы. Все изменения сохраняются "на лету".

## Небольшая демонстрация возможностей
<center>
<div id="media">
             <object id="csSWF" classid="clsid:d27cdb6e-ae6d-11cf-96b8-444553540000" width="224" height="224" codebase="http://active.macromedia.com/flash7/cabs/ swflash.cab#version=8">
                <param name="src" value="{{< resource "adaptive-menu.swf" >}}"/>
                <param name="bgcolor" value="FFFFFF"/>
                <param name="quality" value="best"/>
                <param name="flashVars" value="csConfigFile=/files/swf/adaptive-menu/adaptive-menu_config.xml&csColor=FFFFFF"/>
                <embed name="csSWF" src="{{< resource "adaptive-menu.swf" >}}" width="224" height="224" bgcolor="FFFFFF" quality="best" allowScriptAccess="always" pluginspage="http://www.macromedia.com/shockwave/download/index.cgi?P1_Prod_Version=ShockwaveFlash"></embed>
             </object>
          </div>
</center>
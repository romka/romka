---
title: Опубликовал в Google Play свою первую Android-игрушку Tetcolor
date: 2013-11-11 09:23:19 +0400
draft: false
tags: [old-site, игра, Tetcolor, Gideros, mobile]
---
[{{< img-right "feature.png" "Tetcolor" >}}](http://tetcolor.net/)

Tetcolor — это ремейк классического Tetris color для OS Android (и в ближайшее время для iOS, так как игра построена на кроссплатформенном движке Gideros). В игре реализовано несколько режимов, локальные и глобальные таблицы рекордов и удобное управление (пара слов об этом ниже).

Сайт игры с подробным описанием правил и таблицами рекордов: http://tetcolor.net/.
Прямая ссылка на Google Play: https://play.google.com/store/apps/details?id=eu.romka.tetcolor.

Это мой первый опыт разработки игры по мобильные платформы в целом и с использованием [Gideros Mobile](http://giderosmobile.com/) в частности, по этому начать решил с максимально простого проекта, чтобы параллельно с разработкой освоить базовые API движка. В отличии от десятка подобных игр уже опубликованных в Google Play в моей версии игры управление основано не на кнопках (в которые сложно попасть не глядя), а на жестах, которые можно использовать в любой части экрана.

Гидерос оказался достаточно функциональным движком (заточенным только по 2D-приложения!), практически все мои потребности были покрыты или стандартным его функционалом, или готовыми сторонними библиотеками. Из недостатков могу пока назвать только отсутствие возможности использовать native UI компоненты, по этому мне не удалось реализовать полноценный сервис рекордов с регистрацией пользователей, но разработчики, судя по [roadmap](http://giderosmobile.com/roadmap), активно над этим работают.

[![]({{< relref "opublikoval-v-google-play-svoyu-pervuyu-android-igrushku-tetcolor" >}}/ru_generic_rgb_wo_60.png)](https://play.google.com/store/apps/details?id=eu.romka.tetcolor)
[![]({{< relref "opublikoval-v-google-play-svoyu-pervuyu-android-igrushku-tetcolor" >}}/Badge_RU_135x40.png)](https://itunes.apple.com/us/app/tetcolor-classic/id765111441)

**Обновление от 01.12.2013** Теперь игра доступна и в Apple AppStore.
<!--more-->

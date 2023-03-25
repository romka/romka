---
title: Автоматическая "газетная" верстка (верстка в несколько колонок)
date: 2008-09-05 14:35:52 +0400
draft: false
tags: [old-site, jquery, Штуки-дрюки, газетная верстка, журнальная верстка, верстка в несколько колонок]
deprecated: true
---
Наткнулся на еще один очень интересный плагин [Columnizer](http://plugins.jquery.com/project/Columnizer) для библиотеки [jQuery](jquery.com), который позволяет **автоматически** форматировать текст в "газетном" стиле, то есть разбивать его на несколько колонок.
<!--more-->
Выглядит это так:
```
<div class="column-2" id="column">
<h1>Lorem ipsum ne justo</h1>
		<p>Bonorum has. His ut cibo quas tantas, vis ut probo adhuc definiebas, has at meis debet vulputate. No sed velit essent suavitate, in pro decore <a href='javascript;'>ceteros temporibus</a>, usu in odio offendit theophrastus. Mel labore indoctum cu, ad soleat admodum delicatissimi sed, mei viris tritani ullamcorper eu. Ut vim simul aperiam.</p>
		<p>Eu eleifend repudiandae has. Mea eu ridens aliquam. Nisl aeque sit ut, posse dolor utinam cum in. Ad timeam sapientem eos, et eripuit inermis nam. Eos integre voluptaria ne, iriure concludaturque ut eum.</p>
		<p>Vis erant intellegat in. Soleat legere no ius, usu ex laoreet molestie. Sit <a href='javascript;'>eu sint inermis</a>. Ea zzril scribentur pro.</p>
		<h1>Tempor essent appetere</h1>
		<p>Ius mutat commune expetendis in. Nam et quas sensibus <a href='javascript;'>reprimique</a>, vix no erat soluta suavitate. At mel eius dictas latine. Corrumpit inciderint reformidans sed no, no usu omnis utinam noluisse.</p>
		<p>Sit et, an ius nihil apeirian. Eu posse tempor iuvaret cum. No diam dolor sea, postea mnesarchum ne ius, vel no utinam ignota dolores. Malis suscipit accusamus his ne, utinam assentior prodesset ea eam, facer partem antiopam et cum.</p>
		<blockquote><p>Probo debet quaestio an eos, no mel assum <a href='javascript;'>iracundia delicatissimi</a>, rebum facete utroque sed ex. Eu melius invidunt repudiandae vix, eu paulo reformidans deterruisset duo, solum voluptaria efficiantur ea mel. Qui summo zzril alienum et. Eu est ferri iuvaret, mazim epicurei sententiae ut cum, modo reque intellegat ex vix. Vim eu tibique accusamus, quot electram at qui.</p></blockquote>
		<p>Ex iisque eleifend periculis has. Sit aeterno virtute partiendo ei, eam nonumy bonorum adolescens ad. Ut nec suas vocent ornatus, cetero legendos <a href='javascript;'>constituam mea ea</a>, pri cu delenit iracundia. Mundi decore nec te.</p>
		<h1>Soleat civibus in pri</h1>
		<p>In petentium erroribus percipitur per. Takimata accommodare ius ut, eam no postulant urbanitas. Qui ei tantas consectetuer, quis dictas euripidis duo ei. Quaeque democritum concludaturque has ne.</p>
		<p>Blandit insolens constituto vix an. Has diam wisi in, eum unum repudiare no. Sit at virtute rationibus, qui vitae explicari cu. Vim ne singulis voluptatum, sed puto accusata salutandi ei. Ad mel civibus adversarium.</p>
		<p>Per ne solum vivendo, fabulas dolorem vivendo in pro. Nec duis ignota cotidieque no, an per possit nostrum. Pro detraxit definitionem eu. Vivendo officiis no nam, eu has reque maiestatis percipitur, dolore reprimique accommodare cum ad. No utinam voluptua oportere pri, augue sonet dicant ei sea.</p>
		<p>Sit et, an ius nihil apeirian. Eu posse tempor iuvaret cum. No diam dolor sea, postea mnesarchum ne ius, vel no utinam ignota dolores. Malis suscipit accusamus his ne, utinam assentior prodesset ea eam, facer partem antiopam et cum.</p>
</div>
```

Для того чтобы добиться такого эффекта, необходимо скачать и подключить библиотеку [jQuery](http://docs.jquery.com/Downloading_jQuery) и плагин [Columnizer](http://plugins.jquery.com/project/Columnizer), а также файл с настройками:
```
<script src="jquery.js" type="text/javascript" charset="utf-8"></script>
<script src="autocolumn.min.js" type="text/javascript" charset="utf-8"></script>
<script src="autocolumn.settings.js" type="text/javascript" charset="utf-8"></script>
```

Затем обернуть необходимый текст в слой (или параграф) с определенным классом, например "column":
```
<div class="column">
<h1>Lorem ipsum ne justo</h1>
<p>Bonorum has. His ut cibo quas tantas, vis ut probo adhuc definiebas, has at meis debet vulputate. No sed velit essent suavitate, in pro decore <a href='javascript;'>ceteros temporibus</a>, usu in odio offendit theophrastus. Mel labore indoctum cu, ad soleat admodum delicatissimi sed, mei viris tritani ullamcorper eu. Ut vim simul aperiam.</p>
<p>Eu eleifend repudiandae has. Mea eu ridens aliquam. Nisl aeque sit ut, posse dolor utinam cum in. Ad timeam sapientem eos, et eripuit inermis nam. Eos integre voluptaria ne, iriure concludaturque ut eum.</p>
</div>
```

В файле autocolumn.settings.js необходимо прописать на сколько колонок должен быть разбит текст в контейнере с классом "column":
```
$(function(){
	$('.column').columnize({columns:2});
});
```

Всё, теперь весь текст, который находится внутри слоя "column" будет разбит на 2 колонки. Таких контейнеров на странице может быть несколько. 

Для того чтобы при маленьких размерах окна строка с текстом не была слишком короткой (оптимальной длиной строки считается размер в 45-76 символов) можно указать минимальную ширину для колонки:
```
$(function(){
	$('.column').columnize({columns:2, width: 300});
});
```

Если в разных местах страницы нужно бить текст на разное количество колонок, то в файле autocolumn.settings.js достаточно добавить необходимые настройки, например:
```
$(function(){
$('.column-2').columnize({columns:2});
$('.column-3').columnize({columns:3});
});
```

Теперь в слоях с классом column-2 текст будет автоматически разбиваться на 2 колонки, а в слоях с классом column-3 &mdash; на 3.
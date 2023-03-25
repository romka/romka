---
title: Футер, прибитый к низу страницы
date: 2011-03-27 13:36:12 +0400
draft: false
tags: [old-site, Работа]
deprecated: true
---
Давно не занимался версткой, сейчас понадобилось сверстать страницу с прибитым к низу страницы футером, помню что раньше не мог найти простого и универсального решения этой задачи, по этому обрадовался, когда нашел вот это решение: http://ryanfait.com/resources/footer-stick-to-bottom-of-page/.

Css:
```
* {
  margin: 0;
  }

html, body {
height: 100%;
}

.wrapper {
min-height: 100%;
height: auto !important;
height: 100%;
margin: 0 auto -4em;
}

.footer, .push {
height: 4em;
}
```

Html:
```
<html>
    <head>
        <link rel="stylesheet" href="layout.css" ... />
    </head>
    <body>
        <div class="wrapper">
            <p>Your website content here.</p>
            <div class="push"></div>
        </div>
        <div class="footer">
            <p>Copyright (c) 2008</p>
        </div>
    </body>
</html>
```

Для многоколоночной верстки нужно добавить атрибут `clear: both;` к классу `.footer, .push`.

Действующий пример: http://ryanfait.com/sticky-footer/.
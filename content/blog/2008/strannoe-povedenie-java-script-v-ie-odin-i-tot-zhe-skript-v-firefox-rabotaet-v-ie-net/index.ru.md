---
title: Странное поведение Java-script в IE. Один и тот же скрипт в Firefox работает, а в IE – нет.
date: 2008-03-01 16:29:36 +0300
draft: false
tags: [old-site, Работа, firefox, ie, jquery, java-script]
---
Столкнулся со странной проблемой, на решение которой убил пол дня. Один и тот же скрипт в Firefox'e работает корректно, а в IE – нет. Дальше приведено решение проблемы.
<!--more-->
Столкнулся со странной проблемой, на решение которой убил пол дня. Есть java-скрипт, использующий библиотеку jQuery:
{{< highlight javascript >}}
$.ajax(
{
    type: "POST",
    url: "http://" + p + "check/ajax",
    data: "code=" + code,
    dataType: 'json',
    success: function(data){$('div#loading').html(data.result);},
    error: function(data){$('div#loading').html(data.result);}
});
{{< / highlight >}}

В Firefox'e он работает на ура, а в Internet Explorer 6 - нет. Методом научного тыка выяснил, что если записать этот скрипт в одну строчку:
{{< highlight javascript >}}
$.ajax({type: 'POST',	url: 'http://' + p + 'check/ajax',data: 'code=' + code,dataType: 'json',success: function(data){$('div#loading').html(data.result);},error: function(data){$('div#loading').html(data.result);}});
{{< / highlight >}}

то и в ИЕ он сработает корректно.
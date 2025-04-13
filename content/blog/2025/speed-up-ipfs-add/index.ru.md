---
title: Ускорение выполнения команды ipfs add
date: 2025-04-06 14:25:00 +0100
draft: false
telegram: true
tags: [Работа, ipfs, ускорение]
---
В двух предыдущих постах я рассказал о том, [что такое ipfs]({{< relref "/blog/2025/ipfs" >}}) и [как развернуть сайт в ipfs]({{< relref "/blog/2025/hosting-static-web-site-on-ipfs" >}}) и, помимо этого, для эксперимента настроил раздачу своего блога через ipfs: [ipfs.romka.eu](https://ipfs.romka.eu). 

Сайт обслуживается дешёвой виртуальной машиной, а, как оказалось, ipfs довольно прожорлив до ресурсов процессора, особенно при выполнении команды `ipfs add`. Несколько раз хостер просто молча прибивал мою виртуалку из-за превышения ею каких-то лимитов.

В моём случае ipfs работает в докер-контейнере, который запускается через `docker compose`. Поэтому я сконфигурировал запуск контейнера следующим образом, чтобы сильно ограничить потребляемые ресурсы:
```
  ipfs:
    image: ipfs/kubo:latest
    container_name: ipfs_container
    <...>
    restart: always
    command: daemon --enable-gc --migrate=true --enable-pubsub-experiment
    cpus: 0.3
    mem_limit: 256m
    memswap_limit: 256m
    environment:
      GOMAXPROCS: 1
```
Теперь ipfs-процесс ограничен по ресурсам и хостер доволен, но вот команда `ipfs add` стала падать с ошибкой вида `Error: unexpected EOF`. Я не стал копать глубже, но в свете того что ошибка появилась после добавления ограничений, похоже на то что это следствие того что ОС просто прибивает процесс ipfs из-за Out of Memory error (OOM). Дальше я расскажу как мне удалось исправить эту проблему.
{{< more >}}
<!--more-->

После нескольких подходов к решению проблемы, среди которых были эксперименты с флагом `--only-hash`, MFS и другие, максимально простым и надёжным решением оказалось просто останавливать ipfs демон на время добавления файлов. Однако есть один нюанс. С конфигурацией выше, а именно из-за строки `command: daemon --enable-gc --migrate=true --enable-pubsub-experiment`, ipfs становится init-процессом (PID 1) внутри контейнера, поэтому при его остановке докер считает, что контейнер завершился, и из-за `restart: always` тут же перезапускает его. Поэтому конфиг пришлось переписать так:
```
  ipfs:
    image: ipfs/kubo:latest
    container_name: ipfs_container
    <...>
    restart: always
    init: true
    entrypoint: ["sh", "-c", "sleep infinity"]

    cpus: 0.3
    mem_limit: 256m
    memswap_limit: 256m
    environment:
      GOMAXPROCS: 1
```
Теперь, из-за параметра `init: true`, init-процессом становится [tini](https://github.com/krallin/tini), который в свою очередь запускает `sleep` (параметр `entrypoint`), а ipfs демон нужно отдельно стартануть руками `docker exec -d ipfs_container ipfs daemon`. Это немного неудобно, так как появляется дополнительное действие после запуска контейнера, зато, для добавления файлов в ipfs, демон можно временно остановить и перезапустить после добавления файлов:
```
docker exec ipfs_container ipfs shutdown
docker exec -it ipfs_container ipfs add -r --nocopy /data/ipfs/public
docker exec -d ipfs_container ipfs daemon
docker exec ipfs_container ipfs name publish /ipfs/<Root directory CID>/
```
С такой конфигурацией все около 10 Гб файлов сайта добавляются в ipfs меньше чем за пару минут.
---
title: Ускорение выполнения команды ipfs add
date: 2025-04-06 14:25:00 +0100
draft: false
tags: [Работа, ipfs, ускорение]
---
В двух предыдущих постах я рассказал о том, [что такое ipfs]({{< relref "/blog/2025/ipfs" >}}) и [как развернуть сайт в ipfs]({{< relref "/blog/2025/hosting-static-web-site-on-ipfs" >}}) и, помимо этого, для эксперимента настроил раздачу своего блога через ipfs: [ipfs.romka.eu](https://ipfs.romka.eu). 

Сайт обслуживается дешёвой виртуальной машиной, а, как оказалось, ipfs довольно прожорлив до ресурсов процессора, особенно при выполнении команды `ipfs add`. Несколько раз хостер просто молча прибивал мою виртуалку из-за превышения ею каких-то лимитов.

В моём случае ipfs работает в докер-контейнере, который запускается через `docker compose`. Поэтому я сконфигурировал запуск контейнера следующим образом, чтобы сильно ограничить потребляемые ресурсы:
```
  ipfs:
    image: ipfs/kubo:latest
    container_name: ipfs_container
    volumes:
      - /home/romka/ipfs:/data/ipfs
      - /var/www/romka.eu/public:/data/ipfs/public:ro
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

После нескольких подходов к решению проблемы, среди которых были эксперименты с флагом `--only-hash`, MFS и другие, максимально простым и надёжным решением оказалось просто останавливать ipfs демон на время добавления файлов. Однако есть один нюанс. С конфигурацией выше, а именно из-за строки `command: daemon --enable-gc --migrate=true --enable-pubsub-experiment`, ipfs становится init-процессом (PID 1) внутри контейнера, поэтому при его остановке докер считает, что контейнер завершился, и из-за `restart: always` тут же перезапускает его. 

При этом с одной стороны мне важно чтобы контейнер автоматически рестартился если ipfs daemon падает, с другой стороны -- мне нужна возможность иногда останавливать ipfs для того чтобы добавлять файлы. Я пробовал переписать конфиг так, чтобы использовался стандартный Докер-образ `ipfs/kubo:latest`, но внутри контейнера запускался кастомный init-процесс, управляющий ipfs демоном. Однако в такой конфигурации мне не удалось сделать так, чтобы и была возможность временно остановить ipfs, и контейнер рестартился в случае падения по OOM.

В итоге пришлось собрать [кастомный образ](/ipfs-s6-supervise/), в котором супервизор [s6-supervise](https://skarnet.org/software/s6/s6-supervise.html) управляет ipfs демоном. Вот мой `Dockerfile`:
```
FROM ipfs/kubo:latest AS kubo
FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    s6 \
    curl \
    ca-certificates && \
    rm -rf /var/lib/apt/lists/*

COPY --from=kubo /usr/local/bin/ipfs /usr/local/bin/ipfs

RUN mkdir -p /etc/s6/ipfs
COPY ./run-ipfs-daemon.sh /etc/s6/ipfs/run
RUN chmod +x /etc/s6/ipfs/run

ENTRYPOINT ["/usr/bin/s6-svscan", "/etc/s6"]
```
В этом образе выполняются следующие действия:
- берётся последний LTS-релиз Ubuntu, 
- в него копируется последний доступный релиз `kubo` (это официальная реализация протокола ipfs), 
- устанавливается супервизор `s6`, 
- для этого супервизора написан скрипт `run-ipfs-daemon.sh`, запускающий ipfs daemon:
```
#!/bin/sh
exec ipfs daemon --enable-gc --migrate=true --enable-pubsub-experiment
```
Чтобы начать использовать этот образ, его нужно собрать. Для этого в директории где лежат указанные выше `Dockerfile` и `run-ipfs-daemon.sh` нужно выполнить следующую команду:
```
docker build -t ipfs-s6-supervise .
```
Здесь `ipfs-s6-supervise` это имя нового образа, которое можно будет использовать для запуска контейнера.

Когда образ собран его нужно прописать в `docker-compose.yaml` вместо `ipfs/kubo:latest`. Помимо этого пришлось немного подправить пути куда монтируются директории внутри контейнера:
```
  ipfs:
    image: ipfs-s6-supervise
    container_name: ipfs_container
    volumes:
      - /home/romka/ipfs:/root/.ipfs
      - /var/www/romka.eu/public:/root/.ipfs/public:ro
    <...>
    restart: always
    # Следующая строка больше не нужна, так как эта команда переехала в run-ipfs-daemon.sh
    # command: daemon --enable-gc --migrate=true --enable-pubsub-experiment
    cpus: 0.3
    mem_limit: 256m
    memswap_limit: 256m
    environment:
      GOMAXPROCS: 1
```

Теперь процедура публикации сайта в ipfs выглядит так:
```
docker exec ipfs_container s6-svc -d /etc/s6/ipfs
docker exec ipfs_container ipfs add -r --nocopy /root/.ipfs/public
docker exec ipfs_container s6-svc -u /etc/s6/ipfs
docker exec ipfs_container ipfs name publish /ipfs/<Root directory CID>/
```
С такой конфигурацией все около 10 Гб файлов сайта добавляются в ipfs меньше чем за пару минут.
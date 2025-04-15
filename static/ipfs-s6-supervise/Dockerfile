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

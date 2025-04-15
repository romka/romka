#!/bin/sh
exec ipfs daemon --enable-gc --migrate=true --enable-pubsub-experiment

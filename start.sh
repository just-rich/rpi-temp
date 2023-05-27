#!/bin/bash

trap "kill 0" EXIT

python3 temp.py &
python3 server.py &

wait

#!/bin/bash
./state-server 2>&1 > /dev/null &
sleep 3
./endpoint-server
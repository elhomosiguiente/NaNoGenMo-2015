#!/bin/bash

for i in $(seq 1 8334); do
    printf "## Story %'d" $i
    echo ""
    python randomsentencebot.py --hashtags None -x --quiet
    echo ""
    echo ""
done

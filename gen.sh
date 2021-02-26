#!/bin/bash
for i in a b c d e f; do python main.py <$i.txt >$i-output.txt; done

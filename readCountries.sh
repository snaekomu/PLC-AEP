#!/bin/bash

ls -1 $1 | awk '{print $1"	"$3}' | sed 's/\.txt//g' > countries.txt
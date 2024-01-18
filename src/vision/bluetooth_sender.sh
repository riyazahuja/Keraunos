#!/bin/bash

FILE_DIR="test.json"

BLUETOOTH_ADDR="5C:E9:1E:90:AA:3C"

blueman-sendto --device=$BLUETOOTH_ADDR $FILE_DIR

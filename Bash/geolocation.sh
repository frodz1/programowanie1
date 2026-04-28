#!/bin/bash

image=$1

exiftool $image | grep GPS

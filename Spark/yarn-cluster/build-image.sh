#!/bin/bash

echo ""

echo -e "\nbuild docker hadoop & spark image\n"
docker build -t spark-hadoop:latest .

echo ""

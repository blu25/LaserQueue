#!/bin/bash
cd ${0%/*}

cd backend
python3 initialize.py $*
./start.sh $*

#!/bin/bash
echo "BUILD START"
python3 -m pip install -r requirements.txt
python3 manage.py collectstatic --noinput --clear
mkdir -p staticfiles
echo "BUILD END"

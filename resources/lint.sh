#!/bin/bash

RESULT=lintResult

echo "== Clearing previous lint results"
rm $RESULT
cur_dir=$(pwd)

echo "== Checking location (!) Should be launched on resources folder (!)"
if [[ $cur_dir != *"resources"* ]]; then
    echo "== ERROR: Should be launched on resources/";
fi

echo "== Trying linting from pylint command"
find ../ -name *.py -exec bash -c "pylint --rcfile pylint.cfg {}" \; > $RESULT

if [ ! -f $RESULT ]; then
    echo "== pylint not found, trying with python -m pylint"
    find ../ -name *.py -exec bash -c "python -m pylint --rcfile pylint.cfg {}" \; > $RESULT
fi

if [ ! -f $RESULT ]; then
    echo "== ERROR: pylint not found"
    echo "== Install pylint -> 'pip install pylint' for pylint only"
    echo "== OR 'pip install -r requirements.txt' for all project dependencies"
fi

#!/bin/bash
cd `dirname $0`
source bin/activate
python gmail-plotly.py "${@:1}"

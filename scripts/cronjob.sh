#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

source $DIR/../winenv/bin/activate
source $DIR/env_setup.sh
python $DIR/../manage.py cronjob

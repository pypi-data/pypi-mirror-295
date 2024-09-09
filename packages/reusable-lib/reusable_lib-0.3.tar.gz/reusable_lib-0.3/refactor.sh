#!/bin/bash

yapf --style google -i src/reusable_lib/*.py

pip freeze > requirements.txt

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# it fails in an old python
#pylint --rcfile="$SCRIPT_DIR/pylintrc" --output=fix_python.txt ./*.py

pylint --rcfile="$SCRIPT_DIR/pylintrc" src/reusable_lib/*.py |tee ./fix_python.txt

shellcheck ./*.sh |tee ./fix_bash.txt

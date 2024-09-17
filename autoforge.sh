#!/usr/bin/bash

dir="$(dirname "$0")"

if [ ! -r "$dir/autoforge.py" ]; then
  echo "Couldn't find autoforge.py! Please visit https://github.com/Yoghurt4C/autoforge to download it."
  exit 1
fi

if [ ! -d "$dir/bin" ]; then
  if ! hash python3; then
    echo "Python is not installed. Please install Python 3 (at least 3.4)."
    exit 1
  fi

  pyV=($(python -c 'import sys; ver = sys.version_info; print(" ".join(str(v) for v in ver[:]))')) || die-with-error

  if [ "${pyV[0]}" -eq 3 ] && [ "${pyV[1]}" -ge 4 ]; then
    echo "Creating a Python venv inside $dir"
    command python -m venv "$dir"
  fi

fi

if [ -d "$dir/bin" ] && [ -r "$dir/bin/activate" ]; then
  source "$dir/bin/activate"
  if command -v python &> /dev/null; then
    echo "Using the Python venv inside $dir"
    command python -V
    mPynput=$(command pip freeze | grep "pynput")
    if [ "$mPynput" = "" ]; then
      echo "Couldn't find pynput in the venv. Attempting to install with pip..."
      command pip install pynput
    else
      echo "${mPynput//==/ }"
    fi

    echo "Starting Autoforge!"
    if command python "$dir/autoforge.py" == 0; then
      echo "Autoforge stopped successfully."
    else
      echo "Autoforge crashed!"
    fi
    exit 0
  else
    echo "There is no Python venv inside $dir."
  fi
fi
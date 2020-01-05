#!/bin/bash

cd "$(dirname "$0")"

declare -a PIP_OPTS=()
if [[ "$1" == "--no-pyenv" ]]; then
	if ! which pyenv >/dev/null; then
		echo 'Install pyenv first:'
		echo '$ curl https://pyenv.run | bash'
		echo
		echo 'OR, if you are installing on an embedded system, you can skip using pyenv:'
		echo '$ ./bootstrap.sh --no-pyenv'
		exit 1
	fi

	pyenv install --skip-existing "$(cat .python-version)"
else
	PIP_OPTS=("--user")
fi

pip install "${PIP_OPTS[@]}" -r requirements.txt

garden install --app iconfonts
garden install --app mapview

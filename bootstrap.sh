#!/bin/bash

if ! which pyenv >/dev/null; then
	echo 'Install pyenv first:'
	echo '$ curl https://pyenv.run | bash'
	exit 1
fi

cd "$(dirname "$0")"

pyenv install --skip-existing "$(cat .python-version)"

pip install -r requirements.txt

garden install --app iconfonts
garden install --app mapview

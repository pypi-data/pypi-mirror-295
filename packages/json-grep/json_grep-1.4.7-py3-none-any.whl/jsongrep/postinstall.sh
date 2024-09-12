#!/bin/bash

echo "*** Activating bash completion for jgrep, jsongrep, and json-grep ***"

activate-global-python-argcomplete --user --yes
eval $(register-python-argcomplete jgrep)
eval $(register-python-argcomplete jsongrep)
eval $(register-python-argcomplete json-grep)

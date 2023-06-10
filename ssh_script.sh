#!/usr/bin/env bash

GITHUB_EMAIL=$1

printf "Generating SSH key..."
ssh-keygen -q -t rsa -N '' -b 4096 -f "$HOME"/.ssh/id_rsa -C "$GITHUB_EMAIL"
printf "Generated"

printf "\n\n"

printf "Starting SSH agent..."
eval "$(ssh-agent -s)" >/dev/null 2>&1
printf "Started"

printf "\n\n"

printf "Adding private SSH key to SSH agent..."
ssh-add -k "$HOME/.ssh/id_rsa"
printf "Added"

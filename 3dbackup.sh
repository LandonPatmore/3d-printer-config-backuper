#!/usr/bin/env bash

#==============================================================================
# title           : 3dbackup.sh
# description     : Gets all of the necessary information to setup your raspberry pi to auto backup your printer config files.
# author		      : LandonPatmore
# version         : 0.1
# usage		        : ./3dbackup.sh
# license         : MIT
#==============================================================================

PERSONAL_TOKEN=""
GITHUB_USERNAME=""
GITHUB_EMAIL=""
GITHUB_NAME=""
PRIVATE_REPO=""
PRINTER_CONFIG_PATH=""
RASPBERRY_PI_USERNAME=""
RASPBERRY_PI_IP=""
RASPBERRY_PI_SCRIPT_NAME="rpi_3d_printer_config_backuper.sh"
CRON_CONFIG=""

function prompt_yes_no() {
  INPUT=$1
  ALT=$2

  if [ "$ALT" ]; then PROMPT="$ALT"; else PROMPT="You typed ($INPUT)."; fi

  while true; do
    printf "\n"
    read -rp "$PROMPT
    Is this the correct? (y/n)" YN

    case $YN in
    [Yy]*) break ;;
    [Nn]*) exit ;;
    *) echo "Please type y or n." ;;
    esac
  done
}

read -rp "
Click the following link and sign in/up if necessary.
Link: https://github.com/settings/tokens/new

PLEASE READ THE FOLLOWING AS THIS MUST BE FOLLOWED EXACTLY OR THIS SCRIPT WILL NOT WORK:
1. In the 'Note' section, please put a note that will remind you of what this personal token is for. It can be anything
2. Set the expiration to '7 days'
3. Select the 'admin:public_key' option (it selects all the child boxes as well)
4. Click 'Generate token'
5. Copy the token that is generated (you must copy it now since it will not be shown again)

Enter personal token: " PERSONAL_TOKEN

prompt_yes_no "$PERSONAL_TOKEN"

printf "
Click the following link to find the information needed.
Link: https://github.com/settings/profile
"

read -rp "
Enter your Github username (the one you used to sign up with, it is within the () at the top left)

Name: " GITHUB_USERNAME

prompt_yes_no "$GITHUB_USERNAME"

read -rp "
Enter your Github email (the one you used to sign up with)

Email: " GITHUB_EMAIL

prompt_yes_no "$GITHUB_EMAIL"

read -rp "
Enter your Github name (the one you used to sign up with, it is within the 'Name' field on your profile)

Name: " GITHUB_NAME

prompt_yes_no "$GITHUB_NAME"

read -rp "
Enter the name of your repository

Repo name: " REPO_NAME

prompt_yes_no "$REPO_NAME"

read -rp "
Wwe will setup the repository your config files will live in.

There are two options:

1. Private - No one can see your printer config files except you and those you explicitly share them with
2. Public - Anyone on the internet can find and view your repository

Which would you like to create?

Type 1 for 'Private' or 2 for 'Public': " PRIVATE_REPO

prompt_yes_no "$PRIVATE_REPO"

if [ "$PRIVATE_REPO" == "1" ]; then PRIVATE_REPO="true"; else PRIVATE_REPO="false"; fi

read -rp "
Enter the path of your printer config folder. Example: /home/bob/printer/printer_config

Path: " PRINTER_CONFIG_PATH

prompt_yes_no "$PRINTER_CONFIG_PATH"

read -rp "
Enter the username of your raspberry pi

Username: " RASPBERRY_PI_USERNAME

prompt_yes_no "$RASPBERRY_PI_USERNAME"

read -rp "
Enter the IP address of your raspberry pi

IP: " RASPBERRY_PI_IP

prompt_yes_no "$RASPBERRY_PI_IP"

read -rp "
Click the following link to generate a crontab configuration. This will schedule an auto commit to happen at a certain
time interval to back up your printer config.

Link: https://crontab-generator.org/

Please make sure to copy it EXACTLY how it is, or your autocommits will not work properly.


Cron tab config: " CRON_CONFIG

prompt_yes_no "$CRON_CONFIG"

prompt_yes_no "" "
Please take a look at your settings one more time, things will be automated from here:

Personal token: $PERSONAL_TOKEN
Github name: $GITHUB_USERNAME
Github email: $GITHUB_EMAIL
Github name: $GITHUB_NAME
Repo name: $REPO_NAME
Is private repo?: $PRIVATE_REPO
Printer config path: $PRINTER_CONFIG_PATH
Raspberry pi ip address: $RASPBERRY_PI_IP
Raspberry pi username: $RASPBERRY_PI_USERNAME
Crontab config: $CRON_CONFIG
"

SCRIPT_PATH="/home/$RASPBERRY_PI_USERNAME/$RASPBERRY_PI_SCRIPT_NAME"

# SCP script file over

printf "Sending script to raspberry pi..."
scp "$RASPBERRY_PI_SCRIPT_NAME" landon@192.168.1.149:"$SCRIPT_PATH"
print "Sent"

# SSH in

printf "Executing script on raspberry pi..."
ssh -t "$RASPBERRY_PI_USERNAME"@"$RASPBERRY_PI_IP" "
  sudo chmod +x \"$SCRIPT_PATH\";
  sudo $SCRIPT_PATH \"$PERSONAL_TOKEN\" \"$GITHUB_USERNAME\" \"$GITHUB_EMAIL\" \"$GITHUB_NAME\" \"$PRIVATE_REPO\" \"$PRINTER_CONFIG_PATH\" \"$RASPBERRY_PI_USERNAME\" \"$CRON_CONFIG\"; \
  sudo rm \"$SCRIPT_PATH\"
"
printf "Done!"

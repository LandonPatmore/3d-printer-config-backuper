## 3dbakup

This utility will walk you through getting setup with Github to make sure you have a backup of your files in the
unfortunate event your machine breaks, or you spill coffee on it!

### How does it work?

You will run the `3dbackup.sh` file on your host machine (Windows, OSX, or Linux). This script is responsible for
getting all the required parameters required to automate the setup on the Raspberry pi.

There are no changes on the host machine whatsoever. Everything after the final prompt before the SCP
and SSH is done on the RPi. Nothing is saved on the host machine either.

Once all the parameters are gathered, the script will SCP into the RPi to place the second script file on it. It will
then use SSH to run the second script with all the parameters from the first script. (Unfortunately you
will have to enter your password twice in a row, I don't have a way around it besides setting up SSH keys between
the machines, but that is overkill for this script that will only be used once.)

It will also prompt and set up a cron job to auto backup your printer config files automatically.

And don't worry, there is a backup to your config files before anything is done to them and is saved in
the same directory that the printer config files are in for quick retrieval.

### License
```
MIT License

Copyright (c) 2023 Landon Patmore

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
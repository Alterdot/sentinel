#!/bin/bash
set -evx

mkdir ~/.alterdot

# safety check
if [ ! -f ~/.alterdot/.alterdot.conf ]; then
  cp share/alterdot.conf.example ~/.alterdot/alterdot.conf
fi

#!/bin/bash

APP_IMAGE="/app/extra/gssh-1.0.0.AppImage"

# Allow image to execute

chmod +x $APP_IMAGE

# Extract image

unappimage $APP_IMAGE

# Install data

DEST="/app/extra/bin/"
mkdir $DEST
cp -r squashfs-root/* $DEST


done

# Clean up
rm -rf squashfs-root/
rm $APP_IMAGE

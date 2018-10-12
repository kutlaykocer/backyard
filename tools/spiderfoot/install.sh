#!/bin/bash

FILENAME=spiderfoot-2.12.0-src.tar.gz
CHECKSUM=cd2befa8a7cb0fa2f26378f430081f55b1b1eb0c

echo "Downloading $FILENAME ..."
curl "https://www.spiderfoot.net/files/$FILENAME" --output "$FILENAME"
 
CHECK_OK=$(echo "$CHECKSUM $FILENAME" |  sha1sum -c -)

if [[ "$CHECK_OK" != *": OK" ]]
then
    echo "Error: checksum of spiderfoot incorrect: $CHECK_OK"
    exit 1
else
    echo Checksum verified!
fi

echo Extracting file ...
mkdir -p spiderfoot
tar -zxvf "$FILENAME" -C spiderfoot --strip-components=1


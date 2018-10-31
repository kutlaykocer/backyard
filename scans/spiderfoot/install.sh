#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
FILENAME=spiderfoot-2.12.0-src.tar.gz
CHECKSUM=cd2befa8a7cb0fa2f26378f430081f55b1b1eb0c

echo "Downloading $FILENAME ..."
curl "https://www.spiderfoot.net/files/$FILENAME" --output "$DIR/$FILENAME"

CHECK_OK=$(echo "$CHECKSUM $DIR/$FILENAME" |  sha1sum -c -)

if [[ "$CHECK_OK" != *": OK" ]]
then
    echo "Error: checksum of spiderfoot incorrect: $CHECK_OK"
    exit 1
else
    echo Checksum verified!
fi

echo Extracting file ...
mkdir -p "$DIR"/download
tar -zxvf "$DIR/$FILENAME" -C "$DIR"/download --strip-components=1
rm "$DIR/$FILENAME"

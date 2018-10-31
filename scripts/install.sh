#!/bin/bash

echo "Download software and additional images ..."


DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"

echo "Download spiderfoot ..."
"$DIR"/../scans/spiderfoot/install.sh

echo "Pull NATS ..."
docker pull nats:1.3.0

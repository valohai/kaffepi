#!/bin/sh
[ -z "$URL" ] && echo "URL is required" && exit 1
[ -z "$NODE" ] && echo "NODE is required" && exit 1
set -e
MEASUREMENTS=$(./temper-raspbian | jq -r '[.[0].sensors[] | "temp" + (.id | tostring) + "=" + (.value | tostring)] | join("&")')
curl -XPOST "$URL?node=$NODE&$MEASUREMENTS"
#!/bin/bash

set -e

cd /app

python3 main.py

mega-login "$MEGA_USERNAME" "$MEGA_PASSWORD"



while IFS= read -r line
do
    file=$(echo $line | cut -f1 -d";")
    comment=$(echo $line | cut -f2 -d";")

    mega-put "./$file" nnys2021clips
    link=`mega-export -a nnys2021clips/$file`
    python3 reply.py "$comment" "$link"
done < "replies.txt"

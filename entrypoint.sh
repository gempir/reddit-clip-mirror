#!/bin/bash

set -e

cd /app

bash

python3 main.py

mega-login "$MEGA_USERNAME" "$MEGA_PASSWORD"

while IFS= read -r line
do
    file=$(echo $line | cut -f1 -d";")
    comment=$(echo $line | cut -f2 -d";")

    mega-put -v "./$file" nnys2021clips/clips
    link=`mega-export -a "nnys2021clips/$file" | awk '{print $4}`
    python3 reply.py "$comment" "$link"
done < "replies.txt"

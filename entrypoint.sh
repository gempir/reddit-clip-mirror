#!/bin/bash

set -e

cd /app

bash

python3 main.py

mega-login "$MEGA_USERNAME" "$MEGA_PASSWORD"

cat replies.txt

while IFS= read -r line
do
    file=$(echo $line | cut -f1 -d";")
    comment=$(echo $line | cut -f2 -d";")

    mega-put -v "$file" nnys2021clips/clips
    link=`mega-export -a "nnys2021clips/$file" | rev | cut -d ' ' -f 1 | rev`
    python3 reply.py "$comment" "${link#'https://'}"
done < "replies.txt"

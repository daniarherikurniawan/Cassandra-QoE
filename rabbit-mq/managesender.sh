#!/bin/bash
cp sender.py temp_sender.py
sed -i "s/PACKETLENGTH/$1/g" temp_sender.py
sed -i "s/MSGNUM/$2/g" temp_sender.py
python3 temp_sender.py
rm temp_sender.py

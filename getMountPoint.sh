#!/bin/bash
mountStatus=$( df -kh | grep /dev/mmcblk1p1 )
if [ $? -eq 0 ]
then
        read  -a mountOutput <<< $mountStatus
        echo "${mountOutput[-1]}"
        exit 0
else
        exit 1
fi

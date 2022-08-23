#!/usr/bin/expect -f
set user sun
set host 192.168.50.132
set port 22
set timeout 30
set password 19970130SWh
spawn ssh -p $port $user@$host
expect "password:*"
send "$password\r"
interact
#expect eof

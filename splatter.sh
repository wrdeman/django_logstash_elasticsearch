#!/bin/bash

# get cookies
curl -c cookies.txt -XGET http://localhost:8001/auth/login/ 2>&1

# get csrftoken
CSRF=$(cat cookies.txt | grep csrftoken | awk -F" " '{print $7}')

# login
curl -i --cookie cookies.txt -H "X-CSRFToken:"$CSRF"" -H"Content-Type: application/x-www-form-urlencoded" -X POST -d "username="$UNAME -d "password="$PWORD http://localhost:8001/auth/login/ -c new_cookies.txt

CSRF=$(cat new_cookies.txt | grep csrftoken | awk -F" " '{print $7}')
SESSION=$(cat new_cookies.txt | grep session | awk -F" " '{print $7}')

ab -n 50000000 -c 10 -C "sessionid=$SESSION;csrftoken=$CSRF" -H "X-CSRFToken:$CSRF" -T"Content-Type: application/json" -mPOST http://localhost:8001/accounts/withdraw/
curl -i --cookie cookies.txt -X GET http://localhost:8001/accounts/withdraw/ 
rm cookies.txt
rm new_cookies.txt

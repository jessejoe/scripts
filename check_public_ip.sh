#!/bin/bash
EXPECTED_IP="X.X.X.X"
CURRENT_IP=$(curl -s http://api.ipify.org)
if [ "$EXPECTED_IP" != "$CURRENT_IP" ]
then
    printf "Expected IP: $EXPECTED_IP\nNew IP: $CURRENT_IP\nMimir whitelists will probably not work!" | mail -s "Home IP changed!" foo@bar.com
fi

#!/bin/bash

TV_IP="192.168.1.150"
TV_PORT="7142"

tv_on() {
    echo "Turning TV ON..."
    # Correct NEC power ON command: SOH-0-A-0-A-0-C-STX-C-2-0-3-D-6-0-0-0-1-ETX-BCC-CR
    response=$((echo -ne '\x01\x30\x41\x30\x41\x30\x43\x02\x43\x32\x30\x33\x44\x36\x30\x30\x30\x31\x03\x73\x0D'; sleep 1) | nc $TV_IP $TV_PORT | xxd -p)
    if [[ -n "$response" ]]; then
        echo "✅ Power ON command sent - TV responded: $response"
    else
        echo "✅ Power ON command sent"
    fi
}

tv_off() {
    echo "Turning TV OFF..."
    # Correct NEC power OFF command: SOH-0-A-0-A-0-C-STX-C-2-0-3-D-6-0-0-0-4-ETX-BCC-CR
    response=$((echo -ne '\x01\x30\x41\x30\x41\x30\x43\x02\x43\x32\x30\x33\x44\x36\x30\x30\x30\x34\x03\x76\x0D'; sleep 1) | nc $TV_IP $TV_PORT | xxd -p)
    if [[ -n "$response" ]]; then
        echo "✅ Power OFF command sent - TV responded: $response"
    else
        echo "✅ Power OFF command sent"
    fi
}

case "$1" in
    on)
        tv_on
        ;;
    off)
        tv_off
        ;;
    test)
        echo "Testing TV control..."
        tv_on
        echo "Waiting 5 seconds..."
        sleep 5
        tv_off
        ;;
    *)
        echo "Usage: $0 {on|off|test}"
        echo "  on   - Turn TV on"
        echo "  off  - Turn TV off" 
        echo "  test - Turn on, wait 5s, turn off"
        exit 1
        ;;
esac

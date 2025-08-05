#!/usr/bin/env python3
"""
Test script for NEC TV Control
"""

import socket
import sys

def test_tv_connection(ip, port):
    """Test connection to NEC TV"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect((ip, port))
        sock.close()
        print(f"✓ Successfully connected to TV at {ip}:{port}")
        return True
    except Exception as e:
        print(f"✗ Failed to connect to TV at {ip}:{port}: {e}")
        return False

def test_power_commands(ip, port):
    """Test power commands"""
    commands = {
        'power_on': b'\x01\x30\x41\x30\x41\x30\x43\x02\x43\x32\x30\x33\x44\x36\x30\x30\x30\x31\x03\x73\x0D',
        'power_off': b'\x01\x30\x41\x30\x41\x30\x43\x02\x43\x32\x30\x33\x44\x36\x30\x30\x30\x34\x03\x76\x0D'
    }
    
    for name, command in commands.items():
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.connect((ip, port))
            sock.send(command)
            sock.close()
            print(f"✓ Successfully sent {name} command")
        except Exception as e:
            print(f"✗ Failed to send {name} command: {e}")

def main():
    """Main test function"""
    if len(sys.argv) != 3:
        print("Usage: python3 test_nec_tv.py <tv_ip> <tv_port>")
        print("Example: python3 test_nec_tv.py 192.168.1.150 7142")
        sys.exit(1)
    
    ip = sys.argv[1]
    port = int(sys.argv[2])
    
    print(f"Testing NEC TV Control for {ip}:{port}")
    print("=" * 50)
    
    # Test connection
    if test_tv_connection(ip, port):
        # Test commands
        test_power_commands(ip, port)
    else:
        print("Skipping command tests due to connection failure")
    
    print("=" * 50)
    print("Test completed")

if __name__ == '__main__':
    main() 
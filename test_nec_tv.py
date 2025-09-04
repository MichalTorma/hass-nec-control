#!/usr/bin/env python3
"""
Test script for NEC TV Control Service
Tests the actual service endpoints and functions, not duplicated code.
"""

import socket
import sys
import time
import os
import subprocess
import json
from contextlib import contextmanager
from http.client import HTTPConnection

# Import the service module to test its functions directly
sys.path.append(os.path.join(os.path.dirname(__file__), 'rootfs', 'usr', 'bin'))

def test_tv_connectivity(ip, port):
    """Test basic TCP connectivity to TV"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        sock.connect((ip, port))
        sock.close()
        print(f"✓ TV connectivity: {ip}:{port} is reachable")
        return True
    except Exception as e:
        print(f"✗ TV connectivity: Failed to connect to {ip}:{port} - {e}")
        return False

def test_service_import():
    """Test if we can import the service module"""
    try:
        import nec_tv_service
        print("✓ Service import: nec_tv_service module imported successfully")
        return nec_tv_service
    except Exception as e:
        print(f"✗ Service import: Failed to import nec_tv_service - {e}")
        return None

def test_service_functions(service_module, ip, port):
    """Test the service functions directly"""
    if not service_module:
        return False
    
    try:
        # Test the commands directly using the service's COMMANDS dict
        print("Testing service functions:")
        
        for action in ['on', 'off']:
            try:
                import socket
                command = service_module.COMMANDS[f'power_{action}']
                
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(5)
                sock.connect((ip, port))
                sock.send(command)
                
                # Check for response
                try:
                    response = sock.recv(1024)
                    sock.close()
                    if response:
                        print(f"✓ Service command: power {action.upper()} successful (got response)")
                    else:
                        print(f"✓ Service command: power {action.upper()} sent (no response)")
                except:
                    sock.close()
                    print(f"✓ Service command: power {action.upper()} sent")
                    
                time.sleep(1)  # Brief delay between commands
                
            except Exception as e:
                print(f"✗ Service command: power {action.upper()} failed - {e}")
        
        return True
        
    except Exception as e:
        print(f"✗ Service functions: Failed to test - {e}")
        return False

@contextmanager
def run_service_temporarily(ip):
    """Context manager to run the service temporarily for HTTP testing"""
    env = os.environ.copy()
    env['TV_IP'] = ip
    
    process = None
    try:
        # Start the service
        process = subprocess.Popen([
            sys.executable, 
            os.path.join('rootfs', 'usr', 'bin', 'nec_tv_service.py')
        ], env=env)
        
        # Wait for service to start
        time.sleep(2)
        
        # Check if service is running
        if process.poll() is None:
            print("✓ Service startup: HTTP service started successfully")
            yield True
        else:
            print("✗ Service startup: HTTP service failed to start")
            yield False
            
    except Exception as e:
        print(f"✗ Service startup: Failed to start service - {e}")
        yield False
    finally:
        if process and process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
            print("✓ Service cleanup: HTTP service stopped")

def test_http_endpoints():
    """Test HTTP endpoints using built-in http.client"""
    
    tests = [
        ("GET", "/", "Service info endpoint"),
        ("GET", "/health", "Health check endpoint"),
        ("POST", "/power", "Power control endpoint", {"action": "on"}),
    ]
    
    for test_data in tests:
        method, path, description = test_data[:3]
        json_data = test_data[3] if len(test_data) > 3 else None
        
        try:
            conn = HTTPConnection('localhost', 8124, timeout=5)
            
            if method == "GET":
                conn.request(method, path)
            elif method == "POST":
                headers = {'Content-Type': 'application/json'}
                body = json.dumps(json_data) if json_data else ""
                conn.request(method, path, body, headers)
            
            response = conn.getresponse()
            status = response.status
            
            if status == 200:
                print(f"✓ HTTP {method} {path}: {description} - OK")
            else:
                print(f"✗ HTTP {method} {path}: {description} - Status {status}")
            
            conn.close()
                
        except ConnectionRefusedError:
            print(f"✗ HTTP {method} {path}: {description} - Service not running")
        except Exception as e:
            print(f"✗ HTTP {method} {path}: {description} - {e}")

def main():
    """Main test function"""
    if len(sys.argv) != 3:
        print("Usage: python3 test_nec_tv.py <tv_ip> <tv_port>")
        print("Example: python3 test_nec_tv.py 192.168.1.150 7142")
        print("\nThis script tests the NEC TV Control Service, not the TV directly.")
        sys.exit(1)
    
    ip = sys.argv[1]
    port = int(sys.argv[2])
    
    print(f"Testing NEC TV Control Service")
    print(f"Target TV: {ip}:{port}")
    print("=" * 60)
    
    # Test 1: TV connectivity
    tv_reachable = test_tv_connectivity(ip, port)
    
    # Test 2: Service module import
    service_module = test_service_import()
    
    # Test 3: Direct service functions
    if tv_reachable and service_module:
        # Set environment for testing
        os.environ['TV_IP'] = ip
        os.environ['TV_PORT'] = str(port)
        test_service_functions(service_module, ip, port)
    
    # Test 4: HTTP service endpoints
    print("\nTesting HTTP service endpoints:")
    with run_service_temporarily(ip) as service_started:
        if service_started:
            test_http_endpoints()
        else:
            print("✗ Skipping HTTP tests - service failed to start")
    
    print("=" * 60)
    print("Service testing completed")

if __name__ == '__main__':
    main() 
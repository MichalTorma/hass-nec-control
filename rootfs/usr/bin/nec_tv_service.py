#!/usr/bin/env python3
"""
NEC TV Control Service for Home Assistant
"""

import os
import socket
import time
import json
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
TV_IP = os.environ.get('TV_IP', '192.168.1.150')
TV_PORT = int(os.environ.get('TV_PORT', 7142))

# NEC TV Commands (hex format)
COMMANDS = {
    'power_on': b'\x01\x30\x41\x30\x41\x30\x43\x02\x43\x32\x30\x33\x44\x36\x30\x30\x30\x31\x03\x73\x0D',
    'power_off': b'\x01\x30\x41\x30\x41\x30\x43\x02\x43\x32\x30\x33\x44\x36\x30\x30\x30\x34\x03\x76\x0D'
}

class NECTVHandler(BaseHTTPRequestHandler):
    """HTTP request handler for NEC TV control"""
    
    def do_GET(self):
        """Handle GET requests for device discovery"""
        parsed_url = urlparse(self.path)
        
        if parsed_url.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            response = {
                'name': 'NEC TV Control',
                'version': '1.0.0',
                'tv_ip': TV_IP,
                'tv_port': TV_PORT
            }
            self.wfile.write(json.dumps(response).encode())
            
        elif parsed_url.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            response = {
                'status': 'healthy',
                'service': 'NEC TV Control',
                'version': '1.0.0'
            }
            self.wfile.write(json.dumps(response).encode())
            
        elif parsed_url.path == '/discovery':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            # Return Home Assistant device discovery info
            discovery_info = {
                'devices': [{
                    'identifiers': [f'nec_tv_{TV_IP}'],
                    'name': 'NEC TV',
                    'manufacturer': 'NEC',
                    'model': 'Network TV',
                    'sw_version': '1.0.0'
                }],
                'entities': [
                    {
                        'entity_id': 'switch.nec_tv_power',
                        'name': 'NEC TV Power',
                        'type': 'switch',
                        'device_class': 'switch',
                        'state_topic': 'nec_tv/state',
                        'command_topic': 'nec_tv/power/set'
                    }
                ]
            }
            self.wfile.write(json.dumps(discovery_info).encode())
            
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        """Handle POST requests for TV control"""
        parsed_url = urlparse(self.path)
        
        if parsed_url.path == '/power':
            if 'Content-Length' not in self.headers:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'Content-Length header required'}).encode())
                return
                
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode('utf-8'))
                action = data.get('action')
                
                if action in ['on', 'off']:
                    success = self.send_tv_command(action)
                    
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    
                    response = {
                        'success': success,
                        'action': action,
                        'message': f'TV power {action} command sent' if success else 'Failed to send command'
                    }
                    self.wfile.write(json.dumps(response).encode())
                else:
                    self.send_response(400)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'error': 'Invalid action'}).encode())
                    
            except json.JSONDecodeError:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'Invalid JSON'}).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def send_tv_command(self, action):
        """Send command to NEC TV"""
        try:
            command = COMMANDS[f'power_{action}']
            
            # Create socket connection
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)  # Increased timeout for better reliability
            
            # Connect to TV
            sock.connect((TV_IP, TV_PORT))
            
            # Send command
            sock.send(command)
            
            # Close connection
            sock.close()
            
            logger.info(f"Successfully sent {action} command to TV at {TV_IP}:{TV_PORT}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send {action} command to TV: {e}")
            return False
    
    def log_message(self, format, *args):
        """Override to use our logger"""
        logger.info(f"{self.address_string()} - {format % args}")

def main():
    """Main service function"""
    logger.info("Starting NEC TV Control Service")
    logger.info(f"TV IP: {TV_IP}")
    logger.info(f"TV Port: {TV_PORT}")
    
    # Start HTTP server
    server_address = ('', 8124)
    httpd = HTTPServer(server_address, NECTVHandler)
    
    logger.info("Server started on port 8124")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logger.info("Shutting down server")
        httpd.shutdown()

if __name__ == '__main__':
    main() 
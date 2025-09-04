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

# NEC TV Commands (hex format) - FIXED WORKING COMMANDS
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
                'version': '1.0.9',
                'tv_ip': TV_IP,
                'tv_port': TV_PORT
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
                    'sw_version': '1.0.9'
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
            
        elif parsed_url.path == '/homeassistant':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            # Return HTML page with YAML configuration
            yaml_config = f"""# NEC TV Control Integration
switch:
  - platform: rest
    name: "NEC TV Power"
    resource: "http://localhost:8124/power"
    body_on: '{{"action": "on"}}'
    body_off: '{{"action": "off"}}'
    headers:
      Content-Type: application/json
    # Note: TV state cannot be queried via network, so we use a default template
    is_on_template: "false"  # Always shows as off, but commands still work"""
            
            html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NEC TV Control - Home Assistant Setup</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #03a9f4;
            margin-bottom: 20px;
        }}
        .step {{
            background: #e3f2fd;
            padding: 15px;
            margin: 15px 0;
            border-radius: 5px;
            border-left: 4px solid #03a9f4;
        }}
        .yaml-block {{
            background: #263238;
            color: #eeffff;
            padding: 20px;
            border-radius: 5px;
            font-family: 'Courier New', monospace;
            white-space: pre-wrap;
            overflow-x: auto;
            margin: 15px 0;
            position: relative;
        }}
        .copy-btn {{
            position: absolute;
            top: 10px;
            right: 10px;
            background: #03a9f4;
            color: white;
            border: none;
            padding: 5px 10px;
            border-radius: 3px;
            cursor: pointer;
            font-size: 12px;
        }}
        .copy-btn:hover {{
            background: #0288d1;
        }}
        .success {{
            background: #e8f5e8;
            border-left-color: #4caf50;
            color: #2e7d32;
        }}
        .warning {{
            background: #fff3e0;
            border-left-color: #ff9800;
            color: #e65100;
        }}
        .info {{
            background: #e1f5fe;
            border-left-color: #00bcd4;
            color: #006064;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🎮 NEC TV Control - Home Assistant Setup</h1>
        
        <div class="step info">
            <strong>📋 Quick Setup Instructions:</strong><br>
            Copy the configuration below and add it to your Home Assistant configuration.yaml file.
        </div>
        
        <div class="step">
            <strong>1️⃣ Copy Configuration</strong><br>
            Click the "Copy" button below to copy the YAML configuration:
        </div>
        
        <div class="yaml-block" id="yaml-config">
            <button class="copy-btn" onclick="copyToClipboard()">Copy</button>{yaml_config}
        </div>
        
        <div class="step">
            <strong>2️⃣ Add to Home Assistant</strong><br>
            • Go to <strong>Settings</strong> → <strong>Files</strong> → <strong>configuration.yaml</strong><br>
            • Paste the configuration at the end of the file<br>
            • Click <strong>Save</strong>
        </div>
        
        <div class="step">
            <strong>3️⃣ Restart Home Assistant</strong><br>
            • Go to <strong>Settings</strong> → <strong>System</strong> → <strong>Restart</strong><br>
            • Click <strong>Restart</strong>
        </div>
        
        <div class="step success">
            <strong>✅ Done!</strong><br>
            After restart, you'll have a new switch called <strong>"NEC TV Power"</strong> that you can control from your dashboard.
        </div>
        
        <div class="step warning">
            <strong>⚠️ Important Notes:</strong><br>
            • Make sure the add-on is running (status should be "Running")<br>
            • The TV IP address is configured in the add-on settings<br>
            • If it doesn't work, check the add-on logs for errors
        </div>
        
        <div class="step info">
            <strong>🔧 Need Help?</strong><br>
            • Check add-on logs: Go to the add-on page and click "Logs"<br>
            • Test the API: Visit <a href="/health" target="_blank">http://localhost:8124/health</a><br>
            • Create an issue in the repository for bugs or questions
        </div>
    </div>
    
    <script>
        function copyToClipboard() {{
            const yamlText = document.getElementById('yaml-config').textContent.replace('Copy', '').trim();
            navigator.clipboard.writeText(yamlText).then(function() {{
                const btn = document.querySelector('.copy-btn');
                const originalText = btn.textContent;
                btn.textContent = 'Copied!';
                btn.style.background = '#4caf50';
                setTimeout(function() {{
                    btn.textContent = originalText;
                    btn.style.background = '#03a9f4';
                }}, 2000);
            }});
        }}
    </script>
</body>
</html>"""
            
            self.wfile.write(html_content.encode())
            
        elif parsed_url.path == '/power':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            # For now, we'll return a default state since we can't query the TV
            # In a real implementation, you might want to try to query the TV's actual state
            response = {
                'state': 'unknown',
                'message': 'TV state cannot be determined via network query',
                'note': 'This is a limitation of the NEC TV protocol - we can only send commands, not query state'
            }
            self.wfile.write(json.dumps(response).encode())
            
        elif parsed_url.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            response = {
                'status': 'healthy',
                'service': 'NEC TV Control',
                'version': '1.0.9'
            }
            self.wfile.write(json.dumps(response).encode())
            
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
            logger.info(f"Sending {action} command: {command.hex()}")
            
            # Create socket connection
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)  # Shorter timeout to match bash script behavior
            
            # Connect to TV
            logger.info(f"Connecting to TV at {TV_IP}:{TV_PORT}")
            sock.connect((TV_IP, TV_PORT))
            logger.info("Connected successfully")
            
            # Send command
            bytes_sent = sock.send(command)
            logger.info(f"Sent {bytes_sent} bytes")
            
            # Wait for response like the bash script does
            import time
            time.sleep(1)
            try:
                response = sock.recv(1024)
                if response:
                    logger.info(f"TV responded: {response.hex()}")
                else:
                    logger.warning("No response from TV")
            except socket.timeout:
                logger.info("No response from TV (timeout - this may be normal)")
            except Exception as resp_e:
                logger.warning(f"Error reading response: {resp_e}")
            
            # Close connection
            sock.close()
            logger.info("Connection closed")
            
            logger.info(f"Successfully sent {action} command to TV at {TV_IP}:{TV_PORT}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send {action} command to TV: {e}")
            import traceback
            logger.error(f"Full traceback: {traceback.format_exc()}")
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
    logger.info("Visit http://localhost:8124/homeassistant for setup instructions")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logger.info("Shutting down server")
        httpd.shutdown()

if __name__ == '__main__':
    main() 
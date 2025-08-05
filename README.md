# NEC TV Control Add-on

A Home Assistant add-on that allows you to control your NEC TV via network commands.

## Features

- Control NEC TV power on/off via network
- Configurable TV IP address and port
- REST API for integration with Home Assistant
- Automatic device discovery

## Configuration

### Add-on Configuration

| Option | Default | Description |
|--------|---------|-------------|
| `tv_ip` | `192.168.1.150` | IP address of your NEC TV |
| `tv_port` | `7142` | Network port for TV control (usually 7142) |

### Example Configuration

```yaml
tv_ip: "192.168.1.100"
tv_port: 7142
```

## Installation

1. Add this repository to your Home Assistant instance
2. Install the "NEC TV Control" add-on
3. Configure the TV IP address in the add-on configuration
4. Start the add-on

## Usage

### REST API

The add-on provides a REST API on port 8124:

#### Get Service Info
```bash
GET http://localhost:8123/
```

#### Get Device Discovery Info
```bash
GET http://localhost:8123/discovery
```

#### Control TV Power
```bash
POST http://localhost:8123/power
Content-Type: application/json

{
  "action": "on"  # or "off"
}
```

### Home Assistant Integration

The add-on automatically provides device discovery information that can be used to create entities in Home Assistant.

#### Manual Integration

You can also manually create a switch entity in your `configuration.yaml`:

```yaml
switch:
  - platform: rest
    name: "NEC TV Power"
    resource: "http://localhost:8124/power"
    body_on: '{"action": "on"}'
    body_off: '{"action": "off"}'
    is_on_template: "{{ value_json.success }}"
    headers:
      Content-Type: application/json
```

## Troubleshooting

### TV Not Responding

1. Verify the TV IP address is correct
2. Ensure the TV is on the same network
3. Check that port 7142 is not blocked by firewall
4. Verify the TV supports network control

### Add-on Won't Start

1. Check the add-on logs for error messages
2. Verify the configuration is valid
3. Ensure the TV IP address is reachable

## Technical Details

The add-on uses a Python service that communicates with NEC TVs using the network protocol to send binary commands:

- Power On: `\x01\x30\x41\x30\x41\x30\x43\x02\x43\x32\x30\x33\x44\x36\x30\x30\x30\x31\x03\x73\x0D`
- Power Off: `\x01\x30\x41\x30\x41\x30\x43\x02\x43\x32\x30\x33\x44\x36\x30\x30\x30\x34\x03\x76\x0D`

The service provides a REST API for easy integration with Home Assistant and handles all network communication, error handling, and logging.

## Support

For issues and feature requests, please create an issue in the repository.

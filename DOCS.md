# NEC TV Control Add-on Documentation

## Overview

The NEC TV Control add-on provides network-based control for NEC TVs that support the NEC network protocol. This add-on allows you to integrate your NEC TV into your Home Assistant setup for automated control.

## Architecture

The add-on consists of several components:

1. **Python Service** (`nec_tv_service.py`): Main service that provides HTTP API and handles all TV communication
2. **Configuration**: YAML-based configuration system
3. **Docker Container**: Isolated environment for the add-on
4. **Service Management**: s6-overlay for proper service lifecycle management

## Network Protocol

The add-on communicates with NEC TVs using a proprietary binary protocol over TCP port 7142. The protocol uses specific hex commands:

- **Power On**: `01 30 41 30 41 30 43 02 43 32 30 33 44 36 30 30 30 31 03 73 0D`
- **Power Off**: `01 30 41 30 41 30 43 02 43 32 30 33 44 36 30 30 30 34 03 76 0D`

## API Endpoints

### GET /
Returns basic service information:
```json
{
  "name": "NEC TV Control",
  "version": "1.0.0",
  "tv_ip": "192.168.1.150",
  "tv_port": 7142
}
```

### GET /discovery
Returns Home Assistant device discovery information:
```json
{
  "devices": [{
    "identifiers": ["nec_tv_192.168.1.150"],
    "name": "NEC TV",
    "manufacturer": "NEC",
    "model": "Network TV",
    "sw_version": "1.0.0"
  }],
  "entities": [{
    "entity_id": "switch.nec_tv_power",
    "name": "NEC TV Power",
    "type": "switch",
    "device_class": "switch",
    "state_topic": "nec_tv/state",
    "command_topic": "nec_tv/power/set"
  }]
}
```

### POST /power
Controls TV power state:
```json
{
  "action": "on"  // or "off"
}
```

Response:
```json
{
  "success": true,
  "action": "on",
  "message": "TV power on command sent"
}
```

## Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `tv_ip` | string | `192.168.1.150` | IP address of the NEC TV |
| `tv_port` | integer | `7142` | Network port for TV control |

## Troubleshooting

### Common Issues

1. **Connection Refused**
   - Verify TV IP address is correct
   - Check if TV is powered on
   - Ensure TV supports network control

2. **Command Not Working**
   - Verify port 7142 is not blocked
   - Check TV network settings
   - Try manual command testing

3. **Add-on Won't Start**
   - Check configuration syntax
   - Verify all required files are present
   - Check add-on logs for errors

### Testing

Use the provided test script to verify connectivity:
```bash
python3 test_nec_tv.py 192.168.1.150 7142
```

### Logs

Check add-on logs for detailed error information:
```bash
ha addon logs hass-nec-control
```

## Development

### Building the Add-on

1. Clone the repository
2. Navigate to the add-on directory
3. Build the Docker image:
   ```bash
   docker build -t hass-nec-control .
   ```

### Testing Locally

1. Run the container:
   ```bash
   docker run -p 8124:8124 -e TV_IP=192.168.1.150 -e TV_PORT=7142 hass-nec-control
   ```

2. Test the API:
   ```bash
   curl http://localhost:8124/
   ```

## Security Considerations

- The add-on runs in a containerized environment
- Network access is limited to the specified TV IP and port
- No persistent data is stored
- All communication is over local network only

## Support

For technical support and feature requests, please create an issue in the repository with:
- Home Assistant version
- Add-on version
- TV model and firmware version
- Detailed error logs
- Steps to reproduce the issue

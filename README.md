# NEC TV Control Add-on

A Home Assistant add-on that allows you to control your NEC TV via network commands. Turn your TV on and off remotely through Home Assistant.

## 🚀 Quick Start

### 1. Install the Add-on

1. **Add this repository** to your Home Assistant instance:
   - Go to **Settings** → **Add-ons** → **Add-on Store**
   - Click the three dots (⋮) in the top right
   - Select **Repositories**
   - Add: `https://github.com/MichalTorma/ha-repository`
   - Click **Add**

2. **Install the add-on**:
   - Find **"NEC TV Control"** in the add-on store
   - Click **Install**
   - Configure your TV's IP address
   - Click **Start**

### 2. Integrate with Home Assistant

#### Option A: Automatic Setup (Recommended)

1. **Get the configuration**:
   - Open your browser and go to: `http://localhost:8124/homeassistant`
   - Copy the configuration shown on that page

2. **Add to Home Assistant**:
   - Go to **Settings** → **Files** → **configuration.yaml**
   - Add the copied configuration at the end of the file
   - Click **Save**

3. **Restart Home Assistant**:
   - Go to **Settings** → **System** → **Restart**
   - Click **Restart**

#### Option B: Manual Configuration

Add this to your `configuration.yaml`:

```yaml
# NEC TV Control Integration
switch:
  - platform: rest
    name: "NEC TV Power"
    resource: "http://localhost:8124/power"
    body_on: '{"action": "on"}'
    body_off: '{"action": "off"}'
    headers:
      Content-Type: application/json
```

Then restart Home Assistant.

### 3. Use Your TV Control

After restart, you'll have a new switch called **"NEC TV Power"** that you can:
- **Turn on/off** from your dashboard
- **Add to automations** and scripts
- **Control via voice** (if you have voice assistants)

## ⚙️ Configuration

### Add-on Settings

| Option | Default | Description |
|--------|---------|-------------|
| `tv_ip` | `192.168.1.150` | IP address of your NEC TV |
| `tv_port` | `7142` | Network port for TV control |

### Example Configuration

```yaml
tv_ip: "192.168.1.100"
tv_port: 7142
```

## 🔧 Troubleshooting

### TV Not Responding

1. **Check TV IP address** - Make sure it's correct in add-on settings
2. **Verify network connectivity** - Ensure TV is on the same network
3. **Check firewall** - Port 7142 should not be blocked
4. **Test TV compatibility** - Verify your TV supports network control

### Add-on Won't Start

1. **Check logs** - Go to add-on page and click **Logs**
2. **Verify configuration** - Make sure TV IP is correct
3. **Check network** - Ensure TV IP is reachable

### Integration Not Working

1. **Check add-on is running** - Should show "Running" status
2. **Verify port** - Default is 8124, check add-on logs
3. **Test API** - Visit `http://localhost:8124/health` in browser
4. **Check configuration.yaml** - Make sure syntax is correct

## 📋 Requirements

- **Home Assistant** 2023.8.0 or newer
- **Home Assistant OS** or **Supervised** installation
- **NEC TV** with network control capability
- **Network access** to your TV

## 🎯 Features

- ✅ **Power on/off control** via network commands
- ✅ **Configurable TV IP** and port settings
- ✅ **REST API** for easy integration
- ✅ **Automatic setup instructions** via web interface
- ✅ **Health monitoring** and status checking
- ✅ **Error handling** and logging

## 🏠 Home Assistant Configuration

Add this to your `configuration.yaml`:

```yaml
# NEC TV Control Switch with Real State Detection
switch:
  - platform: rest
    name: "NEC TV Power"
    resource: "http://localhost:8124/power"
    body_on: '{"action": "on"}'
    body_off: '{"action": "off"}'
    headers:
      Content-Type: application/json
    is_on_template: "{{ value_json.is_on }}"
```

After adding this configuration:
1. **Restart Home Assistant**
2. **Check for errors** in the logs
3. **Find your switch** in the Entities page as "NEC TV Power"

## 🔌 API Endpoints

The add-on provides these endpoints:

- **`GET /`** - Service information and status
- **`GET /health`** - Health check endpoint
- **`GET /power`** - Get current TV state (returns `{"state": "on/off", "is_on": true/false}`)
- **`POST /power`** - Control TV power (send `{"action": "on"}` or `{"action": "off"}`)

## 🆘 Support

- **Check logs** in the add-on page for detailed error messages
- **Visit setup page** at `http://localhost:8124/homeassistant` for configuration help
- **Create an issue** in the repository for bugs or feature requests

---

**Note**: This add-on communicates with your TV over your local network. Make sure your TV supports the NEC network protocol and is configured for network control.

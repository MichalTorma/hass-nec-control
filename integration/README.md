# NEC TV Control Integration

This is a custom Home Assistant integration for controlling NEC TVs via the NEC TV Control addon.

## Installation

### Method 1: HACS (Recommended)

1. Install [HACS](https://hacs.xyz/) if you haven't already
2. Go to HACS → Integrations
3. Click the "+" button
4. Search for "NEC TV Control"
5. Click "Download"
6. Restart Home Assistant

### Method 2: Manual Installation

1. Download this integration folder
2. Copy the `nec_tv` folder to your `config/custom_components/` directory
3. Restart Home Assistant

## Setup

1. Go to **Settings** → **Devices & Services** → **Integrations**
2. Click **"Add Integration"**
3. Search for **"NEC TV Control"**
4. Configure the connection:
   - **Name**: Any name you want
   - **Host**: `localhost` (or your addon host)
   - **Port**: `8124` (default addon port)
5. Click **"Submit"**

## Usage

After setup, you'll have a switch entity called "NEC TV Power" that you can:
- Turn on/off from the dashboard
- Use in automations
- Control via scripts

## Requirements

- NEC TV Control addon must be installed and running
- Home Assistant 2023.8.0 or newer 
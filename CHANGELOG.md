# Changelog

## [1.0.8] - 2024-08-05

### Changed
- Completely revamped README with step-by-step integration instructions
- Added clear Quick Start guide with visual navigation steps
- Improved troubleshooting section with specific solutions
- Added features list and API endpoints documentation
- Made Home Assistant integration much more user-friendly

## [1.0.7] - 2024-08-05

### Changed
- Cleaned up repository structure - removed HACS integration files
- Simplified README with clear setup instructions
- Focused on addon + REST switch approach (standard Home Assistant pattern)
- Removed test files and unnecessary complexity

## [1.0.6] - 2024-08-05

### Changed
- Removed custom integration from addon (addons cannot add integrations directly)
- Added `/homeassistant` endpoint that provides setup instructions
- Improved API with better configuration information
- Added setup instructions endpoint for easy Home Assistant configuration

### Setup Instructions
Visit `http://localhost:8124/homeassistant` in your browser to get the exact configuration needed for Home Assistant.

## [1.0.5] - 2024-08-05

### Added
- Added custom Home Assistant integration for automatic discovery
- Integration appears in Settings → Devices & Services → Integrations
- No more manual configuration needed - just click "Add Integration"
- User-friendly setup with connection testing

## [1.0.4] - 2024-08-05

### Fixed
- Added Python 3 installation to Dockerfile as it's not included in the base image
- Fixed "No such file or directory" error for /usr/bin/python3

## [1.0.3] - 2024-08-05

### Fixed
- Fixed s6-overlay permission issue by removing s6-setuidgid command that was causing "Operation not permitted" errors

## [1.0.2] - 2024-08-05

### Fixed
- Fixed service run script permissions - added execute permissions to run and finish scripts

## [1.0.1] - 2024-08-05

### Changed
- Simplified Dockerfile to use Home Assistant base images properly
- Removed redundant package installations (Python already included in base image)
- Updated repository URLs to point to correct GitHub repository
- Improved build efficiency and reduced image size

## [1.0.0] - 2024-08-05

### Added
- Initial release of NEC TV Control add-on
- Support for NEC TV power on/off control via network
- Configurable TV IP address and port
- REST API for Home Assistant integration
- Automatic device discovery
- Python service with HTTP server
- Updated shell scripts with environment variable support

### Features
- Power on/off commands for NEC TV
- Network communication via TCP port 7142
- Home Assistant add-on structure
- Docker containerization
- Comprehensive documentation and examples

"""Platform for NEC TV Control switch integration."""
from __future__ import annotations

import logging
import aiohttp
import voluptuous as vol

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .const import DOMAIN, CONF_HOST, CONF_PORT

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the NEC TV Control switch."""
    config = config_entry.data
    host = config[CONF_HOST]
    port = config[CONF_PORT]

    async_add_entities([NECTVSwitch(host, port, config_entry.entry_id)])


class NECTVSwitch(SwitchEntity):
    """Representation of a NEC TV Control switch."""

    def __init__(self, host: str, port: int, entry_id: str) -> None:
        """Initialize the switch."""
        self._host = host
        self._port = port
        self._entry_id = entry_id
        self._attr_name = "NEC TV Power"
        self._attr_unique_id = f"{entry_id}_power"
        self._attr_is_on = False

    async def async_turn_on(self, **kwargs) -> None:
        """Turn the TV on."""
        await self._send_command("on")

    async def async_turn_off(self, **kwargs) -> None:
        """Turn the TV off."""
        await self._send_command("off")

    async def _send_command(self, action: str) -> None:
        """Send command to the NEC TV Control add-on."""
        url = f"http://{self._host}:{self._port}/power"
        data = {"action": action}

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url, json=data, headers={"Content-Type": "application/json"}, timeout=10
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        if result.get("success"):
                            self._attr_is_on = action == "on"
                            self.async_write_ha_state()
                            _LOGGER.info("Successfully sent %s command to TV", action)
                        else:
                            _LOGGER.error("Failed to send %s command: %s", action, result.get("message"))
                    else:
                        _LOGGER.error("HTTP error %d when sending %s command", response.status, action)
        except Exception as e:
            _LOGGER.error("Error sending %s command: %s", action, str(e)) 
"""Config flow for NEC TV Control integration."""
from __future__ import annotations

import logging
import aiohttp
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError

from .const import DOMAIN, DEFAULT_NAME, DEFAULT_HOST, DEFAULT_PORT

_LOGGER = logging.getLogger(__name__)


class NECTVConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for NEC TV Control."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        if user_input is None:
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema(
                    {
                        vol.Required("name", default=DEFAULT_NAME): str,
                        vol.Required("host", default=DEFAULT_HOST): str,
                        vol.Required("port", default=DEFAULT_PORT): int,
                    }
                ),
            )

        errors = {}

        try:
            # Test connection
            await self._test_connection(user_input["host"], user_input["port"])
        except CannotConnect:
            errors["base"] = "cannot_connect"
        except Exception:  # pylint: disable=broad-except
            _LOGGER.exception("Unexpected exception")
            errors["base"] = "unknown"

        if not errors:
            return self.async_create_entry(
                title=user_input["name"], data=user_input
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required("name", default=user_input["name"]): str,
                    vol.Required("host", default=user_input["host"]): str,
                    vol.Required("port", default=user_input["port"]): int,
                }
            ),
            errors=errors,
        )

    async def _test_connection(self, host: str, port: int) -> None:
        """Test connection to the NEC TV Control add-on."""
        url = f"http://{host}:{port}/health"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10) as response:
                if response.status != 200:
                    raise CannotConnect()


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect.""" 
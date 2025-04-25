"""The Steca coolcept inverter platform integration."""

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

DOMAIN = "steca"


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the Steca custom component.

    This function is called by Home Assistant during the initialization
    of the custom component. It performs any necessary setup and returns
    a boolean indicating whether the setup was successful.

    Args:
        hass (HomeAssistant): The Home Assistant instance.
        config (dict): The configuration dictionary.

    Returns:
        bool: True if the setup was successful, False otherwise.

    """
    # Return boolean to indicate that initialization was successful.
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up a config entry."""
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
    return True

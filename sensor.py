import aiohttp
import asyncio
import async_timeout
import logging
import untangle
import voluptuous as vol

from datetime import timedelta

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)

from homeassistant.components.sensor import PLATFORM_SCHEMA

from homeassistant.const import (
    CONF_HOST,
    ELECTRIC_CURRENT_AMPERE,
    ELECTRIC_POTENTIAL_VOLT,
    FREQUENCY_HERTZ, 
    PERCENTAGE,
    POWER_WATT,
    TEMP_CELSIUS
)

from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
import homeassistant.helpers.config_validation as cv

from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)


PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_HOST): cv.string,
})

_LOGGER = logging.getLogger(__name__)

async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the platform."""
    _LOGGER.warning(f"Calling async_setup_platform({hass},{config},,{discovery_info})")

    coordinator = MyCoordinator(hass, config["host"])

    # Fetch initial data so we have data when entities subscribe
    #
    # If the refresh fails, async_config_entry_first_refresh will
    # raise ConfigEntryNotReady and setup will try again later
    #
    # If you do not want to retry setup on failure, use
    # coordinator.async_refresh() instead
    #
    await coordinator.async_config_entry_first_refresh()

    async_add_entities(
        [ 
            StecaEntity(
                coordinator=coordinator, 
                name="AC Voltage", 
                unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,
                device_class=SensorDeviceClass.VOLTAGE,
                identifier="AC_Voltage" 
            ),
            StecaEntity(
                coordinator=coordinator, 
                name="AC Current", 
                unit_of_measurement=ELECTRIC_CURRENT_AMPERE,
                device_class=SensorDeviceClass.CURRENT,
                identifier="AC_Current" 
            ),
            StecaEntity(
                coordinator=coordinator, 
                name="Generated Power", 
                unit_of_measurement=POWER_WATT,
                device_class=SensorDeviceClass.POWER,
                identifier="AC_Power" 
            ),
            StecaEntity(
                coordinator=coordinator, 
                name="AC Frequency", 
                unit_of_measurement=FREQUENCY_HERTZ,
                device_class=SensorDeviceClass.FREQUENCY,
                identifier="AC_Frequency" 
            ),
            StecaEntity(
                coordinator=coordinator, 
                name="DC Voltage", 
                unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,
                device_class=SensorDeviceClass.VOLTAGE,
                identifier="DC_Voltage" 
            ),
            StecaEntity(
                coordinator=coordinator, 
                name="DC Current", 
                unit_of_measurement=ELECTRIC_CURRENT_AMPERE,
                device_class=SensorDeviceClass.CURRENT,
                identifier="DC_Current" 
            ),
            StecaEntity(
                coordinator=coordinator, 
                name="Temperature", 
                unit_of_measurement=TEMP_CELSIUS,
                device_class=SensorDeviceClass.TEMPERATURE,
                identifier="Temp" 
            ),
            StecaEntity(
                coordinator=coordinator, 
                name="Grid Power", 
                unit_of_measurement=POWER_WATT,
                device_class=SensorDeviceClass.POWER,
                identifier="GridPower" 
            ),
            StecaEntity(
                coordinator=coordinator, 
                name="Derating", 
                unit_of_measurement=PERCENTAGE,
                device_class=SensorDeviceClass.POWER_FACTOR,
                identifier="Derating" 
            )
        ]
    )


class MyCoordinator(DataUpdateCoordinator):
    """My custom coordinator."""

    def __init__(self, hass: HomeAssistant, host: str):
        """Initialize my coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            # Name of the data. For logging purposes.
            name="Steca coolcept inverter",
            # Polling interval. Will only be polled if there are subscribers.
            update_interval=timedelta(seconds=10),
        )

        self._host = host

    async def _async_update_data(self):
        """Fetch data from API endpoint.

        This is the place to pre-process the data to lookup tables
        so entities can quickly look up their data.
        """
        async with aiohttp.ClientSession() as session:
            async with async_timeout.timeout(10):
                async with session.get(f"http://{self._host}/measurements.xml") as response:
                    html = await response.text()
                    document = untangle.parse(html)                        
                    data = {
                        'device': document.root.Device["Name"]
                    }

                    for item in document.root.Device.Measurements.Measurement:
                        data[item['Type']] = (
                            item['Value'] if item['Value'] else 0,
                            item['Unit']
                        )
                    
                    return data


class StecaEntity(CoordinatorEntity, SensorEntity):
    """Steca inverter entity.

    The CoordinatorEntity class provides:
      should_poll
      async_update
      async_added_to_hass
      available

    """

    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, coordinator: DataUpdateCoordinator, name: str, unit_of_measurement, device_class: SensorDeviceClass, identifier: str):
        """Pass coordinator to CoordinatorEntity."""
        super().__init__(coordinator)
        self._attr_name = name
        self._attr_native_unit_of_measurement = unit_of_measurement
        self._attr_device_class = device_class
        self._identifier = identifier


    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._attr_native_value = self.coordinator.data[self._identifier][0]
        self._attr_native_unit_of_measurement = self.coordinator.data[self._identifier][1]
        self.async_write_ha_state()

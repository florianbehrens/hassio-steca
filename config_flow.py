"""Config flow for Steca coolcept inverter platform integration."""

from voluptuous import Required, Schema

from homeassistant import config_entries


class StecaConfigFlow(config_entries.ConfigFlow, domain="steca"):
    """Handle a Steca config flow."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the user step of the configuration flow.

        This method is invoked when the user initiates the configuration flow
        or provides input through the form. If user input is provided, it creates
        a configuration entry with the specified IP address. Otherwise, it displays
        a form prompting the user to input the required data.

        Args:
            user_input (dict, optional): A dictionary containing user-provided
                input. Expected to have a key "IP address" with the IP address
                as its value. Defaults to None.

        Returns:
            FlowResult: The result of the configuration flow step. This can be
            either a form to collect user input or the creation of a configuration
            entry.

        """
        if user_input is not None:
            return self.async_create_entry(
                title="Steca coolcept inverter IP address",
                data={"ip": user_input["IP address"]},
            )

        return self.async_show_form(
            step_id="user", data_schema=Schema({Required("IP address"): str})
        )

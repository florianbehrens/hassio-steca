from homeassistant import config_entries
from voluptuous import Schema, Required


class ExampleConfigFlow(config_entries.ConfigFlow, domain="steca"):
    """Handle a Steca config flow."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            # Validate user input
            valid = True
            if valid:
                # See next section on create entry usage
                return self.async_create_entry(
                            title="Steca coolcept inverter IP address",
                            data={
                                "ip": user_input["ip"]
                            },
                        )

            errors["base"] = "auth_error"

        return self.async_show_form(
            step_id="user", data_schema=Schema({Required('ip'): str})
        )

import argparse
import simplejson as json


class ConfigAction(argparse.Action):
    """An `action` for CLI arguments that takes the config file path and returns the resultant config `dict`."""

    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        if nargs:
            raise ValueError("nargs not allowed")
        self.dest = dest
        super(ConfigAction, self).__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        config = get_config(values)
        setattr(namespace, self.dest, config)


def get_config(config_path):
    """Parse the JSON config file at the given path and return the `dict`."""
    with open(config_path, 'r') as input:
        return json.load(input)

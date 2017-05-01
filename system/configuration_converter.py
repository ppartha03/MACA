
import sys
# Convert the config to the latest version

INITIAL_VERSION = 'v0.1'
CURRENT_VERSION = 'v0.1'

def _convert_from_v0_1(system_description):
    """
        Convert to latest version
    """
    return system_description # Nothing to convert. This is now the latest version.

def convert_to_latest_config(system_description):
    version = system_description.get('version', INITIAL_VERSION)
    try:
        converstion_function = getattr(sys.modules[__name__], '_convert_from_{}'.format(version.replace('.', '_')))
        return converstion_function(system_description)
    except:
        raise Exception('Unable to determine convert from version {} to the latest version'.format(version))

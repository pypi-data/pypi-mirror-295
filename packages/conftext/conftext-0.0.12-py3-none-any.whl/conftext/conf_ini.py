import os
import logging
import configparser

logging.basicConfig()
log = logging.getLogger(__name__)

def read_config(filepath):
    if os.path.isfile(filepath):
        config = configparser.ConfigParser()
        config.read(filepath)
        return config
    raise FileNotFoundError(filepath)


def get_config_section(config_file, conftext_section):
    """
    Get config section
    
    First check the loaded config to see if we have more than one section to choose from. Only if we
    do, we move on to use conftext to select the appropriate config section.
    """
    section_name = None
    
    if config_file.sections():
        
        if conftext_section:
            # We select section based on two hard-coded dimmensions for now; service and context. This
            # should be based on the config schema.
            if "service" in conftext_section and conftext_section["service"] in config_file:
                section_name = conftext_section["service"]
            elif "context" in conftext_section and conftext_section["context"] in config_file:
                section_name = conftext_section["context"]
            else:
                log.warning(f"No match for {conftext_section} in {config_file}. Using DEFAULT section.")
                section_name = configparser.DEFAULTSECT
        else:
            raise configparser.NoSectionError(
                f"No conftext_section ({conftext_section}) for selecting among sections "
                f"({config_file._sections}) in config file {config_file}.")

    elif config_file.defaults():
        section_name = configparser.DEFAULTSECT
    
    return config_file[section_name]

import configparser
import pathlib
import logging
import shutil


def load_config(file='config.ini', delete_config=False):
    # check if config file exists
    abs_file = pathlib.Path.cwd() / file
    if delete_config:
        logging.warning("Deleting config file")

        #fixed the bug when trying to delete file without existing file
        if abs_file in pathlib.Path.cwd().iterdir():
            pathlib.Path.unlink(abs_file)
    if abs_file not in pathlib.Path.cwd().iterdir():
        logger = logging.getLogger('scrap_logger')
        logger.warning("Config file " + file + " not found!")
        template = pathlib.Path.cwd() / pathlib.Path('template_' + file)
        logger.warning("Trying to create config file from template " + str(template))
        # if config file is missing a default config is created from the template
        if template not in pathlib.Path.cwd().iterdir():
            logging.error("Config template file " + str(template) + " not found!")
        else:
            shutil.copy(str(template), str(abs_file))

            logging.info("Created config file from template.")
    config = configparser.ConfigParser()
    config.read(file)

    return config
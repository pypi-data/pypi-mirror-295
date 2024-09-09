"""
Created on Nov 4, 2015

@author: krgupta
@updated: William Hinz
"""

from configparser import ConfigParser

import os
import logging
import pathlib

logger = logging.getLogger(__name__)

ROOT_DIR = pathlib.Path(__file__).parent.parent  # Should point to the root of the project!


class Helper:

    def __init__(self, property_filename: str):
        self.property_filename = property_filename
        self.property_file_uri = None
        self.parser = None
        self.set_property_file(self.property_filename)
        self.create_parser()

    def set_property_file(self, property_filename: str):
        if property_filename is not None:
            temp_file_uri = pathlib.Path(ROOT_DIR, property_filename)
            if temp_file_uri.is_file():
                self.property_file_uri = temp_file_uri

    def create_parser(self):
        if self.parser is None:
            try:
                self.parser = ConfigParser({"http": "", "https": "", "ftp": ""})
            except Exception:
                logger.warning("Parser could not be initialized")

        if self.parser is not None and self.property_file_uri is not None:
            try:
                files_successfully_read_in = self.parser.read(self.property_file_uri)
                logger.debug(f'config files successfully read in: {files_successfully_read_in}')
            except Exception:
                logger.warning("An error occurred when loading the property file. Unable to create parser.")
        else:
            logger.warning("Either parser or property file has not been read in. Unable to create parser.")

    def get_property(self, property_name):
        string_value = None
        if self.property_file_uri is not None and self.parser is not None:
            try:
                string_value = self.parser.get("properties", property_name)
            except Exception:
                logger.debug(f"{property_name} not found\n")

        if string_value is None:
            string_value = os.getenv(property_name)
        return string_value

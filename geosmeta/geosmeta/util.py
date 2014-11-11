# Copyright (c) The University of Edinburgh, 2014.
#
import os
import sys
import ConfigParser
import logging

class GeosMetaConfig(object):
    """Class encapsulating GeosMeta configuration"""

    DEFAULT_CONFIG_FILE_NAME = "geosmeta.cfg"
    DEFAULT_CONFIG_FILE_DIRECTORY = ".geosmeta"

    def __init__(self, configFilePath = None):
        """Constructor.

        :param configFilePath: The location of the geosmeta configuration
                               file. If not present this defaults to
                               $HOME/.geosmeta/geosmeta.cfg
        """
        if (configFilePath is None):
            # Not set, so construct default location
            homeDirectory = os.path.expanduser("~")
            configFilePath = os.path.join(homeDirectory,
                                          self.DEFAULT_CONFIG_FILE_DIRECTORY,
                                          self.DEFAULT_CONFIG_FILE_NAME)

        self.configFilePath = configFilePath

        # Read configuration file
        try:
            self.readConfigFile()
        except IOError as err:
            sys.stderr.write('Error reading file:\n')
            sys.stderr.write('%s\n' % str(err))
            sys.exit(1)
        except Exception as err:
            sys.stderr.write('Error processing configuration file:\n')
            sys.stderr.write('%s\n' % str(err))
            sys.exit(1)

    def readConfigFile(self):
        """Reads the configuration file and sets options"""
        # Check file exists
        try:
            with open(self.configFilePath) as file:
                pass
        except IOError as e:
            raise e
        else:
            file.closed

        # Read configuration file and set options
        try:
            config = ConfigParser.SafeConfigParser()
            config.read(self.configFilePath)

            self._serverURI = config.get('Server', 'URL')
            self._logfile = config.get('Logging', 'logfile')
            self._loglevel = config.get('Logging', 'loglevel')
            self._username = config.get('Authentication', 'username')
            self._secret = config.get('Authentication', 'secret')
        except Exception as e:
            raise e

    @property
    def serverURI(self):
        """Get the Eve Server URI"""
        return self._serverURI

    @property
    def logfile(self):
        """Get the Logfile"""
        return self._logfile

    @property
    def loglevel(self):
        """Get the log level"""
        return self._loglevel

    @property
    def username(self):
        """Get the username"""
        return self._username

    @property
    def secret(self):
        """Get the secret"""
        return self._secret

def setupLogging(logfile, loglevel, name):
    """
    Setup Logging based on configuration file options

    :param logfile: The file to write logging to
    :param loglevel: The log level to use
    :param name: The logger name
    :returns: The logger
    """
    numericLevel = getattr(logging, loglevel.upper(), None)
    if not isinstance(numericLevel, int):
        raise ValueError('Invalid log level: %s' % loglevel)
    logFormat = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(filename=logfile,
                        level=numericLevel,
                        format=logFormat)
    logger = logging.getLogger(name)
    logger.debug('Logging configured')
    return logger

def queryYesNo(question):
    """
    Ask a yes/no question and return the answer.

    :param question: String containing the question to present to the user.
    :returns: Boolean
    """
    validYesAnswers = set(['yes', 'y', 'ye', ''])
    validNoAnswers = set(['no', 'n'])
    prompt = " [Y/n] "

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if choice in validYesAnswers:
            return True
        elif choice in validNoAnswers:
            return False
        else:
            sys.stdout.write("Please respond with 'yes' or 'no'.")

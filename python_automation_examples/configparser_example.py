
import configparser

# Create a configuration parser
config = configparser.ConfigParser()

# Read a configuration file
config.read('config.ini')

# Access a value from the configuration file
print(config['DEFAULT']['Server'])

# Write a new configuration file
config['DEFAULT']['Server'] = 'localhost'
with open('new_config.ini', 'w') as configfile:
    config.write(configfile)

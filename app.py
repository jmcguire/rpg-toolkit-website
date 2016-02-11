#!/usr/bin/env python
"""
app.py

Generate a random webpage from a config file.

Lots of gaming resources are simple variations on a theme. Here's a big list, choose a random thing from the list, and interpolate a bit using data from some other lists.

Here's how this program works: given a config file, figure out how to make a website from it. It looks for the "meta" config hash to figure out how to kick itself off. It also knows how to interpolate simple variables.

Created by Justin McGuire <jm@landedstar.com>.
Content of config files have copyright information inside them.
"""

import sys
import random
import re

class ToolConfig:

  config = None

  def __init__(self, config_file):
    self.load_config(config_file)

  def load_config(self, config_file):
    """load the config file into the static config variable, but only once"""
    if os.path.isfile(config_file):
      pass

    if not self.config:
      with open(config_file) as file:
        self.config = yaml.load(file)

  def get_random_item_from(self, listname):
    pick = random.randint(0, config[listname].length - 1)
    return config[listname].pop(pick)
    

def main():
  

if __name__ == '__main__':
  main()

  potato.have()

# load config file
# have a potato
# get meta information
# if generate is > 1, make a list, otherwise just a p
# foreach generate
#   copy config to modifiable object
#   look at start
#   get random item from start list
#   remove that item from list
#   while finding new items to interpolate:
#     get random item form appropriate list
#     remove list list
#     add to string


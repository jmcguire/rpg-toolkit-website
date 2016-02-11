#!/usr/bin/env python
"""
app.py

Generate a random webpage from a config file.

Lots of gaming resources are simple variations on a theme. Here's a big list, choose a random thing from the list, and interpolate a bit using data from some other lists.

Here's how this program works: given a config file, figure out how to make a website from it. It looks for the "meta" config hash to figure out how to kick itself off. It also knows how to interpolate simple variables.

Created by Justin McGuire <jm@landedstar.com>.
"""

import sys
import random
import re
import yaml
import os

class ToolConfig:

  config = None

  def __init__(self, config_file):
    self.load_config(config_file)

    self.title     = self.config['meta']['title']
    self.copyright = self.config['meta']['copyright']
    self.generate  = self.config['meta']['generate']
    self.start     = self.config['meta']['start']
    self.norepeats = True

  def load_config(self, config_file):
    """load the config file into the static config variable, but only once"""
    if os.path.isfile(config_file):
      pass

    if not self.config:
      with open(config_file) as file:
        self.config = yaml.load(file)

  def start(self):
    """get an random selection."""

    # if we don't care about repeats, reload the config file after every use
    if not self.norepeats:
      self.backup_config = self.config

    # start the string with the "start" variable
    select = self.get_random_item_from( self.config[self.start] )
    self.interpolate(select)
    self.saved_names = {}

    if not self.norepeats:
      self.config = self.backup_config

    return select

  def get_random_item_from(self, listname):
    """remove a random item from one of the lists in the config, and return it"""
    pick = random.randint(0, config[listname].length - 1)
    return config[listname].pop(pick)

  def interpolate(self, string):
    """replace references in string with other items from hash, recursive"""

    # look for a reference, which looks like [hashname]
    m = re.search(r'\[([^]]*)\]', string)
    if m:
      tag = m.group(0)

      # the listname may need to be saved, so it can be reused later
      (list_name, saved_name) = tag.split(':')

      # get the new selection to replace the tag with
      selection = ''
      if self.config[list_name]:
        # check the saved variables first
        selection = self.config[saved_name]
      else:
        # otherwise grab a random selection from the choosen list
        selection = self.get_random_item_from(list_name)

      # if we want to save the selection, do that now
      if saved_name:
        self.config[saved_name] = selection

      # there may be more interpolation
      string = self.interpolate( string.replace('[%s]' % tag, selection) )

    return string

def main(config_file):
  config = ToolConfig(config_file)
  print config.title

  # print out each random selection
  for x in range(config.generate):
    item = config.start()
    print "%d: %s\n" % (x, item)

if __name__ == '__main__':
  if len(sys.argv) > 1:
    config_file = sys.argv[1]
    if not os.path.isfile(config_file):
      sys.exit("config file %s isn't a file\nusage: %s <config_file>" % (config_file, sys.argv[0]))
    main(config_file)
  else:
    sys.exit("usage: %s <config_file>" % sys.argv[0])


#!/usr/bin/env python
"""
rpgtoolkit.py

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
import logging

class ToolConfig:

  config = None

  def __init__(self, config_file):
    self.load_config(config_file)

    self.title     = self.config['meta']['title']
    self.copyright = self.config['meta']['copyright']
    self.generate  = self.config['meta']['generate']
    self.start     = self.config['meta']['start']
    self.norepeats = True
    self.saved_tags = {}

  def load_config(self, config_file):
    """load the config file into the static config variable, but only once"""

    if not os.path.isfile(config_file):
      sys.exit("config file: %s is not a file" % config_file)

    if not self.config:
      with open(config_file) as file:
        self.config = yaml.load(file)

  def create(self):
    """get an random selection."""

    # if we don't care about repeats, reload the config file after every use
    if not self.norepeats:
      self.backup_config = self.config

    # start the string with the "start" variable
    select = self.get_random_item_from( self.start )
    logging.debug("inital string %s" % select)
    select = self.interpolate(select)

    # these get set in interpolate, but must be unset elsewhere, since it's a
    # recursive function that doesn't know when its time is over
    self.saved_tags = {}

    if not self.norepeats:
      self.config = self.backup_config

    return select

  def get_random_item_from(self, listname):
    """remove a random item from one of the lists in the config, and return it"""

    pick = random.randint(0, len(self.config[listname]) - 1)
    return self.config[listname].pop(pick)

  def interpolate(self, string):
    """replace references in string with other items from hash, recursive"""

    # look for a reference, which looks like [hashname]
    m = re.search(r'\[([^]]*)\]', string)
    if m:
      tag = m.group(1)

      logging.debug("found tag %s" % tag)

      # the listname may need to be saved, so it can be reused later
      if ':' in tag:
        (list_name, saved_tag) = tag.split(':')
      else:
        list_name = tag
        saved_tag = ''

      logging.debug("tag split into list_name/saved_tag: %s/%s" % (list_name, saved_tag))

      # get the new selection to replace the tag with
      selection = ''
      if list_name in self.saved_tags:
        # check if the list_name is actually a saved tag
        selection = self.saved_tags[list_name]
      else:
        # otherwise grab a random selection from the choosen list
        selection = self.get_random_item_from(list_name)

      # if we want to save the selection, do that now
      if saved_tag:
        self.saved_tags[saved_tag] = selection

      # there may be more interpolation
      logging.debug("replacing [%s] with %s" % (tag, selection))
      string = self.interpolate( string.replace('[%s]' % tag, selection, 1) )

    return string

def main(config_file):
  logging.basicConfig(level=logging.WARNING)
  tool_config = ToolConfig(config_file)
  print tool_config.title

  # print out each random selection
  for x in range(tool_config.generate):
    item = tool_config.create()
    print "%d: %s" % (x+1, item)

def usage(error_msg=''):
  usage_msg = "usage: %s <config_file>" % sys.argv[0]
  if error_msg:
    sys.exit("%s\n%s" % (error_msg, usage_msg))
  else:
    sys.exit(usage_msg)

if __name__ == '__main__':
  # make sure our arguments are correct
  if len(sys.argv) > 1:
    config_file = sys.argv[1]
    if not os.path.isfile(config_file):
      usage("config file %s isn't a file" % config_file)
    main(config_file)
  else:
    usage()


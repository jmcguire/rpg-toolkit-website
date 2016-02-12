#!/usr/bin/env python
# -*- coding: utf-8 -*-

import web
import yaml
import rpg-toolkit

urls = (
  '/',     'index',
  '/(.+)', 'toolkit'
)

# TODO:
# create a superclass that contains the generic template, where the title and
# content are ready to go.

class index:

  def __init__(self):
    pass

  def GET(self, file_name):
    """Create a webpage that lists all toolkits available."""

    # TODO:
    #  - get all the config files in config/*.yaml
    #  - open each one, get the title
    #  - create a hash of title => filename (wihout the .yaml)

    return """
<title>RPG Toolkits</title>
<h1>404</h1>
<p>Please go to a specific toolkit.</p>
"""

class toolkit:

  def __init__(self):
    self.config = {}

  def GET(self, file_name):
    """Create a webpage using the config file_name.yaml."""

    tool_config = ToolConfig("config/%s.yaml" % file_name)

    # create our list results
    result_list = []
    for x in range(tool_config.generate):
      result_list.push(tool_config.create())

    # transform the contact info to a url
    author_url = tool_config.copyright['contact'],
    if author_url[0] == '@': # check for twitter
      author_url = "https://twitter.com/%s" % author_url[1:]
    else: # else assume it's an email
      author_url = "mailto:" % author_url

    webpage = Template("""
<!doctype html>
<html class="no-js" lang="en">
<meta charset="utf-8">
<meta http-equiv="x-ua-compatible" content="ie=edge">
<title>$title</title>
<meta name="description" content="Refresh to get a random kingdom history">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="http://reset5.googlecode.com/hg/reset.min.css">
<link href='https://fonts.googleapis.com/css?family=Cabin' rel='stylesheet' type='text/css'>
<link href='https://fonts.googleapis.com/css?family=Lobster' rel='stylesheet' type='text/css'>
<!-- design inspired by http://www.twosentencestories.com/ -->
<style>
html {
height: auto;
min-height: 100%%;
margin: 0 1em;
}
body{
height: 100%%;
background: #FFF8EF;
background: linear-gradient(to bottom, #FFF8EF 0%%, #CEC3B5 100%%);
}
* {
font-family: Cabin, sans-serif;
}
h1 {
font-family: 'Lobster', Georgia, "Times New Roman", Times, serif;
font-weight: normal;
text-align: center;
margin: .5em auto 0;
color: #cc4d22;
font-size: 4em;
line-height: 1.3em;
text-shadow: -1px -1px 0 #7F3218;
}
li {
list-style: none;
}
body >ul >li {
color: #123;
font-size: 1.5em;
font-style: italic;
margin-top: .5em;
}
li li {
margin-top: 1em;
font-size: 0.8em;
color: #484747;
padding-left: 1.3em;
}
li li:before {
content: "—";
display: inline-block;
margin-left: -1.3em; /* same as padding-left set on li */
width: 1.3em; /* same as padding-left set on li */
}
</style>
<h1>$title</h1>
<ul> $result_list </ul>
<footer>
  <p>Content &copy; <a href="$author_url">$author</a>, <em><a href="$source_url">$source</a></em></p>
  <p>Code &copy; Justin McGuire, <a href="mailto:jm@landedstar.com">jm@landedstar.com</a>, <a href="https://twitter.com/landedstar">@landedstar</a></p>, <a href="https://github.com/jmcguire/rpg-toolkit-website">Find this code on GitHub</a>
<footer>
<script>
(function(b,o,i,l,e,r){b.GoogleAnalyticsObject=l;b[l]||(b[l]=
function(){(b[l].q=b[l].q||[]).push(arguments)});b[l].l=+new Date;
e=o.createElement(i);r=o.getElementsByTagName(i)[0];
e.src='https://www.google-analytics.com/analytics.js';
r.parentNode.insertBefore(e,r)}(window,document,'script','ga'));
ga('create','UA-42761539-5','auto');ga('send','pageview');
</script>
""")

    return webpage.substitute(
      title=tool_config.title,
      author=tool_config.copyright['author'],
      author_url=author_url,
      source_title=ool_config.copyright['title']
      source_url=tool_config.copyright['url'],
      result_list="<li>" + result_list.join("</li><li>") + "</li>"
    )


if __name__ == "__main__": 
  app = web.application(urls, globals())
  app.run() 

# rpg-toolkit-website

Create an entire website for your own RPG random generator using just one YAML file.

## Synopsis

Many creative and motivated tabletop gamers are coming up with tables to create
random things for their role playing game. this project aims to make it easy for
these people to convert their random tables to a fully functioning command-line
tool and mobile-friendly website.

Now you can check your random generator from your phone.

The only thing you need to do to create your own website is create a YAML file.
The YAML file syntax is a bit undocumented right now, but there are two working
files in the config directory so copy and modify.

## Usage

In command-line form:

    ./rpg-toolkit.py config/<configfile.yaml>

In web form:

https://rpg-toolkit.herokuapp.com/<configfile>

To actually see this in action, check out https://rpg-toolkit.herokuapp.com/dokclaw .

## Heroku

This repo is built to be deployed to Heroku. After you have an account on heroku and heroku installed, just deploy as normal:

    heroku create
    heroku login
    git deploy master heroku

## Credits

Programming by Justin McGuire <jm@landedstar.com> @landedstar

## License

Code is licenced under the MIT licence.


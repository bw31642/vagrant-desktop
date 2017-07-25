# Vagrant Desktop

Simple script to prepare a Vagrantfile for a linux desktop
Parameter driven from a YAML config file.

## Requirements

The following Python modules are required. All are avaiable via pip install.

- pyyaml
- docopt
- json
- jinja2

## Usage

    $ git clone https://github.com/bw31642/vagrant-desktop
    $ cd vagrant-desktop
    $ mkdir ansible
    $ cd ansible
    $ git clone https://github.com/bw31642/ansible-desktop.git .
    $ cd ..
    $ vim config.yml
    $ ./setup.py
    $ vagrant up 

## Environment
I prefer a management interface on my virtual machines to enable direct connectivity from the host (my laptop).

    $ vim /etc/hosts - insert ip address for private_network defined in config.yml


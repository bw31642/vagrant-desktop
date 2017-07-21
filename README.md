# Vagrant Desktop

Simple script to prepare a Vagrantfile for a linux desktop
Parameter driven from a YAML config file.

## Usage

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


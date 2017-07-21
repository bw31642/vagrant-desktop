#!/opt/local/bin/python
"""
Usage:
    setup.py (-h | --help )
    setup.py [--ansible_dir=<ansible_dir>] [--template_dir=<template_dir>] [--config=<config_yml>]

Options:
    <ansible_dir>     The directory containing the ansible tree used for provisioning
    <template_dir>    The directory containing the Jinja2 templates used for creating
                      the Vagrantfile
    <config_yml>      The name of the input YAML configuration file
"""

import os
import sys
import yaml
import json
from  jinja2 import Environment, FileSystemLoader
import docopt


def make_template(data, template_dir, templatefn, outputfn):
     # Create Vagrant File
     try:
         env = Environment(loader=FileSystemLoader(template_dir))
         env.filters['jsonify'] = json.dumps
         template = env.get_template(templatefn)
     except IOError as err:
         print "error reading file, {0}: {1}".format(templatefn, err)
         sys.exit(1)

     new_file = template.render(data)
     if new_file:
         try:
             with open(outputfn, "w") as of:
                 of.write(new_file)
         except IOError as err:
             print "error, unable to create output file {0} {1}".format(outputfn, err)
             sys.exit(1)


def make_yaml(data, outputfn):
     try:
         with open(outputfn, "w") as of:
		yaml.dump(data, of, default_flow_style=False, default_style=False)
     except IOError as err:
         print "error, unable to create yaml file {0} {1}".format(outputfn, err)
         sys.exit(1)

def make_ansible_inventory(data, outputfn):
     try:
         with open(outputfn, "w") as of:
             for group in data['groups']:
	         of.write("[" + group + "]\n")
                 of.write(data['entry'] + "\n")
     except IOError as err:
         print "error, unable to create ansible inventory file {0} {1}".format(outputfn, err)
         sys.exit(1)

def make_ansible_config(data, outputfn):
     try:
         with open(outputfn, "w+") as of:
             for section in data['config']:
                 items = section.keys()
                 for item in items:
	            of.write("[" + item + "]\n")
                    for element in section[item].keys():
                        of.write (element + "=" + section[item][element] + "\n")
     except IOError as err:
         print "error, unable to create ansible config file {0} {1}".format(outputfn, err)
         sys.exit(1)


if __name__ == '__main__':
    args = docopt.docopt(__doc__, version="version: 0.1")

    ansible_dir = args.get('--ansible_dir') or "./ansible"
    template_dir = args.get('--template_dir') or "./templates"
    config_yml = args.get('--config_yml') or "./config.yml"

    if not os.path.isdir(ansible_dir):
        print "error, ansible dir %s not found!" % (ansible_dir)
        sys.exit(1)
    if not os.path.isdir(template_dir):
        print "error, template dir %s not found!" % (template_dir)
        sys.exit(1)
    if not os.path.exists(config_yml):
        print "error, config file %s not found!" % (config_yml)
        sys.exit(1)

    # Load config yaml
    with open(config_yml,'r') as conf_file:
        config_data = yaml.load(conf_file)

    # Create a dict that contains the 'vagrant' and 'ansible' sections from the config file
    key_list = config_data['vagrant'].keys()
    a = {i:config_data['vagrant'][i] for i in key_list}
    if 'ansible' in config_data:
        key_list = config_data['ansible'].keys()
        b = {i:config_data['ansible'][i] for i in key_list}
        data = a.copy()
        data.update(b)

    # Create the Vagrantfile from template
    make_template(data,template_dir,"Vagrantfile.j2","Vagrantfile")

    # Creates host_vars for the machine
    if 'ansible' in config_data:
        key_list = config_data['host_vars'].keys()
        host_vars = {i:config_data['host_vars'][i] for i in key_list}
        hvfn = ansible_dir+"/host_vars/"+config_data['vagrant']['name']+".yml"
        make_yaml(host_vars, hvfn)

        # Create Inventory entries
        inv_file = config_data['ansible']['inventory_file']
        make_ansible_inventory(config_data['ansible']['inventory'], inv_file)

        # Generate ansible.cfg
        if 'config' in config_data['ansible']:
            conf_file = config_data['ansible']['config_file']
            make_ansible_config(config_data['ansible'],conf_file)


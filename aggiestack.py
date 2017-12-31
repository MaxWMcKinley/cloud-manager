#!/usr/bin/env python

import sys
import click
import os
from config import *
from log import *
from admin import *

# aggiestack.py CLI group
@click.group()
def cli():
    pass

# server command
@cli.command()
@click.argument('command', nargs=-1)
@click.option('-i', '--image', help='Specify the image type')
@click.option('-f', '--flavor', nargs=2, help='Specify the flavor and instance names')
def server(command, image, flavor):
    if not command:
        print 'Please enter which server command you would like to execute'
        log('Please enter which server command you would like to execute')
    elif command[0] == 'create':
        instance = flavor[1]
        flavor = flavor[0]

        # Find machine that can support flavor
        objs = loadConfig('hardware')
        if objs:
            for obj in objs:
                if canHost(obj.name, flavor):
                    machine = obj.name
                    break
            
            if machine:
                addInstance(instance, flavor, image, machine)
                log('Created instance')
                log('SUCCESS')
            else:
                print "No current machine can support this instance"
                log('No current machine can support this instance')
                log('FAILURE')


    elif command[0] == 'delete':
        deleteInstance(command[1])
    elif command[0] == 'list':
        serverList()
    else:
        print command[0] + ' is not a proper server command, please use create, delete, or list'

    logCmd(sys.argv)

# config command
@cli.command()
@click.option('-h', '--hardware', type=click.Path(exists=True), help='File path to the hardware configuration file')
@click.option('-i', '--images', type=click.Path(exists=True), help='File path to the images configuration file')
@click.option('-f', '--flavors', type=click.Path(exists=True), help='File path to the flavors configuration file')
def config(hardware, images, flavors):
    logCmd(sys.argv)

    if hardware:
        configHardware(hardware)
    elif images:
        configImages(images);
    elif flavors:
        configFlavors(flavors)
    else:
        eprint('Please include a connfig option. Use aggiestack config --help for more information.')
        log("FAILURE")

# show command
@cli.command()
@click.argument('type')
def show(type):
    logCmd(sys.argv)

    if type == 'hardware':
        showHardware()
    elif type == 'images':
        showImages()
    elif type == 'flavors':
        showFlavors()
    elif type == 'all':
        showAll()
    else:
        eprint('Invalid command. Use aggiestack show --help for more information.')
        log("FAILURE")

# admin command
@cli.command()
@click.argument('command', nargs=1)
@click.argument('params', nargs=-1)
@click.option('-m', '--mem', help='Specify the amount of memory')
@click.option('-d', '--disk', help='Specify the number of disks')
@click.option('-v', '--vcpus', help='Specify the amount of vcpus')
@click.option('-i', '--ip', help='Specify the ip address')
@click.option('-r', '--rack', nargs=2, help='Specify the rack')
def admin(command, params, mem, disk, vcpus, ip, rack):
    logCmd(sys.argv)

    if command == 'show':
        if params[0] == 'hardware':
            showHardware()
        elif params[0] == 'instances':
            showInstances()
        else:
            log("FAILURE")
    elif command == 'can_host':
        machine = params[0]
        flavor = params[1]
        if canHost(machine, flavor):
            print 'Yes'
        else:
            print 'No'

        log("SUCCESS")
    elif command == 'evacuate':
        rack = params[0]
        evacuateRack(rack)
    elif command == 'remove':
        machine = params[0]
        removeMachine(machine)
    elif command == 'add':
        machine = Machine(rack[1], rack[0], ip, mem, disk, vcpus)
        machine.save()
    else:
        eprint('Invalid command. Use aggiestack show --help for more information.')
        log("FAILURE")

# Add hardware configuration
# Overwrites any previous configuration
def configHardware(file):
    # Open config file and read how many machines are included
    fo = open(file, 'r')
    count = int(fo.readline())

    error = False   # Keep track of succesful program execution
    racks = []
    machines = []   # List to be populated with all machines in config file

    # Parse rack information one at a time and append it to machines
    for i in range(count):
        line = fo.readline()
        if not line:
            break

        specs = line.split()
        name = specs[0]
        capacity = specs[1]

        try:
            racks.append(Rack(name, capacity))
        except Exception as err:
            eprint(err)
            error = True

    count = int(fo.readline())

    # Parse machine information one at a time and append it to machines
    for i in range(count):
        line = fo.readline()
        if not line:
            break

        specs = line.split()
        name = specs[0]
        rack = specs[1]
        ip = specs[2]
        mem = specs[3]
        numDisks = specs[4]
        numVcpus = specs[5]

        try:
            machines.append(Machine(name, rack, ip, mem, numDisks, numVcpus))
        except Exception as err:
            eprint(err)
            error = True

    if error:
        eprint("There was an error loading your configuration file")
        log("FAILURE")
    else:
        saveConfig('racks', racks)
        saveConfig('hardware', machines)
        log("SUCCESS")

# Add images configuration
# Overwrites any previous configuration
def configImages(file):
    # Open config file and read how many images are included
    fo = open(file, 'r')
    count = int(fo.readline())

    error = False   # Keep track of succesful program execution
    images = []     # List to be populated with all images in config file

    # Parse image information one at a time and append it to images
    for i in range(count):
        line = fo.readline()
        if not line:
            break

        specs = line.split()
        name = specs[0]
        size = specs[1]
        path = specs[2]

        try:
            images.append(Image(name, size, path))
        except Exception as err:
            eprint(err)
            error = True

    if error:
        eprint("There was an error loading your configuration file")
        log("FAILURE")
    else:
        saveConfig('images', images)
        log("SUCCESS")

# Add flavors configuration
# Overwrites any previous configuration
def configFlavors(file):
    # Open config file and read how many flavors are included
    fo = open(file, 'r')
    count = int(fo.readline())

    error = False   # Keep track of succesful program execution
    flavors = []    # List to be populated with all flavors in config file

    # Parse flavor information one at a time and append it to flavors
    for i in range(count):
        line = fo.readline()
        if not line:
            break

        specs = line.split()
        name = specs[0]
        mem = specs[1]
        numDisks = specs[2]
        numVcpus = specs[3]

        try:
            flavors.append(Flavor(name, mem, numDisks, numVcpus))
        except Exception as err:
            eprint(err)
            error = True

    if error:
        eprint("There was an error loading your configuration file")
        log("FAILURE")
    else:
        saveConfig('flavors', flavors)
        log("SUCCESS")

def addInstance(instance, flavor, image, machine):
    file = 'instances.pickle'

    log('Adding instance')

    instance = {
        "name": instance,
        "flavor": flavor,
        "image": image,
        "machine": machine
    }

    with open(file, 'ab') as file:
        pickle.dump(instance, file)

    log('SUCCESS')

# This function is very inefficient 
# Could be cleaned greatly by creating an instance class or using a custom load function for instances
def deleteInstance(instanceName):
    instances = loadConfig('instances')

    log('Deleting instance')

    i = 0
    for instance in instances:
        if instance["name"] == instanceName:
            break   

        i += 1

    try:
        del instances[i]
        os.remove('instances.pickle')

        for instance in instances:
            addInstance(instance["name"], instance["flavor"], instance["image"], instance["machine"])
            log('SUCCESS')
    except Exception as err:
        print "Instance " + instanceName + " does not exist"
        log('FAILURE')

def serverList():
    log('Printing server list')

    instances = loadConfig('instances')
    if instances:
        for instance in instances:
            print("%s %s %s" % (instance["name"], instance["flavor"], instance["image"]))

def showInstances():
    log('Printing instance list')

    instances = loadConfig('instances')
    if instances:
        for instance in instances:
            print("%s %s" % (instance["name"], instance["machine"]))

def evacuateRack(rackName):
    log('Evacuating rack ' + rackName)

    racks = loadConfig('racks')
    if racks:
        for rack in racks:
            if rack.name != rackName:
                newRack = rack
                break
    else:
        print 'There are currently no racks configured'
        log('FAILURE')

    if not newRack:
        print 'There are no other available racks to move the machines'
        log('FAILURE')

    hardware = loadConfig('hardware')
    newHardware = []

    if hardware:
        i = 0
        for machine in hardware:
            if machine.rack == rackName:
                machine.rack = newRack.name

            newHardware.append(machine)
            i += 1

    saveConfig('hardware', hardware)
    log('SUCCESS')

def removeMachine(machineName):
    log('Removing Machine')

    hardware = loadConfig('hardware')

    if hardware:
        i = 0
        for machine in hardware:
            if machine.name == machineName:
                break

            i += 1
    else:
        print 'No hardware currently configured'
        log('FAILURE')

    try:
        del hardware[i]
    except Exception as err:
        print 'Machine ' + machineName + ' does not exist'
        log('FAILURE')

    saveConfig('hardware', hardware)
    log('SUCCESS')


if __name__ == '__main__':
    cli()

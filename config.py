from __future__ import print_function
import socket
import pickle
from log import *
from admin import loadInstances

# Representation of a rack
class Rack:
    def __init__ (self, name, capacity):
        self.name = name
        self.capacity = capacity

    # Add a new machine to the configuration
    def save(self):
        with open('racks.pickle', 'ab') as file:
            pickle.dump(self, file)

# Representation of a physical server
class Machine:
    def __init__ (self, name, rack, ip, mem, numDisks, numVcpus):
        self.name = name
        self.rack = rack

        try:
            socket.inet_aton(ip)
            self.ip = ip
        except socket.error:
            raise Exception("Invalid IP address: " + ip)

        self.mem = mem
        self.numDisks = numDisks
        self.numVcpus = numVcpus

    # Add a new machine to the configuration
    def save(self):
        with open('hardware.pickle', 'ab') as file:
            pickle.dump(self, file)

# Representation of an OS option
class Image:
    def __init__ (self, name, size, path):
        self.name = name
        self.size = size
        self.path = path

    # Add a new image to the configuration
    def save(self):
        with open('images.pickle', 'ab') as file:
            pickle.dump(self, file)

# Representation of an virtual server option
class Flavor:
    def __init__ (self, name, mem, numDisks, numVcpus):
        self.name = name
        self.mem = mem
        self.numDisks = numDisks
        self.numVcpus = numVcpus

    # Add a new flavor to the configuration
    def save(self):
        with open('flavors.pickle', 'ab') as file:
            pickle.dump(self, file)

# Loads the instance from storage
# Type: hardware, images, or flavors
# Name: specific name of instance
def load(type, name):
    file = type + '.pickle'
    with open(file, 'rb') as file:
        while 1:
            try:
                obj = pickle.load(file)
                if obj.name == name:
                    break
            except EOFError:
                obj = 0
                break

    return obj

# Stores a configuration, overwriting the previous one
# Type: hardware, images, or flavors
# List: list of objects to be saved
def saveConfig(type, list):
    file = type + '.pickle'
    with open(file, 'wb') as file:
        for obj in list:
            pickle.dump(obj, file)

# Loads a configuration, returning a list of objects
# Type: hardware, images, or flavors
def loadConfig(type):
    file = type + '.pickle'
    objs = []

    try:
        with open(file, 'rb') as file:
            while 1:
                try:
                    objs.append(pickle.load(file))
                except EOFError:
                    break

        return objs
    except Exception as err:
        eprint(err)
        log('Error trying to load configuration file')
        return 0

# Prints the current hardware configuration
# This code uses repeat code from can_host, could use a function to get available hardware specs
def showHardware():
    objs = loadConfig('hardware')
    if objs:
        for obj in objs:
            instances = loadInstances(obj.name)

            for instance in instances:
                temp = load('flavors', instance["flavor"])
                obj.mem = int(obj.mem) - int(temp.mem)
                obj.numDisks = int(obj.numDisks) - int(temp.numDisks)
                obj.numVcpus = int(obj.numVcpus) - int(temp.numVcpus)

            print("%s %s %s %s %s %s" % (obj.name, obj.rack, obj.ip, obj.mem, obj.numDisks, obj.numVcpus))

# Prints the current image configuration
def showImages():
    objs = loadConfig('images')
    if objs:
        for obj in objs:
            print("%s %s %s" % (obj.name, obj.size, obj.path))

# Prints the current flavor configuration
def showFlavors():
    objs = loadConfig('flavors')
    if objs:
        for obj in objs:
            print("%s %s %s %s" % (obj.name, obj.mem, obj.numDisks, obj.numVcpus))

# Prints the current hardware, image, and flavor configurations
def showAll():
    print("\nHardware:")
    showHardware()
    print("\nImages:")
    showImages()
    print("\nFlavors:")
    showFlavors()
    print("\n")

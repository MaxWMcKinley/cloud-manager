from config import *
from os import path

# Checks if a specific server has the available resources to host the given flavor
def canHost(machine, flavor):
    machine = load('hardware', machine)
    flavor = load('flavors', flavor)
    instances = loadInstances(machine.name)

    for instance in instances:
        temp = load('flavors', instance["flavor"])
        machine.mem = int(machine.mem) - int(temp.mem)
        machine.numDisks = int(machine.numDisks) - int(temp.numDisks)
        machine.numVcpus = int(machine.numVcpus) - int(temp.numVcpus)

    can = True
    if int(machine.mem) < int(flavor.mem):
        can = False
    if int(machine.numDisks) < int(flavor.numDisks):
        can = False
    if int(machine.numVcpus) < int(flavor.numVcpus):
        can = False

    return can

def loadInstances(machine):
    file = 'instances.pickle'
    instances = []

    if path.isfile(file):
        with open(file, 'rb') as file:
            while 1:
                try:
                    obj = pickle.load(file)
                    if obj["machine"] == machine:
                        instances.append(obj)
                except EOFError:
                    break

    return instances
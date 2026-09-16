#!/usr/bin/python

"""
This example shows how to create a Mininet object and add nodes to it manually.
"""

# Importing Libraries
from mininet.net import Mininet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.term import makeTerms


# Function definition: This is called from the main function
def firstNetwork():

    # Create an empty network and add nodes to it.
    net = Mininet()

    info('*** Adding controller\n')
    net.addController('c0')

    info('*** Adding hosts\n')
    h1 = net.addHost('h1', ip='10.0.0.1')
    h2 = net.addHost('h2')

    info('*** Adding switch\n')
    s12 = net.addSwitch('s12')

    info('*** Creating links\n')
    net.addLink(h1, s12)
    net.addLink(h2, s12)

    info('*** Starting network\n')
    net.start()

    # Open an independent xterm for each host using Mininet's
    # built-in terminal handling.
    info('*** Starting xterm on hosts\n')
    net.terms += makeTerms([h1, h2], title='Host', term='xterm')

    info('*** Running the command line interface\n')
    CLI(net)

    info('*** Stopping network\n')
    net.stop()


# main Function: This is called when the Python file is run
if __name__ == '__main__':
    setLogLevel('info')
    firstNetwork()
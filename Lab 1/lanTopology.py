#!/usr/bin/python

"""
This example shows how to create a Mininet object and add nodes to it manually.
"""

"Importing Libraries"
from mininet.net import Mininet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.term import makeTerms


"Function definition: This is called from the main function"
def firstNetwork():

    "Create an empty network and add nodes to it."
    net = Mininet()

    info('*** Adding controller\n')
    net.addController('c0')

    info('*** Adding hosts\n')
    PC1 = net.addHost('PC1')

    info('*** Adding switch\n')
    s14 = net.addSwitch('s14')

    info('*** Creating links\n')
    net.addLink(PC1, s14)

    info('*** Starting network\n')
    net.start()

    "This is used to run commands on the hosts"

    info('*** Starting terminals on hosts\n')
    net.terms += makeTerms(
        [PC1],
        title='Host',
        term='xterm'
    )

    info('*** Running the command line interface\n')
    CLI(net)

    info('*** Stopping network\n')
    net.stop()


"main Function: This is called when the Python file is run"
if __name__ == '__main__':
    setLogLevel('info')
    firstNetwork()
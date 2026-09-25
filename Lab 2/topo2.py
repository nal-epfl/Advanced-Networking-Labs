#!/usr/bin/python
""" This example shows how to create a Mininet object and add nodes to
it manually.  """

"Importing Libraries"
from mininet.net import Mininet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.term import makeTerms

"Function definition:  This is called from the main function"
def firstNetwork():

	"Create an empty network and add nodes to it."
	net = Mininet()

	info( '*** Adding controller\n' ) 
	net.addController( 'c0' )

	info( '*** Adding hosts \n' )
	h1 = net.addHost( 'h1', ip='10.0.0.1/24' ) 
	h2 = net.addHost( 'h2', ip='10.0.0.2/24' )
	h3 = net.addHost( 'h3', ip='10.0.0.3/24' ) 
	h4 = net.addHost( 'h4', ip='10.0.0.4/24' ) 

	info( '*** Adding switches\n' ) 
	s1 = net.addSwitch( 's1' )
	s2 = net.addSwitch( 's2' )
	s3 = net.addSwitch( 's3' )

	info( '*** Creating links\n' ) 
	net.addLink( h1, s1 ) 
	net.addLink( h2, s1 )
	net.addLink( h3, s2 )
	net.addLink( h4, s3 )
	net.addLink( s1, s2 )
	net.addLink( s2, s3 )
	net.addLink( s1, s3 )

	info( '*** Starting network\n') 
	net.start()
	"This is used to run commands on the hosts"

	info( '*** Starting xterm on hosts\n' )
	net.terms += makeTerms(
		[h1, h2, h3, h4],
		title='Host',
		term='xterm'
	)

	info( '*** Running the command line interface\n' ) 
	CLI( net )

	info( '*** Stopping network' )
	net.stop()

"main Function: This is called when the Python file is run" 
if __name__ == '__main__':
	setLogLevel( 'info' )
	firstNetwork()
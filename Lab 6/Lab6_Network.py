#!/usr/bin/python3

""" Lab6 Topology """

"Importing Libraries"
import os
from mininet.net import Mininet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.term import makeTerms
from mininet.node import Controller, OVSSwitch

"Function definition:  This is called from the main function"
def Lab6_Network():

	dir_name = "/home/advnet/Desktop/lab6/"

	# In order to enable (disable) daemons on router, set the corresponding elements to 1 (0, resp.):
	#                        r1    r2    r3    r4    r5
	daemons = [[1,     1,     1,     1,    1],     # zebra
               [0,     0,     0,     0,    0],     # bgpd
               [0,     0,     0,     0,    0],     # ospfd
               [0,     0,     0,     0,    0]]     # ospf6d

	"Create an empty network and add nodes to it."
	net = Mininet()

	info( '*** Adding controller\n' )
	net.addController( 'c0' )

	info( '*** Adding hosts \n' )
	h1 = net.addHost( 'h1', ip='192.10.10.10/24')
	h2 = net.addHost( 'h2', ip='192.20.20.20/24')
	h5 = net.addHost( 'h5', ip='192.50.50.50/24')

	info( '*** Adding routers \n' )

	r1 = net.addHost( 'r1', ip='192.10.10.1/24' )
	r2 = net.addHost( 'r2', ip='192.20.20.2/24' )
	r3 = net.addHost( 'r3', ip='192.13.13.3/24' )
	r4 = net.addHost( 'r4', ip='192.24.24.4/24' )
	r5 = net.addHost( 'r5', ip='192.50.50.5/24' )

	routers = [r1, r2, r3, r4, r5]

	info( '*** Adding switches \n' )

	SW1 = net.addSwitch('SW1')
	SW2 = net.addSwitch('SW2')
	SW5 = net.addSwitch('SW5')
	SW12 = net.addSwitch('SW12')
	SW13 = net.addSwitch('SW13')
	SW24 = net.addSwitch('SW24')
	SW345 = net.addSwitch('SW345')

	SW1.cmd('ovs-vsctl set bridge SW1 protocols=OpenFlow13')
	SW2.cmd('ovs-vsctl set bridge SW2 protocols=OpenFlow13')
	SW5.cmd('ovs-vsctl set bridge SW5 protocols=OpenFlow13')
	SW12.cmd('ovs-vsctl set bridge SW12 protocols=OpenFlow13')
	SW13.cmd('ovs-vsctl set bridge SW13 protocols=OpenFlow13')
	SW24.cmd('ovs-vsctl set bridge SW24 protocols=OpenFlow13')
	SW345.cmd('ovs-vsctl set bridge SW345 protocols=OpenFlow13')

	info( '*** Creating links\n' )

	net.addLink( SW1, h1, intfName2='h1-eth1'  )
	net.addLink( SW1, r1, intfName2='r1-eth3'  )

	net.addLink( SW2, h2, intfName2='h2-eth1'  )
	net.addLink( SW2, r2, intfName2='r2-eth1'  )

	net.addLink( SW5, h5, intfName2='h5-eth1'  )
	net.addLink( SW5, r5, intfName2='r5-eth1'  )

	net.addLink( SW12, r1, intfName2='r1-eth2'  )
	net.addLink( SW12, r2, intfName2='r2-eth3'  )

	net.addLink( SW13, r1, intfName2='r1-eth1'  )
	net.addLink( SW13, r3, intfName2='r3-eth1'  )

	net.addLink( SW24, r2, intfName2='r2-eth2'  )
	net.addLink( SW24, r4, intfName2='r4-eth1'  )

	net.addLink( SW345, r3, intfName2='r3-eth2'  )
	net.addLink( SW345, r4, intfName2='r4-eth2'  )
	net.addLink( SW345, r5, intfName2='r5-eth2'  )

	r1.cmd('sysctl -w net.ipv4.conf.all.rp_filter=0')
	r2.cmd('sysctl -w net.ipv4.conf.all.rp_filter=0')
	r3.cmd('sysctl -w net.ipv4.conf.all.rp_filter=0')
	r4.cmd('sysctl -w net.ipv4.conf.all.rp_filter=0')
	r5.cmd('sysctl -w net.ipv4.conf.all.rp_filter=0')

	r1.cmd('sysctl -w net.ipv4.conf.r1-eth1.rp_filter=0')
	r1.cmd('sysctl -w net.ipv4.conf.r1-eth2.rp_filter=0')
	r1.cmd('sysctl -w net.ipv4.conf.r1-eth3.rp_filter=0')

	r2.cmd('sysctl -w net.ipv4.conf.r2-eth1.rp_filter=0')
	r2.cmd('sysctl -w net.ipv4.conf.r2-eth2.rp_filter=0')
	r2.cmd('sysctl -w net.ipv4.conf.r2-eth3.rp_filter=0')

	r3.cmd('sysctl -w net.ipv4.conf.r3-eth1.rp_filter=0')
	r3.cmd('sysctl -w net.ipv4.conf.r3-eth2.rp_filter=0')

	r4.cmd('sysctl -w net.ipv4.conf.r4-eth1.rp_filter=0')
	r4.cmd('sysctl -w net.ipv4.conf.r4-eth2.rp_filter=0')

	r5.cmd('sysctl -w net.ipv4.conf.r5-eth1.rp_filter=0')
	r5.cmd('sysctl -w net.ipv4.conf.r5-eth2.rp_filter=0')

	info( '*** Starting network\n')
	net.start()
	"This is used to run commands on the hosts"

	info( '*** Configuring hosts\n' )
	h1.cmd('ip route add default via 192.10.10.1')
	h2.cmd('ip route add default via 192.20.20.2')
	h5.cmd('ip route add default via 192.50.50.5')

	h1.cmd('ip -6 addr add 2001:1:0:1010::10/64 dev h1-eth1')
	h1.cmd('ip -6 route add default via 2001:1:0:1010::1')

	h2.cmd('ip -6 addr add 2001:1:0:2020::20/64 dev h2-eth1')
	h2.cmd('ip -6 route add default via 2001:1:0:2020::2')

	h5.cmd('ip -6 addr add 2001:1:0:5050::50/64 dev h5-eth1')
	h5.cmd('ip -6 route add default via 2001:1:0:5050::5')

	info( '*** Activating daemons \n' )

	k = 0
	for r in routers:
		if daemons[0][k] == 1:
			r.cmd('/usr/lib/frr/zebra -d -f ' + dir_name + 'configs/'+ 'zebra_r' + str(k+1) + '.cfg -i ' + dir_name + 'run/'+ 'zebra_r' + str(k+1) + '.pid -z ' + dir_name + 'run/'+ 'frr_r' + str(k+1) + '.api -u frr -g frr')
		if daemons[1][k] == 1:
			r.cmd('/usr/lib/frr/bgpd -d -f ' + dir_name + 'configs/'+ 'bgpd_r' + str(k+1) + '.cfg -i ' + dir_name + 'run/'+ 'bgpd_r' + str(k+1) + '.pid -z ' + dir_name + 'run/'+ 'frr_r' + str(k+1) + '.api -u frr -g frr')
		if daemons[2][k] == 1:
			r.cmd('/usr/lib/frr/ospfd -d -f ' + dir_name + 'configs/'+ 'ospfd_r' + str(k+1) + '.cfg -i ' + dir_name + 'run/'+'ospfd_r' + str(k+1) + '.pid -z ' + dir_name + 'run/'+ 'frr_r' + str(k+1) + '.api -u frr -g frr')
		if daemons[3][k] == 1:
			r.cmd('/usr/lib/frr/ospf6d -d -f ' + dir_name + 'configs/'+ 'ospf6d_r' + str(k+1) + '.cfg -i ' + dir_name + 'run/'+ 'ospf6d_r' + str(k+1) + '.pid -z ' + dir_name + 'run/'+ 'frr_r' + str(k+1) + '.api -u frr -g frr')
		k = k+1

	info( '*** Starting xterm on hosts\n' )
	net.terms += makeTerms(
		[h1, h2, h5] + routers,
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
	
	info('***Cleaning mininet...\n')
	os.system('sudo mn -c')
	
	info('*** Removing .pid and .api files\n')
	for item in os.listdir('/home/advnet/Desktop/lab6/run/'):
		if (item.endswith(".pid") or item.endswith(".api")):
			os.remove(os.path.join('/home/advnet/Desktop/lab6/run/', item))
	
	for item in os.listdir('/home/advnet/Desktop/lab6/logs/'):
		if (item.endswith(".log")):
			os.remove(os.path.join('/home/advnet/Desktop/lab6/logs/', item))

	info('***Killing zebra/bgpd/ospfd/ospf6d processes...\n')
	os.system('sudo pkill zebra')
	os.system('sudo pkill bgpd')
	os.system('sudo pkill ospfd')
	os.system('sudo pkill ospf6d')
	
	Lab6_Network()

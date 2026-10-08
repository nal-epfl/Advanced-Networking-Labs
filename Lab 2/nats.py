#!/usr/bin/python
"""
Lab 2 NAT types topology.
"""

from mininet.net import Mininet
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.term import makeTerms


class NATTypesCLI(CLI):
    """Mininet prompt commands specific to this activity."""

    def do_setupnat(self, _line):
        """Install the final port-restricted UDP NAT."""
        PC4 = self.mn.get('PC4')

        commands = [
            'sysctl -w net.ipv4.ip_forward=1',
            'iptables -F',
            'iptables -t nat -F',
            'iptables -P FORWARD DROP',
            # TCP control mapping: intentionally no remote-endpoint restriction.
            'iptables -A FORWARD -i PC4-eth0 -o PC4-eth1 -p tcp -j ACCEPT',
            'iptables -A FORWARD -i PC4-eth1 -o PC4-eth0 -p tcp '
            '-d 10.10.10.1 --dport 40000 -j ACCEPT',
            'iptables -t nat -A POSTROUTING -s 10.10.10.1 -o PC4-eth1 '
            '-p tcp --sport 40000 -j SNAT --to-source 128.178.122.4:41000',
            'iptables -t nat -A PREROUTING -i PC4-eth1 -d 128.178.122.4 '
            '-p tcp --dport 41000 -j DNAT --to-destination 10.10.10.1:40000',
            # A UDP reply is forwarded only after PC1 contacts its endpoint.
            'iptables -A FORWARD -i PC4-eth0 -o PC4-eth1 -p udp -j ACCEPT',
            'iptables -A FORWARD -i PC4-eth1 -o PC4-eth0 -p udp '
            '-m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT',
            'iptables -t nat -A POSTROUTING -s 10.10.10.1 -o PC4-eth1 '
            '-p udp --sport 40000 -j SNAT --to-source 128.178.122.4:41000',
            'iptables -t nat -A PREROUTING -i PC4-eth1 -d 128.178.122.4 '
            '-p udp --dport 41000 -j DNAT --to-destination 10.10.10.1:40000',
        ]

        for command in commands:
            PC4.cmd(command)

        info('*** Port-restricted UDP NAT is ready.\n')

    def do_sendUDP(self, line):
        """Send PC1's initial UDP packet to PC2's supplied source port."""
        try:
            port = int(line.strip())
            if not 1 <= port <= 65535:
                raise ValueError
        except ValueError:
            info('*** Usage: sendUDP <PC2-UDP-source-port>\n')
            return

        PC1 = self.mn.get('PC1')
        output = PC1.cmd(
            'python3 -c "import socket; '
            's=socket.socket(socket.AF_INET, socket.SOCK_DGRAM); '
            's.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1); '
            's.bind((\'\', 40000)); '
            's.sendto(b\'temp\', (\'128.178.122.2\', ' + str(port) + ')); '
            's.close()"'
        )
        if output:
            info('*** sendUDP failed:\n%s' % output)
            return
        info('*** PC1 sent a packet to PC2 UDP port %d.\n' % port)


def natTypesNetwork():
    net = Mininet()

    info('*** Adding controller\n')
    net.addController('c0')

    info('*** Adding hosts\n')
    PC1 = net.addHost('PC1', ip='10.10.10.1/24')
    PC2 = net.addHost('PC2', ip='128.178.122.2/24')
    PC3 = net.addHost('PC3', ip='128.178.122.3/24')
    PC4 = net.addHost('PC4', ip='10.10.10.4/24')

    info('*** Adding switches\n')
    s14 = net.addSwitch('s14')
    s24 = net.addSwitch('s24')

    info('*** Creating links\n')
    net.addLink(PC1, s14)
    net.addLink(PC4, s14, intfName1='PC4-eth0')
    net.addLink(PC2, s24)
    net.addLink(PC3, s24)
    net.addLink(PC4, s24, intfName1='PC4-eth1')

    info('*** Starting network\n')
    net.start()

    # PC4 has one private-side and one public-side interface.
    PC4.cmd('ip addr add 128.178.122.4/24 dev PC4-eth1')
    PC1.cmd('ip route replace default via 10.10.10.4')

    info('*** Topology is ready\n')
    info('*** PC1 private: 10.10.10.1\n')
    info('*** PC4 public:  128.178.122.4\n')
    info('*** PC2 peer:    128.178.122.2\n')
    info('*** PC3 STUN:    128.178.122.3\n')
    info('*** Open terminals with: xterm PC1 PC2 PC3 PC4\n')
    info('*** helpers: setupnat,  sendUDP <PC2-UDP-port>\n')

    net.terms += makeTerms(
        [PC1, PC2, PC3, PC4],
        title='Host',
        term='xterm'
    )

    NATTypesCLI(net)
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    natTypesNetwork()

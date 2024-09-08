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


import os
import subprocess

from sciveo.common.tools.logger import *


class WireGuardBase:
  def __init__(self, interface='wg0'):
    self.interface = interface
    self.config_path = f'/etc/wireguard/{self.interface}.conf'
    self.private_key = None
    self.public_key = None

  def _run_command(self, command):
    try:
      result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
      return result.stdout.decode().strip()
    except subprocess.CalledProcessError as e:
      debug(type(self).__name__, f"Error executing command: {e.stderr.decode().strip()}")
      return None

  def generate_keys(self, private_key_path=None, public_key_path=None):
    # Generate the private key
    self.private_key = self._run_command("wg genkey")
    if not self.private_key:
      raise Exception("Failed to generate private key.")

    # Generate the public key from the private key
    self.public_key = self._run_command(f"echo {self.private_key} | wg pubkey")
    if not self.public_key:
      raise Exception("Failed to generate public key.")

    # Optionally save the keys to files
    if private_key_path:
      with open(private_key_path, 'w') as f:
        f.write(self.private_key)
      debug(type(self).__name__, f"Private key saved to {private_key_path}")

    if public_key_path:
      with open(public_key_path, 'w') as f:
        f.write(self.public_key)
      debug(type(self).__name__, f"Public key saved to {public_key_path}")

    return self.private_key, self.public_key

  def start(self):
    debug(type(self).__name__, f"Starting WireGuard interface {self.interface}...")
    return self._run_command(f'sudo systemctl start [email protected]{self.interface}')

  def stop(self):
    debug(type(self).__name__, f"Stopping WireGuard interface {self.interface}...")
    return self._run_command(f'sudo systemctl stop [email protected]{self.interface}')

  def restart(self):
    debug(type(self).__name__, f"Restarting WireGuard interface {self.interface}...")
    return self._run_command(f'sudo systemctl restart [email protected]{self.interface}')

  def status(self):
    debug(type(self).__name__, f"Checking status of WireGuard interface {self.interface}...")
    return self._run_command(f'sudo systemctl status [email protected]{self.interface}')

class WGServer(WireGuardBase):
  def init(self, private_key=None, listen_port=51820, address='192.168.21.1/24'):
    if not private_key:
      private_key = self.private_key
    config = f"""
    [Interface]
    Address = {address}
    ListenPort = {listen_port}
    PrivateKey = {private_key}
    SaveConfig = true
    """
    with open(self.config_path, 'w') as config_file:
      config_file.write(config.strip())
    debug(type(self).__name__, f"Server configuration written to {self.config_path}")

  def add_peer(self, peer_public_key, allowed_ips):
    peer_config = f"""
    [Peer]
    PublicKey = {peer_public_key}
    AllowedIPs = {allowed_ips}
    """
    with open(self.config_path, 'a') as config_file:
      config_file.write(peer_config.strip())
    debug(type(self).__name__, f"Added peer with PublicKey: {peer_public_key}")

class WGClient(WireGuardBase):
  def init(self, private_key=None, server_public_key=None, endpoint=None, address='192.168.21.2/24', allowed_ips='0.0.0.0/0', keepalive=25):
    if not private_key:
      private_key = self.private_key
    config = f"""
    [Interface]
    Address = {address}
    PrivateKey = {private_key}

    [Peer]
    PublicKey = {server_public_key}
    Endpoint = {endpoint}
    AllowedIPs = {allowed_ips}
    PersistentKeepalive = {keepalive}
    """
    with open(self.config_path, 'w') as config_file:
      config_file.write(config.strip())
    debug(type(self).__name__, f"Client configuration written to {self.config_path}")


if __name__ == "__main__":
  server = WGServer(interface='wg0')
  server.generate_keys(private_key_path='/etc/wireguard/server_private.key', public_key_path='/etc/wireguard/server_public.key')
  server.init(private_key=server.private_key, listen_port=51820, address='192.168.21.1/24')
  server.add_peer(peer_public_key='<client_public_key>', allowed_ips='192.168.21.2/32')
  server.start()
  debug(type(self).__name__, server.status())

  # client = WGClient(interface='wg0')
  # client.generate_keys(private_key_path='/etc/wireguard/client_private.key', public_key_path='/etc/wireguard/client_public.key')
  # client.init(private_key=client.private_key, server_public_key='<server_public_key>', endpoint='<server_ip>:51820')
  # client.start()
  # debug(type(self).__name__, client.status())

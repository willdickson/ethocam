import os
import sys
import time
import socket
import paramiko
import scp


class TransferAgent:


    def __init__(self, config, data_dir):

        self.remote_user = config['Network']['remote_user']
        self.remote_host = config['Network']['remote_host']
        self.remote_path = config['Network']['remote_path']
        self.ssh_key_file = config['Network']['ssh_key_file']
        self.ssh_known_hosts = config['Network']['ssh_known_hosts']
        self.ssh_port = config['Network'].getint('ssh_port')
        self.ssh_max_attempt = config['Network'].getint('ssh_max_attempt')
        self.ssh_attempt_dt = config['Network'].getfloat('ssh_attempt_dt')
        self.video_file = config['Video']['filename']
        self.sensor_file = config['Sensor']['filename']
        self.data_dir = data_dir

        # Add hostname to remote path
        hostname = socket.gethostname()
        self.remote_path = os.path.join(self.remote_path,hostname)

        # Create ssh and scp clients
        #self.ok = self.remote_host and self.remote_path and self.remote_user
        num_attempt = 0
        self.ssh = paramiko.SSHClient()
        self.ok = False
        while (not self.ok) or (num_attempt < self.ssh_max_attempt):
            try:
                self.ssh.load_system_host_keys(filename=self.ssh_known_hosts)
                self.ssh.connect(
                        self.remote_host,
                        port=self.ssh_port,
                        username=self.remote_user,
                        key_filename=self.ssh_key_file
                        ) 
                self.ok = True
            except socket.gaierror as e:
                print('TransferAgent: {}'.format(e), file=sys.stderr)
                time.sleep(self.ssh_attempt_dt)
            num_attempt += 1

        if self.ok: 
            self.scp = scp.SCPClient(self.ssh.get_transport())
        else:
            self.ssh = None
            self.scp = None

    def send_data_directory(self):
        if self.ok:
            self.scp.put(self.data_dir, recursive=True, remote_path=self.remote_path)

    def send_video_file(self): 
        if self.ok:
            _, data_subdir = os.path.split(self.data_dir)
            remote_path = os.path.join(self.remote_path, data_subdir)
            video_file = os.path.join(self.data_dir, self.video_file)
            self.scp.put(video_file, recursive=True, remote_path=remote_path)

    def send_sensor_file(self):
        if self.ok:
            _, data_subdir = os.path.split(self.data_dir)
            remote_path = os.path.join(self.remote_path, data_subdir)
            sensor_file = os.path.join(self.data_dir, self.sensor_file)
            self.scp.put(sensor_file, recursive=True, remote_path=remote_path)

    def close(self):
        if self.ok:
            self.scp.close()
            self.ssh.close()



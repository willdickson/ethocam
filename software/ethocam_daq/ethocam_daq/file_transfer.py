import os
import socket
import paramiko
import scp


class TransferAgent:

    def __init__(self, config, data_dir):

        self.remote_user = config['Network']['remote_user']
        self.remote_host = config['Network']['remote_host']
        self.remote_path = config['Network']['remote_path']
        self.video_file = config['Video']['filename']
        self.sensor_file = config['Sensor']['filename']
        self.data_dir = data_dir

        # Add hostname to remote path
        hostname = socket.gethostname()
        self.remote_path = os.path.join(self.remote_path,hostname)

        # Create ssh and scp clients
        self.ok = self.remote_host and self.remote_path and self.remote_user
        if self.ok:
            self.ssh = paramiko.SSHClient()
            self.ssh.load_system_host_keys()
            self.ssh.connect(self.remote_host,username=self.remote_user)
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



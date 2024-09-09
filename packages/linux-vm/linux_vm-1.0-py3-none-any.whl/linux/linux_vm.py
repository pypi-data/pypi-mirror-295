import subprocess

def create_linux_vm():
    """Create a new Docker container running Ubuntu as a Linux VM."""
    subprocess.run(["docker", "run", "-d", "--name", "linux-vm", "ubuntu:latest"], check=True)

def start_linux_vm():
    """Start the Docker container."""
    subprocess.run(["docker", "start", "linux-vm"], check=True)

def stop_linux_vm():
    """Stop the Docker container."""
    subprocess.run(["docker", "stop", "linux-vm"], check=True)
import subprocess


def check_device_status(ip_address):
    """
    Return 'online' if ip_address (str) responds to a ping request, else 'offline'.
    """
    # Ping parameters as list of strings
    args = ["ping", "-n", "1", "-w", "1000", ip_address]
    try:
        response = subprocess.check_output(args)
    except subprocess.CalledProcessError:
        return 'offline'
    return 'online' if b"TTL=" in response else 'offline'



import paramiko
import sshtunnel

REMOTE_SERVER_IP = "xxx"
REMOTE_USERNAME = "xxx"
REMOTE_PASSWORD = "xxx"
REMOTE_PRIVATE_TUNNEL_PORT = 10022
PRIVATE_SERVER_IP = "xxx"
PRIVATE_USERNAME = "xxx"
PRIVATE_PASSWORD = "xxx"
PRIVATE_COMMAND = "ls -al"

with sshtunnel.open_tunnel(
    (REMOTE_SERVER_IP, 22),
    ssh_username=REMOTE_USERNAME,
    ssh_password=REMOTE_PASSWORD,
    remote_bind_address=(PRIVATE_SERVER_IP, 22),
    local_bind_address=('0.0.0.0', REMOTE_PRIVATE_TUNNEL_PORT)
) as tunnel:
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect('127.0.0.1', port=REMOTE_PRIVATE_TUNNEL_PORT, username=PRIVATE_USERNAME, password=PRIVATE_PASSWORD)
    # execute command in private server
    (stdin, stdout, stderr) = client.exec_command(PRIVATE_COMMAND)
    for line in stdout.readlines():
        print(line, end="") #print without newline
    client.close()

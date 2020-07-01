# Colorama used for coloring of terminal
from colorama import Fore, Back, init
# Netmiko used to connect to devices
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException, NetMikoAuthenticationException
# Datetime used to timestamp files
import datetime
# Getpass for asking for password from user
import getpass

# Get current time in ISO format
time_now = datetime.datetime.now().isoformat(timespec="seconds")

# Initialize colorama and reset style by default
init(autoreset=True)

def read_from_filename(filename):
    """Returns all lines from filename as a list

    Parameters:
    filename - name of the file to read

    Returns:
    list: lines
    """
    with open(filename) as f:
        lines = f.read().splitlines()
        return lines

def get_credentials():
    """Get username and password from user
    
    Parameters:

    Returns:
    str: username
    str: password
    
    """
    username = input("Enter username: ")
    password = getpass.getpass()
    return username, password

def connect_and_send(devices_lines, config_lines, username, password):
    """Connect, run show commands, and save the output
    
    Parameters:
    devices_lines - devices to connect to, gathered from read_devices()
    config_lines - commands to run, gathered from read_commands()
    username - username for logging in to device, gathered from get_credentials()
    password - password for logging in to device, gathered from get_credentials()

    Returns:

    """
    for ip in devices_lines:
        device = { 
            "device_type": "cisco_ios",
            "ip": ip,
            "username": username,
            "password": password
        }
        try:
            print(Fore.MAGENTA + "=" * 70)
            print(Fore.CYAN + "" * 15 + " Connecting to Device: " + ip)
            print(Fore.MAGENTA + "=" * 70)
            net_connect = ConnectHandler(**device)
            print(Fore.MAGENTA + "~" * 70)
            print(Fore.CYAN + "" * 15 + " Now connected to Device: " + ip)
            print(Fore.CYAN + "" * 15 + " Sending commands ")
            print(Fore.CYAN + "" * 15 + " Saving output to: " + ip +"_" + time_now)
            print(Fore.MAGENTA + "~" * 70)
            # Open file to write to
            filename = ip + "_" + time_now + ".txt"
            with open(filename, "w") as f:
                for command in config_lines:
                    f.write("=" * 20)
                    f.write(command)
                    f.write("=" * (80 - len(command)))
                    f.write("\n" * 2)
                    cmd_output = net_connect.send_command(command)
                    f.write(cmd_output + "\n" *2)

        except (NetMikoTimeoutException, NetMikoAuthenticationException) as e:
            print(Fore.RED + "~" * 15 + str(e) + "~" * 15)

if __name__ == "__main__":
    # Get all commands
    config_lines = read_from_filename("commands.txt")
    # Get all devices
    devices_lines = read_from_filename("devices.txt")
    # Get credentials
    username, password = get_credentials()
    # Connect and save
    connect_and_send(devices_lines, config_lines, username, password)


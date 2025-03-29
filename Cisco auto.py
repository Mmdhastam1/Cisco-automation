from netmiko import ConnectHandler

def connect_to_switch(host, username, password, secret):
    return ConnectHandler(
        device_type="cisco_ios",
        host=host,
        username=username,
        password=password,
        secret=secret
    )

def get_interfaces(connection):
    output = connection.send_command("show interfaces status")
    print("Interface Status:")
    print(output)

def get_vlan_info(connection, vlan_id):
    output = connection.send_command(f"show vlan id {vlan_id}")
    print(f"VLAN {vlan_id} Information:")
    print(output)

def configure_vlan(connection):
    vlan_id = input("Enter VLAN ID: ")
    vlan_name = input("Enter VLAN Name: ")
    commands = [
        f"vlan {vlan_id}",
        f"name {vlan_name}"
    ]
    connection.send_config_set(commands)
    print(f"VLAN {vlan_id} configured successfully.")

def configure_interface(connection):
    interface = input("Enter Interface (e.g., GigabitEthernet0/1): ")
    commands = []
    while True:
        cmd = input("Enter command (type 'exit' to finish): ")
        if cmd.lower() == "exit":
            break
        commands.append(cmd)
    connection.send_config_set([f"interface {interface}"] + commands)
    print(f"Configuration applied to {interface}.")

def turn_off_interface(connection):
    output = connection.send_command("show interfaces status")
    print("Interface List:")
    print(output)
    interface = input("Enter interface to turn off: ")
    connection.send_config_set([f"interface {interface}", "shutdown"])
    print(f"Interface {interface} has been turned off.")

def main():
    host = input("Enter switch IP: ")
    username = input("Enter username: ")
    password = input("Enter password: ")
    secret = input("Enter enable password: ")
    
    try:
        connection = connect_to_switch(host, username, password, secret)
        connection.enable()
        
        while True:
            command = input("Enter command (Eth, VLAN, confV, confE, offeth, exit): ")
            if command.lower() == "eth":
                get_interfaces(connection)
            elif command.lower().startswith("vlan"):
                vlan_id = command.split()[1] if len(command.split()) > 1 else input("Enter VLAN ID: ")
                get_vlan_info(connection, vlan_id)
            elif command.lower() == "confv":
                configure_vlan(connection)
            elif command.lower() == "confe":
                configure_interface(connection)
            elif command.lower() == "offeth":
                turn_off_interface(connection)
            elif command.lower() == "exit":
                break
            else:
                print("Invalid command.")
        
        connection.disconnect()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

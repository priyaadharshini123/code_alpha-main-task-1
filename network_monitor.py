import psutil
import subprocess
import time

# Function to get active network connections using psutil
def get_network_connections():
    print("Monitoring network connections...\n")
    try:
        while True:
            print("Active connections:")
            for conn in psutil.net_connections(kind='inet'):
                print(f"Local Address: {conn.laddr}, Remote Address: {conn.raddr}, Status: {conn.status}")
            time.sleep(5)  # Repeat every 5 seconds
    except KeyboardInterrupt:
        print("\nMonitoring stopped.")

# Function to get the current open ports using netstat
def monitor_open_ports():
    print("\nMonitoring open ports using netstat... Press CTRL+C to stop")
    try:
        while True:
            # Running netstat to see all open ports
            result = subprocess.run(['netstat', '-an'], stdout=subprocess.PIPE)
            print(result.stdout.decode())  # Display result from netstat
            time.sleep(10)  # Wait for 10 seconds before repeating
    except KeyboardInterrupt:
        print("\nStopped monitoring open ports.")

# Main program to choose between network connections or open ports
def main():
    print("Choose monitoring option:")
    print("1. Monitor Network Connections (Active IPs & Ports)")
    print("2. Monitor Open Ports (using netstat)")

    choice = input("Enter your choice (1 or 2): ")

    if choice == "1":
        get_network_connections()  # Monitor network connections
    elif choice == "2":
        monitor_open_ports()  # Monitor open ports using netstat
    else:
        print("Invalid option, please enter 1 or 2.")

# Start the program
if __name__ == "__main__":
    main()

import socket
import csv

# Get the local IP address and subnet mask
ip_address = socket.gethostbyname(socket.gethostname())
subnet_mask = socket.inet_ntoa(socket.inet_aton(ip_address) & socket.inet_aton("255.255.255.0"))

# Calculate the network address from the IP address and subnet mask
network_address = socket.inet_ntoa(socket.inet_aton(ip_address) & socket.inet_aton(subnet_mask))

# Split the network address into individual octets
octets = network_address.split(".")

# Calculate the range of IP addresses in the network
start_ip = octets[0] + "." + octets[1] + "." + octets[2] + ".1"
end_ip = octets[0] + "." + octets[1] + "." + octets[2] + ".254"

# Define the range of ports to scan
start_port = 1
end_port = 1024

# Open the output CSV file for writing
with open("ports.csv", "w") as csvfile:
  # Create a CSV writer
  writer = csv.writer(csvfile)

  # Write the CSV header row
  writer.writerow(["IP Address", "Port", "Service"])

  # Loop through the IP addresses in the network
  for i in range(start_ip, end_ip):
    # Get the current IP address
    ip_address = f"{octets[0]}.{octets[1]}.{octets[2]}.{i}"

    # Loop through the ports
    for port in range(start_port, end_port + 1):
      # Try to connect to the port on the IP address
      try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip_address, port))
        s.close()
      except:
        # The port is not open
        continue

      # Try to get the service name for the open port
      try:
        service = socket.getservbyport(port)
      except:
        service = ""

      # Write the IP address, port, and service name to the CSV file
      writer.writerow([ip_address, port, service])

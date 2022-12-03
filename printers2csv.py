import socket
import csv

# Define the subnet to scan
subnet = "192.168.0.0/24"

# Split the subnet into individual IP addresses
addresses = subnet.split("/")[0].split(".")
prefix = int(subnet.split("/")[1])

# Calculate the range of IP addresses in the subnet
start_ip = int(addresses[3]) + 1
end_ip = 2**(32 - prefix) + start_ip

# Open the output CSV file for writing
with open("printers.csv", "w") as csvfile:
  # Create a CSV writer
  writer = csv.writer(csvfile)

  # Write the CSV header row
  writer.writerow(["IP Address", "Hostname", "Model"])

  # Loop through the IP addresses in the subnet
  for i in range(start_ip, end_ip):
    # Get the current IP address
    ip_address = f"{addresses[0]}.{addresses[1]}.{addresses[2]}.{i}"

    # Try to get the hostname of the IP address
    try:
      hostname = socket.gethostbyaddr(ip_address)[0]
    except:
      hostname = ""

    # Try to get the printer model of the IP address
    try:
      s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      s.connect((ip_address, 9100))
      s.send(b"\x1b\x1d\x61\x01")
      printer_model = s.recv(1024).decode("utf-8")
      s.close()
    except:
      printer_model = ""

    # Write the IP address, hostname, and printer model to the CSV file
    writer.writerow([ip_address, hostname, printer_model])

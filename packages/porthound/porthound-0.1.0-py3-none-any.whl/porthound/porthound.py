import socket
import argparse
import sys
from colorama import init, Fore

init()
GREEN = Fore.GREEN
RESET = Fore.RESET

class CustomArgumentParser(argparse.ArgumentParser):
    def format_help(self):
        """help menu."""
        help_text = """
PortHound Scanner

Available options:
  -H HOST, --host HOST  The host IP address to scan (required)
  -p PORTS, --ports PORTS
                        Port range to scan (e.g., 1-1024, default: 1-1024)
  -h, --help            Show this help message

Usage examples:
  python3 porthound.py -H 192.168.1.1
  python3 porthound.py -H 192.168.1.1 -p 80-443

        """
        return help_text

def is_port_open(host, port):
    """determine port status."""
    s = socket.socket()
    try:
        s.settimeout(0.2)
        s.connect((host, port))
    except:
        return False
    else:
        return True
    finally:
        s.close()

def validate_port_range(port_range):
    """port range validation."""
    try:
        start, end = map(int, port_range.split('-'))
        if 1 <= start <= end <= 65535:
            return start, end
        raise ValueError
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid port range: {port_range}. Format should be start-end (e.g., 1-1024) with max value of 65535.")

def parse_arguments():
    """parse arguments"""
    parser = CustomArgumentParser(add_help=False)
    parser.add_argument("-H", "--host", help="The host IP address to scan.")
    parser.add_argument("-p", "--ports", type=validate_port_range, default="1-1024", help="Port range to scan (e.g., 1-1024, default: 1-1024).")
    parser.add_argument("-h", "--help", action="help", help="Shows this help message.")
    
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    
    args = parser.parse_args()
    
    if not args.host:
        print("Error: Please specify a target host using the -H or --host option.")
        sys.exit(1)
    
    return args

def main():
    args = parse_arguments()
    start_port, end_port = args.ports
    
    print(f"\nScanning {args.host} for open ports from {start_port} to {end_port}...\n")

    # check for any open ports.
    open_ports_found = False
    for port in range(start_port, end_port + 1):
        if is_port_open(args.host, port):
            print(f"{GREEN}[+] {args.host}:{port} is open {RESET}")
            open_ports_found = True

    if not open_ports_found:
        print(f"{Fore.YELLOW}No open ports found.{RESET}")

    print("\nScan completed.\n")

if __name__ == "__main__":
    main()
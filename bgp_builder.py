"""
Cisco BGP Configuration Builder

This script generates a basic Cisco IOS BGP configuration.

It supports:
- Local autonomous system number
- Router ID
- Multiple BGP neighbors
- Neighbor descriptions
- Multiple advertised networks
- Optional text-file export

This script does not connect to a network device.
"""

import ipaddress
from pathlib import Path


def get_as_number(prompt):
    """Validate and return a BGP autonomous system number."""

    while True:
        value = input(prompt).strip()

        if not value.isdigit():
            print("Enter a valid numeric AS number.")
            continue

        as_number = int(value)

        if 1 <= as_number <= 4294967295:
            return as_number

        print("AS number must be between 1 and 4294967295.")


def get_ipv4_address(prompt):
    """Validate and return an IPv4 address."""

    while True:
        value = input(prompt).strip()

        try:
            address = ipaddress.IPv4Address(value)
            return str(address)

        except ipaddress.AddressValueError:
            print("Enter a valid IPv4 address, such as 10.1.1.1.")


def get_ipv4_network(prompt):
    """Validate and return an IPv4 network and subnet mask."""

    while True:
        value = input(prompt).strip()

        try:
            network = ipaddress.IPv4Network(value, strict=False)

            return {
                "network_address": str(network.network_address),
                "subnet_mask": str(network.netmask),
            }

        except ValueError:
            print("Enter a valid IPv4 network in CIDR format.")
            print("Example: 192.168.10.0/24")


def get_yes_no(prompt):
    """Return True for yes and False for no."""

    while True:
        answer = input(prompt).strip().lower()

        if answer in ["y", "yes"]:
            return True

        if answer in ["n", "no"]:
            return False

        print("Enter y or n.")


def collect_neighbors():
    """Collect one or more BGP neighbor configurations."""

    neighbors = []

    print("\n--- BGP Neighbors ---")

    while True:
        neighbor_ip = get_ipv4_address(
            "\nNeighbor IP address: "
        )

        remote_as = get_as_number(
            "Neighbor remote AS number: "
        )

        description = input(
            "Neighbor description, or press Enter to skip: "
        ).strip()

        neighbors.append(
            {
                "ip_address": neighbor_ip,
                "remote_as": remote_as,
                "description": description,
            }
        )

        if not get_yes_no("Add another neighbor? (y/n): "):
            break

    return neighbors


def collect_networks():
    """Collect networks that BGP should advertise."""

    networks = []

    print("\n--- Advertised Networks ---")

    while True:
        network = get_ipv4_network(
            "\nNetwork to advertise, such as 192.168.10.0/24: "
        )

        networks.append(network)

        if not get_yes_no("Add another network? (y/n): "):
            break

    return networks


def build_bgp_configuration(
    local_as,
    router_id,
    neighbors,
    networks,
):
    """Build the Cisco IOS BGP configuration."""

    configuration = []

    configuration.append(f"router bgp {local_as}")
    configuration.append(f" bgp router-id {router_id}")
    configuration.append(" bgp log-neighbor-changes")

    for neighbor in neighbors:
        neighbor_ip = neighbor["ip_address"]
        remote_as = neighbor["remote_as"]
        description = neighbor["description"]

        if description:
            configuration.append(
                f" neighbor {neighbor_ip} description {description}"
            )

        configuration.append(
            f" neighbor {neighbor_ip} remote-as {remote_as}"
        )

    for network in networks:
        network_address = network["network_address"]
        subnet_mask = network["subnet_mask"]

        configuration.append(
            f" network {network_address} mask {subnet_mask}"
        )

    configuration.append("exit")

    return "\n".join(configuration)


def save_configuration(configuration):
    """Save the generated BGP configuration to a text file."""

    filename = input(
        "\nEnter the filename without an extension: "
    ).strip()

    if not filename:
        filename = "bgp_configuration"

    safe_filename = "".join(
        character
        for character in filename
        if character.isalnum() or character in ["-", "_"]
    )

    if not safe_filename:
        safe_filename = "bgp_configuration"

    output_path = Path(f"{safe_filename}.txt")

    try:
        output_path.write_text(
            configuration + "\n",
            encoding="utf-8",
        )

        print(
            f"\nConfiguration saved to: "
            f"{output_path.resolve()}"
        )

    except OSError as error:
        print(f"\nUnable to save the file: {error}")


def main():
    """Run the Cisco BGP Configuration Builder."""

    print("=" * 55)
    print("          CISCO BGP CONFIGURATION BUILDER")
    print("=" * 55)

    local_as = get_as_number(
        "\nLocal AS number: "
    )

    router_id = get_ipv4_address(
        "BGP router ID: "
    )

    neighbors = collect_neighbors()
    networks = collect_networks()

    configuration = build_bgp_configuration(
        local_as,
        router_id,
        neighbors,
        networks,
    )

    print("\n" + "=" * 55)
    print("GENERATED CISCO BGP CONFIGURATION")
    print("=" * 55)
    print()
    print(configuration)

    if get_yes_no(
        "\nSave configuration to a text file? (y/n): "
    ):
        save_configuration(configuration)

    print("\nBGP configuration generation complete.")


if __name__ == "__main__":
    main()
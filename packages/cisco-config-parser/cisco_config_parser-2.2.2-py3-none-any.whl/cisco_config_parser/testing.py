import re

cfg_section = """
router bgp 65240
 bgp router-id 10.240.129.45
 bgp log-neighbor-changes
 timers bgp 3 10
 neighbor SHC_RR peer-group
 neighbor LPCH_PEERS peer-group
 neighbor SHC_RR remote-as 65240
 neighbor SHC_RR update-source Loopback1
 neighbor SHC_RR timers 7 21
 neighbor 10.252.248.251 peer-group SHC_RR
 neighbor 10.252.248.251 description STNNC-420-RR-1 
 neighbor 10.252.248.252 peer-group SHC_RR
 neighbor 10.252.248.252 description STNMC-FOR-RR-2 
 neighbor 10.252.248.253 peer-group SHC_RR
 neighbor 10.252.248.253 description STNMC-FOR-RR-3

 address-family ipv4
  bgp nexthop trigger delay 4
  bgp scan-time 5
  neighbor SHC_RR send-community both
  network 10.245.49.132 mask 255.255.255.255
  neighbor 10.252.248.251 activate
  neighbor 10.252.248.252 activate
  neighbor 10.252.248.253 activate
 exit-address-family
"""

# Compile regex patterns
peer_group_regex = re.compile(r"neighbor (\S+) peer-group")
remote_as_regex = re.compile(r"neighbor (\S+) remote-as (\d+)")
update_source_regex = re.compile(r"neighbor (\S+) update-source (\S+)")
neighbor_ip_regex = re.compile(r"neighbor (\d+\.\d+\.\d+\.\d+) peer-group (\S+)")
neighbor_desc_regex = re.compile(r"neighbor (\d+\.\d+\.\d+\.\d+) description (.+)")

# Parsing peer groups
peer_groups = peer_group_regex.findall(cfg_section)
peer_group_details = []

for pg in peer_groups:
    details = {
        "peer_group": {
            "name": pg,
            "remote_as": "",
            "update_source": "",
            "route-map": {"in": "", "out": ""},
            "neighbors": []
        }
    }
    # Remote AS
    ras = remote_as_regex.search(cfg_section)
    if ras and ras.group(1) == pg:
        details["peer_group"]["remote_as"] = ras.group(2)

    # Update Source
    ups = update_source_regex.search(cfg_section)
    if ups and ups.group(1) == pg:
        details["peer_group"]["update_source"] = ups.group(2)

    # Neighbors
    for nip in neighbor_ip_regex.finditer(cfg_section):
        if nip.group(2) == pg:
            neighbor_info = {
                "ip": nip.group(1),
                "description": ""
            }
            # Description
            ndesc = neighbor_desc_regex.search(cfg_section)
            if ndesc and ndesc.group(1) == nip.group(1):
                neighbor_info["description"] = ndesc.group(2)
            details["peer_group"]["neighbors"].append(neighbor_info)

    peer_group_details.append(details)

# Output the structured data
import json

print(json.dumps(peer_group_details, indent=2))

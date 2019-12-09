ospf_route = 'O        10.0.24.0/24 [110/41] via 10.0.13.3, 3d18h, FastEthernet0/0'
ospf_route = ospf_route.split()
print('{:25}{:15}\n{:25}{:15}\n{:25}{:15}\n{:25}{:15}\n{:25}{:15}\n{:25}{:15}\n'.format('Protocol:', 'OSPF', 'Prefix:', ospf_route[1], 'AD/Metric:', ospf_route[2].strip('[]'), 'Next-Hop:', ospf_route[4].strip(','), 'Last update:', ospf_route[5].strip(','), 'Outbound Interface:', ospf_route[6]))

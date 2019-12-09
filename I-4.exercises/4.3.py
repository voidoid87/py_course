config = 'switchport trunk allowed vlan 1,3,10,20,30,100'
vlan_string = config.split()[-1].split(',')
print(list(vlan_string))

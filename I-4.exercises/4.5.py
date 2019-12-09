command1 = 'switchport trunk allowed vlan 1,2,3,5,8'
command2 = 'switchport trunk allowed vlan 1,3,8,9'
command1 = set(command1.split()[-1].split(','))
command2 = set(command2.split()[-1].split(','))
vlan = command1 & command2
print(vlan)

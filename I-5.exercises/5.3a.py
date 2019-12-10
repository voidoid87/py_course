access_template = [
    'switchport mode access', 'switchport access vlan {}',
    'switchport nonegotiate', 'spanning-tree portfast',
    'spanning-tree bpduguard enable'
]

trunk_template = [
    'switchport trunk encapsulation dot1q', 'switchport mode trunk',
    'switchport trunk allowed vlan {}'
]

access = '\n'.join(access_template)
trunk = '\n'.join(trunk_template)

conf = {'access' : access, 'trunk': trunk}
ask = {'access' :'Enter VLAN number: ', 'trunk': 'Enter allowed VLANs: '}

mode = input('Enter interface mode (trunk/access): ')
interface = input('Enter interface type and number: ')
vlan = input(ask.get(mode))


print('interface '+interface + '\n' + conf.get(mode).format(vlan))


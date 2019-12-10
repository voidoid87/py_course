ip = input('Enter ip address: ')
ip_list = ip.split('.')
if int(ip_list[0]) <= 223:
	print('unicast')
elif 224 <= int(ip_list[0]) <= 239:
	print('multicast')
elif ip == '255.255.255.255':
	print('local broadcast')
elif ip == '0.0.0.0':
	print('unassigned')
else:
	print('unused')

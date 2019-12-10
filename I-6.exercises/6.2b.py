while True:
	ip = input('Enter ip address: ')
	ip_list = ip.split('.')

	try:
		for i in range(3):
			if len(ip_list) > 4:
				raise IndexError
			elif 0 <= int(ip_list[i]) <= 255:
				continue
			else:
				raise ValueError
	except (IndexError, ValueError):
		print('Incorrect ip address')
	else:
		break		
if ip == '0.0.0.0': 
	print('unassigned')
elif 224 <= int(ip_list[0]) <= 239:
	print('multicast')
elif ip == '255.255.255.255':
	print('local broadcast')
elif int(ip_list[0]) <= 223:
	print('unicast')
else:
	print('unused')

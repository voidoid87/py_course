net = input('Enter network IP: ')
ip = net.split('/')[0].split('.')
mask = int(net.split('/')[1])
str_mask = '1' * mask + '0' * (32-mask)
result =  'Network:\n{:10}{:10}{:10}{:10}\n{:10}{:10}{:10}{:10}'.format(ip[0],ip[1],ip[2],ip[3],bin(int(ip[0])).replace('0b','')\
	,bin(int(ip[1])).replace('0b',''),bin(int(ip[2])).replace('0b',''),bin(int(ip[3])).replace('0b','')) + '\n\n'\
	+ 'Mask:\n/' + str(mask) + '\n{:10}{:10}{:10}{:10}\n{:10}{:10}{:10}{:10}'.format(str(int(str_mask[0:8],2)),str(int(str_mask[8:16],2))\
	,str(int(str_mask[16:24],2)),str(int(str_mask[24:32],2)),str_mask[0:8],str_mask[8:16],str_mask[16:24],str_mask[24:32])
print(result)



#!/usr/bin/env python3

from sys import argv
net = argv[1]
ip = net.split('/')[0].split('.')
mask = int(net.split('/')[1])
bmask = '1' * mask + '0' * (32-mask)
oct1 = bin(int(ip[0])).replace('0b','')
oct1 = '0' * (8 - len(oct1)) + oct1
oct2 = bin(int(ip[1])).replace('0b','')
oct2 = '0' * (8 - len(oct2)) + oct2
oct3 = bin(int(ip[2])).replace('0b','')
oct3 = '0' * (8 - len(oct3)) + oct3
oct4 = bin(int(ip[3])).replace('0b','')
oct4 = '0' * (8 - len(oct4)) + oct4 
bip = oct1 + oct2 + oct3 + oct4
bnetip = bip[0:mask] + '0'*(32-mask)
ip = [int(bnetip[0:8],2),int(bnetip[8:16],2),int(bnetip[16:24],2),int(bnetip[24:32],2)]
result =  'Network:\n{:<10}{:<10}{:<10}{:<10}\n{:10}{:10}{:10}{:10}'.format(ip[0],ip[1],ip[2],ip[3],bnetip[0:8],bnetip[8:16],bnetip[16:24],bnetip[24:32]) + '\n\n'\
	+ 'Mask:\n/' + str(mask) + '\n{:10}{:10}{:10}{:10}\n{:10}{:10}{:10}{:10}'.format(str(int(bmask[0:8],2)),str(int(bmask[8:16],2))\
	,str(int(bmask[16:24],2)),str(int(bmask[24:32],2)),bmask[0:8],bmask[8:16],bmask[16:24],bmask[24:32])
print(result)



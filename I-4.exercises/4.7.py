mac = 'AAAA:BBBB:CCCC'
mac = mac.replace(':','') 
result = (bin(int(mac[0:2],16))+bin(int(mac[2:4],16))+bin(int(mac[4:6],16))+bin(int(mac[6:8],16))+bin(int(mac[8:10],16))+bin(int(mac[10:],16))).replace('0b','')
print(result)



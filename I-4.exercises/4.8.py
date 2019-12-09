ip = '192.168.3.1'
ip = ip.split('.')
result =  '{:10}{:10}{:10}{:10}\n{:10}{:10}{:10}{:10}'.format(ip[0],ip[1],ip[2],ip[3],bin(int(ip[0])).replace('0b',''),bin(int(ip[1])).replace('0b',''),bin(int(ip[2])).replace('0b',''),bin(int(ip[3])).replace('0b',''))
print(result)

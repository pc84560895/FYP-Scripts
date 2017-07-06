import os, time, MySQLdb, hashlib, re
import settings

filepattern = r'^honeypy.log(\..*)?$'
path = '/var/lib/docker/volumes/Deployment_159/_data'
dockerid = '49045bb57ba386496d0e500ae2df694faba4db24cc3092050c02608d017dfa41'

def insertIntoDB(sql):
	db = MySQLdb.connect(host=settings.DB_HOST,port=settings.DB_PORT,user=settings.DB_USER,passwd=settings.DB_PASSWORD,db=settings.DB_DEFAULT)
	cur = db.cursor()
	cur.execute(sql)
	db.commit()
	db.close()

files = []
listdir = os.listdir(path)
for i in listdir:
	if re.match(filepattern,i):
		f = '{}/{}'.format(path,i)
		files.append(f)

sql = 'INSERT IGNORE INTO Honeypot (id,docker,timestamp,remote_ip,remote_port,local_ip,local_port,protocol) VALUES '
		
for f in files:
	with open(f,'r') as file:
		values = ''
		
		for i,line in enumerate(file):
			data = {
				'docker': dockerid
			}
			
			message = '{}_{}'.format(dockerid,str(line))
			hash = hashlib.sha256(message.encode('utf-8')).hexdigest()
			
			parts = line.split(' ')
			
			if len(parts) > 10:
				time_parts = parts[1].split(',')
				data['timestamp'] = '{} {}'.format(parts[0],time_parts[0])
				
				if 'TCP' == parts[4]:
					data['r_ip'] = parts[9]
					data['r_port'] = parts[10]
					data['l_ip'] = parts[6]
					data['l_port'] = parts[7]
					data['protocol'] = parts[4]
				else:
					data['r_ip'] = parts[10]
					data['r_port'] = parts[11]
					data['l_ip'] = parts[7]
					data['l_port'] = parts[8]
					data['protocol'] = parts[5]
					
				data['id'] = hash
				s = '(\'{id}\', \'{docker}\', \'{timestamp}\', \'{r_ip}\', {r_port} ,\'{l_ip}\', {l_port},\'{protocol}\'),'.format(**data)
				values += s
				
				if i > 0 and (i % 5000) == 0:
					insert = sql + values[:-1]
					insertIntoDB(insert)
					values = ''
						
		if values:						
			insert = sql + values[:-1]
			insertIntoDB(insert)
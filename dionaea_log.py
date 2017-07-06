import docker, os, sqlite3, time, MySQLdb, hashlib
import settings

db = MySQLdb.connect(host=settings.DB_HOST,port=settings.DB_PORT,user=settings.DB_USER,passwd=settings.DB_PASSWORD,db=settings.DB_DEFAULT)
cur = db.cursor()

timeformat = '%Y-%m-%d %H:%M:%S'
path = '/var/lib/docker/volumes/dionaea-custom/_data/dionaea.sqlite'
filename = os.path.basename(path)
dockerid = '716cc963ab91267403d1f366e88d32766a50035b6f23a57f3230afe576e01334'

def insertIntoDB(sql):
	db = MySQLdb.connect(host=settings.DB_HOST,port=settings.DB_PORT,user=settings.DB_USER,passwd=settings.DB_PASSWORD,db=settings.DB_DEFAULT)
	cur = db.cursor()
	cur.execute(sql)
	db.commit()
	db.close()

conn = sqlite3.connect(filename)
cursor = conn.cursor()
cursor.execute('SELECT * FROM connections')

sql = 'INSERT IGNORE INTO Honeypot (id,docker,timestamp,remote_ip,remote_port,local_ip,local_port,protocol) VALUES '
values = ''

for i,row in enumerate(cursor):
	timestamp = row[4]
	r_ip = row[9][7:]
	r_port = row[11]
	l_ip = row[7][7:]
	l_port = row[8]
	protocol = row[2]
	
	timestamp = time.strftime(timeformat, time.localtime(timestamp))
	
	data = {
		'docker': dockerid,
		'timestamp': timestamp,
		'r_ip': r_ip,
		'r_port': r_port,
		'l_ip': l_ip,
		'l_port': l_port,
		'protocol': protocol
	}
	
	message = '{}_{}'.format(dockerid,str(row))
	hash = hashlib.sha256(message.encode('utf-8')).hexdigest()
	
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

conn.close()
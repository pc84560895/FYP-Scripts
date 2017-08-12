#!/opt/dionaea/bin/python3
import sqlite3
import getopt
import sys

#
#	Basic script for automating queries against Dionaea's logsql.sqlite
#
#	Author:	Andrew Waite - www.infosanity.co.uk
# Date:		2009-12-01
#

def executeQuery(sql):
	conn = sqlite3.connect('/opt/dionaea/var/dionaea/dionaea.sqlite')
	c = conn.cursor()
	c.execute(sql)
	
	for row in c:
		print(row)



def parseOpts():
	try:
		opts, args = getopt.getopt(sys.argv[1:],"hV", ["query=", "help", "version"])
	except:
		usage()
		sys.exit(2)

	for o, a in opts:
		if o in ("--query"):

			#Port attack frequency
			if a == '1':
				queryDesc = "List of attacked ports"
				querySQL = 'SELECT COUNT(local_port) AS hitcount,local_port AS port FROM connections WHERE connection_type = "accept" GROUP BY local_port HAVING COUNT(local_port) > 10'
				queryColumns = ("HitCount", "port")
				sys.stdout.write("Description:\n\t%s\nExecuted Query:\n\t%s\n\n%s\n" %(queryDesc, querySQL, queryColumns))
				executeQuery(querySQL)

			#Attacks over a day
			elif a == '2':
				queryDesc = "Attacks over a day"
				querySQL = 'SELECT ROUND((connection_timestamp%(3600*24))/3600) AS hour, COUNT(*) FROM connections WHERE connection_parent IS NULL GROUP BY ROUND((connection_timestamp%(3600*24))/3600)'
				queryColumns = ("Hour", "Hits")
				sys.stdout.write("Description:\n\t%s\nExecuted Query:\n\t%s\n\n%s\n" %(queryDesc, querySQL, queryColumns))
				executeQuery(querySQL)

			#Popular Malware Downloads
			elif a == '3':
				queryDesc = "Popular Malware Downloads"
				querySQL = 'SELECT COUNT(download_md5_hash), download_md5_hash FROM downloads GROUP BY download_md5_hash ORDER BY COUNT(download_md5_hash) DESC LIMIT 10'
				queryColumns = ("Num Submissions", "MD5 Hash")
				sys.stdout.write("Description:\n\t%s\nExecuted Query:\n\t%s\n\n%s\n" %(queryDesc, querySQL, queryColumns))
				executeQuery(querySQL)
			
			#Busy Attackers
			elif a == '4':
				queryDesc = "Busy Attackers"
				querySQL = 'SELECT COUNT(remote_host), remote_host FROM connections WHERE connection_type = "accept" GROUP BY remote_host ORDER BY COUNT(remote_host) DESC LIMIT 10'
				queryColumns = ("Hits", "Remote Host")
				sys.stdout.write("Description:\n\t%s\nExecuted Query:\n\t%s\n\n%s\n" %(queryDesc, querySQL, queryColumns))
				executeQuery(querySQL)

			#Popular Download locations
			elif a == '5':
				queryDesc = "Popular download locations"
				querySQL = 'SELECT COUNT(*),download_url FROM downloads GROUP BY download_url ORDER BY COUNT(*) DESC LIMIT 20'
				queryColumns = ("Hits", "Download_url")
				sys.stdout.write("Description:\n\t%s\nExecuted Query:\n\t%s\n\n%s\n" %(queryDesc, querySQL, queryColumns))
				executeQuery(querySQL)

			#Connections in last 24 hours
			elif a == '6':
				queryDesc = "Connections in last 24hours"
				querySQL = 'SELECT * FROM connections WHERE connections.connection_timestamp > strftime("%s", "now", "-1 day")'
				queryColumns = ("!!!To-Do!!!")
				sys.stdout.write("Description:\n\t%s\nExecuted Query:\n\t%s\n\n%s\n" %(queryDesc, querySQL, queryColumns))
				executeQuery(querySQL)

			else:
				usage()
		elif o in ("-h", "--help"):
			usage()
		elif o in ("-V", "--version"):
			version()

def version():
	sys.stdout.write("\nDionaea database query collection\n")
	sys.stdout.write("Author: Andrew Waite - www.InfoSanity.co.uk\n\n")
	sys.stdout.write("Inspiration from carnivore.it article:\n")
	sys.stdout.write("\thttp://carnivore.it/2009/11/06/dionaea_sql_logging\n")

def usage():
	version()
	sys.stdout.write("\nUsage:\n")
	sys.stdout.write("\t /path/to/python dionaea-sqlquery.py --query #\n")
	sys.stdout.write("Where # is:\n")
	sys.stdout.write("\t1:\tPort Attack Frequency\n")
	sys.stdout.write("\t2:\tAttacks over a day\n")
	sys.stdout.write("\t3:\tPopular Malware Downloads\n")
	sys.stdout.write("\t4:\tBusy Attackers\n")
	sys.stdout.write("\t5:\tPopular Download Locations\n")
	sys.stdout.write("\t6:\tConnections in last 24 hours\n")

def main():
        parseOpts()

        sys.exit()

if __name__ == "__main__":
        main()


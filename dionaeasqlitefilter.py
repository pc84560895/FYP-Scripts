#!/usr/bin/env python


# To autorun this script, run this few commands:
# put this script in the Dionaea deployment volume in docker. (e.g. /var/lib/docker/volumes/<Deployment_id>/_data/)
# Run crontab -e
# Add */5 * * * * python3 /var/lib/docker/volumes/<Deployment_id>/_data/dionaeasqlitefilter.py
# This will run the dionaeasqlitefilter script every 5 minutes to grab the data.


import os
import datetime
import sqlite3
import requests

#Deployment_id example: Deployment_6
sqliteDB = "/var/lib/docker/volumes/<Deployment_id>/_data/dionaea.sqlite"
log_file = "/var/lib/docker/volumes/<Deployment_id>/_data/dionaeaconn.log"
last_conn = "/var/lib/docker/volumes/<Deployment_id>/_data/lastconn.id"

conn_start = 0
conn_id = 0

#Deployment_id example: Deployment_6
log_file2 = "/var/lib/docker/volumes/<Deployment_id>/_data/dionaeaoffers.log"
last_offer = "/var/lib/docker/volumes/<Deployment_id>/_data/lastoffer.id"

offer_start = 0
offer_id = 0

l_ip = requests.get("http://ipinfo.io").json().get('ip')

if os.path.isfile(sqliteDB):

#Start of extracting data out of connections table
    if os.path.isfile(last_conn):
        with open(last_conn, 'r') as f:
            line = int(f.read())
            if line > 0:
                conn_start = line

#Connections table
    conn = sqlite3.connect(sqliteDB)
    cursor = conn.cursor()
    sqlstmt = "SELECT * FROM connections WHERE connection > {} ORDER BY connection ASC".format(conn_start)
    cursor.execute(sqlstmt)

    for i,row in enumerate(cursor):
        timestamp = datetime.datetime.fromtimestamp(row[4]).strftime('%Y-%m-%d %H:%M:%S')
        conn_id = row[0]
        connection_type = row[1]
        protocol = row[2]
        connection_protocol = row[3]
        l_port = row[8]
        r_ip = row[9][7:]
        r_port = row[11]
        hostname = row[10]
        with open(log_file, "a+") as f:
            f.write("{} : {:10} \t {:10} \t {} \t {} \t {} \t {:15} \t {:5} \t {}\n".format(timestamp, connection_type, connection_protocol, protocol, l_ip, l_port, r_ip, r_port, hostname))

    conn.close()

    if conn_id > 0:
        with open(last_conn, 'w+') as f:
            f.write(str(conn_id))
#End of Connections table


#Start of extracting data out of offers table
    if os.path.isfile(last_offer):
        with open(last_offer, 'r') as f:
            line = int(f.read())
            if line > 0:
                offer_start = line

    conn = sqlite3.connect(sqliteDB)
    cursor = conn.cursor()
    sqlstmt = "SELECT offer, o.connection, offer_url, connection_timestamp FROM offers o, connections c WHERE c.connection = o.connection AND offer > {} ORDER BY offer ASC".format(offer_start)
    cursor.execute(sqlstmt)

    for i,row in enumerate(cursor):
        timestamp = datetime.datetime.fromtimestamp(row[3]).strftime('%Y-%m-%d %H:%M:%S')
        offer_id = row[0]
        offer_url = row[2]
        with open(log_file2, "a+") as f:
            f.write("{} : {}\n".format(timestamp, offer_url))
    conn.close()

    if offer_id > 0:
        with open(last_offer, 'w+') as f:
            f.write(str(offer_id))

else:
    print("Sqlite DB not found: {}".format(sqliteDB))

import MySQLdb

db = MySQLdb.connect("localhost", "root", "bugaosuni")

cursor = db.cursor()

cursor.execute("create database IF NOT EXISTS filteredlogsdb")

cursor.execute("use filteredlogsdb")

#connections table
cursor.execute('''CREATE TABLE IF NOT EXISTS
                        connections(
                                connection_id int NOT NULL AUTO_INCREMENT,
                                connection_transport varchar(255),
                                connection_protocol varchar(255),
                                connection_timestamp timestamp,
                                local_host varchar(255),
                                local_port int,
                                remote_host varchar(255),
                                remote_port int,
								PRIMARY KEY(connection_id)
                        )''')

#Downloads table
cursor.execute('''CREATE TABLE IF NOT EXISTS 
			downloads (
				download_id int NOT NULL AUTO_INCREMENT,
				connection int,
				download_url varchar(1000),
				download_md5_hash varchar(500),
				PRIMARY KEY(download_id),
				CONSTRAINT downloads_connection_fkey FOREIGN KEY (connection) REFERENCES connections (connection_id)
			)''')

#sqllogins table
cursor.execute('''CREATE TABLE IF NOT EXISTS
			sqllogins (
				login_id int AUTO_INCREMENT,
				connection int,
				login_username varchar(1000),
				login_password varchar(1000),
				PRIMARY KEY(login_id),
				CONSTRAINT logins_connection_fkey FOREIGN KEY (connection) REFERENCES connections (connection_id)
			)''')

#mssql_commands table
cursor.execute('''CREATE TABLE IF NOT EXISTS
			mssql_commands (
				mssql_command_id int AUTO_INCREMENT,
				connection int,
				mssql_command_status varchar(1000),
				mssql_command_cmd varchar(5000),
				PRIMARY KEY(mssql_command_id),
				CONSTRAINT mssql_commands_connection_fkey FOREIGN KEY (connection) REFERENCES connections (connection_id)
			)''')

#mssql_fingerprints table
cursor.execute('''CREATE TABLE IF NOT EXISTS
			mssql_fingerprints (
				mssql_fingerprint_id int AUTO_INCREMENT,
				connection int,
				mssql_fingerprint_hostname varchar(1000),
				mssql_fingerprint_appname varchar(1000),
				mssql_fingerprint_cltintname varchar(1000),
				PRIMARY KEY(mssql_fingerprint_id),
				CONSTRAINT mssql_fingerprints_connection_fkey FOREIGN KEY (connection) REFERENCES connections (connection_id)
			)''')
			
#mysql_command_args table
cursor.execute('''CREATE TABLE IF NOT EXISTS
			mysql_command_args (
				mysql_command_arg_id int AUTO_INCREMENT,
				mysql_command int,
				mysql_command_arg_index int NOT NULL,
				mysql_command_arg_data varchar(5000) NOT NULL,
				PRIMARY KEY(mysql_command_arg_id),
			)''')			

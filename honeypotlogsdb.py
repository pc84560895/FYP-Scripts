#!/usr/bin/env python

import sqlite3

conn = sqlite3.connect(r"filteredlogs.db")
cursor = conn.cursor()
#connections table
cursor.execute('''CREATE TABLE IF NOT EXISTS
                        connections(
                                connection_id INTEGER PRIMARY KEY,
                                connection_type TEXT,
                                connection_transport TEXT,
                                connection_protocol TEXT,
                                connection_timestamp INTEGER,
                                local_host TEXT,
                                local_port INTEGER,
                                remote_host TEXT,
                                remote_port INTEGER
                        )''')

#Downloads table
cursor.execute('''CREATE TABLE IF NOT EXISTS 
			downloads (
				download_id INTEGER PRIMARY KEY,
				connection INTEGER,
				download_url TEXT,
				download_md5_hash TEXT
				-- CONSTRAINT downloads_connection_fkey FOREIGN KEY (connection) REFERENCES connections (connection)
			)''')

#sqllogins table
cursor.execute('''CREATE TABLE IF NOT EXISTS
			sqllogins (
				login_id INTEGER PRIMARY KEY,
				connection INTEGER,
				login_username TEXT,
				login_password TEXT
				-- CONSTRAINT logins_connection_fkey FOREIGN KEY (connection) REFERENCES connections (connection)
			)''')

#mssql_commands table
cursor.execute('''CREATE TABLE IF NOT EXISTS
			mssql_commands (
				mssql_command_id INTEGER PRIMARY KEY,
				connection INTEGER,
				mssql_command_status TEXT,
				mssql_command_cmd TEXT
				-- CONSTRAINT mssql_commands_connection_fkey FOREIGN KEY (connection) REFERENCES connections (connection)
			)''')

#mssql_fingerprints table
cursor.execute('''CREATE TABLE IF NOT EXISTS
			mssql_fingerprints (
				mssql_fingerprint_id INTEGER PRIMARY KEY,
				connection INTEGER,
				mssql_fingerprint_hostname TEXT,
				mssql_fingerprint_appname TEXT,
				mssql_fingerprint_cltintname TEXT
				-- CONSTRAINT mssql_fingerprints_connection_fkey FOREIGN KEY (connection) REFERENCES connections (connection)
			)''')

#mysql_command_args table
cursor.execute("""CREATE TABLE IF NOT EXISTS
			mysql_command_args (
				mysql_command_arg_id INTEGER PRIMARY KEY,
				mysql_command INTEGER,
				mysql_command_arg_index NUMBER NOT NULL,
				mysql_command_arg_data TEXT NOT NULL
				-- CONSTRAINT mysql_commands_connection_fkey FOREIGN KEY (connection) REFERENCES connections (connection)
			)""")

#mysql_command_ops table
cursor.execute("""CREATE TABLE IF NOT EXISTS
			mysql_command_ops (
				mysql_command_op_id INTEGER PRIMARY KEY,
				mysql_command_cmd INTEGER NOT NULL,
				mysql_command_op_name TEXT NOT NULL,
				CONSTRAINT mysql_command_cmd_uniq UNIQUE (mysql_command_cmd)
			)""")

#mysql_commands
cursor.execute('''CREATE TABLE IF NOT EXISTS
			mysql_commands (
				mysql_command_id INTEGER PRIMARY KEY,
				connection INTEGER,
				mysql_command_cmd NUMBER NOT NULL
				-- CONSTRAINT mysql_commands_connection_fkey FOREIGN KEY (connection) REFERENCES connections (connection)
			)''')

#offer table for dl links if there is one
cursor.execute('''CREATE TABLE IF NOT EXISTS 
			offers (
				offer INTEGER PRIMARY KEY,
				connection INTEGER,
				offer_url TEXT
				-- CONSTRAINT offers_connection_fkey FOREIGN KEY (connection) REFERENCES connections (connection)
			)''')

#sip commands table
cursor.execute('''CREATE TABLE IF NOT EXISTS
			sip_commands (
				sip_command INTEGER PRIMARY KEY,
				connection INTEGER,
				sip_command_method ,
				sip_command_call_id ,
				sip_command_user_agent ,
				sip_command_allow INTEGER
			-- CONSTRAINT sip_commands_connection_fkey FOREIGN KEY (connection) REFERENCES connections (connection)
		)''')

#sip addresses table
cursor.execute("""CREATE TABLE IF NOT EXISTS
			sip_addrs (
				sip_addr INTEGER PRIMARY KEY,
				sip_command INTEGER,
				sip_addr_type ,
				sip_addr_display_name,
				sip_addr_uri_scheme,
				sip_addr_uri_user,
				sip_addr_uri_password,
				sip_addr_uri_host,
				sip_addr_uri_port
				-- CONSTRAINT sip_addrs_command_fkey FOREIGN KEY (sip_command) REFERENCES sip_commands (sip_command)
			)""")

#sip vias table
cursor.execute('''CREATE TABLE IF NOT EXISTS
			sip_vias (
				sip_via INTEGER PRIMARY KEY,
				sip_command INTEGER,
				sip_via_protocol,
				sip_via_address,
				sip_via_port
				-- CONSTRAINT sip_vias_command_fkey FOREIGN KEY (sip_command) REFERENCES sip_commands (sip_command)
			)''')



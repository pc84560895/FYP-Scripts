from twisted.internet import protocol
from twisted.python import log
import uuid
import re

class FTPUnix(protocol.Protocol):
	localhost   = None
	remote_host = None
	session     = None

	### START CUSTOM VARIABLES ###############################################################
	username = None
	UNAUTH, INAUTH = range(2)
	state = UNAUTH
	##########################################################################################
	
	# handle events
	def connectionMade(self):
		self.connect()

		### START CUSTOM CODE ####################################################################
		self.tx('220 (vsFTPd 3.0.2)')
		##########################################################################################

	def dataReceived(self, data):
		self.rx(data)

		### START CUSTOM CODE ####################################################################
		cmd, args = re.match(r'(\S+)\s*(.*)$', data.rstrip()).groups()
		cmd = cmd.upper()

		if cmd == 'USER':
			if self.state != self.UNAUTH:
				self.tx('530 Please login with USER and PASS.')
			else:
				self.username = args
				self.state = self.INAUTH
				self.tx('331 Please specify the password.')
		elif cmd == 'PASS':
			if self.state != self.INAUTH:
				self.tx('503 Login with USER first.')
			else:
				self.state = self.UNAUTH
				self.tx('230 Login successful.\n')
		else:
			self.tx('451 Requested action aborted. Local error in processing.')
		#############################################################################

	### START CUSTOM FUNCTIONS ###################################################################

	##############################################################################################

	def connect(self):
		self.local_host  = self.transport.getHost()
		self.remote_host = self.transport.getPeer()
		self.session     = uuid.uuid1()
		log.msg('%s %s CONNECT %s %s %s %s %s' % (self.session, self.remote_host.type, self.local_host.host, self.local_host.port, self.factory.name, self.remote_host.host, self.remote_host.port))

	def clientConnectionLost(self):
		self.transport.loseConnection()
	
	def tx(self, data):
		log.msg('%s %s TX %s %s %s %s %s %s' % (self.session, self.remote_host.type, self.local_host.host, self.local_host.port, self.factory.name, self.remote_host.host, self.remote_host.port, data.encode("hex")))
		self.transport.write(data + '\r\r\n')

	def rx(self, data):
		log.msg('%s %s RX %s %s %s %s %s %s' % (self.session, self.remote_host.type, self.local_host.host, self.local_host.port, self.factory.name, self.remote_host.host, self.remote_host.port, data.encode("hex")))

class pluginFactory(protocol.Factory):
	protocol = FTPUnix ### Set protocol to custom protocol class name
	
	def __init__(self, name=None):
		self.name = name or 'HoneyPy'
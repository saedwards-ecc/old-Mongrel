import sys, os, time
from server import Server
from poller import Poller

CURRENT_DIR = os.getcwd() + '/' # current dir with slas

<<<<<<< HEAD
class Server:
	"""This is a main initialization class
	Here we will have all main initialization functions and objects"""

	def __init__(self, pidfile, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
		self.stdin = stdin
		self.stdout = stdout
		self.stderr = stderr
		self.pidfile = pidfile

		# Configuration import
		config = ConfigParser()
		config.readfp(open(CURRENT_DIR + 'include/' + 'mong.conf', 'rb'))

		# Database initialization
		host = config.get('Database', 'host')
		user = config.get('Database', 'user')
		passwd = config.get('Database', 'passwd')
		dbname = config.get('Database', 'dbname')
		db = dbApi(host, user, passwd, dbname)

	def daemonize(self):
		"""
		UNIX double-fork magic. Some info:
		Fork a second child and exit immediately to prevent zombies.  This
		causes the second child process to be orphaned, making the init
		process responsible for its cleanup.  And, since the first child is
		a session leader without a controlling terminal, it's possible for
		it to acquire one by opening a terminal in the future (System V-
		based systems).  This second fork guarantees that the child is no
		longer a session leader, preventing the daemon from ever acquiring
		a controlling terminal.
		"""

		try:
			pid = os.fork()
			if pid > 0:
				# exit first parrent
				sys.exit(0)
		except OSError, e:
			sys.stderr.write("fork #1: failed: %d (%s)\n" % (e.errno, e.sdrerror))
			sys.exit(1)

		# decouple from parrent environment
		os.chdir('/')
		os.setsid()
		os.umask(0)

		# do second fork
		try:
			pid = os.fork()
			if pid > 0:
		# exit from second parrent
				sys.exit(0)
		except OSError, e:
			sys.stderr.write("fork #2: failed: %d (%s)\n" % (e.errno, e.sdrerror))
			sys.exit(1)

		# redirect standart file descriptors
		sys.stdout.flush()
		sys.stderr.flush()
		si = file(self.stdin, 'r')
		so = file(self.stdout, 'a+')
		se = file(self.stderr, 'a+', 0)
		os.dup2(si.fileno(), sys.stdin.fileno())
		os.dup2(so.fileno(), sys.stdin.fileno())
		os.dup2(se.fileno(), sys.stdin.fileno())

		# write pid file
		atexit.register(self.delpid)
		pid = str(os.getpid())
		file(self.pidfile, 'w+').write("%s\n" % pid)

	def delpid(self):
		os.remove(self.pidfile)

	def start(self):
		"""
		Start the daemon
		"""
	# Check for pid file to see if the daemon already runs
		try:
			pf = file(self.pidfile, 'r')
			pid = int(pf.read().strip())
			pf.close()
		except IOError:
			pid = None

		if pid:
			message = "pidfile %s already exist, maybe Mongrel already running?\n"
			sys.stderr.write(message % self.pidfile)
			sys.exit(1)

		# Start the daemon
		self.daemonize()
		self.run()

	def stop(self):
		"""
		Stop the daemon
		"""
		# Get the pid from pidfile
		try:
			pf = file(self.pidfile, 'r')
			pid = int(pf.read().strip())
			pf.close()
		except IOError:
			pid = None

		if not pid:
			message = "pidfile %s does not exist, maybe Mongrel not running?\n"
			sys.stderr.write(message % self.pidfile)
			return # not and error in restart

		# Try killing the daemon process
		try:
			while 1:
				os.kill(pid, SIGTERM)
				time.sleep(0.1)
		except OSError, err:
			err = str(err)
			if err.find("No such process") > 0:
				if os.path.exists(self.pidfile):
					os.remove(self.pidfile)
				else:
					print str(err)
					sys.exit(1)

	def restart(self):
		"""
		Restart the daemon
		"""
		self.stop()
		self.start()

	def run(self):
		pass

##### IMPLEMENTATION  - WATCH OUT - ITS UGLY!!! #####
=======
>>>>>>> experimental
class Mongrel(Server):
	def run(self):
		while True:
			time.sleep(1)

# UGLY CALL!!!
app = Mongrel(stdout = CURRENT_DIR + 'logs/' + 'output.log', stderr = CURRENT_DIR + 'logs/' + 'error.log')
#print len(app.data)
if len(sys.argv) == 2:
	if 'start' == sys.argv[1]:
		app.start()
		app.status()
	elif 'stop' == sys.argv[1]:
		app.stop()
	elif 'restart' == sys.argv[1]:
		app.restart()
	elif 'status' == sys.argv[1]:
		app.status()
	else:
		print "Unknown command\n"
		print "usage: %s start|stop|restart" % sys.argv[0]
		sys.exit(2)
else:
		print "usage: %s start|stop|restart" % sys.argv[0]
		sys.exit(2)

#poller = Poller(app.data, 'tmp/mongrel-poller.pid')
#poller.start()

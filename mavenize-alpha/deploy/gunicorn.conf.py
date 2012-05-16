"""gunicorn web server settings."""


import os


def num_cpus():
	"""Return the total amount of CPUs on the system."""

	if not hasattr(os, 'sysconf'):
		raise RuntimeError('No sysconf detected.')
	return os.sysconf('SC_NPROCESSORS_ONLN')


bind = '127.0.0.1:8000'
workers = num_cpus()*2 + 1

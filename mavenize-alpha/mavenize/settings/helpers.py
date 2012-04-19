"""Useful helper functions."""


from random import choice


def gen_secret_key(l):
	"""Generate a random secret key of length l."""

	return ''.join(
		[choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in
				range(l)]
	)

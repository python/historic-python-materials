__doc__ = """\
Persistent Object Store
-----------------------

This module implements a limited form of persistent objects,
using the algorithm implemented by the flatten module.

This particular interface was designed by Anders Lindstrom
<anders@cs.su.oz.au>, who used a different representation of the
database on disk (a Python program -- cute but if it grows too big the
parser will choke).

The requirement of the original interface that classes must be
subclasses of PosObject is dropped here -- instead, classes should
have a class or instance variable __module__ whose value is the
module name containing the class name (this will be added automatically
in future generations of the interpreter).  For backward compatibility,
a PosObject class is provide which stores this attribute on the instance.
It must also be possible to create class instances by calling the class
without arguments.

The interface is the following:

db = pos.create(filename) -- create a new database
db = pos.open(filename)   -- open an existing database
db.setroot(object)        -- set the root object of the database
object = db.getroot()     -- get the root object of the database
db.save()                 -- write the database to the file
db.compress()             -- compress the database
db.uncompress()           -- uncompress the database

Compression is transparent to the user: once a database has
acquired the 'compressed' attribute, it is automatically uncompressed
when it is opened, and and it will automatically be saved in compressed
form.  Compression uses gzip by default but also supports compress.
"""

__version__ = "1.0"

import os
import flatten
import __builtin__

# Rename open because we export a function called open
_open = __builtin__.open

# Exception
Error = 'pos.Error'

# Magic first line of database files
Magic = 'Python Persistent Object Store; pos %s; flatten %s\n' % \
        (__version__, flatten.__version__)

# Map compressors to uncompressors
_uncompressor = {
	'gzip':     'gunzip',
	'compress': 'uncompress',
}

# Map compressors to extensions
_extension = {
	'gzip':     '.gz',
	'compress': '.Z',
}


# Database class

class _Database:

	def __init__(self, filename, root = None):
		self._filename = filename
		self._root = root
		self._compressor = None
		self._check()

	def _check(self):
		if os.path.exists(self._filename):
			self._exists = 1
			self._compressor = None
		elif os.path.exists(self._filename + '.gz'):
			self._exists = 1
			self._compressor = "gzip"
		elif os.path.exists(self._filename + '.Z'):
			self._exists = 1
			self._compressor = "compress"
		else:
			self._exists = 0
			# self._compressor remains unchanged

	def setroot(self, object):
		self._root = object

	def getroot(self):
		return self._root

	def compress(self, compressor = "gzip"):
		if not compressor:
			return self.uncompress()
		self._check()
		if not self._compressor:
			if self._exists:
				sts = os.system('%s %s' %
				                (compressor, self._filename))
				if sts != 0:
					raise Error, 'compression failed'
			self._compressor = compressor

	def uncompress(self):
		self._check()
		if self._compressor:
			if self._exists:
				uncompressor = _uncompressor[self._compressor]
				sts = os.system('%s %s' %
				                (uncompressor, self._filename))
				if sts != 0:
					raise Error, 'decompression failed'
			self._compressor = None

	def save(self):
		self._check()
		tempfile = self._filename + '_'
		if self._compressor:
			tempfile = tempfile + _extension[self._compressor]
			fp = os.popen('%s >%s' %
			              (self._compressor, tempfile), 'w')
		else:
			fp = _open(tempfile, 'w')
		fp.write(Magic)
		F = flatten.Flattener(fp)
		F.dump(self._root)
		sts = fp.close()
		if sts:
			raise Error, 'save-compression failed'
		filename = self._filename
		if self._compressor:
			filename = filename + _extension[self._compressor]
		backupfile = filename + '~'
		try:
			os.unlink(backupfile)
		except os.error:
			pass
		try:
			os.rename(filename, backupfile)
		except os.error:
			pass
		try:
			os.rename(tempfile, filename)
		except os.error, msg:
			raise Error, 'save--rename failed: %s' % str(msg)

	def _load(self):
		self._check()
		filename = self._filename
		if self._compressor:
			filename = filename + _extension[self._compressor]
			fp = os.popen('%s <%s' %
			              (_uncompressor[self._compressor], filename), 'r')
		else:
			fp = _open(filename, 'r')
		line = fp.readline()
		if line != Magic:
			fp.close()
			raise Error, 'load--bad magic first line'
		U = flatten.Unflattener(fp)
		self._root = U.load()
		sts = fp.close()
		if sts:
			raise Error, 'load--decompression failed'

	def destroy(self):
		self._check()
		if self._exists:
			filename = self._filename
			if self._compressor:
				filename = filename + _extension[self._compression]
			os.unlink(filename)

_opendbs = {}

def create(filename, root = None):
	if not os.path.isabs(filename):
		filename = os.path.join(os.getcwd(), filename)
	if _opendbs.has_key(filename):
		raise Error, 'create--file %s already open' % `filename`
	db = _Database(filename, root)
	if db._exists:
		raise Error, 'create--file %s already exists' % `filename`
	return db

def open(filename):
	if not os.path.isabs(filename):
		filename = os.path.join(os.getcwd(), filename)
	if _opendbs.has_key(filename):
		return _opendbs[filename]
	db = _Database(filename)
	if not db._exists:
		raise Error, 'open--file %s not found' % `filename`
	db._load()
	return db


# Backward compatibility stuff (DO NOT USE):

PosError = Error

CompGzip     = "gzip"
CompCompress = "compress"

class PosObject:
	def __init__(self, modname):
		self.__dict__['__module__'] = modname


# Test program:

def _test(N = 20, fn = 'postest_tmp'):
	import time
	a = []
	for i in range(N):
		a.append(range(N))

	t1 = time.time()
	db = create(fn)
	db.setroot(a)
	db.save()
	t2 = time.time()

	print "Saved %d copies of range(%d) in %6.3f seconds" % (N, N, t2-t1)

	t1 = time.time()
	db = open(fn)
	b = db.getroot()
	t2 = time.time()

	print "Loaded %d copies of range(%d) in %6.3f seconds" % (N, N, t2-t1)

	if a == b:
		print "Result has the same value as saved"
		db.destroy()
	else:
		print "*** RESULT DIFFERS FROM SAVED VALUE ***"


if __name__ == '__main__':
	_test()

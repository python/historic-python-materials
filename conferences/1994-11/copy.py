# Generic (deep) copying operation

# XXX
# What about types like module, class, function, method?
# Or stack trace, stack frame?
# Or file?

import types

CopyError = 'copy.CopyError'	# XXX Why not copy.Error?

def copy(x, memo = None):
	if memo is None:
		memo = {}
	d = id(x)
	if memo.has_key(d):
		return memo[d]
	try:
		copierfunction = _copy_dispatch[type(x)]
	except KeyError:
		try:
			copier = x.__copy__
		except AttributeError:
			raise CopyError, "uncopyable object of type %s" % type(x)
		y = copier(memo)
	else:
		y = copierfunction(x, memo)
	memo[d] = y
	return y

_copy_dispatch = d = {}

def _copy_atomic(x, memo):
	return x
d[types.NoneType] = _copy_atomic
d[types.IntType] = _copy_atomic
d[types.LongType] = _copy_atomic
d[types.FloatType] = _copy_atomic
d[types.StringType] = _copy_atomic
d[types.CodeType] = _copy_atomic
d[types.TypeType] = _copy_atomic
d[types.XRangeType] = _copy_atomic

def _copy_list(x, memo):
	y = []
	memo[id(x)] = y
	for a in x:
		y.append(copy(a, memo))
	return y
d[types.ListType] = _copy_list

def _copy_tuple(x, memo):
	y = []
	for a in x:
		y.append(copy(a, memo))
	d = id(x)
	try:
		return memo[d]
	except KeyError:
		pass
	for i in range(len(x)):
		if x[i] is not y[i]:
			return tuple(y)
	return x
d[types.TupleType] = _copy_tuple

def _copy_dict(x, memo):
	y = {}
	memo[id(x)] = y
	for key in x.keys():
		y[copy(key, memo)] = copy(x[key], memo)
	return y
d[types.DictionaryType] = _copy_dict

def _copy_inst(x, memo):
	if hasattr(x, '__copy__'):
		return x.__copy__()
	if hasattr(x, '__getinitargs__'):
		args = x.__getinitargs__()
		args = copy(args, memo)
	else:
		args = ()
	y = apply(x.__class__, args)
	memo[id(x)] = y
	if hasattr(x, '__getstate__'):
			state = x.__getstate__()
	else:
			state = x.__dict__
	state = copy(state, memo)
	if y.hasattr('__setstate__'):
			y.__setstate__(state)
	else:
			for key in state.keys():
				setattr(y, key, state[key])
	return y
d[types.InstanceType] = _copy_inst

del d, types

def _test():
	l = [None, (1, 2L), [3.14, 'abc'], {'abc': 'ABC'}, (), [], {}]
	l1 = copy(l)
	print l1==l
	class C:
		def __init__(self, arg=None):
			self.a = 1
			self.arg = arg
			self.fp = open('copy.py')
			self.fp.close()
		def __getstate__(self):
			return {'a': self.a, 'arg': self.arg}
		def __setstate__(self, state):
			for key in state.keys():
				setattr(self, key, state[key])
		def __copy__(self, memo = None):
			new = self.__class__(copy(self.arg, memo))
			new.a = self.a
			return new
	c = C('argument sketch')
	l.append(c)
	l2 = copy(l)
	print l == l2
	print l
	print l2
	l.append({l[1]: l, 'xyz': l[2]})
	l3 = copy(l)
	import repr
	print map(repr.repr, l)
	print map(repr.repr, l1)
	print map(repr.repr, l2)
	print map(repr.repr, l3)

if __name__ == '__main__':
	_test()

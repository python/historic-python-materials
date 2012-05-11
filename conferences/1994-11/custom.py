"""Module customizations mechanism.

Regular interface by which users configure custom settings for modules, and
modules implement those customizations at initialization time.

$Id: custom.py 4678 2002-02-28 16:45:09Z barry $
Created by Ken.Manheimer@nist.gov,  16-Nov-1994

The customization process does not depend on prior loading of the target
module in order to register customizations.  The module, conversely, controls
adoption of the customizations.

Users employ the custom.config() routine to specify custom settings.  Modules
use the custom.implement() routine to:
  - register default values for vars, and
  - to deploy the actual value for the var:
      - the custom value, if one has been designated using custom.config(), 
      - or else the default value specified in the custom.implement() call.

custom.status() returns info about the status of specific customization vars,
and custom.cancel() remove registration for a variable.`

In order to enable special provisions for custom vars, modules can use
custom.implement() to designate routines that implement the var's actual
assignment.  The FUNCTION must take three values - module, variable name, and
value.  It is responsible for actually assigning the variable, and should
return the value assigned. 

Custom vars with no designated assignment function actually use the 'assign'
routine, below.  It simply assigns the value to the var within the module.

(A few, trivial alternate assignment functions are also provided:
  - 'loudassign', which does same thing as assign, but prints an informative
    announcement about it, and
  - 'ignore', which does not actually do the assignment.)"""

__version__ = '$Revision: 4678 $'

import sys

CustomError = 'CustomError'
unique = ()			# for default args, to distinguish from, eg,
				# None as a valid value.  id() is used to
				# distinguish from other empty tuples.

# 'custs' is a dictionary mapping module names to dictionaries of variable
# names.  Each variable name maps to a CustomVar instance, which tracks the
# customization state (default, set value, implemented, change func) of the
# var. 
try:					# Only reinit if not already extant.
    custs
except NameError:
    custs = {}			

class CustomVar:
    """Track custom var registration state, and deploy val when appropriate.

    ("When appropriate" means, when default value is being set, or when custom
     value is being set, and a default value has already been established.)"""

    access default, custom, func: public
    access setting, deploy, implemented: private

    unsetVal = ()
    access unsetVal: read
    chngFunc = []

    def __init__(self, moduleName, varName):
	self.moduleName = moduleName
	self.varName = varName
	self.defaultVal = self.unsetVal
	self.customVal = self.unsetVal
	self.func(assign)
	self.implementedVal = 0
	

    # Public interface:
    def custom(self, val=unsetVal):
	"""Set custom val of var, if val passed in call, or retrieve current.
	Custom val is deployed if the var has already been implemented.

	NameError raised if get attempted and no val set."""

	setVal = self.setting('customVal', val)				# ===>
	if id(val) != id(self.unsetVal) and self.implemented():
	    # Re-deploy if already implemented (and doing set)
	    return self.deploy()					# ===>
	else:
	    return setVal						# ===>
    def default(self, val=unsetVal):
	"""Set default val of var, if val passed in call, or get current, and 
	'deploy' appropriate value if doing set.

	NameError raised if get attempted and no val set."""

	setVal = self.setting('defaultVal', val)
	if id(val) != id(self.unsetVal):
	    # deploy (if doing set)
	    return self.deploy()					# ===>
	else:
	    return setVal
    def func(self, val=unsetVal):
	"""Set change func for var, if val passed in call, or get current.

	NameError raised if get attempted and no change func set."""

	# We wrap func in a list (and unwrap it, coming back out), in order to
	# avoid having it converted to a method by the class mechanism.
	if id(val) != id(self.unsetVal):
	    self.chngFunc = [val]
	    return self.chngFunc
	else:
	    if self.chngFunc:
		return self.chngFunc[0]					# ===>
	    else:
		raise NameError

    # Private:
    def implemented(self, val=None):
	"""Return 0 if var has been implemented (default set and value imposed),
	1 otherwise."""

	if val:
	    self.implementedVal = val
	return self.implementedVal					# ===>
    def deploy(self):
	"""Impose actual assignment for variable, in module.

	Value used is either custom, if any, or else default."""

	try:
	    val = self.setting('customVal')
	except NameError:
	    val = self.setting('defaultVal')
	# Apply assignment func to val
	val = self.func()(self.moduleName,self.varName, val)
	# Register the fact that the var has been implemented
	self.implemented(1)
	return val							# ===>
    def setting(self, which, val=unsetVal):
	"""Set custom or default var val, if val passed, or return current.

	NameError is raised if get attempted of nonexistent setting."""

	if id(val) == id(self.unsetVal):
	    # No val specified - retrieve current setting
	    val = getattr(self, which)
	    if id(val) == id(self.unsetVal):
		raise NameError, ("No established %s." % which)		# ===>
	    else:
		return val						# ===>
	else:				# Register setting
	    setattr(self, which, val)
	    return val							# ===>

def status(module=None, var=None):
    """Get customization variable registration status.

    With no args, return a list of modules for which customizations have been
    registered.

    Given MODULE, return a list of var names which have customizations.

    Given MODULE and VAR name, return a dict with 'default' value, 'custom'
    value, a 0 or 1 value for 'implemented', and a change 'func', for each
    aspect that has been registered.  (That is, there will only be an, eg,
    'func' entry if a change function was registered for the var.)"""

    if not module:
	# Return a list of modules registered:
	return custs.keys()						# ===>
    else:
	try: vars = custs[module]
	except KeyError:
	    return None							# ===>
	if not var:
	    return vars.keys()						# ===>

	# We have a var - get the status of it:
	try: it = vars[var]
	except KeyError:
	    return None							# ===>
	got = {'implemented': it.implemented()}
	for attr, query in (('default', it.default),
			    ('custom', it.custom),
			    ('func', it.func)):
	    try: got[attr] = query()
	    except NameError: pass
	return got							# ===>

def config(module, var, val):
    """User-side interface to package customization mechanism.

    Given MODULE name, VARIABLE name, and VALUE, register that custom
    value, and have it deployed if a default value has been registered."""

    # Get the registration dict and CustomVar for the module and var:
    varObj = getVarObj(module, var)

    # Register the value:
    varObj.custom(val)

def implement(module, var, val, func=None):
    """Package-side interface to package customization mechanism.

    Given MODULE name, VARIABLE name, register VALUE as default, and
    have the correct value (custom if one exists, or else this default)
    deployed, using optional fourth argument, assignment FUNCTION, if
    specified, or default assignment function, 'assign', if not."""

    # Get the registration dict and CustomVar for the module and var:
    varObj = getVarObj(module, var)

    # Register the value:
    if func:
	varObj.func(func)
    return varObj.default(val)

# Utility funcs.

def cancel(module, var):
    """Deregister from MODULE, VAR, so that future 'configs' will not
    inherently implement the new value."""

    if not status(module, var):
	raise NameError, "No registration for var %s in module %s" % (module,
								      var)
    else:
	del custs[module][var]

def getVarObj(module, var):
    """Given MODULE and VARIABLE names, return a CustomVar instance to
     represent it."""

    try:
	modDict = custs[module]
	try:				# Module has registrations, try var
	    varObj = modDict[var]
	except KeyError:		# Var not yet registered
	    varObj = CustomVar(module, var)
	    modDict[var] = varObj
    except KeyError:			# Nothing registered for module so far
	varObj = CustomVar(module, var)
	custs[module] = {var: varObj}

    return varObj							# ===>


# Var/val assignment functions:

def assign(mod, var, val):
    """Trivial variable-setting routine, used by default by implement().

    Returns prevailing value, as all change-funcs should."""
    try:
	sys.modules[mod].__dict__[var] = val
    except KeyError:
	raise CustomError, "No module '%s' found in sys.modules" % mod
    return val

def loudassign(mod, var, val):
    """Same as 'assign', but print an announcement before doing so."""
    stat = status(mod, var)
    if stat and stat.has_key('custom'):
	form = 'custom'
    else: form = 'default'
    print "Assigning %s.%s = '%s' (%s val)" % (mod, var, val, form)
    assign(mod, var, val)

def ignore(mod, var, val):
    """Null variable-setting routine, available to prevent updates.

    Returns prevailing value, as all change-funcs should."""
    return getattr(mod, var, val)

python-dev Summary for 2007-04-01 through 2007-04-15
++++++++++++++++++++++++++++++++++++++++++++++++++++

.. contents::

[The HTML version of this Summary is available at
http://www.python.org/dev/summary/2007-04-01_2007-04-15]



=========
Summaries
=========

---------------
About SSL tests
---------------

An open bug about missing SSL tests (#451607) was brought up to close or keep
open. Jean-Paul Calderone mentioned an improved testing method by spawning a
'openssl s_server' for testing purposes. This sparked some talk about the
terminating of subprocesses in a cross-platform manner (See `Cross-Platform
Subprocess Termination`).

Contributing thread:

- `About SSL tests <http://mail.python.org/pipermail/python-dev/2007-April/072443.html>`__

-------------------------------------
Cross-Platform Subprocess Termination
-------------------------------------

Because os.kill only works on nix and OS X platforms, leaving Windows
platforms uncovered. Although subprocess.TerminateProcess exists for Windows
platforms, it requires the use of handles and additional overhead for use.
Support was overall given for adding a UNIX-only signal() method and a cross-
platform terminate() method to Popen instances. Nothing was said of actually
incorporating these changes into the subprocess module, although code was
given.

This was mixed in with the above thread.

------------------------
Extended buffer protocol
------------------------

Updates to the buffer protocol are discussed, along with the proposal pre-PEP
documenting the updates for Python 3000, but brought to Python-Dev, due so the
plans of backporting to 2.6 afterwards.

(Note: I couldn't summarize this well enough to cover much of it do any real
degree, but it is currently a Py3k issue, so maybe that is OK. If no one wants
to add to the summary, it will stay short.)

Contributing threads:

- `Extended buffer PEP <http://mail.python.org/pipermail/python-dev/2007-April/072620.html>`__
- `PEP 3118: Extended buffer protocol (new version) <http://mail.python.org/pipermail/python-dev/2007-April/072537.html>`__
- `Extended Buffer Protocol - simple use examples <http://mail.python.org/pipermail/python-dev/2007-April/072535.html>`__

-----------------------------------------
function for counting items in a sequence
-----------------------------------------

A patch was submitted by Steven Bethard (http://bugs.python.org/1696199),
implemented a discussed collections.counts() function to provide a mapping
between items in an iterable and the number of times they appear. There were
suggested names, but none overthrew the original 'counts()' and a question of
items not appearing being counted as 0 or raising a KeyError, with 0 winning
due to a just-makes-sense factor.

Contributing thread:

- `function for counting items in a sequence <http://mail.python.org/pipermail/python-dev/2007-April/072502.html>`__

----------------------------------------
context manager - generator interaction?
----------------------------------------

A problem was brought up with iterator context managers and iteration inside
the with-block raising its StopIteration, but being caught by the context
manager mechanics. It was also responded that the problem would not exist
without the use of overly broad try blocks, and this lead to the addition of
a formal note in PEP 8 about keeping narrow try blocks.

Contributing thread:

- `context manager - generator interaction? <http://mail.python.org/pipermail/python-dev/2007-April/072484.html>`__

-----------------------------
proposed which.py replacement
-----------------------------

Suggestion of replacing the which.py script in the Tools directory migrated to
its proposal for inclusion into the standard library. A patch and tests have
yet to be provided.

Contributing thread:

- `proposed which.py replacement <http://mail.python.org/pipermail/python-dev/2007-April/072424.html>`__

-----------------------
minidom and DOM level 2
-----------------------

What is missing for DOM Level 2 support in minidom was highlighted and some work jumpstarted.

Contributing thread:

- `minidom and DOM level 2 <http://mail.python.org/pipermail/python-dev/2007-April/072499.html>`__

----------------------------------------------
test_pty.py hangs in verbose mode on Mac OS X?
----------------------------------------------

Differing buffering behavior was causing test_pty to block only in verbose
mode. Solutions may include reading to clear the buffer of child processes
before a waitpid() call.

Contributing thread:

- `test_pty.py hangs in verbose mode on Mac OS X? <http://mail.python.org/pipermail/python-dev/2007-April/072592.html>`__

-------------------------
HTTP Responses and Errors
-------------------------

In 2xx HTTP responses mean that the request was handled OK.  The
existing library was special-casing the most common responses and
treating others as errors.  After verifying that there wasn't a good
reason for the old behavior, Facundo Batista fixed it.

Contributing thread:

- `HTTP responses and errors <http://mail.python.org/pipermail/python-dev/2007-April/072547.html>`__

------------------------
Build Problem on Windows
------------------------

It is a generated file; the actual problem is in make_buildinfo

Contributing thread:

- `build problem on windows: unable to find getbuildinfo2.c <http://mail.python.org/pipermail/python-dev/2007-April/072580.html>`__

--------------------------
BaseException Pickle Issue
--------------------------

Exceptions are now new-style classes; this caused some obscure
problems with picking and unpickling.

   http://www.python.org/sf/1498571

and later

   http://www.python.org/sf/1692335

should resolve the issue.

Contributing thread:

- `BaseException pickle issue <http://mail.python.org/pipermail/python-dev/2007-April/072416.html>`__

---------------------------------
Deprecating BaseException.message
---------------------------------

Plans changed; BaseException will still accept an args tuple, so don't
bother with the .message attribute. Probably the shortest leaved Python
feature ever. See PEP 352.

Contributing thread:

- `deprecating BaseException.message <http://mail.python.org/pipermail/python-dev/2007-April/072542.html>`__

---------------------
Changes to decimal.py
---------------------

The external standard has been updated; python's implementation will
be updated to match.

Contributing threads:

- `Changes to decimal.py <http://mail.python.org/pipermail/python-dev/2007-April/072548.html>`__
- `Fwd: Re: Changes to decimal.py <http://mail.python.org/pipermail/python-dev/2007-April/072556.html>`__

----------------------------------------
Pydoc Rewrite Discussion at doc-sig list
----------------------------------------

An announcement that the (normally quiet) doc-sig mailing list would
be discussing a rewrite of pydoc.
http://mail.python.org/pipermail/doc-sig/

Contributing thread:

- `Pydoc Rewrite Discussion at doc-sig list. <http://mail.python.org/pipermail/python-dev/2007-April/072596.html>`__

------------------------------
Making builtins more efficient
------------------------------

Andrea Griffini posted a patch at sourceforge that makes builtin
lookups almost as fast as locals.

https://sourceforge.net/tracker/?func=detail&atid=305470&aid=1616125&group_id=5470

Contributing thread:

- `Making builtins more efficient <http://mail.python.org/pipermail/python-dev/2007-April/072610.html>`__

===============
Skipped Threads
===============

- `Checking PEP autobuild results <http://mail.python.org/pipermail/python-dev/2007-April/072544.html>`__
- `Python 2.5.1c1 pickle problem <http://mail.python.org/pipermail/python-dev/2007-April/072565.html>`__
- `Summary of Tracker Issues <http://mail.python.org/pipermail/python-dev/2007-April/072417.html>`__
- `possible urllib bug on Windows XP <http://mail.python.org/pipermail/python-dev/2007-April/072445.html>`__
- `Py2.5.1 release candidate <http://mail.python.org/pipermail/python-dev/2007-April/072550.html>`__
- `Some new additions to functools <http://mail.python.org/pipermail/python-dev/2007-April/072614.html>`__
- `Python+XUL <http://mail.python.org/pipermail/python-dev/2007-April/072435.html>`__
- `Distutils and -framework on MacOSX <http://mail.python.org/pipermail/python-dev/2007-April/072451.html>`__
- `[Python-checkins] svn dead? <http://mail.python.org/pipermail/python-dev/2007-April/072559.html>`__
- `Just saying hello <http://mail.python.org/pipermail/python-dev/2007-April/072572.html>`__
- `ok to just checkin minor obvious fixes? <http://mail.python.org/pipermail/python-dev/2007-April/072600.html>`__
- `__lltrace__ <http://mail.python.org/pipermail/python-dev/2007-April/072608.html>`__
- `new subscriber looking for grunt work <http://mail.python.org/pipermail/python-dev/2007-April/072612.html>`__
- `functools additions <http://mail.python.org/pipermail/python-dev/2007-April/072615.html>`__
- `Python Documentation Problem Example <http://mail.python.org/pipermail/python-dev/2007-April/072427.html>`__
- `Get 2.5 changes in now, branch will be frozen soon <http://mail.python.org/pipermail/python-dev/2007-April/072429.html>`__
- `Quoting netiquette reminder [Re: proposed which.py replacement] <http://mail.python.org/pipermail/python-dev/2007-April/072440.html>`__
- `branch is frozen for release of 2.5.1c1 (and 2.5.1) <http://mail.python.org/pipermail/python-dev/2007-April/072483.html>`__
- `More exposure for PEP8 (was: context manager - generator interaction?) <http://mail.python.org/pipermail/python-dev/2007-April/072496.html>`__
- `[Python-checkins] Python Regression Test Failures opt (1) <http://mail.python.org/pipermail/python-dev/2007-April/072498.html>`__
- `Weekly Python Patch/Bug Summary <http://mail.python.org/pipermail/python-dev/2007-April/072534.html>`__
- `USE_FAST code in stringobject.c <http://mail.python.org/pipermail/python-dev/2007-April/072551.html>`__
- `Fwd: Re: Py2.5.1 release candidate <http://mail.python.org/pipermail/python-dev/2007-April/072553.html>`__
- `svn.python.org <http://mail.python.org/pipermail/python-dev/2007-April/072561.html>`__
- `[PATCH] pep 0324 URL update <http://mail.python.org/pipermail/python-dev/2007-April/072574.html>`__
- `my 2.5 checkins <http://mail.python.org/pipermail/python-dev/2007-April/072604.html>`__
- `fdopen mode needs sanitizing <http://mail.python.org/pipermail/python-dev/2007-April/072611.html>`__
- `Py3: function signatures, type checking, and related crap <http://mail.python.org/pipermail/python-dev/2007-April/072625.html>`__
- `concerns regarding callable() method <http://mail.python.org/pipermail/python-dev/2007-April/072514.html>`__
- `A Survey on Defect Management Practices in Free/Open Source Software <http://mail.python.org/pipermail/python-dev/2007-April/072470.html>`__
- `RELEASED Python 2.5.1, release candidate 1 <http://mail.python.org/pipermail/python-dev/2007-April/072558.html>`__
- `Python 3000 PEP: Postfix type declarations <http://mail.python.org/pipermail/python-dev/2007-April/072419.html>`__
- `test_socketserver flakey? <http://mail.python.org/pipermail/python-dev/2007-April/072441.html>`__




========
Epilogue
========

This is a summary of traffic on the `python-dev mailing list`_ from
April 01, 2007 through April 15, 2007.
It is intended to inform the wider Python community of on-going
developments on the list on a semi-monthly basis.  An archive_ of
previous summaries is available online.

An `RSS feed`_ of the titles of the summaries is available.
You can also watch comp.lang.python or comp.lang.python.announce for
new summaries (or through their email gateways of python-list or
python-announce, respectively, as found at http://mail.python.org).

This python-dev summary is written by Steven Bethard.

To contact me, please send email:

- Steven Bethard (steven dot bethard at gmail dot com)

Do *not* post to comp.lang.python if you wish to reach me.

The `Python Software Foundation`_ is the non-profit organization that
holds the intellectual property for Python.  It also tries to advance
the development and use of Python.  If you find the python-dev Summary
helpful please consider making a donation.  You can make a donation at
http://python.org/psf/donations.html .  Every cent counts so even a
small donation with a credit card, check, or by PayPal helps.


--------------------
Commenting on Topics
--------------------

To comment on anything mentioned here, just post to
`comp.lang.python`_ (or email python-list@python.org which is a
gateway to the newsgroup) with a subject line mentioning what you are
discussing.  All python-dev members are interested in seeing ideas
discussed by the community, so don't hesitate to take a stance on
something.  And if all of this really interests you then get involved
and join `python-dev`_!


-------------------------
How to Read the Summaries
-------------------------

This summary is written using reStructuredText_. Any unfamiliar
punctuation is probably markup for reST_ (otherwise it is probably
regular expression syntax or a typo :); you can safely ignore it.  We
do suggest learning reST, though; it's simple and is accepted for
`PEP markup`_ and can be turned into many different formats like HTML
and LaTeX.

.. _python-dev: http://www.python.org/dev/
.. _python-dev mailing list: http://mail.python.org/mailman/listinfo/python-dev
.. _comp.lang.python: http://groups.google.com/groups?q=comp.lang.python
.. _PEP Markup: http://www.python.org/peps/pep-0012.html

.. _reST:
.. _reStructuredText: http://docutils.sf.net/rst.html
.. _Python Software Foundation: http://python.org/psf/

.. _archive: http://www.python.org/dev/summary/
.. _RSS feed: http://www.python.org/dev/summary/channews.rdf


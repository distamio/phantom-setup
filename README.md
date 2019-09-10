Phantom setup
=============

> phantom-setup: generate initial conditions for [Phantom](https://bitbucket.org/danielprice/phantom) simulations


[![Build Status](https://travis-ci.org/dmentipl/phantom-setup.svg?branch=master)](https://travis-ci.org/dmentipl/phantom-setup)
[![Coverage Status](https://coveralls.io/repos/github/dmentipl/phantom-setup/badge.svg?branch=master)](https://coveralls.io/github/dmentipl/phantom-setup?branch=master)
[![PyPI](https://img.shields.io/pypi/v/phantomsetup)](https://pypi.org/project/phantomsetup/)

Install
-------

```
pip install phantomsetup
```

Usage
-----

To generate initial conditions for a Phantom simulation via a Python script with phantom-setup:

1. Instantiate a `phantomsetup.Setup` object.
2. Add particles, set arrays, units, equation of state, and other parameters.
3. Write a Phantom HDF5 dump file containing the particle arrays.
4. Write a Phantom in file containing the run time parameters.

Examples
--------

See `examples/setup_dustybox.py` to setup a Phantom simulation to perform the DUSTYBOX test.

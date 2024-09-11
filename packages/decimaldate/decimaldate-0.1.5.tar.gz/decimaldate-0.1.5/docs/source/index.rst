######################################################
  ``decimaldate`` Documentation
######################################################

.. image:: https://readthedocs.org/projects/decimaldate/badge/?version=latest
    :target: https://decimaldate.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://img.shields.io/badge/python-3.12-blue
   :target: https://www.python.org/downloads/release/python-3120/

.. image:: https://img.shields.io/badge/python-3.11-blue
   :target: https://www.python.org/downloads/release/python-3110/

.. image:: https://img.shields.io/pypi/v/decimaldate.svg
   :target: https://pypi.org/project/Sphinx/
   :alt: Package on PyPI

.. image:: https://img.shields.io/badge/License-BSD%203--Clause-blue.svg
   :target: https://opensource.org/licenses/BSD-3-Clause
   :alt: BSD 3 Clause

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black

.. meta::
   :description: Supports decimal dates on the form yyyymmdd
   :keywords: decimaldate Decimal Date

.. toctree::
   :hidden:
   :maxdepth: 2
   :caption: Contents:

   Overview <self>
   installation
   changelog

================
  Introduction
================

This documentation was generated |today|.

``decimaldate`` is a python utility package to handle integer dates on the form ``yyyymmdd``.

Many times when you work with databases and dates you encounter dates on the form ``yyyymmdd`` stored as integers.
Compared to other formats like ``ddmmyyyy``, ``mmddyyyy``, and ``mmddyy`` these are easily comparable and thus sortable.

-----------
Convenience
-----------

As the base is an integer, there are no separators used.

For convenience you can use a Python feature using ``_`` to improve readability
in your source code when writing ``int`` values
like: ``2024_02_28`` which is equivalent ``20240228`` (or ``2_0_2_4_0_2_2_8``).

Using ``_`` is convenient for integers with information like:
dates, phone numbers, social security numbers, and zip codes.

The documentation and source code will use ``_`` extensively to improve readability.

>>> 2024_03_12
   20240312

This also works for strings when parsed as an integer:

>>> int("2024_03_12")
   20240312

>>> from decimaldate import DecimalDate
>>> DecimalDate("2024_02_14")
   DecimalDate(20240214)

=======
  Use
=======



===============
  Outstanding
===============

- range negative index
- range step

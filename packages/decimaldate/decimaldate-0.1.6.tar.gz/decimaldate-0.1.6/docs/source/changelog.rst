##############
  Change Log
##############

==========
  Latest
==========

======================
  0.1.6 (2024-09-11)
======================

New Features
------------

* None.

Other Changes
-------------

* Updates to documentation.

Bugfixes
--------

* None.

======================
  0.1.5 (2024-09-10)
======================

New Features
------------

* range index ``[]`` now accepts negative integer values.

  >>> from decimaldate import DecimalDate
  >>> DecimalDate.range(2024_03_01, 2024_05_04)[2]
    DecimalDate(20240303)

  >>> from decimaldate import DecimalDate
  >>> DecimalDate.range(2024_03_01, 2024_05_04)[-2]
    DecimalDate(20240502)

Other Changes
-------------

* None.

Bugfixes
--------

* None.

======================
  0.1.4 (2024-09-10)
======================

Initial Release
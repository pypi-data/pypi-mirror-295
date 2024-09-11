Welcome to OASIS_stat's documentation!
======================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   readme
   installation
   contributing
   api/index
   history
   authors


Installation
============

To install OASIS, use the following pip command:

.. code-block:: bash

   pip install OASIS_stat

This will install the latest version of OASIS from PyPI (additional code and information on github at https://github.com/TavorB/oasis_stat). For more background on the test, and a detailed description of it's theoretical guarantees and the optimization procedures devised, please refer to the original paper: https://www.pnas.org/doi/10.1073/pnas.2304671121.

Minimal Example
===============

The main function in the package is OASIS_pvalue. Here is a minimal example of how to use it:

.. code-block:: python

   from oasis_stat import OASIS_pvalue

   # Generate a contingency table
   contingency_table = [[10, 20], [30, 40]]

   # Compute the p-value
   p_value = OASIS_pvalue(contingency_table)

   print(p_value)

This will output the finite-sample valid p-value of the OASIS test on the given contingency table.



Indices and tables
==================
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

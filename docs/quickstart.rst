Quickstart Guide
================


About
-----

..
    .. image:: ../../images/iudx_python_sdk.png
        :width: 150
        :alt: IUDX Python SDK

Simplifies using the **India Urban Data Exchange** `IUDX <https://iudx.org.in>`_ platform. 
Provides an API interface to perform scientific computing over various smart city resources.
Vist the `IUDX Catalogue <https://catalogue.iudx.org.in>`_ to discover datasets of your interest.

`IUDX Python SDK <https://github.com/datakaveri/iudx-python-sdk>`_ is developed entirely 
in `Python3 <https://www.python.org/download/releases/3.0/>`_ and uses IUDX core apis to provide 
a simple interface to access smart city's data.


Installation
------------

IUDX Python SDK can be directly downloaded using the **pip** 
(`Python Package Installer <https://pip.pypa.io/en/stable/>`_) using the following command:

::

   pip install git+https://github.com/datakaveri/iudx-python-sdk


Sample Ipython Notebooks
------------------------

| A simple IPython notebook going throught the entire process can be found at `Getting Started.ipynb <https://github.com/datakaveri/iudx-python-sdk/blob/master/examples/Getting%20Started.ipynb>`_
| A sample notebook to download sensors' data is also available at `Download ITMS Dataset.ipynb <https://github.com/datakaveri/iudx-python-sdk/blob/master/examples/Download%20ITMS%20Dataset.ipynb>`_


Example Usage
-------------

Catalogue text search example
*****************************
Get the catalogue list of all sensors based on a text search query.

.. literalinclude:: sample_codes/cat_text_search.py
    :language: python
   
Resources get latest example
****************************
Get the latest data for specific entity id.

.. literalinclude:: sample_codes/rs_get_latest.py
    :language: python

Resources during example
************************
Get the during data for specific entity id.

.. literalinclude:: sample_codes/rs_during.py
    :language: python

Entity data download example
****************************
Get the data for the specific entity and download the generated pandas.dataframe as a .CSV zipped file.

.. literalinclude:: sample_codes/entity_download.py
    :language: python


CLI Usage
---------

Download temporal data
**********************

Download the data based on a during entity query.

::

   # Sample command
   iudx 
   --entity <entity_id> 
   --token <token_id> (only for private resources which requires auth)
   --start <start_timestamp> 
   --end <end_timestamp> 
   --download <file_name>
   --type <file_type_csv_or_json>

   # Example
   iudx --entity datakaveri.org/04a15c9960ffda227e9546f3f46e629e1fe4132b/rs.iudx.org.in/pune-env-aqm/f36b4669-628b-ad93-9970-f9d424afbf75 --start 2021-01-01T14:20:00Z --end 2021-01-07T14:20:00Z --download test_file --type csv


Print latest data
*****************

Print the latest entity data in the console.

::

   # Sample command
   iudx 
   --entity <entity_id> 
   --token <token_id> (only for private resources which requires auth)
   --latest

   # Example
   iudx --entity datakaveri.org/04a15c9960ffda227e9546f3f46e629e1fe4132b/rs.iudx.org.in/pune-env-aqm/f36b4669-628b-ad93-9970-f9d424afbf75 --latest

**NOTE**: :code:`--token` is required for the entities which are not public.
Use :code:`iudx --help` to know more about all possible options.


Tests and IPython Samples
-------------------------

The `Tests <https://github.com/datakaveri/iudx-python-sdk/tree/master/tests>`_ directory and the `Examples <https://github.com/datakaveri/iudx-python-sdk/tree/master/examples>`_ directory contain further usage example codes. 


.. toctree::
   :maxdepth: 4
   :caption: Contents:

   



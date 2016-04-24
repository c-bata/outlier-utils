=============
outlier-utils
=============

.. image:: https://travis-ci.org/c-bata/outlier-utils.svg?branch=master
    :target: https://travis-ci.org/c-bata/outlier-utils

Utility library for detecting and removing outliers from normally distributed datasets using the Smirnov-Grubbs_ test.

Requirements
------------

- Python_ (version 2.7, 3.4 and 3.5)
- SciPy_
- NumPy_

Overview
--------

Both the two-sided and the one-sided version of the test are supported. The former allows extracting outliers from both ends of the dataset, whereas the latter only considers min/max outliers. When running a test, every outlier will be removed until none can be found in the dataset. The output of the test is flexible enough to match several use cases. By default, the outlier-free data will be returned, but the test can also return the outliers themselves or their indices in the original dataset.

Examples
--------

- Two-sided Grubbs test with a Pandas series input

::

   >>> from outliers import smirnov_grubbs as grubbs
   >>> import pandas as pd
   >>> data = pd.Series([1, 8, 9, 10, 9])
   >>> grubbs.test(data, alpha=0.05)
   1     8
   2     9
   3    10
   4     9
   dtype: int64
   
- Two-sided Grubbs test with a NumPy array input   

::

   >>> import numpy as np
   >>> data = np.array([1, 8, 9, 10, 9])
   >>> grubbs.test(data, alpha=0.05)
   array([ 8,  9, 10,  9])
   
- One-sided (min) test returning outlier indices

::

   >>> grubbs.min_test_indices([8, 9, 10, 1, 9], alpha=0.05)
   [3]
   
- One-sided (max) tests returning outliers

::

   >>> grubbs.max_test_outliers([8, 9, 10, 1, 9], alpha=0.05)
   []
   >>> grubbs.max_test_outliers([8, 9, 10, 50, 9], alpha=0.05)
   [50]


.. _Smirnov-Grubbs: https://en.wikipedia.org/wiki/Grubbs%27_test_for_outliers
.. _SciPy: https://www.scipy.org/
.. _NumPy: http://www.numpy.org/
.. _Python: https://www.python.org/


License
=======

This software is licensed under the MIT License.


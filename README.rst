=============
outlier-utils
=============

This is the utils library for removing outliers.

- Smirnov Grubbs Tests

::

   >>> from outliers import smirnov_grubbs as grubbs
   
   >>> import pandas as pd
   >>> data = pd.Series([1, 8, 9, 10, 9])
   >>> grubbs.test(data, 0.05)
   1     8
   2     9
   3    10
   4     9
   dtype: int64
   
   >>> import numpy as np
   >>> data = np.array([1, 8, 9, 10, 9])
   >>> grubbs.test(data, 0.05)
   [ 8  9 10  9]

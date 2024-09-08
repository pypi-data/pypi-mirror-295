# pymof

## Installation
You can install `pymof` using pip

```
pip install pymof           # normal install
pip install --upgrade pymof  # or update if needed
```
**Required Dependencies** :
- Python 3.9 or higher
- numpy>=1.23
- numba>=0.56.0
- scipy>=1.8.0
- scikit-learn>=1.2.0
- matplotlib>=3.5

## Mass ratio variance-based outlier factor (MOF)
----

the outlier score of each data point is called `MOF`. It measures the global deviation of density given sample with respect to other data points.
it is global in the outlier score depend on how isolated. data point is with respect to all data points in the data set.
the variance of mass ratio can identify data points that have a substantially. lower density compared to other data points. 
These are considered outliers.

#### MOF()

> Initial a model of `MOF`

    Parameters :
    Return :
            self : object
                    object of MOF model
#### MOF.fit(Data)
> Fit data to  `MOF` model\
> **Note** The data size should not exceed **10000** points because MOF uses high memory.

    Parameters :
            Data  : numpy array of shape (n_points, d_dimensions)
                    The input samples.
    Return :
            self  : object
                    fitted estimator
#### MOF.visualize()
> Visualize data points with `MOF`'s scores\
> **Note** cannot visualize data points with dimension more than 3

    Parameters :
    Return :
        decision_scores_ : numpy array of shape (n_samples)
                                    decision score for each point
#### MOF attributes
| Attributes | Type | Details |
| ------ | ------- | ------ |
| MOF.Data | numpy array of shape (n_points, d_dimensions) | input data for model |
| MOF.MassRatio | numpy array of shape (n_samples, n_points) | MassRatio for each a pair of points |
| MOF.decision_scores_ | numpy array of shape (n_samples) | decision score for each point |
### Examples
```
# This example demonstrates  the usage of MOF
from pymof import MOF
import numpy as np
X = [[-2.30258509,  7.01040212,  5.80242044],
    [ 0.09531018,  7.13894636,  5.91106761],
    [ 0.09531018,  7.61928251,  5.80242044],
    [ 0.09531018,  7.29580291,  6.01640103],
    [-2.30258509, 12.43197678,  5.79331844],
    [ 1.13140211,  9.53156118,  7.22336862],
    [-2.30258509,  7.09431783,  5.79939564],
    [ 0.09531018,  7.50444662,  5.82037962],
    [ 0.09531018,  7.8184705,   5.82334171],
    [ 0.09531018,  7.25212482,  5.91106761]]
X = np.array(X)
c = MOF()
c.fit(X)
scores = c.decision_scores_
print(scores)
c.visualize()
```
**Output**
```
[0.34541068 0.11101711 0.07193073 0.07520904 1.51480377 0.94558894 0.27585581 0.06242823 0.2204504  0.02247725]
```
![](https://github.com/oakkao/pymof/blob/main/example.png?raw=true)

 
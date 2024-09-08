import numpy as np
from numba import jit
from scipy.stats import rankdata
from scipy.spatial.distance import cdist
from tqdm import tqdm
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt

# Calculate mass ratio matrix
@jit(nopython=True)
def _Massratio(Indexdm,Sortdm,n):
  n= Indexdm.shape[1]
  MassRatio=np.ones((Indexdm.shape[0],Indexdm.shape[1]))
  for r in range(n):
      rm = Sortdm[r,n-1]
      ii = n-1
      for i in range(n-1,-1,-1) :
# when pairwise distance is same, the mass is also same
        if Sortdm[r,i] !=rm:
          rm = Sortdm[r,i]
          ii =i
# Calculate mass ratio
        MassRatio[int(Indexdm[r,i]),r]=MassRatio[int(Indexdm[r,i]),r]*(ii+1)
        MassRatio[r,int(Indexdm[r,i])]=MassRatio[r,int(Indexdm[r,i])]/(ii+1)
  return MassRatio

class MOF:
  '''
  Mass ratio variance-based outlier factor (MOF)
  the outlier score of each data point is called MOF.
  It measures the global deviation of density given sample with respect to other data points.
  it is global in the outlier score depend on how isolated
  data point is with respect to all data points in the data set.
  the variance of mass ratio can identify data points that have a substantially
  lower density compared to other data points.
  These are considered outliers.
  '''
  # Parameters-free
  # ----------
  def __init__(self):
    self.name='MOF'
    self.Sortdm = []
    self.Data = []

  def fit(self,Data):

    '''
    Parameters
    ----------
    Data : numpy array of shape (n_samples, n_features)
        The input samples.
    '''
    '''
    Returns
    -------
    self : object
    '''
#     Fitted estimator.
    n = len(Data)
    self.Data =Data
# Calculate distance matrix
    Dm=cdist(Data,Data)

# Calculate sorted distance matrix
    self.Sortdm = np.sort(Dm)

# Calculate indices of sorted distance matrix
    self.Indexdm = np.argsort(Dm)

# Calculate mass ratio variance (MOF)
    MassRatio=_Massratio(self.Indexdm,self.Sortdm,n)
    self.dif = MassRatio

#  Calculate mass ratio variance (MOF)
    np.fill_diagonal(MassRatio,np.nan)
    self.MassRatio = MassRatio
    score=np.nanvar(MassRatio,axis=1)
    self.decision_scores_=score

# ----------------
# Note The data szie should not exceed 10000 points because MOF uses high memory.
  def visualize(self):
    '''
    Parameters free
    Visualize data points
    '''
    '''
    Parameters
    ----------
    '''
    '''
    Returns
    -------
    '''
    if self.Data.shape[1] == 3:
      fig = plt.figure(figsize=(15, 15))
      ax = fig.add_subplot(111, projection='3d')
      p = ax.scatter(self.Data[:, 0], self.Data[:, 1], self.Data[:, 2], c = np.log(self.decision_scores_+0.00001), cmap='jet')
      fig.colorbar(p)
    elif self.Data.shape[1] == 2:
      fig = plt.figure(figsize=(15, 15))
      ax = fig.add_subplot()
      p = ax.scatter(self.Data[:, 0], self.Data[:, 1], c = np.log(self.decision_scores_+0.00001), cmap='jet')
      fig.colorbar(p)
    else :
      print("Cannot visualize dimension space more than 3")
    return self.decision_scores_

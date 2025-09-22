#Main file to plot the clinical scores
#Vineet Tiruvadi, Sept 27, 2017

import numpy as np
import json
import matplotlib.pyplot as plt
from collections import defaultdict

from mpl_toolkits.mplot3d import Axes3D

import scipy
import scipy.stats as stats

plt.ion()

ClinVect = json.load(open('/home/virati/Dropbox/ClinVec.json'))

do_scales = ['HDRS17','MADRS','GAF']

big_dict = defaultdict(dict)

for ss,scale in enumerate(do_scales):
	plt.figure()
	for pp in range(len(ClinVect['HAMDs'])):
		ab = ClinVect['HAMDs'][pp]
		big_dict[ab['pt']][scale] = ab[scale]

		plt.plot(ab[scale],linewidth=3,alpha=0.6,label=ab['pt'])
	plt.title(scale)
	plt.xlabel('Time (weeks)')
	plt.ylabel('Value')
	plt.legend()
	
from sklearn import linear_model
#%%
#Scatter of HDRS and MADRS
#Do regression ON THIS
do_pts = ['DBS906','DBS905','DBS907','DBS908']
X = []
Y = []

for pat in do_pts:
	#plt.figure()
	#plt.scatter(stats.zscore(big_dict[pat]['HDRS17']),stats.zscore(big_dict[pat]['GAF']))
	#plt.xlabel('HDRS17')
	#plt.ylabel('GAF')
	#plt.title('Scale Scatter')

	fig = plt.figure()
	ax = fig.add_subplot(111,projection='3d')
	ax.scatter(stats.zscore(big_dict[pat]['HDRS17']),stats.zscore(big_dict[pat]['GAF']),stats.zscore(big_dict[pat]['MADRS']))
	ax.set_xlabel('HDRS')
	ax.set_ylabel('GAF')
	ax.set_zlabel('MADRS')
	plt.title(pat)

	X.append(stats.zscore(big_dict[pat]['HDRS17']).reshape(-1,1))
	Y.append(stats.zscore(big_dict[pat]['GAF']).reshape(-1,1))

X = np.array(X).reshape(-1,1)
Y = np.array(Y).reshape(-1,1)
ransac = linear_model.RANSACRegressor()
ransac.fit(X,Y)

lr = linear_model.LinearRegression()
lr.fit(X,Y)

plt.figure()
line_X = np.linspace(-2,2,100).reshape(-1,1)
line_Y = ransac.predict(line_X)
line_Yols = lr.predict(line_X)

plt.plot(line_X,line_Y,label='RANSAC')
plt.plot(line_X,line_Yols,color='red',label='OLS')
plt.scatter(X,Y,alpha=0.2)
plt.title(do_pts)
plt.xlabel('HDRS17')
plt.ylabel('GAF')
plt.legend()

plt.show()

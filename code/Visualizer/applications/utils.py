import numpy as np
# import torch
import random
from sklearn import datasets
from PIL import Image
import pandas as pd
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
from bokeh.plotting import figure, show
from bokeh.embed import json_item
import visualizer.settings as settings
import heapq 

def filter_unique(oldlist, field):
	obj = {}
	newlist = []
	for ele in oldlist:
		if ele[field] not in obj:
			newlist.append(ele)
			obj[ele[field]] = True
	return newlist

def preprocess_data(f_path, i_path, movies):

	## intialization
	rows = min(len(movies), settings.E_NUM)
	rows = len(movies)
	Y_test = np.ones((rows, 1))
	X_test = np.zeros((rows, 1178))
	I_test = []

	## randomly shuffle input movies and take atmost 500
	random.shuffle(movies)
	movies = movies[:rows]

	## intialize labels for each movie
	labels = {}
	cnt = 0
	for row in range(len(movies)):
		image = movies[row]['image']
		image = image.split('.')[0].split('_')[1]
		if image in labels:
			Y_test[row: ] = labels[image]
		else:
			labels[image] = cnt
			Y_test[row: ] = cnt
			cnt = cnt + 1

	## computing X_test, I_test
	for row in range(len(movies)):
		# X_test[row: ] = torch.load(f_path + movies[row]['image'], map_location='cpu').numpy()
		img = np.array(Image.open(i_path + movies[row]['image']).resize((100,100), Image.BICUBIC).convert('RGBA'))
		img = np.rot90(img, 2)
		img = np.fliplr(img)
		I_test.append(img)

	return X_test, Y_test, I_test

def apply_pca(data, pca_components):
	pca = PCA(n_components=pca_components)
	pca_result = pca.fit_transform(data)
	return pca_result

def apply_tsne(data):
	tsne = TSNE(n_components=2, verbose=1, perplexity=40, n_iter=settings.E_ITER)
	tsne_result = tsne.fit_transform(data)
	return tsne_result

def bokeh_plot(I_test, df):
	p = figure(x_range=(-10, 10), y_range=(-10, 10), plot_width=1600, plot_height=800)
	p.image_rgba(image=I_test, x=df['c1'], y=df['c2'], dw=1, dh=2)
	return json_item(p)

def visualize_features(X_test, Y_test, I_test, pca_components):
	feat_cols = [ 'pixel'+str(i) for i in range(X_test.shape[1]) ]
	df = pd.DataFrame(X_test, columns=feat_cols)
	df['label'] = Y_test
	df['label'] = df['label'].apply(lambda i: str(i))

	# if only one data point then pca returns error.
	if X_test.shape[0] == 1:
		df['c1'] = [0]
		df['c2'] = [0]
		return bokeh_plot(I_test, df)

	rndperm = np.random.permutation(df.shape[0])
	pca_result = apply_pca(df[feat_cols].values, pca_components)
	tsne_result = apply_tsne(pca_result[rndperm])
	df_tsne = df.loc[rndperm,:].copy()
	I_copy = []
	for i in range(rndperm.shape[0]):
		I_copy.append(I_test[rndperm[i]])

	df_tsne['c1'] = tsne_result[:, 0]
	df_tsne['c2'] = tsne_result[:, 1]
	return bokeh_plot(I_copy, df_tsne)

def get_distance(x, y):
	return np.linalg.norm(x-y)

def get_top_neighbours(path, image, movies, k):
	k = k + 1
	# features = torch.load(path + image, map_location='cpu').numpy()
	# features = np.array(Image.open(path + image).resize((10,10), Image.BICUBIC)).flatten()[:100]
	random.shuffle(movies)
	maxHeap = []
	for j in range(len(movies)):
		# features2 = torch.load(path + movies[j]['image'], map_location='cpu').numpy()
		# features2 = np.array(Image.open(path + movies[j]['image']).resize((10,10), Image.BICUBIC)).flatten()[:100]
		# d = get_distance(features, features2)
		# print(features.shape, features2.shape)
		# d = np.sum(np.square(features - features2))
		# print(d,j)
		d = 0
		if len(maxHeap) < k:
			heapq.heappush(maxHeap, (-d, j))
		else:
			top = heapq.heappop(maxHeap)
			if (d < -top[0]):
				heapq.heappush(maxHeap, (-d, j))
			else:
				heapq.heappush(maxHeap, top)

	neighbours = []
	for j in range(k - 1, -1, -1):
		top = heapq.heappop(maxHeap)
		neighbours.append(movies[top[1]])
	neighbours = neighbours[::-1]
	return neighbours

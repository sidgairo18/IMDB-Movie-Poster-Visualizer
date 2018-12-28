import numpy as np
# import torch
import json
import random
from sklearn import datasets
from PIL import Image
import pandas as pd
from scipy import spatial
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
from bokeh.plotting import figure, show
from bokeh.embed import json_item
import visualizer.settings as settings
from applications.movies.models import *
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
	# rows = len(movies)
	Y_test = np.ones((rows, 1))
	# Y_test = []
	X_test = np.zeros((rows, np.load(f_path + movies[0]['image'] + '.npy').shape[1]))
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
	# for row in range(len(movies)):
	# 	image = movies[row]['image']
	# 	Y_test.append(image)

	## computing X_test, I_test
	for row in range(len(movies)):
		# X_test[row: ] = torch.load(f_path + movies[row]['image'], map_location='cpu').numpy()
		X_test[row: ] = np.load(f_path + movies[j]['image'] + '.npy')
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

def bokeh_plot(I_test, x_cor, y_cor):
	p = figure(x_range=(-10, 10), y_range=(-10, 10), plot_width=1600, plot_height=800)
	p.image_rgba(image=I_test, x=x_cor, y=y_cor, dw=1, dh=2)
	return json_item(p)

def visualize_features(X_test, Y_test, I_test, pca_components):
	feat_cols = [ 'pixel'+str(i) for i in range(X_test.shape[1]) ]
	df = pd.DataFrame(X_test, columns=feat_cols)
	# df['label'] = Y_test
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
	# save_coordinates(df_tsne['label'], df_tsne['c1'], df_tsne['c2'], 'pca')
	return bokeh_plot(I_copy, df_tsne['c1'], df_tsne['c2'])

def save_coordinates(images, x, y, feature):
	obj = {}
	obj['data'] = []
	for i in range(len(images)):
		obj['data'].append({})
		obj['data'][i]['image'] = images[i]
		obj['data'][i]['x'] = x[i]
		obj['data'][i]['y'] = y[i]
		obj['data'][i]['feature'] = features
	with open('temp.json', 'w') as outfile:
		json.dump(obj, outfile, indent=4, sort_keys=True)

def get_plot_values(i_path, movies, f_name):
	I_test = []
	X_cor = []
	Y_cor = []
	for row in range(len(movies)):
		print(row, len(movies))
		movie = Movie.objects.filter(image=movies[row]['image'])[0]
		feature = Feature.objects.filter(name=f_name)[0]
		feature_to_movie = FeatureToMovie.objects.filter(movie=movie,feature=feature)[0].serialize()
		img = np.array(Image.open(i_path + movies[row]['image']).resize((100,100), Image.BICUBIC).convert('RGBA'))
		img = np.rot90(img, 2)
		img = np.fliplr(img)
		X_cor.append(feature_to_movie['x'])
		Y_cor.append(feature_to_movie['y'])
		I_test.append(img)
	return X_cor, Y_cor, I_test

def get_distance(x, y):
	return np.linalg.norm(x-y)

def get_cosine_similarity(x, y):
	return 1 - spatial.distance.cosine(x, y)

def get_top_neighbours(path, image, movies, k):
	k = k + 1
	features = np.load(path + image + '.npy')
	random.shuffle(movies)
	maxHeap = []
	for j in range(len(movies)):
		features2 = np.load(path + movies[j]['image'] + '.npy')
		d = get_cosine_similarity(features, features2)
		movies[j]['cdistance'] = str(d)[:8]
		d = get_distance(features, features2)
		print(d,j)
		movies[j]['fdistance'] = str(d)[:8]
		# d = 0
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

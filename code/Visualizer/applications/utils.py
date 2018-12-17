import numpy as np
import random
from sklearn import datasets
from PIL import Image
import pandas as pd
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
from bokeh.plotting import figure, show
from bokeh.embed import json_item

def filter_unique(oldlist, field):
	obj = {}
	newlist = []
	for ele in oldlist:
		if ele[field] not in obj:
			newlist.append(ele)
			obj[ele[field]] = True
	return newlist

def preprocess_data(path, movies):

	## intialization
	rows = min(len(movies), 500)
	Y_test = np.ones((rows, 1))
	X_test = np.zeros((rows, 300))
	I_test = []

	## randomly shuffle input movies and take atmost 500
	random.shuffle(movies)
	movies = movies[:rows]

	## intialize labels for each movie
	## TODO

	## computing X_test, I_test
	for row in range(len(movies)):
		X_test[row: ] = np.array(Image.open(path + movies[row]['image']).resize((10,10), Image.BICUBIC)).flatten()
		img = np.array(Image.open(path + movies[row]['image']).resize((100,100), Image.BICUBIC).convert('RGBA'))
		img = np.rot90(img, 2)
		img = np.fliplr(img)
		I_test.append(img)

	return X_test, Y_test, I_test

def apply_pca(data, pca_components):
	pca = PCA(n_components=pca_components)
	pca_result = pca.fit_transform(data)
	return pca_result

def apply_tsne(data):
	tsne = TSNE(n_components=2, verbose=1, perplexity=40, n_iter=500)
	tsne_result = tsne.fit_transform(data)
	return tsne_result

def bokeh_plot(X_test, I_test, df):
	p = figure(x_range=(-500, 500), y_range=(-500, 500), plot_width=950, plot_height=950)
	p.image_rgba(image=I_test, x=df['c1'], y=df['c2'], dw=1, dh=1)
	return json_item(p)

def visualize_features(X_test, Y_test, I_test, pca_components):
	feat_cols = [ 'pixel'+str(i) for i in range(X_test.shape[1]) ]
	df = pd.DataFrame(X_test, columns=feat_cols)
	df['label'] = Y_test
	df['label'] = df['label'].apply(lambda i: str(i))

	rndperm = np.random.permutation(df.shape[0])
	pca_result = apply_pca(df[feat_cols].values, pca_components)
	tsne_result = apply_tsne(pca_result[rndperm])
	df_tsne = df.loc[rndperm,:].copy()
	I_copy = []
	for i in range(rndperm.shape[0]):
		I_copy.append(I_test[rndperm[i]])

	df_tsne['c1'] = tsne_result[:, 0]
	df_tsne['c2'] = tsne_result[:, 1]
	return bokeh_plot(X_test, I_copy, df_tsne)
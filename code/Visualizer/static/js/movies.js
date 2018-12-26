var utils = {
	jsonRequest: function (method, url, data, successCallback, errorCallback) {
        $.ajax({
            headers: {
                'Accept': 'application/json'
            },
            method: method,
            data: method == 'GET' ? data : JSON.stringify(data),
            url: url,
            success: successCallback,
            error: errorCallback
        });
    },
    addGenres: function (genres, select) {
		str = "";
		for(var i = 0; i < genres.length; i++) {
			str += "<option>" + genres[i].name + "</option>";
		}
		select.html(str);
	},
	addFeatures: function(features, select) {
		str = "";
		for(var i = 0; i < features.length; i++) {
			str += "<option>" + features[i].name + "</option>";
		}
		select.html(str);
	},
    shuffle: function (array) {
  		var currentIndex = array.length, temporaryValue, randomIndex;
		while (0 !== currentIndex) {
		randomIndex = Math.floor(Math.random() * currentIndex);
		currentIndex -= 1;
		temporaryValue = array[currentIndex];
		array[currentIndex] = array[randomIndex];
		array[randomIndex] = temporaryValue;
		}
		return array;
	}
};
var global_var;

var top_k_neighbours = {
	'images_per_row': 13,
	'img_limit': 26,
	init: function () {
		$('#optionsSubmit').click(function () {
			syear = $('#optionsSyear').val();
			eyear = $('#optionsEyear').val();
			category = $('#optionsGenre').val();
			syear = (syear != "")? parseInt(syear) : null;
			eyear = (eyear != "")? parseInt(eyear) : null;
			andopr = $('#optionsGenreAnd').is(':checked');
			top_k_neighbours.getMovies(syear, eyear, category, andopr);
		});

		// get genres and random movies at first
		top_k_neighbours.getGenres();
		top_k_neighbours.getFeatures();
		top_k_neighbours.getMovies(null, null, null, null);
	},
	getFeatures: function () {
		utils.jsonRequest('GET', '/ajax/features', {},
		successCallback = function (response) {
			$.notify('successfully fetched features', 'success');
			utils.addFeatures(response.features, $('#optionsFeature'));
		},
		errorCallback = function(response) {
			$.notify('failed to get features', 'error');
		}); 
	},
	getGenres: function () {
		utils.jsonRequest('GET', '/ajax/genres', {},
		successCallback = function (response) {
			$.notify('successfully fetched genres', 'success');
			utils.addGenres(response.genres, $('#optionsGenre'));
		},
		errorCallback = function(response) {
			$.notify('failed to get genres', 'error');
		});
	},
	getMovies: function (syear, eyear, category, andopr) {
		params = {};
		if(syear != null) {
			params.syear = syear;
		}
		if(eyear != null) {
			params.eyear = eyear;
		}
		if(category != null) {
			params.category = category;
		}
		if(andopr != null) {
			params.andopr = andopr;
		}
		utils.jsonRequest('GET', '/ajax/movies', params,
		successCallback = function (response) {
			$.notify('successfully fetched movies', 'success');
			top_k_neighbours.createTable(response.movies);
		},
		errorCallback = function(response) {
			$.notify('failed to get movies', 'error');
		});
	},
	createTable: function (movies) {
		movies = utils.shuffle(movies);
		limit = Math.min(movies.length, top_k_neighbours.img_limit);
		tbody = $('#postersTable').children();
		str = "";
		for(var i = 0; i < top_k_neighbours.img_limit; ) {
			str += '<tr style="align:center">';
			for(var j = 0; j < top_k_neighbours.images_per_row; j++) {
				if(i < limit) {
					str += '<td id="' + (movies[i].image).split(".", 2)[0] + '">';
					str += '<a class="list-group-item list-group-item-action">';
					str += '<img src="/static/' + movies[i].image + '" alt="Image"/>';
				}
				else {
					str += '<td><a class="list-group-item list-group-item-action">';
					str += '<img alt="Image"/>';
				}
				str += '</a></td>';
				i++;
			}
			str += '</tr>';
		}
		tbody.html(str);
		for(var i = 0; i < limit; i++) {
			$('#' + (movies[i].image).split(".", 2)[0]).click(function() {
				top_k_neighbours.getTopNeighbours(this.id + ".txt.jpg");
			});
		}
	},
	getTopNeighbours: function(image) {
		k = $('#optionsK').val();
		k = (k != "")? parseInt(k) : 8;
		feature = $('#optionsFeature').val();
		utils.jsonRequest('GET', '/ajax/top_neighbours', {
			'image': image,
			'k': k,
			'feature': feature
		},
		successCallback = function (response) {
			$.notify('successfully gathered top k','success');
			top_k_neighbours.displayTopNeighbours(response.movies);
		},
		errorCallback = function (response) {
			$.notify('failed to gather top k','error');			
		});
	},
	displayTopNeighbours: function (movies) {
		var num = movies.length;
		var rows = parseInt(num / top_k_neighbours.images_per_row);
		if(num % top_k_neighbours.images_per_row != 0) {
			rows++;
		}
		tbody = $('#topNeighboursTable').children();
		str = "";
		for(var i = 0; i < rows*top_k_neighbours.images_per_row; ) {
			str += '<tr style="align:center">';
			for(var j = 0; j < top_k_neighbours.images_per_row; j++) {
				str += '<td><a class="list-group-item list-group-item-action">';
				if(i < num) {
					str += '<img src="/static/' + movies[i].image + '" alt="Image"/>';
				}
				else {
					str += '<img alt="Image"/>';
				}
				str += '</a>';
				if(i < num) {
					str += top_k_neighbours.getMovieInfo(movies[i]);
				}
				str += '</td>';
				i++;
			}
			str += '</tr>';
		}
		tbody.html(str);
	},
	getMovieInfo: function (movie) {
		var str = "";
		str += '<div class="card text-white bg-primary mb-3" style="max-width: 30rem; text-align:center;">';
		str += '<div class="card-header" style="font-size:17px; padding:3px;">Movie Info</div>';
		str += '<h5 style="padding:10px;">Title</h5><p style="height:50px;">';
		str += movie.title + '</p>';
		str += '<h5 style="padding:10px;">Label</h5><p style="height:25px;">';
		str += movie.image.split("_")[1].split(".")[0] + '</p>';
		str += '<h5 style="padding:10px;">Feature Distance</h5><p style="height:25px;">';
		str += movie.fdistance + '</p>';
		str += '<h5 style="padding:10px;">Cosine Similarity</h5><p style="height:25px;">';
		str += movie.cdistance + '</p>';
		str += '<h5 style="padding:10px;">Genre</h5><p style="height:70px;">';
		for(var k = 0; k < movie.genres.length; k++) {
			str += movie.genres[k] + '<br/>';
		}
		str += '</p></div>';
		return str;
	}
};

var embeddings = {
	init: function () {
		$('#eoptionsSubmit').click(function () {
			syear = $('#eoptionsSyear').val();
			eyear = $('#eoptionsEyear').val();
			category = $('#eoptionsGenre').val();
			syear = (syear != "")? parseInt(syear) : null;
			eyear = (eyear != "")? parseInt(eyear) : null;
			andopr = $('#eoptionsGenreAnd').is(':checked');
			embeddings.bokehPlot(syear, eyear, category, andopr);
		});

		// get all movies plot at first
		embeddings.getGenres();
		embeddings.getFeatures();
		// embeddings.bokehPlot(null, null, null, null);
	},
	bokehPlot: function (syear, eyear, category, andopr) {
		params = {};
		if(syear != null) {
			params.syear = syear;
		}
		if(eyear != null) {
			params.eyear = eyear;
		}
		if(category != null) {
			params.category = category;
		}
		if(andopr != null) {
			params.andopr = andopr;
		}
		utils.jsonRequest('GET', '/ajax/embeddings', params,
		successCallback = function (response) {
			$.notify('successfully fetched embeddings', 'success');
			if(response.error !== undefined) {
				$.notify(response.error, 'error');
			}
			else {
				$('#plot1').html("");
				Bokeh.embed.embed_item(response.plot, "plot1");
			}
		},
		errorCallback = function(response) {
			$.notify('failed to get bokeh plot', 'error');
		});
	},
	getFeatures: function () {
		utils.jsonRequest('GET', '/ajax/features', {},
		successCallback = function (response) {
			$.notify('successfully fetched features', 'success');
			utils.addFeatures(response.features, $('#eoptionsFeature'));
		},
		errorCallback = function(response) {
			$.notify('failed to get features', 'error');
		}); 
	},	getGenres: function () {
		utils.jsonRequest('GET', '/ajax/genres', {},
		successCallback = function (response) {
			$.notify('successfully fetched genres', 'success');
			utils.addGenres(response.genres, $('#eoptionsGenre'));
		},
		errorCallback = function(response) {
			$.notify('failed to get genres', 'error');
		});
	},

}

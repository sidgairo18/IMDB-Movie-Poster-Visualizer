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
		str = "<option>None</option>";
		for(var i = 0; i < genres.length; i++) {
			str += "<option>" + genres[i].name + "</option>";
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
			year = $('#optionsYear').val();
			category = $('#optionsGenre').val();
			year = (year != "")? parseInt(year) : null;
			category = (category != "")? category : null;
			top_k_neighbours.getMovies(year, category);
		});

		// get genres and random movies at first
		top_k_neighbours.getGenres();
		top_k_neighbours.getMovies(null, null);
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
	getMovies: function (year, category) {
		params = {};
		if(year != null) {
			params.year = year;
		}
		if(category != null) {
			params.category = category;
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
		utils.jsonRequest('GET', '/ajax/top_neighbours', {
			'image': image,
			'k': k
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
				str += '</a></td>';
				i++;
			}
			str += '</tr>';
		}
		tbody.html(str);
	}
};

var embeddings = {
	init: function () {
		$('#eoptionsSubmit').click(function () {
			year = $('#eoptionsYear').val();
			year = (year != "")? parseInt(year) : null;
			category = $('#eoptionsGenre').val();
			category = (category != "")? category : null;
			embeddings.bokehPlot(year, category);
		});
		embeddings.getGenres();
	},
	bokehPlot: function (year, category) {
		params = {};
		if(year != null) {
			params.year = year;
		}
		if(category != null) {
			params.category = category;
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
	getGenres: function () {
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
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
		select.innerHTML = str;
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
// var global_var;

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
			utils.addGenres(response.genres, $('#optionsGenre')[0]);
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
		tbody = $('#postersTable').children()[0];
		str = "";
		for(var i = 0; i < top_k_neighbours.img_limit; ) {
			str += '<tr style="align:center">';
			for(var j = 0; j < top_k_neighbours.images_per_row; j++) {
				str += '<td><a href="#" class="list-group-item list-group-item-action">';
				if(i < limit) {
					str += '<img src="/static/images/' + movies[i].image + '" alt="Image"/>';
				}
				else {
					str += '<img alt="Image"/>';
				}
				str += '</a></td>';
				i++;
			}
			str += '</tr>';
		}
		tbody.innerHTML = str;
	}
};

var embeddings = {
	init: function () {
		$('#eoptionsSubmit').click(function () {
			year = $('#eoptionsYear').val();
			year = (year != "")? parseInt(year) : null;
			embeddings.bokehPlot(year);
		});
	},
	bokehPlot: function (year) {
		params = {};
		if(year != null) {
			params.year = year;
		}
		utils.jsonRequest('GET', '/ajax/embeddings', params,
		successCallback = function (response) {
			$.notify('successfully fetched embeddings', 'success');
		},
		errorCallback = function(response) {
			$.notify('failed to get bokeh plot', 'error');
		});		
	}
}
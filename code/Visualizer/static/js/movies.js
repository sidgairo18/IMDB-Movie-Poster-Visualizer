var apis = {
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
		apis.jsonRequest('GET', '/ajax/genres', {},
		successCallback = function (response) {
			$.notify('successfully fetched genres', 'success');
			top_k_neighbours.addGenres(response.genres);
		},
		errorCallback = function(response) {
			$.notify('failed to get genres', 'error');
		});
	},
	addGenres: function (genres) {
		select = $('#optionsGenre')[0];
		str = "";
		for(var i = 0; i < genres.length; i++) {
			str += "<option>" + genres[i].name + "</option>";
		}
		select.innerHTML = str;
	},
	getMovies: function (year, category) {
		params = {};
		if(year != null) {
			params.year = year;
		}
		if(category != null) {
			params.category = category;
		}
		apis.jsonRequest('GET', '/ajax/movies', params,
		successCallback = function (response) {
			$.notify('successfully fetched movies', 'success');
			top_k_neighbours.createTable(response.movies);
		},
		errorCallback = function(response) {
			$.notify('failed to get movies', 'error');
		});
	},
	createTable: function (movies) {
		movies = top_k_neighbours.shuffle(movies);
		limit = Math.min(movies.length, top_k_neighbours.img_limit);
		tbody = $('#postersTable').children()[0];
		str = "";
		for(var i = 0; i < limit;) {
			str += '<tr style="align:center">';
			for(var j = 0; j < top_k_neighbours.images_per_row && i < limit; j++) {
				str += '<td><a href="#" class="list-group-item list-group-item-action"><img src="/static/images/'
				str += movies[i].image + '"/></a></td>';
				i++;
			}
			str += '</tr>';
		}
		tbody.innerHTML = str;
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
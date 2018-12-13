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
// var global_var;

var top_k_neighbours = {
	init: function () {
		$('#optionsSubmit').click(function () {
			year = $('#optionsYear').val();
			category = $('#optionsGenre').val();
			year = (year != "")? parseInt(year) : null;
			category = (category != "")? category : null;
			top_k_neighbours.getMovies(year, category);
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
		apis.jsonRequest('GET', '/ajax/movies', params,
		successCallback = function (response) {
			$.notify('successfully fetched images', 'success');
			top_k_neighbours.createTable(response.movies);
		},
		errorCallback = function(response) {
			$.notify('failed to get images', 'error');
		});
	},
	createTable: function (movies) {
		movies = top_k_neighbours.shuffle(movies);
		limit = Math.min(movies.length, 30);
		tbody = $('#postersTable').children()[0];
		str = "";
		for(var i = 0; i < limit;) {
			str += '<tr style="align:center">';
			for(var j = 0; j < 15 && i < limit; j++) {
				str += '<td><img src="/static/images/' + movies[i].image + '"/></td>';
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
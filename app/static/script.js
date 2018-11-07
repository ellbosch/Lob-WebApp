$(function() {
	// get current date
	var today = new Date();
	var dd = today.getDate();
	var mm = today.getMonth()+1; //January is 0!
	var yyyy = today.getFullYear();
	var hh = today.getHours();

	// sets default date
	$(".datetimepicker").datetimepicker({
		defaultDate: mm + "/" + dd + "/" + yyyy + " " + hh + ":00",
		icons: {
			time: 'far fa-clock',
            date: 'far fa-calendar-alt',
            up: 'fas fa-arrow-up',
            down: 'fas fa-arrow-down',
            previous: 'fas fa-chevron-left',
            next: 'fas fa-chevron-right',
            today: 'far fa-calendar-check',
            clear: 'far fa-trash-alt',
            close: 'fas fa-times'
		}
	});

	// won't set a default date if we're editing an already created event
	$(".datetimepicker_edit_event").datetimepicker({
		defaultDate: convert_python_dt_to_js($('.datetimepicker_edit_event').attr("value")),
		icons: {
			time: 'far fa-clock',
            date: 'far fa-calendar-alt',
            up: 'fas fa-arrow-up',
            down: 'fas fa-arrow-down',
            previous: 'fas fa-chevron-left',
            next: 'fas fa-chevron-right',
            today: 'far fa-calendar-check',
            clear: 'far fa-trash-alt',
            close: 'fas fa-times'
		}
	});

	// change event submission form options if user selects "default" or "sports - game"
	$('input[type=radio][name=event_type]').change(function() {
		update_event_submit_form(this)
	});

	function update_event_submit_form(obj) {
		if (obj != null) {
			// show default options and hide sports options
			if (obj.value == 'default') {
				$('.event_sports').hide();
				$('.event_default').show();
			} 
			// opposite of above
			else {
				$('.event_sports').show();
				$('.event_default').hide();
			}
		}
	}

	// update event form on load
	update_event_submit_form($('input[type=radio][name=event_type]:checked')[0])

	// change event submission form after league is selected
	// $("#league").change(function() {
	// 	var league = $("#league").children("option:selected").val();

	// 	var index = window.location.href.indexOf("?league=");
	// 	window.location.href = window.location.href.substring(0, index) + '?league=' + league;
	// });


	// converts python datetime to js datetime object
	function convert_python_dt_to_js(ts) {
		if (ts != null) {
			var year = ts.substring(0, 4);
			var month = parseInt(ts.substring(5, 7)) - 1;
			var date = ts.substring(8, 10);
			var hours = ts.substring(11, 13);
			var minutes = ts.substring(14, 16);
			var seconds = ts.substring(17, 19);
			return new Date(Date.UTC(year, month, date, hours, minutes, seconds));
		}
	}

	// converts js timestamp to string for time ago
	function get_time_back(date) {
		var date_now = new Date();
		var timedelta = date_now - date;
		var years_ago = parseInt(timedelta / (1000 * 60 * 60 * 24 * 365));
		var months_ago = parseInt(timedelta / (1000 * 60 * 60 * 24 * 30));
		var days_ago = parseInt(timedelta / (1000 * 60 * 60 * 24));
		var hours_ago = parseInt(timedelta / (1000 * 60 * 60));
		var minutes_ago = parseInt(timedelta / (1000 * 60));
		
		// CREATE FRIENDLY STRING TO DESCRIBE WHEN VIDEO WAS POSTED
		if (years_ago > 1) {
			return years_ago + " years ago";
		} else if (years_ago == 1) {
			return years_ago + " year ago";
		} else if (months_ago > 1) {
			return months_ago + " months ago";
		} else if (months_ago == 1) {
			return months_ago + " month ago";
		} else if (days_ago > 1) {
			return days_ago + " days ago";
		} else if (days_ago == 1) {
			return days_ago + " day ago";
		} else if (hours_ago > 1) {
			return hours_ago + " hours ago";
		} else if (hours_ago == 1) {
			return hours_ago + " hour ago";
		} else if (minutes_ago > 1) {
			return minutes_ago + " minutes ago";
		} else {
			return minutes_ago + " minute ago";
		}
	}

	// update timestamps everywhere applicable
	$('.timestamp').each(function() {
		var date_posted = convert_python_dt_to_js($(this).attr("value"));
		$(this).text(get_time_back(date_posted));
	});

	// load more posts when user scrolls
	var waypoints;

	// function call that makes gets more posts
	$SCRIPT_ROOT = $("#script_root").attr("value");
	function append_posts() {
		$.ajax({
			type: "GET",
			url: $SCRIPT_ROOT + "/load-more",
			contentType: "application/javascript",
			dataType: "json",
			crossDomain: true
		}).done(function(data) {
			// store scrollTop value
			pos = $("div_content_block").scrollTop();

			// append html content
			html = ""
			var posts = data.result['posts'];
			for (var i = 0; i < posts.length; i++) {
				post = posts[i]
				var date_posted = new Date(post.uploaded_at);

				html = html + 
					`<div class="card card_video border-light">
						<video class="card-img-top" loop controls playsinline preload="auto"><source src="` + post.url + `" type="video/mp4"></video>
						<div class="card-body">
							<h5 class="card-title">` + post.text + `</h5>
							<small class="text-muted timestamp" value="` + post.uploaded_at + `">` + get_time_back(date_posted) + `&nbsp;&nbsp;&nbsp;</small>
						</div>
					</div>`;

				$("div_content_block").scrollTop(pos);
			}
			Waypoint.destroyAll();			// destroys waypoint, but we'll recreate it
			$(".container_videos").append(html);	// updates DOM

			// only recreate waypoint if there are more posts to load
			if (!data.result['error']) {
				create_waypoint();
			} else {
				$("#load-more-posts").hide();
			}
		}).fail(function(e) {
			console.log(e);
		});
	}

	// create waypoint for loading more posts
	function create_waypoint() {
		waypoints = $("#load-more-posts").waypoint({
			handler: function() {
				append_posts();
			},
			offset: 'bottom-in-view'//,
			// context: $("#div_content_block")
		})
	}

	create_waypoint();


});
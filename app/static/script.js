$(function() {
	// get current date
	var today = new Date();
	var dd = today.getDate();
	var mm = today.getMonth()+1; //January is 0!
	var yyyy = today.getFullYear();
	var hh = today.getHours();

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

	// update timestamps everywhere applicable
	$('.timestamp').each(function() {
		var ts = $(this).attr("value");
		var year = ts.substring(0, 4);
		var month = parseInt(ts.substring(5, 7)) - 1;
		var date = ts.substring(8, 10);
		var hours = ts.substring(11, 13);
		var minutes = ts.substring(14, 16);
		var seconds = ts.substring(17, 19);

		var date_posted = new Date(Date.UTC(year, month, date, hours, minutes, seconds));
		var date_now = new Date();
		var timedelta = date_now - date_posted;
		var years_ago = parseInt(timedelta / (1000 * 60 * 60 * 24 * 365));
		var months_ago = parseInt(timedelta / (1000 * 60 * 60 * 24 * 30));
		var days_ago = parseInt(timedelta / (1000 * 60 * 60 * 24));
		var hours_ago = parseInt(timedelta / (1000 * 60 * 60));
		var minutes_ago = parseInt(timedelta / (1000 * 60));
		
		// CREATE FRIENDLY STRING TO DESCRIBE WHEN VIDEO WAS POSTED
		if (years_ago > 1) {
			$(this).text(years_ago + " years ago");
		} else if (years_ago == 1) {
			$(this).text(years_ago + " year ago");
		} else if (months_ago > 1) {
			$(this).text(months_ago + " months ago");
		} else if (months_ago == 1) {
			$(this).text(months_ago + " month ago");
		} else if (days_ago > 1) {
			$(this).text(days_ago + " days ago");
		} else if (days_ago == 1) {
			$(this).text(days_ago + " day ago");
		} else if (hours_ago > 1) {
			$(this).text(hours_ago + " hours ago");
		} else if (hours_ago == 1) {
			$(this).text(hours_ago + " hour ago");
		} else if (minutes_ago > 1) {
			$(this).text(minutes_ago + " minutes ago");
		} else {
			$(this).text(minutes_ago + " minute ago");
		}
	});

});
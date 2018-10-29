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
});
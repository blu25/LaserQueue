// put any utilities and functions here


// logs text to devlog on page
function logText(text) {
	var currentTime = new Date();
	var currentHours = currentTime.getHours();
	var currentMinutes = currentTime.getMinutes();
	var currentSeconds = currentTime.getSeconds();
	var currentMillis = currentTime.getMilliseconds();

	var hoursZero = (currentHours < 10 ? '0' : '');
	var minutesZero = (currentMinutes < 10 ? '0' : '');
	var secondsZero = (currentSeconds < 10 ? '0' : '');
	var millisZero = (currentMillis < 10 ? '00' : currentMillis < 100 ? '0' : '');
	$(".log-pre").prepend("<span class='log-time'> [" + hoursZero + currentHours + ":" + minutesZero + currentMinutes + ":" + secondsZero + currentSeconds + "." + millisZero + currentMillis + "]:</span> " + text + "\n");
}

// repopulate action button index
function populateActions() {
	$(".cutting-table tr:not(.table-first-row) td:nth-child(1)").each(function(index, el) {
		$(el).children('i').prop('data-index', index);
	});

	// reinitialize bootstrap tooltips
	$('[data-toggle="tooltip"]').tooltip();
	
	// handler to remove a job
	$(".remove-job").mouseup(function() {
		logText("removing item " + $(this).attr("data-index"));
		socket.send(JSON.stringify({
			"action": "sremove",
			"args": [+$(this).attr("data-index")]
		}));
	});

	// handler to lower a job
	$(".lower-priority").mouseup(function() {
		logText("passing item " + $(this).attr("data-index"));
		socket.send(JSON.stringify({
			"action": "spass",
			"args": [+$(this).attr("data-index")]
		}));
	});
}

// displays message in modal
function modalMessage(modalTitle, modalBody) {
	$('.notify-modal-title').html(modalTitle);
	$('.notify-modal-body').html(modalBody);
	$('#notify-modal').modal();
}

// reset a form
// with thanks to http://stackoverflow.com/questions/680241/resetting-a-multi-stage-form-with-jquery
function resetForm(form) {
	form.find('input:text, input:password, input:file, textarea').val(''); // removed 'select'
	form.find('input:radio, input:checkbox').removeAttr('checked').removeAttr('selected');
	if($(form).selector == ".new-cut-form") {
		// here is for resetting the form
		// later. maybe milestone 0.1.0
	}
}
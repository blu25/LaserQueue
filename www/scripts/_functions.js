// put any utilities and functions here


// logs text to devlog on page
function logText(text) {
	if(devLog) {
		var currentTime = new Date();
		var currentHours = currentTime.getHours();
		var currentMinutes = currentTime.getMinutes();
		var currentSeconds = currentTime.getSeconds();
		var currentMillis = currentTime.getMilliseconds();

		var hoursZero = (currentHours < 10 ? '0' : '');
		var minutesZero = (currentMinutes < 10 ? '0' : '');
		var secondsZero = (currentSeconds < 10 ? '0' : '');
		var millisZero = (currentMillis < 10 ? '00' : currentMillis < 100 ? '0' : '');
		$('.log-pre').prepend('<span class="log-time"> [' + hoursZero + currentHours + ':' + minutesZero + currentMinutes + ':' + secondsZero + currentSeconds + '.' + millisZero + currentMillis + ']:</span> ' + text + '\n');
	}
}

// repopulate action button index
function populateActions() {
	logText('Populating actions');
	$('.cutting-table-template tr td:nth-child(1)').each(function(index, el) {
		$(el).children('i').each(function(iIndex, iElement) {
			$(iElement).attr('data-uuid', allCuts[index].uuid);
			$(iElement).unbind('click');
		});
	});

	// reinitialize bootstrap tooltips
	if(isTouchDevice() == false) {
		$('[data-toggle="tooltip"]').tooltip();
	}
	// handler to remove a job
	$('.remove-job').click(function() {
		logText('removing item ' + $(this).attr('data-uuid'));
		socketSend({
			'action': 'uremove',
			'args': [$(this).attr('data-uuid')]
		});
	});

	// handler to lower a job
	$('.lower-priority').click(function() {
		logText('passing item ' + $(this).attr('data-uuid'));
		socketSend({
			'action': 'upass',
			'args': [$(this).attr('data-uuid')]
		});
	});

	// handler to decrement a job
	$('.decrement-job').click(function() {
		logText('removing item ' + $(this).attr('data-uuid'));
		socketSend({
			'action': 'udecrement',
			'args': [$(this).attr('data-uuid')]
		});
	});

	// handler to increment a job
	$('.increment-job').click(function() {
		logText('passing item ' + $(this).attr('data-uuid'));
		socketSend({
			'action': 'uincrement',
			'args': [$(this).attr('data-uuid')]
		});
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
	form.find('input:text, input:password, input[type=number], input:file, textarea').val(''); // removed 'select'
	form.find('input:radio, input:checkbox').removeAttr('checked').removeAttr('selected');
	if($(form).selector == '.new-cut-form') {
		form.find('.selected').prop('selected', true);
	}
}

function socketSend(jdata) {
	jdata.sid = SID;
	socket.send(JSON.stringify(jdata));
}

function rickRoll() {
	if (easterEggs) {
		modalMessage('Never gonna give you up', '<iframe width="420" height="315" src="http://www.youtube.com/embed/dQw4w9WgXcQ?autoplay=1&disablekb=1&controls=0&loop=1&showinfo=0&iv_load_policy=3" frameborder="0" allowfullscreen></iframe>');
		$('html').addClass('lol');
	}
	else {
		logText('This is a serious establishment, son. I\'m dissapointed in you.');
	}
}

function isTouchDevice(){
	return true == ('ontouchstart' in window || window.DocumentTouch && document instanceof DocumentTouch);
}

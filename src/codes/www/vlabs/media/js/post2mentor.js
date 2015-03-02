/*
 * post2mentor.js
 *
 * Barun Saha, 17-Feb-2011
 */

function highlightError(container, element, message) {
    $(container).removeClass('noError');
    $(container).addClass('error');
    $(element).tipsy({fade: true, gravity: 'w', fallback: message});
    $("html, body").filter(':not(:animated)').animate({scrollTop: $(container).offset().top}, 500);
}
function hideError(container, element) {
    $(container).removeClass('error');
    $(container).addClass('noError');
    $(element).tipsy({hide: 'true'});
}

function isValidForm() {
    var prefix = 'id_form-0-';
    var isValid = true;

    var answer = jQuery.trim($('#'+prefix+'answer').val());
    if (answer.length< 15) {
       highlightError('#c_answer', '#'+prefix+'answer', "Please type in atleast 15 characters.");
       isValid = isValid && false;
    } else {
       hideError('#c_answer', '#'+prefix+'answer');
    }

    var email = jQuery.trim($('#'+prefix+'email').val());
    if (isBlank(email)) {
       highlightError('#c_email', '#'+prefix+'email', 'Email address cannot be blank!');
       isValid = isValid && false;
    } else {
       hideError('#c_email', '#'+prefix+'email');
    }
    if (! isValidEmail(email)) {
       highlightError('#c_email', '#'+prefix+'email', 'A proper email address is required! Example: someone@somewhere.com');
       isValid = isValid && false;
    } else {
       hideError('#c_email', '#'+prefix+'email');
    }

    return isValid;
}

var ajaxSuccessDiv = $(strAjaxSuccessDiv);
var ajaxErrorDiv = $('<div class="ajax-error-message center-align" style="display: none;">\n\\n\
                            <div class="ajax-message-close-icon">\n\
                                <img src="$MEDIA_URL$images/new/icons/no24x24.png" align="right" alt="[Close]" />\n\
                            </div>\n\
                            <div class="message"></div>\n\
                      </div>');


$(document).ready(function() {
    $('button#btnSubmit').attr('disabled', true);
    $('button#submit').click(function() {
        //$('div.post-mentor-form form').after(ajaxSuccessDiv);
        //$('#f_contact').submit();
        if (isValidForm()) {
            // Indicate that the answer is being posted
            $('div.post-mentor-form form').after(strAjaxLoaderImg);

            $('div.ajax-success-message').remove();
            $('div.ajax-error-message').remove();
            $('button#submit').attr('disabled', true);

            $("html, body").filter(':not(:animated)').animate({scrollTop: $(document).height()}, 500);
            $.ajax({
               type:    'POST',
               url:     $('#f_contact').attr('action')+'/'+$('#h_xid').val()+'/'+$('#h_tid').val()+'/'+$('#h_pid').val()+'/',
               data:    $('div.post-mentor-form form').serialize(),
               cache:   false,
               success: function(mesg, txtStatus, XMLHttpRequest) {
                   //$('img.comment-ajax-loader').attr('src', '/examples/v_media/images/ajax/8_8_transparent.png')
                   $('img.ajax-loader').fadeOut(function(){
                       $(this).remove();
                   });
                   $('img.ajax-loader').after(ajaxSuccessDiv);
                   var dispMesg = 'Your answer has been successfully posted!  (Reference #: <strong>' +
                                    mesg +
                                    '</strong>) <br /><br /> We will soon get back to you. In case of any query, \n\
                                      kindly specify this reference number.';
                   $('div.ajax-success-message').fadeIn(ajaxFadeInTime);
                   $('div.ajax-success-message div.message').html(dispMesg);
                   $('div.ajax-success-message div.message').addClass('center-align');
               },
               error:   function(XMLHttpRequest, txtStatus, errorThrown) {
                   $('img.ajax-loader').fadeOut(function(){
                       $(this).remove();
                   });
                   $('img.ajax-loader').after(ajaxErrorDiv);
                   $('div.ajax-error-message').fadeIn(ajaxFadeInTime);
                   $('div.ajax-error-message div.message').html('An error has occured: ' + errorThrown + ' ' + txtStatus).fadeIn(ajaxFadeInTime);
                   $('div.ajax-error-message div.message').addClass('center-align');
                   $('div.ajax-error-message div.message').addClass('error');
               },
               dataType:    'html'
            });
            $('button#submit').attr('disabled', false);
        }
    });

    $('button#clear').click(function() {
        var prefix = 'id_form-0-';
        $('#'+prefix+'email').val('');
        $('#'+prefix+'answer').val('');

        hideError('#c_email', '#'+prefix+'email');
        hideError('#c_answer', '#'+prefix+'answer');

        $('div.ajax-success-message').remove();
        $('div.ajax-error-message').remove();
    });

    $('div.ajax-message-close-icon').live('click', function(){
            $(this).parent().fadeOut(ajaxFadeOutTime, function(){
                $(this).remove();
            });
        }
    );
});

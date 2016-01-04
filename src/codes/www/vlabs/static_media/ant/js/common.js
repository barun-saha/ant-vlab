$(document).ready(function() {    
    SyntaxHighlighter.config.clipboardSwf = '../lib/wireit/res/SyntaxHighlighter/clipboard.swf';
    SyntaxHighlighter.all();

    $('#top_arrow').mouseover(function() {
        $(this).css('cursor', 'pointer');
        $(this).css('bottom', '10px');
    })
    .mouseout(function() {
        $(this).css('bottom', '5px');
    })
    .click(function() {
        $("html, body").filter(':not(:animated)').animate({scrollTop: 0}, 800);
    });

    //
    // Changes #21: #3, #4
    // Toolbar icons
    //
    $('img.decrease-font-size')
    .mouseover(function() {
        $(this)
        $(this).css( {'cursor': 'pointer'} )
        .addClass('bottom-shadow-1px')
        /*
        .attr('src', '$MEDIA_URL$images/new/icons/page_toolbar/format_font_size_less_32x32_blue.png')
        .css('background-color', '#3b8bb3');
        */
    })
    .mouseout(function() {
        $(this)
        .removeClass('bottom-shadow-1px')
        /*
        .attr('src', '$MEDIA_URL$images/new/icons/page_toolbar/format_font_size_less_32x32_blue.png')
        .css('background-color', 'transparent');
        */
    })
    .click(function() {
       // http://stackoverflow.com/questions/2494448/each-click-i-want-to-increase-the-font-size-using-jquery
       var steps = {
           'font-large':        'font-medium',
           'font-medium':       'font-normal',
           'font-normal':       'font-small',
           'font-small':        'font-small'
       };
       $('div#contents').attr('className', steps[$('div#contents').attr('className')]);
    });

    $('img.increase-font-size')
    .mouseover(function() {
        /*
        $(this)
        .attr('src', '$MEDIA_URL$images/new/icons/page_toolbar/format_font_size_more_32x32_blue.png')
        .css('background-color', '#3b8bb3');
        */
        $(this).css( {'cursor': 'pointer'} )
        .addClass('bottom-shadow-1px')
    })
    .mouseout(function() {
        $(this)        
        .removeClass('bottom-shadow-1px')
    })
    .click(function() {
        // http://stackoverflow.com/questions/2494448/each-click-i-want-to-increase-the-font-size-using-jquery
       var steps = {
           'font-small':        'font-normal',
           'font-normal':       'font-medium',
           'font-medium':       'font-large',
           'font-large':        'font-large'
       };
       $('div#contents').attr('className', steps[$('div#contents').attr('className')]);
    });
    
    // End changes


    $('img.experiments')
    .mouseover(function() {
        $(this).css( {'cursor': 'pointer'} )
        .addClass('bottom-shadow-1px')
    })
    .mouseout(function() {
        $(this)
        .removeClass('bottom-shadow-1px')
    })
    .click(function(e) {                         
        $('.experiment-list-popup')
        .fadeIn('slow')
        .css( {'top': ($('.experiments').outerHeight() + e.pageY) + 'px', 'right': '5px'} )
    });                        
    
    $('.experiment-list-popup')
    .click(function() {
        $(this).fadeOut('slow')
    })
    .hover(
        function() { },
        function() {
            $(this).fadeOut('slow')
        }        
    )
});


var ajax_loading = "<img src='../images/ajax/ajax_loader.gif' alt='Loading ...' \n\
                     style='width: auto; height: auto; border: 0; margin: 0;\n\
                     padding-left: 44.5%; padding-right: 44.5%; padding-top: 25px; padding-bottom: 25px;' />";


var ajax_error = "<p style='color: red;'><strong>Failed to load the contents!</strong></p>";


function myAjaxLoader(container, url) {
    $(container).html(ajax_loading);
    $(container).load(url, "",
        function(responseText, textStatus, XMLHttpRequest) {
            if(textStatus == 'error') {
                $(this).html(ajax_error);
            }
        }
    );
}

function isBlank(text) {
    return (jQuery.trim(text).length == 0);
}

function isValidEmail(text) {
    return text.search(/^[a-zA-Z0-9_\-\.]+?\@[a-zA-Z0-9_\-]+\.[a-zA-Z0-9_\-\.]+$/) == 0
}


/**
 * How to Preserve Line Breaks in <textarea> after a Form is Submitted
 * http://www.techlicity.com/blog/preserving-line-breaks-in-textarea.html
 */

function nl2br (str, is_xhtml) {
    var breakTag = '<br />';
    if (typeof is_xhtml != 'undefined' && !is_xhtml) {
        breakTag = '<br>';
    }
    return (str + '').replace(/([^>]?)\n/g, '$1'+ breakTag +'\n');
}

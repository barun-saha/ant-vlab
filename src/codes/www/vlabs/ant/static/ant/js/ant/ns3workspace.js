$(document).ready(function() {
    var ANT_BASE_URL = '/ant/ant/';
    var INITIAL_POLL_INTERVAL  = 2000 ;     // in milliseconds
    
    // initialisation
    editAreaLoader.window_loaded();
    editAreaLoader.init({
        id: "ns3code"	// id of the textarea to transform
        ,start_highlight: true	// if start with highlight
        ,allow_resize: "both"
        ,allow_toggle: false
        ,word_wrap: true
        ,language: "en"
        ,syntax: "cpp"
        ,replace_tab_by_spaces: 4
    });

	$('textarea.resizable:not(.processed)').TextAreaResizer();


    $('div.ns3-form button#clear').click(function(event) {
        $('div.ns3-code-output').text('');
        $('div.ns3-code-trace').text('');
    });

    /*
     *  Execute simulation code
     */
    $('div.ns3-form button#run').click(function(event) {
       event.preventDefault();

       $('div.ns3-code-output').text('');
       $('div.ns3-code-trace').text('');

       var contents = {'ns3code': editAreaLoader.getValue('ns3code')}; //$('div.ns3-form form').serialize();   // editAreaLoader.getValue('ns3code');
       $('div.ns3-code-output').text(contents);   

       var ajax_loading = $(document.createElement('img'));
       ajax_loading
       .attr({'src': get_static('ant/images/ajax/ajax_loader.gif'), 'alt': 'Loading ...'})
       .css({
                'width': 'auto', 'height': 'auto', 
                'border': 0, 'margin': 0, 
                'padding-left': '44.5%', 'padding-right': '44.5%', 'padding-top': '25px', 'padding-bottom': '25px'
       })
       $('div.ns3-code-output').append(ajax_loading);
       $('textarea.ns3-code-trace').html(ajax_loading);

       // Use AJAX to submit the code
        $.ajax({
            type: 'POST',
            //url: '/ant/ant/ns3_submit/',
	    url: dutils.urls.resolve('ns3_submit'),
            data: contents,
            cache: false,
            success: function(mesg, textStatus, XMLHttpRequest) {
                // Get the task #
                var jObj = $.parseJSON(mesg);
                var disp_mesg = 'Simulation # <b>' + jObj['id'] + '</b> has been submitted. \n\
                <br>The result will appear here shortly.'                               
                
                if (jObj['id']) {
                    
                    // Display task #
                    $(document.createElement('p'))
                    .html(disp_mesg)
                    .css('text-align', 'center')
                    .attr('class', 'sim-start-mesg')
                    .appendTo ('div.ns3-code-output');
                    
                    $.poll(INITIAL_POLL_INTERVAL, function(retry) {
                        
                        //$.getJSON(ANT_BASE_URL + 'cel/state/' + jObj['id'] + '/', function(data) {
						var target_url = dutils.urls.resolve('task_state', { task_id: jObj['id']});
                        $.getJSON(target_url, function(data) {
                            
							var output = data['task'];
							//alert(JSON.stringify(output));

                            //if ( result['state'] && (result['state'].toUpperCase() == 'SUCCESS')) {
							if (output['status'].toUpperCase() == 'SUCCESS') {
                                $('p.sim-start-mesg')
                                .html('<b>Simulation completed ... Loading output</b>');

								var resultObj = output['result'];
								
                                $('div.ns3-code-output').html(resultObj['mesg'].replace(/\n/g, '<br>'));

/** Not for NS-3 simulations
								var output_length = 0;
                                for (var line_num in resultObj['trace']) {
									var line = resultObj['trace'][line_num] + '';
                                    $('textarea.ns3-code-trace').append(line);
									output_length += line.length;
                                }
                                
                                $('textarea.ns2-trace-text').css('height', '250px');
								output_length = output_length / 1024.0;
								var msg = $('div.ns2-code-output').html();
								msg += '<br>Loaded ' + output_length + ' KB of output';
								$('div.ns2-code-output').html(msg);
*/

                            }


//////                            if ( data['state'] && ( data['state'].toUpperCase() == 'SUCCESS') ) {
//////                                //alert(data['state']);
//////                                $('p.sim-start-mesg')
//////                                .html('Simulation completed <br><b>Loading output ...</b>');
//////                                
//////                                //$.getJSON(ANT_BASE_URL + 'cel/result/' + jObj['id'] + '/', function(result_data) {
//////				var result_url = dutils.urls.resolve('task_result', { uuid: jObj['id']});
//////                                $.getJSON(result_url,  function(result_data) {

//////                                    //var resultObj = result_data; 
//////                                    $('div.ns3-code-output').html(result_data['mesg'].replace(/\n/g, '<br>'));                                    
//////                                    var output = '';
//////                                    for (var line_num in result_data['trace']) {
//////                                        output += result_data['trace'][line_num] + '';
//////                                        //$('textarea.ns2-trace-text').append(resultObj['trace'][line_num]);
//////                                    }                                    
//////                                    $('textarea.ns3-code-trace').text(result_data['trace']);
//////                                })                                                                
//////                            }
                            else {
                              retry();
                            }
                        })
                    })
                }
                
                
            },
            error: function(XMLHttpRequest, textStatus, errorThrown) {
                $('div.ns3-code-output').html('Error: ' + textStatus + '; ' +  errorThrown + '; ' +  XMLHttpRequest.responseText);
            },
            dataType: 'html'
        });
        return false;
    });
    
    
    // (Rev #31: #1)
    // Filter the output of simulation based on search pattern
    $('#filter-btn').click(function(event) {
        var count = 0;
        var pattern = $.trim( $('#filter-pattern').val() );
        
        if (pattern.length == 0) {
            alert('Please type in a pattern to search!');
            $('#filter-pattern').focus();
            return;            
        }

        var inputs = [];
        var output = '';        
        var contents = $('.ns3-code-output').html();
        if ( contents.search('<br>') >= 0 )
            inputs = contents.split('<br>');
        else
            inputs = contents.split('<BR>');    // Stupid IE              
                
        for (var i in inputs) {
            if ( inputs[i].match(pattern) ) {
                ++count;            
                output = [ output, inputs[i] ].join('<br>');                
            }
        }      

        $('.filtered-output').html( output );                    
        $('#pattern-match-count').text(count);
    });
    
});


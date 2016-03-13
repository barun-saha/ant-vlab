/*
 * Functionalty of Exercises page for ANT
 */


$(document).ready(function() {

    var ajax_loading_image = get_static('ant/images/ajax/ajax_loader.gif');

    var ajax_loading = "<img src='";
    ajax_loading += ajax_loading_image;
    ajax_loading += "' alt='Loading ...' \n\
                       style='width: auto; height: auto; border: 0; margin: 0;\n\
                       padding-left: 44.5%; padding-right: 44.5%; padding-top: 25px; padding-bottom: 25px;'>";

    $("#ddlExercises").prepend(
        $(document.createElement('option'))
        .attr({'value': 0, 'selected': '0'})
        .text('Exercise #')
    );

    $("#ddlExercises").val('0');
    SyntaxHighlighter.highlight();

    //$("#problem_statement").resizable();
    $("#ddlExercises").change(function() {
       var e_text = $("#ddlExercises option:selected").text();
       var e_value = $("#ddlExercises option:selected").val();

       if (eval(e_value) > 0) {
           $("#problem_statement").html(ajax_loading);
           $("#problem_statement").load(
                //"/ant/ant/load_exercise/" + e_value + "/",
                //dutils.urls.resolve('get_problem', { exercise_id: e_value, }),
                Urls.get_problem(e_value),
                "",
                function(responseText, textStatus, XMLHttpRequest) {
                    if(textStatus == 'error') {
                        $(this).html(ajax_error);
                    }
                    // This button would be disabled at certain portions of code
                    $('#btnSubmit').attr('disabled', false);

                    // Order is: exercise_id/object_id/problem_id/
                    /* Workspace is now fixed for ANT; Barun, 19-Jan-2011 */

                    //myAjaxLoader("#workspace", "/ant/ant/load_workspace/" + e_value + "/" + $("#hObjId").val() + "/" + e_text + "/");
                    //var target_url = dutils.urls.resolve('get_workspace', { exercise_id: e_value, object_id: $("#hObjId").val(), problem_id: e_text,});
                    var target_url = Urls.get_workspace(e_value, $("#hObjId").val(), e_text);
                    $.ajax({
                        type:   'GET',
                        //url:    "/ant/ant/load_workspace/" + e_value + "/" + $("#hObjId").val() + "/" + e_text + "/",
                        url:    target_url,
                        success:function(mesg, txtStatus, XMLHttpRequest) {
                            $('#workspace').html(mesg);
                        },
                        error:  function(XMLHttpRequest, txtStatus, errorThrown) {
                            alert(errorThrown);
                        },
                        dataType:   'html'
                    });
                },
                "html"
            );
       }
       $("#result_display").html("");
    });

    $('#viewSolution').click(function() {
       var e_value = $("#ddlExercises option:selected").val();
       if (eval(e_value) > 0) {
           //var soln_url = dutils.urls.resolve('get_solution', {exercise_id: e_value,});
           var soln_url = Urls.get_solution(e_value);
           if (confirm("Are you sure you want to view the solution?")) {
               //window.open("/ant/ant/show_solution/" + e_value + '/', "ANTSolution",
               window.open(soln_url, "Solution", "width=800,height=600,resizable=yes,toolbar=no,linkbar=no,scrollbars=yes,location=0,directories=no,status=no,menubar=no,copyhistory=no",false);
           }
       } else {
           alert('Please select a problem!');
       }
    });


    // $("#btnSubmit").click(function() {
    //     $("#result_display").html(ajax_loading);
    //     $("html, body").animate({scrollTop: $("#contentBox").height()}, 790);
    //
    //     // Now send the exercise ID to server and obtain the correct solution
    //     // Compare with user's result to verify if he's drawn correctly
    //     var e_value = $("#ddlExercises option:selected").val();
    //        if (eval(e_value) > 0) {
    //             $.get(
    //                 "/ant/ant/answer/" + $("#hObjId").val() + "/" + e_value + "/",
    //                 {
    //                  graph: $("#divStoreGraphForServer").text()
    //                 },
    //                 function(data) {
    //                     $("#result_display").html(data);
    //                 },
    //                 ""
    //             );
    //        } else {
    //            $("#result_display").html('<h2>Please select a problem!</h2>');
    //        }
    // });

});

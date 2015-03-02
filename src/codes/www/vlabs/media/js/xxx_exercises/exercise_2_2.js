$('#btnSave').click(function() {
    $("#result_display").html(ajax_loading);
    $("html, body").animate({scrollTop: $("#contentBox").height()}, 790);

    $.get(
        "/isad/isad/answer/2/7/",
        {
         graph: JSON.stringify({
             operators: $('#txt0').val(),
             operands: $('#txt1').val()
         })
        },
        function(data) {
            $("#result_display").html(data);
        },
        ""
    );
});
for (var i = 0; i < solutions.length; i++) {
    solutions[i] = parseFloat(solutions[i]);
}

$("#btnSave").click(function() {
    var answers = new Array();

    $('input:text[id^=txt]').each(function(index, item) {
        //alert($(this).val());
        answers[index] = $(this).val();
    });
    //alert(answers.length);

    for (var i = 0; i < answers.length; i++) {
        var difference = parseFloat(solutions[i]) - parseFloat(answers[i]);
        //alert(difference);

        if (isNaN(difference)) {
            alert('Please enter the (proper) value of ' + labels[i]);
            return;
        }

        // Values of N1, N2, n1, n2, length, voc, difficulty should match exactly
        if ((i != 6 &&i != 8) && (answers[i] != solutions[i]))  {
            alert('The value entered for ' + labels[i] + ' seems to be wrong!');
            return;
        }
        if (difference > 0.3 || difference < -0.3) {    // 0.3 is a margin for rounding off
            alert('The value of ' + labels[i] + ' doesn\'t seem to be correct!');
            alert(difference);
            return;
        }
    }

    $("html, body").animate({scrollTop: $("#contentBox").height()}, 800);
    $("#result_display").html('<strong><em>Excellent!</em></strong>');

});
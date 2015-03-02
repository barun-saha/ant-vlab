/* Uses jQuery */

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

        // Value of KLOC should match exactly
        if ((i == 0 || i == 6) && (answers[i] != solutions[i]))  {
            alert('The value entered for ' + labels[i] + ' is wrong!');
            return;
        }
        if (difference > 0.5 || difference < -0.5) {
            alert('The value of ' + labels[i] + ' doesn\'t seem to be correct!');
            return;
        }
    }
    
    $("html, body").animate({scrollTop: $("#contentBox").height()}, 800);
    $("#result_display").html('<strong><em>Excellent!</em></strong>');

});
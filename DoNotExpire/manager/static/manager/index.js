function changeText(text, id)
{
    var display = document.getElementById('char-name-label-'+id);
    display.innerHTML = "";
    display.innerHTML = text;
}

// function enableDelete(char_id) {
//     var delete_btn = document.getElementById('delete-btn-'+char_id)
//     delete_btn.setAttribute("action", "")
//     class_str = "{% url 'delete-char' " + char_id + " %}"
//     delete_btn.setAttribute("action", class_str)
// }


$(document).ready(function (){
    // get all char containers with a class
    let charboxes = $('.clickable');
    charboxes.click(function() {
        // add border initially to the div where we clicked
        $(this).addClass('border-yellow')
        // get current account name
        let acc_id = $(this).attr("id");
        // get new querry only with 'local' chars
        query = "#" + acc_id + ".clickable"
        let chars = $(query)
        // clickable div within current scope
        chars.click(function() {
            chars.removeClass('border-yellow')
            $(this).addClass('border-yellow')
        })
    })

})


function changeText(text, id)
{
    var display = document.getElementById('char-name-label-'+id);
    display.innerHTML = "";
    display.innerHTML = text;
}


$(document).ready(function (){
    // get all char containers with a class
    let charboxes = $('.clickable');
    charboxes.click(function() {
        // add border initially to the div where we clicked
        $(this).addClass('border-yellow')
        // get current account name
        let acc_id = $(this).attr("id");

        // change Delete button hidden input value field
        let delete_form = $("#"+acc_id+"[name=char_id]");
        let char_name = $(this).attr("data-char")
        $(delete_form).val(char_name)

        // Toggle delete button
        let delete_btn = delete_form.next()  // takes next element in DOM which is button in this case
        $(delete_btn).removeClass('btn-char-disabled')
        $(delete_btn).attr('disabled', false)

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


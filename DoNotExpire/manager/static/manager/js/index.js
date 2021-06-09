const changeText = (text, id) => {
  const display = document.getElementById("char-name-label-" + id);
  display.innerHTML = "";
  display.innerHTML = text;
};

// Accounts can store up to 18 characters
const maxCharCount = 18;

// Get all the Create New Character buttons
let create_btn = $(".btn-char-create");
create_btn.each(function () {
  // If there are 18 or more characters, disable the button
  if (Number($(this).attr("data-char-count")) >= maxCharCount) {
    $(this).attr("disabled", true);
    $(this).addClass("btn-char-disabled");
  }
});

$(document).ready(function () {
  // get all char containers with a class
  let charboxes = $(".clickable");
  charboxes.click(function () {
    // add border initially to the div where we clicked
    $(this).addClass("border-yellow");
    // get current account name
    let acc_id = $(this).attr("id");

    // change Delete button hidden input value field
    let delete_form = $("#" + acc_id + "[name=char_id]");
    let char_name = $(this).attr("data-char");
    $(delete_form).val(char_name);

    // Toggle delete button
    let delete_btn = delete_form.next(); // takes next element in DOM which is button in this case
    $(delete_btn).removeClass("btn-char-disabled");
    $(delete_btn).attr("disabled", false);

    // get new querry only with 'local' chars
    query = "#" + acc_id + ".clickable";
    let chars = $(query);
    // clickable div within current scope
    chars.click(function () {
      chars.removeClass("border-yellow");
      $(this).addClass("border-yellow");
    });
  });
});

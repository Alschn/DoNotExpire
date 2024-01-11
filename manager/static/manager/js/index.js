const changeText = (text, id) => {
  const display = document.getElementById("char-name-label-" + id);
  display.innerHTML = "";
  display.innerHTML = text;
};

// Accounts can store up to 18 characters
const maxCharCount = 18;

// Get all the Create New Character buttons
let createBtn = $(".btn-char-create");
createBtn.each(function () {
  const btnElement = $(this);

  // If there are 18 or more characters, disable the button
  if (Number(btnElement.attr("data-characters-count")) >= maxCharCount) {
    btnElement.attr("disabled", true);
    btnElement.addClass("btn-char-disabled");
  }
});

$(document).ready(function () {
  // get all char containers with a class, no mather what account
  const allCharBoxes = $(".col-char.clickable");

  allCharBoxes.click(function () {
    const element = $(this);

    // add border initially to the div where we clicked
    element.addClass("border-yellow");

    // get current account and character name
    const accountName = element.attr("data-account-name");
    const charName = element.attr("data-character-name");

    // change Delete button hidden input value field
    const hiddenInput = $(`input[name='char_id'][data-account-name='${accountName}']`);
    $(hiddenInput).val(charName);

    // Toggle delete button
    const deleteBtn = $(`button[data-account-name='${accountName}']`);
    $(deleteBtn).removeClass("btn-char-disabled");
    $(deleteBtn).attr("disabled", false);

    // get new query only with 'local' chars
    const localCharBoxes = $(`.col-char.clickable[data-account-name='${accountName}']`);

    localCharBoxes.removeClass("border-yellow");
    localCharBoxes.attr("data-selected", false);
    localCharBoxes.attr("aria-selected", false);

    element.addClass("border-yellow");
    element.attr("data-selected", true);
    element.attr("aria-selected", true);
  });
});

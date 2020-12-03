const amazon_desc =
  "skilled with the spear and the bow, she is a very vesatile fighter.";
const assassin_desc =
  "schooled in the martial arts, her mind and body are deadly weapons.";
const necromancer_desc =
  "summoning undead minions and cursing his enemies are his specialties.";
const barbarian_desc =
  "he is unequaled in close-quarters combat and mastery of weapons.";
const paladin_desc =
  "he is a natural party leader, holy man, and blessed warrior.";
const sorceress_desc =
  "she has mastered the elemental magicks -- fire, lightning, and ice.";
const druid_desc =
  "commanding the forces of nature, he summons wild beasts and raging storms to his side.";

const amazon = document.getElementById("amazon");
const assassin = document.getElementById("assassin");
const necromancer = document.getElementById("necromancer");
const barbarian = document.getElementById("barbarian");
const paladin = document.getElementById("paladin");
const sorceress = document.getElementById("sorceress");
const druid = document.getElementById("druid");

// Title and description displayed above
const class_desc = document.getElementById("class-description");
const class_name = document.getElementById("class-name");

// forms div
const char_form_popup = document.getElementById("char-form-popup");
// form's fields
const id_char_class = document.getElementById("id_char_class");
const id_level = document.getElementById("id_level");
const id_expansion = document.getElementById("id_expansion");
const id_hardcore = document.getElementById("id_hardcore");

// Initial values
id_expansion.value = "true"; // initially expansion
id_hardcore.value = "false"; // initially softcore

const enablePopup = () => {
  // Show class name (title), description and form
  class_name.style.visibility = "visible";
  class_desc.style.visibility = "visible";
  char_form_popup.style.visibility = "visible";
};

const changeCurrentChar = (char_name, char_desc) => {
  class_desc.textContent = char_desc.toUpperCase(); // Set class description
  class_name.textContent = char_name; // Set class name (title)
  id_char_class.value = char_name; // Set form's char_class field
  exp = document.getElementById("expansion");
  char_name === "Assassin" || char_name === "Druid"
    ? (exp.disabled = true)
    : (exp.disabled = false);
};

document.addEventListener("DOMContentLoaded", function (event) {
  var expansion = document.querySelector("input[name=EXPANSION]"); // expansion checkbox
  expansion.addEventListener("change", function (event) {
    // set expansion field to true/false if checked/not checked
    id_expansion.checked
      ? (id_expansion.value = "true")
      : (id_expansion.value = "false");
  });
});

document.addEventListener("DOMContentLoaded", function (event) {
  var hardcore = document.querySelector("input[name=HARDCORE]"); // hardcore checkbox
  hardcore.addEventListener("change", function (event) {
    // set hardcore field to true/false if checked/not checked
    id_hardcore.checked
      ? (id_hardcore.value = "true")
      : (id_hardcore.value = "false");
  });
});

amazon.addEventListener("click", () => {
  changeCurrentChar("Amazon", amazon_desc);
  enablePopup();
});

assassin.addEventListener("click", () => {
  changeCurrentChar("Assassin", assassin_desc);
  expansion.setAttribute("checked", "true");
  expansion.checked = true;
  id_expansion.value = "true";
  enablePopup();
});

necromancer.addEventListener("click", () => {
  changeCurrentChar("Necromancer", necromancer_desc);
  enablePopup();
});

barbarian.addEventListener("click", () => {
  changeCurrentChar("Barbarian", barbarian_desc);
  enablePopup();
});

paladin.addEventListener("click", () => {
  changeCurrentChar("Paladin", paladin_desc);
  enablePopup();
});

sorceress.addEventListener("click", () => {
  changeCurrentChar("Sorceress", sorceress_desc);
  enablePopup();
});

druid.addEventListener("click", () => {
  changeCurrentChar("Druid", druid_desc);
  expansion.setAttribute("checked", "true");
  expansion.checked = true;
  id_expansion.value = "true";
  enablePopup();
});

const descriptions = {
  "Amazon": "skilled with the spear and the bow, she is a very versatile fighter.",
  "Assassin": "schooled in the martial arts, her mind and body are deadly weapons.",
  "Necromancer": "summoning undead minions and cursing his enemies are his specialties.",
  "Barbarian": "he is unequaled in close-quarters combat and mastery of weapons.",
  "Paladin": "he is a natural party leader, holy man, and blessed warrior.",
  "Sorceress": "she has mastered the elemental magicks -- fire, lightning, and ice.",
  "Druid": "commanding the forces of nature, he summons wild beasts and raging storms to his side.",
};

// Clickable characters
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
const id_expansion = document.getElementById("id_expansion");


const enablePopup = () => {
  // Show class name (title), description and form
  class_name.style.visibility = "visible";
  class_desc.style.visibility = "visible";
  char_form_popup.style.visibility = "visible";
};

const changeCurrentChar = (char_name) => {
  class_desc.textContent = descriptions[char_name].toUpperCase(); // Set class description
  class_name.textContent = char_name; // Set class name (title)
  id_char_class.value = char_name; // Set form's char_class field

  if (char_name === "Assassin" || char_name === "Druid") {
    setExpansion();
    id_expansion.classList.add("checkbox-disabled");
  } else {
    id_expansion.classList.remove("checkbox-disabled");
  }
};

const setExpansion = () => {
  id_expansion.setAttribute("checked", "true");
  id_expansion.checked = true;
  id_expansion.value = true;
};

amazon.addEventListener("click", (e) => {
  changeCurrentChar("Amazon");
  enablePopup();
});

assassin.addEventListener("click", (e) => {
  changeCurrentChar("Assassin");
  setExpansion();
  enablePopup();
});

necromancer.addEventListener("click", (e) => {
  changeCurrentChar("Necromancer");
  enablePopup();
});

barbarian.addEventListener("click", (e) => {
  changeCurrentChar("Barbarian");
  enablePopup();
});

paladin.addEventListener("click", (e) => {
  changeCurrentChar("Paladin");
  enablePopup();
});

sorceress.addEventListener("click", (e) => {
  changeCurrentChar("Sorceress");
  enablePopup();
});

druid.addEventListener("click", (e) => {
  changeCurrentChar("Druid");
  setExpansion();
  enablePopup();
});

const amazon_desc = "skilled with the spear and the bow, she is a very vesatile fighter.";
const assassin_desc = "schooled in the martial arts, her mind and body are deadly weapons.";
const necromancer_desc = "summoning undead minions and cursing his enemies are his specialties.";
const barbarian_desc = "he is unequaled in close-quarters combat and mastery of weapons.";
const paladin_desc = "he is a natural party leader, holy man, and blessed warrior.";
const sorceress_desc = "she has mastered the elemental magicks -- fire, lightning, and ice.";
const druid_desc = "commanding the forces of nature, he summons wild beasts and raging storms to his side.";

const amazon = document.getElementById('amazon');
const assassin = document.getElementById('assassin');
const necromancer = document.getElementById('necromancer');
const barbarian = document.getElementById('barbarian');
const paladin = document.getElementById('paladin');
const sorceress = document.getElementById('sorceress');
const druid = document.getElementById('druid');

const class_desc = document.getElementById('class-description');
const class_name = document.getElementById('class-name');

// forms div
const char_form_popup = document.getElementById('char-form-popup');
// forms
const id_char_class = document.getElementById('id_char_class');
const id_level = document.getElementById('id_level');
const id_expansion = document.getElementById('id_expansion');
const id_hardcore = document.getElementById('id_hardcore');
id_expansion.value = "true";
id_hardcore.value = "false";


const enablePopup = () => {
    class_name.style.visibility = "visible";
    class_desc.style.visibility = "visible";
    char_form_popup.style.visibility = "visible";
}


document.addEventListener("DOMContentLoaded", function (event) {
    var expansion = document.querySelector('input[name=EXPANSION]');
    expansion.addEventListener('change', function (event) {
        if (expansion.checked) {
            id_expansion.value = "true"
        } else {
            id_expansion.value = "false"
        }
    });
});

document.addEventListener("DOMContentLoaded", function (event) {
    var hardcore = document.querySelector('input[name=HARDCORE]');
    hardcore.addEventListener('change', function (event) {
        if (hardcore.checked) {
            id_hardcore.value = "true"
        } else {
            id_hardcore.value = "false"
        }
    });
});

amazon.addEventListener("click", () => {
    class_desc.textContent = amazon_desc.toUpperCase();
    class_name.textContent = "AMAZON";
    document.getElementById("expansion").disabled = false;
    id_char_class.value = "Amazon";
    enablePopup()
})

assassin.addEventListener("click", () => {
    class_desc.textContent = assassin_desc.toUpperCase();
    class_name.textContent = "ASSASSIN";
    id_char_class.value = "Assassin";
    document.getElementById("expansion").disabled = true;
    enablePopup()
})

necromancer.addEventListener("click", () => {
    class_desc.textContent = necromancer_desc.toUpperCase();
    class_name.textContent = "NECROMANCER";
    document.getElementById("expansion").disabled = false;
    id_char_class.value = "Necromancer";
    enablePopup()
})

barbarian.addEventListener("click", () => {
    class_desc.textContent = barbarian_desc.toUpperCase();
    class_name.textContent = "BARBARIAN";
    document.getElementById("expansion").disabled = false;
    id_char_class.value = "Barbarian";
    enablePopup()
})

paladin.addEventListener("click", () => {
    class_desc.textContent = paladin_desc.toUpperCase();
    class_name.textContent = "PALADIN";
    document.getElementById("expansion").disabled = false;
    id_char_class.value = "Paladin";
    enablePopup()
})

sorceress.addEventListener("click", () => {
    class_desc.textContent = sorceress_desc.toUpperCase();
    class_name.textContent = "SORCERESS";
    document.getElementById("expansion").disabled = false;
    id_char_class.value = "Sorceress";
})

druid.addEventListener("click", () => {
    class_desc.textContent = druid_desc.toUpperCase();
    class_name.textContent = "DRUID";
    id_char_class.value = "Druid";
    document.getElementById("expansion").disabled = true;
    enablePopup()
})

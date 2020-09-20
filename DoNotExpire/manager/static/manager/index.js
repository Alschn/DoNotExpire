function changeText(text, id)
{
    var display = document.getElementById('char-name-label-'+id);
    display.innerHTML = "";
    display.innerHTML = text;
}

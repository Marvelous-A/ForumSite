let text_button = document.getElementById('text_button');
let text = document.getElementById('text');
let window = document.getElementById('window');

text_button.onclick = function(){
    if (text.value != ""){
        var div = document.createElement('div');
        div.innerHTML = "<h3>"+text.value+"</h3>";
        text_bar.after(div);
    }
};
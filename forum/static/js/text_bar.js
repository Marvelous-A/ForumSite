let text_button = document.getElementById('text_button');
let text = document.getElementById('text');
// let window = document.getElementById('window');
let text_bar = document.getElementById('text_bar');

text_button.onclick = function(){
    if (text.value != ""){
        var div = document.createElement('div');
        div.innerHTML = "<h3>"+text.value+"</h3>";
        text_bar.ap(div);
    }
};

const questionSocket = new WebSocket(
    'ws://' + window.location.host + '/ws/questions/'
);

questionSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    const questionElement = document.getElementById('question-' + data.id);
    if (questionElement) {
        questionElement.parentNode.removeChild(questionElement);
    }
};

questionSocket.onclose = function(e) {
    console.error('Question socket closed unexpectedly');
};

// image
// let images = document.querySelectorAll('#window img');

// images.forEach(image => image.onclick = function(){
//     console.log(image.src);
//     if (image.hasAttribute('style')){
//         image.removeAttribute('style');
//     }else{
//         image.setAttribute('style', 'width: 1000px;');
//     }
// });
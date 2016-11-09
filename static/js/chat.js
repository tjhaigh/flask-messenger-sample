var socket = io.connect('http://' + document.domain + ':' + location.port);

socket.on('connect', function() {
    socket.emit('connected', 'yes');
});

socket.on('message', function(data) {
    var line = document.createElement("div");
    var text = document.createTextNode('(' + data['timestamp'] + ') ' + data['message']);
    line.appendChild(text);
    var box = document.getElementById('chatbox');
    box.appendChild(line);
    box.scrollTop = box.scrollHeight;
});

function sendMessage(e) {
    var msgbox = document.getElementById("msgbox");
    var msg = msgbox.value;
    msgbox.value = '';
    if (msg != '') {
        socket.emit('message', msg);
    }
    return false;
}


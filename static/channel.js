document.addEventListener('DOMContentLoaded', () => {

  // Connect to websocket
  var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

  // When connected, configure submit button
  socket.on('connect', () => {

    // Chatroom submit button emits 'submit message'
    document.querySelector('#submit_input').onclick = () => {
      const channel_name = document.getElementById('channel_name').innerHTML;
      const message = document.querySelector('#input').value;
      const username = document.getElementById('username').innerHTML;
      document.querySelector('#input').value = '';
      socket.emit('submit message', {'channel_name': channel_name, 'message': message, 'username': username});
      return false;
    }
  });

  const channel_name = document.getElementById('channel_name').innerHTML;
  // When a new message is announced, place message string in <span> tags and 
  // append it to the #chatroom div
  socket.on('announce message' + ':' + channel_name, chat_history => {

    console.log(chat_history);

    for (var key in chat_history) {

      const br = document.createElement('br');
      const span = document.createElement('span');
      span.innerHTML = `${chat_history[key].username}: ${chat_history[key].message}`;
      document.querySelector('#chatroom').append(span);
      document.querySelector('#chatroom').append(br);

    };
  });
});
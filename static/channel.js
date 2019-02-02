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

  // When a new message is announced, place message string in <span> tags and 
  // append it to the #chatroom div
  socket.on('announce message', data => {
    const channel_name = document.getElementById('channel_name').innerHTML;
    console.log(data);
    if (channel_name === data.channel_name) {
      const br = document.createElement('br');
      const span = document.createElement('span');
      span.innerHTML = `${data.username}: ${data.message}`;
      document.querySelector('#chatroom').append(span);
      document.querySelector('#chatroom').append(br);
    };
  });
});
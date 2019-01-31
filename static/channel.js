document.addEventListener('DOMContentLoaded', () => {

  // Connect to websocket
  var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

  // When connected, configure submit button
  socket.on('connect', () => {

    // Chatroom submit button emits 'submit message'
    document.querySelector('#submit_input').onclick = () => {
      const message = document.querySelector('#input').value;
      document.querySelector('#input').value = '';
      socket.emit('submit message', {'message': message});
      return false;
    }
  });

  // When a new message is announced, place message string in <span> tags and 
  // append it to the #chatroom div
  socket.on('announce message', data => {
    const br = document.createElement('br');
    const span = document.createElement('span');
    span.innerHTML = `${data.message}`;
    document.querySelector('#chatroom').append(span);
    document.querySelector('#chatroom').append(br);
  });
});
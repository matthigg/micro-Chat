document.addEventListener('DOMContentLoaded', () => {
  const channel_name = document.getElementById('channel_name').innerHTML;
  const username = document.getElementById('username').innerHTML;

  // The message submit button is disabled by default.
  document.querySelector('#submit_input').disabled = true;

  // Enable message submit button only if there is text in the input field.
  document.querySelector('#input').oninput = () => {
    console.log('key up');
    if (document.querySelector('#input').value.length > 0)
      document.querySelector('#submit_input').disabled = false;
    else
      document.querySelector('#submit_input').disabled = true;
  };

  // Connect to websocket.
  console.log('===== location.protocol =====: ', location.protocol)
  console.log('===== document.domain =====: ', document.domain)
  console.log('===== location.port =====: ', location.port)
  console.log('===== URL =====: ', location.protocol + '//' + document.domain + ':' + location.port)
  // var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
  var socket = io.connect(location.protocol + '//' + document.domain);
  console.log('===== socket =====: ', socket)

  // When connected, configure submit button.
  socket.on('connect', () => {

    // When message is submitted, save it, clear the input field, and disable the
    // submit button.
    document.querySelector('#submit_input').onclick = () => {
      const message = document.querySelector('#input').value;
      document.querySelector('#submit_input').disabled = true;
      document.querySelector('#input').value = '';

      // Reformat time-stamp; the date is calculated in milliseconds since Jan. 1,
      // 1970 (UNIX time).
      const date = new Date();
      const date_ms = date.getTime();

      // Broadcast the message to all listeners.
      socket.emit('submit message', { 'channel_name': channel_name, 'date': date_ms, 'message': message, 'username': username });
      return false;
    };
  });

  // When a new message is announced, place message string in <span> tags and 
  // append it to the #chatroom <div>.
  socket.on('announce message' + ':' + channel_name, new_message => {
    const br = document.createElement('br');
    const span = document.createElement('span');
    const img = document.createElement('img');
    const nbsp = ' ';
    img.src = `https://api.adorable.io/avatars/40/${new_message.username}`;
    span.innerHTML = `[${new_message.date}] ${new_message.username}: ${new_message.message}`;
    document.querySelector('#chatroom').append(img, nbsp, span, br);
  });
});
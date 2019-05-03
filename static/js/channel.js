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
  var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

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
  // append it to the #message_new <div>. Also attach a random-ish avatar to
  // each user's message
  socket.on('announce message' + ':' + channel_name, new_message => {
    const div = document.createElement('div');
    const img = document.createElement('img');
    const nbsp = ' ';
    img.classList.add('avatar');
    img.src = `https://api.adorable.io/avatars/40/${new_message.username}`;
    div.classList.add('message');
    div.style.height = '46px';
    div.style.padding = '3px'
    div.innerHTML = `[${new_message.date}] ${new_message.username}: ${new_message.message}`;
    div.prepend(img, nbsp);    
    document.querySelector('#message_new').append(div);

    // As new messages are added to the chatroom space and eventually exceed the 
    // height of the viewport, start to automatically scroll to the bottom of the 
    // page when new messages are submitted. The window.innerHeight value is
    // offset by 38px to account for the height of the message input bar.
    chatroom_height = document.querySelector('#chatroom').offsetHeight;
    if (chatroom_height > (window.innerHeight - 38)) {
      window.scroll(0, chatroom_height);
    }
  });
});
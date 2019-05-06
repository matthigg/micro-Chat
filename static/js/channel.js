document.addEventListener('DOMContentLoaded', () => {
  const channel_name = document.querySelector('#channel_name').innerHTML;
  const username = document.querySelector('.username').innerHTML;

  // Enable message submit button only if there is text in the input field.
  document.querySelector('.message-input').oninput = () => {
    console.log('key up');
    if (document.querySelector('.message-input').value.length > 0)
      document.querySelector('.submit-input').disabled = false;
    else
      document.querySelector('.submit-input').disabled = true;
  };

  // Scroll down to the newest message if the message history takes up more space
  // than the current viewport when a user first enters the channel. The 
  // window.innerHeight value is offset by 80px to account for the height of the 
  // message input bar.
  chatroom_height_history = document.querySelector('#chatroom').offsetHeight;
  if (chatroom_height_history > (window.innerHeight - 80)) {
    window.scroll(0, chatroom_height_history);
  }

  // Connect to websocket.
  var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
  socket.on('connect', () => {

    // When message is submitted, save it, clear the input field, and disable the
    // submit button.
    document.querySelector('.submit-input').onclick = () => {
      const message = document.querySelector('.message-input').value;
      document.querySelector('.submit-input').disabled = true;
      document.querySelector('.message-input').value = '';

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
  // append it to the #message_new <div>. Also attach an avatar to each user's 
  // message
  socket.on('announce message' + ':' + channel_name, new_message => {
    const div = document.createElement('div');
    const img = document.createElement('img');
    const nbsp = ' ';
    img.classList.add('avatar');
    img.src = `https://api.adorable.io/avatars/40/${new_message.username}`;
    div.classList.add('message');
    div.style.height = '40px';  // match .message_history class in main.css
    div.style.margin = '5px'    // match .message_history class in main.css
    div.innerHTML = `[${new_message.date}] ${new_message.username}: ${new_message.message}`;
    div.prepend(img, nbsp);    
    document.querySelector('#message_new').append(div);

    // As new messages are added to the chatroom space and eventually exceed the 
    // height of the viewport, start to automatically scroll to the bottom of the 
    // page when new messages are submitted. The window.innerHeight value is
    // offset by 80px to account for the height of the message input bar.
    chatroom_height = document.querySelector('#chatroom').offsetHeight;
    if (chatroom_height > (window.innerHeight - 80)) {
      window.scroll(0, chatroom_height);
    }
  });

// =================================== MODAL =====================================
// https://www.w3schools.com/howto/howto_css_modals.asp

  let modal = document.getElementById('modal');
  let btn = document.querySelector('.modal-nav');
  let span = document.getElementsByClassName('close')[0];

  // When the user clicks the button, open the modal 
  btn.onclick = function() {
    modal.style.display = "block";
  }

  // When the user clicks on <span> (x), close the modal
  span.onclick = function() {
    modal.style.display = "none";
  }

  // When the user clicks anywhere outside of the modal, close it
  window.onclick = function(event) {
    if (event.target == modal) {
      modal.style.display = "none";
    }
  }

  // svg_down = document.querySelector('.modal-nav')
});
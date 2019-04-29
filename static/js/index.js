// When an object is returned from application.py to index.html via the
// render_template() method, it can't be directly handled by JS just yet. 
// However, using Jinja2 templating, it can be directly inserted onto the page --
// in this case, the channels[] array that is returned from application.py via
// render_template() is inserted into the DOM: 
//
// <p id="channel_list_hidden">{{ channels }}</p>

document.addEventListener('DOMContentLoaded', () => {

  // Hide the list of channel names string that is stored in a <div> on the DOM 
  // when it is returned from application.py.
  document.querySelector("#channel_list_hidden").style.visibility = "hidden";

  // By default, the 'Create a new channel' submit button is disabled.
  document.querySelector('#submit').disabled = true;

  // Enable 'Create a new channel' submit button only if there is text in the 
  // input field.
  document.querySelector('#new_channel').oninput = () => {
    if (document.querySelector('#new_channel').value.length > 0)
      document.querySelector('#submit').disabled = false;
    else
      document.querySelector('#submit').disabled = true;
  };

  // Custom parser that converts the channel names returned from application.py
  // and stored in a hidden <div> on index.html into an array of channels stored 
  // in the channels[] list.
  var record = false;
  var channel = '';
  var channels = [];
  var channels_string = document.querySelector("#channel_list_hidden").innerHTML;
  console.log('channels_string: ', channels_string);
  console.log('typeof(channels_string): ', typeof(channels_string));

  for (let i = 0; i < channels_string.length; i++) {

    // Start recording at the first single quote character
    if (channels_string[i] === "'" && channel === '') {
      record = !record;

    // Stop recording at the second single quote character
    } else if (channels_string[i] === "'" && channel !== '') {
      record = !record;
      
      // Use *.substring(1) to trim the first single quote character. The second
      // single quote character is omitted by default.
      channel = channel.substring(1)

      // The newly trimmed "channel" string is added to the channels[] array
      channels.push(channel);
      channel = '';
    };
    
    // Piece together the names of each channel 1 character at a time as long as
    // record == True.
    if (record) {
      channel += channels_string[i];
    };
  };

  // Create channel room links with names from the channels[] array
  for (let j = 0; j < channels.length; j++) {
    var a = document.createElement('a');
    var br = document.createElement('br');
    a.href = 'channel/' + channels[j] + '?name=' + channels[j];
    a.name = channels[j];
    a.innerHTML = channels[j];
    document.getElementById('channel_list').appendChild(a);
    document.getElementById('channel_list').appendChild(br);
  };
});

// https://jsfiddle.net/taditdash/hDtA3/
function AvoidSpace(event) {
  var k = event ? event.which : window.event.keyCode;
  if (k == 32) return false;
};
// The application.py file returns 'channel_list' to index.html, which looks like 
// an array but is actually a string, and it is stored in a hidden <div> element 
// on the DOM. There is a custom parser used in this file that turns the string 
// into an actual array (there might be a tool out that there does this but I 
// already wrote the code for it, so...). 

document.addEventListener('DOMContentLoaded', () => {

  alert('index');

  // By default, the 'Create a new channel' submit button is disabled. Enable 
  // 'Create a new channel' submit button only if there is text in the input 
  // field.
  document.querySelector('#submit').disabled = true;
  document.querySelector('#new_channel').oninput = () => {
    if (document.querySelector('#new_channel').value.length > 0)
      document.querySelector('#submit').disabled = false;
    else
      document.querySelector('#submit').disabled = true;
  };

  // Hide the channel_list string that is stored in a <div> on the DOM when it is 
  // returned from application.py.
  document.querySelector("#channel_list_div_hidden").style.visibility = "hidden";

  // Custom parser that converts the channel names returned from application.py
  // and stored in a hidden <div> on index.html into an array of channels stored 
  // in channel_list[].
  var record = false;
  var channel = '';
  var channel_list = [];
  var channel_list_string = document.querySelector("#channel_list_div_hidden").innerHTML;

  for (let i = 0; i < channel_list_string.length; i++) {

    // Start recording at the first single quote character
    if (channel_list_string[i] === "'" && channel === '') {
      record = !record;

    // Stop recording at the second single quote character
    } else if (channel_list_string[i] === "'" && channel !== '') {
      record = !record;
      
      // Use *.substring(1) to trim the first single quote character. The second
      // single quote character is omitted by default.
      channel = channel.substring(1)

      // The newly trimmed "channel" string is added to the channel_list[] array
      channel_list.push(channel);
      channel = '';
    };
    
    // Piece together the names of each channel 1 character at a time as long as
    // record == True.
    if (record) {
      channel += channel_list_string[i];
    };
  };

  // Create channel room links with names from the channel_list[] array
  for (let j = 0; j < channel_list.length; j++) {
    var a = document.createElement('a');
    var br = document.createElement('br');
    a.href = 'channel/' + channel_list[j] + '?name=' + channel_list[j];
    a.name = channel_list[j];
    a.innerHTML = channel_list[j];
    document.getElementById('channel_list').appendChild(a);
    document.getElementById('channel_list').appendChild(br);
  };

// https://jsfiddle.net/taditdash/hDtA3/
function AvoidSpace(event) {
  var k = event ? event.which : window.event.keyCode;
  if (k == 32) return false;
};
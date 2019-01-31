// Custom parser that converts the 'channels' string received from application.py
// into a JavaScript array
var record = false;
var channel = '';
var channels = [];
var channels_string = document.getElementById("channels_hidden").innerHTML;
for (let i = 0; i < channels_string.length; i++) {

  if (channels_string[i] === "'" && channel === '') {
    record = !record;
  } else if (channels_string[i] === "'" && channel !== '') {
    record = !record;
    channel = channel.substring(1)
    channels.push(channel);
    channel = '';
  };
  
  if (record) {
    channel += channels_string[i];
  };
};

// Hide the channels string that is returned from application.py
document.getElementById("channels_hidden").style.visibility = "hidden";

// Create channel room links with names from the channels[] array
for (let j = 0; j < channels.length; j++) {
  var a = document.createElement('a');
  var br = document.createElement('br');
  a.href = 'channel/' + channels[j];
  a.innerHTML = channels[j];
  document.getElementById('channel_list').appendChild(a);
  document.getElementById('channel_list').appendChild(br);
}
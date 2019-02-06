// Custom parser that converts the "channels_string" received from the *.innerHTML
// method into an array of channel names
var record = false;
var channel = '';
var channels = [];
var channels_string = document.getElementById("channels_hidden").innerHTML;

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
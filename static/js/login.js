document.addEventListener('DOMContentLoaded', () => {

  // Enable submit button only if there is text in the input field
  document.querySelector('.input-username').oninput = () => {
    if (document.querySelector('.input-username').value.length > 0)
      document.querySelector('.submit-button').disabled = false;
    else
      document.querySelector('.submit-button').disabled = true;
  };
});

// https://jsfiddle.net/taditdash/hDtA3/
function AvoidSpace(event) {
  var k = event ? event.which : window.event.keyCode;
  if (k == 32) return false;
};
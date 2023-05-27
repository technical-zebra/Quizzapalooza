/**
 * The function selects radio button values and displays/hides certain blocks of HTML code based on the
 * selected value.
 */
function SelectRadioValue() {
  let radios = document.getElementsByName('quiz_mode');

  if (radios.length > 0 && radios[0].checked) {
    // True or False mode is selected
    document.getElementById('choice1Block').style.display = 'block';
    document.getElementById('choice2Block').style.display = 'block';
    document.getElementById('choice3Block').style.display = 'none';
    document.getElementById('choice4Block').style.display = 'none';
    document.getElementById('choice1').value = 'True';
    document.getElementById('choice2').value = 'False';
    document.getElementById('choice1').readOnly = true;
    document.getElementById('choice2').readOnly = true;
  } else {
    // 4 multiple choice mode is selected
    document.getElementById('choice1Block').style.display = 'block';
    document.getElementById('choice2Block').style.display = 'block';
    document.getElementById('choice3Block').style.display = 'block';
    document.getElementById('choice4Block').style.display = 'block';
    document.getElementById('choice1').value = '';
    document.getElementById('choice2').value = '';
    document.getElementById('choice1').readOnly = false;
    document.getElementById('choice2').readOnly = false;
  }
}
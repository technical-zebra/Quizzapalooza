/**
 * The function selects radio button values and displays/hides certain blocks of HTML code based on the
 * selected value.
 */
function SelectRadioValue() {
  let radios = document.getElementsByName('quiz_mode');

  document.getElementById('choice1Block').style.display = 'block';
  document.getElementById('choice2Block').style.display = 'block';

  if (radios.length > 0 && radios[0].checked) {
    // True or False mode is selected
    document.getElementById('choice3Block').style.display = 'none';
    document.getElementById('choice4Block').style.display = 'none';
    document.getElementsByName('choice1')[0].value = 'True';
    document.getElementsByName('choice2')[0].value = 'False';
    document.getElementsByName('choice1')[0].readOnly = true;
    document.getElementsByName('choice2')[0].readOnly = true;
  } else {
    // 4 multiple choice mode is selected

    document.getElementById('choice3Block').style.display = 'block';
    document.getElementById('choice4Block').style.display = 'block';
    document.getElementsByName('choice1')[0].value = '';
    document.getElementsByName('choice2')[0].value = '';
    document.getElementsByName('choice1')[0].readOnly = false;
    document.getElementsByName('choice2')[0].readOnly = false;
  }
}
function validateY() {
  const y = document.getElementById('y-coord-input').value;
  if(!isNaN(y)){
    if(!(y==='')) {
      if ((y > -3) && y < 3){
        return true;
      }
      else {
        return false;
      }
    } else{
      return false;
    }
  } else {
    return false;
  }
}

function validateR() {
  const checkboxes = document.querySelectorAll('input[name="r"]:checked');
  
  if (checkboxes.length > 1 || checkboxes.length<1) {
    return false;
  }
  if (checkboxes.length === 1) {
    return true;
  }
}

function validateAll() {
  if (validateY() === false || validateR() == false) {
    return false;
  } else{
    return true;
  }
}


function getX(){
  return document.getElementById('x-coord-input').value;
}

function getY(){
  return document.getElementById('y-coord-input').value;
}

function getR(){
    const checkboxes = document.querySelectorAll('input[name="r"]');
    let selectedValue = null;

    checkboxes.forEach((checkbox) => {
        if (checkbox.checked) {
            selectedValue = checkbox.value;
        }
    });
    return selectedValue;
}


let statusOfValidation = '';
const validationMessage = document.querySelector('.js-validation-message');

document.getElementById('js-submit-button').addEventListener('click', function(event){
  event.preventDefault();
  if (validateAll()) {
    statusOfValidation = 'Валидация пройдена успешно';
    validationMessage.classList.add('validation-successed');
    validationMessage.classList.remove('validation-failed');
    validationMessage.innerHTML = statusOfValidation;


    fetch(`/fcgi-bin/web_lab1.jar?x=${getX()}&y=${getY()}&r=${getR()}`, {
      method: 'GET'
    })

    .then(response => {
      if (!response.ok) {
        throw new Error(`${response.status}`);
      }
      return response.text();
    })
  
    .then(function (answer) {

      let resultParse = JSON.parse(answer);

      if (resultParse.error === "not"){
      
      document.getElementById('js-logs-from-server').innerHTML = '';
      
      var tableBody = document.getElementById("response-table").getElementsByTagName("tbody")[0];
      const newRow = tableBody.insertRow();
      const isHit = newRow.insertCell(0);
      const X = newRow.insertCell(1); 
      const Y = newRow.insertCell(2); 
      const R = newRow.insertCell(3); 
      const currentTime = newRow.insertCell(4); 
      const workTime = newRow.insertCell(5);
      
      
      if(resultParse.result === "true"){
        isHit.innerHTML = "Есть попадание";
      } else {
        isHit.innerHTML = "Промах";
      }

      
      X.innerHTML = resultParse.x;
      Y.innerHTML = resultParse.y;
      R.innerHTML = resultParse.r;
      currentTime.innerHTML = resultParse.currTime;
      workTime.innerHTML = resultParse.scrTime;
    } else if(resultParse.error === "empty"){
      document.getElementById('js-logs-from-server').innerHTML = 'Есть пустые поля!';
    } else if(resultParse.error === "wrong method"){
      document.getElementById('js-logs-from-server').innerHTML = 'Необходимо использовать GET запрос!';
    } else if(resultParse.error === 'not valid data'){
      document.getElementById('js-logs-from-server').innerHTML = 'Невалидные данные!';
    }
  })
    


  } else{
    statusOfValidation = 'Валидация не пройдена';
    validationMessage.classList.add('validation-failed');
    validationMessage.classList.remove('validation-successed');
    validationMessage.innerHTML = statusOfValidation;
  }

})



  function getX(){
    return document.getElementById('x-cord-input').value;
  }

  function getY(){
    return document.getElementById('y-cord-input').value;
  }

  function getR(){
    return document.getElementById("r-cord-input").value;
  }

  // Функция валидации значения Y
  function validateY(y) {
    const yNum = parseFloat(y);
    if(!isNaN(yNum)){
      return (yNum > -3) && (yNum < 5);
    } else {
      return false;
    }
  }

  // Функция общей валидации
  function validateAll() {
    const yValid = validateY(getY());
    const rValid = !isNaN(getR()) && Number(getR()) !== 0;
    return yValid && rValid;
  }

let statusOfValidation = '';
const validationMessage = document.querySelector('.js-validation-message');

const canvas = document.getElementById('graphCanvas');
const ctx = canvas.getContext('2d');

// Параметры координатной плоскости
const width = canvas.width;
const height = canvas.height;
const originX = width / 2;
const originY = height / 2;
const scale = 40; // Размер одной единицы

// Функция для рисования осей
function drawAxes() {
  ctx.beginPath();
  ctx.strokeStyle = '#000000';
  ctx.lineWidth = 2;

  // Ось X
  ctx.moveTo(0, originY);
  ctx.lineTo(width, originY);

  // Ось Y
  ctx.moveTo(originX, 0);
  ctx.lineTo(originX, height);

  ctx.stroke();
}

// Функция для рисования сетки
function drawGrid() {
  ctx.beginPath();
  ctx.strokeStyle = '#e0e0e0';
  ctx.lineWidth = 1;

  // Вертикальные линии
  for (let x = originX; x <= width; x += scale) {
    ctx.moveTo(x, 0);
    ctx.lineTo(x, height);
  }
  for (let x = originX; x >= 0; x -= scale) {
    ctx.moveTo(x, 0);
    ctx.lineTo(x, height);
  }

  // Горизонтальные линии
  for (let y = originY; y <= height; y += scale) {
    ctx.moveTo(0, y);
    ctx.lineTo(width, y);
  }
  for (let y = originY; y >= 0; y -= scale) {
    ctx.moveTo(0, y);
    ctx.lineTo(width, y);
  }

  ctx.stroke();
}

// Функция для рисования отметок на осях
function drawTicks() {
  ctx.fillStyle = '#000000';
  ctx.font = '8px Arial';
  ctx.textAlign = 'center';
  ctx.textBaseline = 'top';

  // Отметки на оси X
  for (let x = originX + scale, i = 1; x < width; x += scale, i++) {
    ctx.beginPath();
    ctx.moveTo(x, originY - 3);
    ctx.lineTo(x, originY + 3);
    ctx.stroke();
    ctx.fillText(i, x, originY + 8);
  }
  for (let x = originX - scale, i = -1; x > 0; x -= scale, i--) {
    ctx.beginPath();
    ctx.moveTo(x, originY - 3);
    ctx.lineTo(x, originY + 3);
    ctx.stroke();
    ctx.fillText(i, x, originY + 8);
  }

  // Отметки на оси Y
  ctx.textAlign = 'right';
  ctx.textBaseline = 'middle';
  for (let y = originY - scale, i = 1; y > 0; y -= scale, i++) {
    ctx.beginPath();
    ctx.moveTo(originX - 3, y);
    ctx.lineTo(originX + 3, y);
    ctx.stroke();
    ctx.fillText(i, originX - 8, y);
  }
  for (let y = originY + scale, i = -1; y < height; y += scale, i--) {
    ctx.beginPath();
    ctx.moveTo(originX - 3, y);
    ctx.lineTo(originX + 3, y);
    ctx.stroke();
    ctx.fillText(i, originX - 8, y);
  }

  // Стрелки на осях
  const arrowSize = 5;

  // Стрелка на оси X (вправо)
  ctx.beginPath();
  ctx.moveTo(width - arrowSize, originY - arrowSize / 2);
  ctx.lineTo(width, originY);
  ctx.lineTo(width - arrowSize, originY + arrowSize / 2);
  ctx.stroke();

  // Стрелка на оси Y (вверх)
  ctx.beginPath();
  ctx.moveTo(originX - arrowSize / 2, arrowSize);
  ctx.lineTo(originX, 0);
  ctx.lineTo(originX + arrowSize / 2, arrowSize);
  ctx.stroke();

}

// Функция для рисования координатной плоскости
function drawCoordinatePlane() {
  drawGrid();
  drawAxes();
  drawTicks();
}
// Вызов функции рисования
drawCoordinatePlane();

function toCanvasCoords(x, y) {
  return {
    x: originX + x * scale,
    y: originY - y * scale
  };
}
function toLogicalCoords(canvasX, canvasY) {
  return {
    x: (canvasX - originX) / scale,
    y: (originY - canvasY) / scale
  };
}


// Функция для рисования точки
function drawPoint(x, y, color = '#FF0000') {
  const coords = toCanvasCoords(x, y);
  ctx.beginPath();
  ctx.arc(coords.x, coords.y, 5, 0, 2 * Math.PI);
  ctx.fillStyle = color;
  ctx.fill();
  ctx.strokeStyle = '#000000';
  ctx.stroke();
}

// Функция для рисования четверти круга
function drawQuarterCircle(R) {
  // Если R равен 0, ничего не рисуем
  if (R === 0) return;

  // Преобразуем координаты (0,0) для центра
  const center = toCanvasCoords(0, 0);
  const radius = R * scale;

  ctx.beginPath();
  ctx.fillStyle = 'rgba(0, 0, 255, 0.3)'; // Полупрозрачный синий цвет для заливки
  ctx.strokeStyle = '#0000FF'; // Цвет контура (синий)
  ctx.lineWidth = 2;

  // Рисуем закрашенную четверть круга в первой четверти
  // В математических координатах: от 0 до 90 градусов
  // В canvas: от -0.5π до 0 радиан
  ctx.moveTo(center.x, center.y); // Начинаем путь в центре
  ctx.arc(center.x, center.y, radius, -0.5 * Math.PI, 0, false); // Рисуем дугу
  ctx.closePath(); // Замыкаем путь

  ctx.fill(); // Заливаем область
  ctx.stroke(); // Рисуем контур
}
function drawRectangle(R) {
  // Если R равен 0, ничего не рисуем
  if (R === 0) return;

  // Координаты углов прямоугольника
  const topLeft = toCanvasCoords(-R, 0);
  const topRight = toCanvasCoords(0, 0);
  const bottomLeft = toCanvasCoords(-R, -R / 2);
  const bottomRight = toCanvasCoords(0, -R / 2);

  ctx.beginPath();
  ctx.fillStyle = 'rgba(0, 0, 255, 0.3)'; // Полупрозрачный синий цвет для заливки
  ctx.strokeStyle = '#0000FF'; // Цвет контура (синий)
  ctx.lineWidth = 2;

  ctx.moveTo(topLeft.x, topLeft.y);
  ctx.lineTo(topRight.x, topRight.y);
  ctx.lineTo(bottomRight.x, bottomRight.y);
  ctx.lineTo(bottomLeft.x, bottomLeft.y);
  ctx.closePath();

  ctx.fill(); // Заливаем область
  ctx.stroke(); // Рисуем контур
}
function drawTriangle(R) {
  // Если R равен 0, ничего не рисуем
  if (R === 0) return;

  // Вершины треугольника
  const vertex1 = toCanvasCoords(-R, 0);
  const vertex2 = toCanvasCoords(0, 0);
  const vertex3 = toCanvasCoords(0, R / 2);

  ctx.beginPath();
  ctx.fillStyle = 'rgba(0, 0, 255, 0.3)'; // Полупрозрачный синий цвет для заливки
  ctx.strokeStyle = '#0000FF'; // Цвет контура (синий)
  ctx.lineWidth = 2;

  ctx.moveTo(vertex1.x, vertex1.y);
  ctx.lineTo(vertex2.x, vertex2.y);
  ctx.lineTo(vertex3.x, vertex3.y);
  ctx.closePath();

  ctx.fill(); // Заливаем область
  ctx.stroke(); // Рисуем контур
}

function clearCanvas() {
  ctx.clearRect(0, 0, width, height);
  drawCoordinatePlane();
}

// Функция для обработки изменения значения R
function handleRChange() {
  const rSelect = document.getElementById('r-cord-input');
  const R = parseFloat(rSelect.value, 10);
  clearCanvas();
  if (R > 0) {
    drawQuarterCircle(R);
    drawRectangle(R);
    drawTriangle(R);
  }
}

  // Добавляем обработчик события изменения выбора R
document.getElementById('r-cord-input').addEventListener('change', handleRChange);

// Функция для добавления результата в таблицу
function addResultToTable(result) {
  const tableBody = document.querySelector('#response-table tbody');
  const row = document.createElement('tr');

  const countCell = document.createElement('td');
  countCell.textContent = tableBody.children.length + 1;
  row.appendChild(countCell);

  const xCell = document.createElement('td');
  xCell.textContent = result.x;
  row.appendChild(xCell);

  const yCell = document.createElement('td');
  yCell.textContent = result.y;
  row.appendChild(yCell);

  const rCell = document.createElement('td');
  rCell.textContent = result.r;
  row.appendChild(rCell);

  const hitCell = document.createElement('td');
  hitCell.textContent = result.hit ? "Да" : "Нет";
  row.appendChild(hitCell);

  tableBody.appendChild(row);
}

// Функция для обработки клика по canvas
function handleCanvasClick(event) {
  const r = parseFloat(getR());
  if (r!==0) {
    const rect = canvas.getBoundingClientRect();
    const canvasX = event.clientX - rect.left;
    const canvasY = event.clientY - rect.top;

    const logicalCoords = toLogicalCoords(canvasX, canvasY);
    const x = logicalCoords.x;
    const y = logicalCoords.y;

    // Округляем координаты до 2 знаков после запятой
    const roundedX = Math.round(x * 100) / 100;
    const roundedY = Math.round(y * 100) / 100;

    const formData = new URLSearchParams();
    formData.append('x', roundedX);
    formData.append('y', roundedY);
    formData.append('r', r);
    formData.append('ajax', 'true'); // Указываем, что это AJAX-запрос

    fetch('controller-servlet', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
      },
      body: formData.toString()
    })
        .then(response => {
          if (response.ok) {
            return response.json();
          } else {
            return response.json().then(err => { throw new Error(err.error); });
          }
        })
        .then(result => {
          drawPoint(result.x, result.y, result.hit ? '#00FF00' : '#FF0000');

          addResultToTable(result);
        })
        .catch(error => {
          console.error('Ошибка:', error);
          alert('Ошибка при обработке клика по canvas: ' + error.message);
        });
  }
  else{
    statusOfValidation = 'Чтобы отправить запрос по клику установите значение R > 0';
    validationMessage.classList.add('validation-failed');
    validationMessage.classList.remove('validation-successed');
    validationMessage.innerHTML = statusOfValidation;
  }

}

  // Добавляем обработчик клика по canvas
canvas.addEventListener('click', handleCanvasClick)

document.addEventListener('DOMContentLoaded', () => {
  const form = document.querySelector('.coords-form');

  form.addEventListener('submit', function(event) {
    event.preventDefault(); // Предотвращаем стандартную отправку формы
    if (validateAll()) {
      // Обновляем статус валидации
      statusOfValidation = 'Валидация пройдена успешно';
      validationMessage.classList.add('validation-successed');
      validationMessage.classList.remove('validation-failed');
      validationMessage.innerHTML = statusOfValidation;

      // Собираем данные формы
      const formData = new URLSearchParams();
      formData.append('x', getX());
      formData.append('y', getY());
      formData.append('r', getR());

      fetch('controller-servlet', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
        },
        body: formData.toString()
      })
          .then(response => {
            if (response.ok) {
              return response.text();
            } else {
              throw new Error('Сетевая ошибка при отправке формы');
            }
          })
          .then(html => {
            // Замещаем текущий контент полученным HTML
            document.open();
            document.write(html);
            document.close();
          })
          .catch(error => {
            console.error('Ошибка:', error);
            statusOfValidation = 'Ошибка при отправке формы';
            validationMessage.classList.add('validation-failed');
            validationMessage.classList.remove('validation-successed');
            validationMessage.innerHTML = statusOfValidation;
          });

    } else {
      // Если валидация не прошла, обновляем статус
      statusOfValidation = 'Валидация не пройдена';
      validationMessage.classList.add('validation-failed');
      validationMessage.classList.remove('validation-successed');
      validationMessage.innerHTML = statusOfValidation;
    }
  });
});




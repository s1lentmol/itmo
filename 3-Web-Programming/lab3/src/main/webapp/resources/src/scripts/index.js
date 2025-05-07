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

// Функции для рисования фигур
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
  ctx.arc(center.x, center.y, radius, 0, 0.5 * Math.PI, false); // Рисуем дугу
  ctx.closePath(); // Замыкаем путь

  ctx.fill(); // Заливаем область
  ctx.stroke(); // Рисуем контур
}
function drawRectangle(R) {
  // Если R равен 0, ничего не рисуем
  if (R === 0) return;
  // Координаты углов прямоугольника
  const topLeft = toCanvasCoords(-R / 2, R);
  const topRight = toCanvasCoords(0, R);
  const bottomLeft = toCanvasCoords(-R / 2, 0);
  const bottomRight = toCanvasCoords(0, 0);

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
  const vertex1 = toCanvasCoords(-R / 2, 0);
  const vertex2 = toCanvasCoords(0, 0);
  const vertex3 = toCanvasCoords(0, -R / 2);

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

function updateFigures() {
  const r = parseInt(document.querySelector('input[name="r-cord-input"]:checked').value);
  clearCanvas();
  drawQuarterCircle(r);
  drawRectangle(r);
  drawTriangle(r);
}


// Отрисовывание точки после отправки формы
function handleSubmitComplete() {
  const lastHitElement = document.getElementById('lastHit');
  const lastXElement = document.getElementById('lastX');
  const lastYElement = document.getElementById('lastY');
  if (lastHitElement && lastXElement && lastYElement) {
    const hit = lastHitElement.textContent.trim();
    const x = parseFloat(lastXElement.textContent.trim());
    const y = parseFloat(lastYElement.textContent.trim());
    const color = (hit === "true") ? '#00FF00' : '#FF0000';
    drawPoint(x, y, color);
  }
}

function handleProcessClickComplete() {
  const lastHitElement = document.getElementById('lastHit');
  if (lastHitElement) {
    const hit = lastHitElement.textContent.trim();
    const color = (hit === "true") ? '#00FF00' : '#FF0000';
    drawPoint(lastXParam, lastYParam, color);
  }
}
let lastXParam = 0;
let lastYParam = 0;
// Обработчик кликов по канвасу
canvas.addEventListener('click', function(event) {
  const rect = canvas.getBoundingClientRect();
  const canvasX = event.clientX - rect.left;
  const canvasY = event.clientY - rect.top;

  const logical = toLogicalCoords(canvasX, canvasY);
  const x = logical.x;
  const y = logical.y;

  // Округление координат до двух знаков
  const roundedX = Math.round(x * 100) / 100;
  const roundedY = Math.round(y * 100) / 100;

  // Проверка выбран ли R
  const rSelected = document.querySelector('input[name="r-cord-input"]:checked');
  if (!rSelected) {
    // Отображение сообщения об ошибке
    const validationMessageElement = document.getElementById('validationMessage');
    if (validationMessageElement) {
      validationMessageElement.textContent = "Значение R необходимо выбрать!";
      validationMessageElement.style.color = "red";
    }
    return; // Прерываем выполнение, не отправляем запрос на сервер
  }

  lastXParam = roundedX;
  lastYParam = roundedY;

  let lastRParam = parseInt(document.querySelector('input[name="r-cord-input"]:checked').value);

  // Вызов remoteCommand с передачей параметров
  processClick([{name: 'x', value: roundedX}, {name: 'y', value: roundedY}, {name: "r", value: lastRParam}]);
});
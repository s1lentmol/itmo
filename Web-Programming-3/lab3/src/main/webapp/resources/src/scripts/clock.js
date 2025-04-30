document.addEventListener("DOMContentLoaded", function() {
    const canvas = document.getElementById('clock');
    const ctx = canvas.getContext('2d');
    const radius = canvas.width / 2;
    ctx.translate(radius, radius); // Перенос начала координат в центр канваса
    const clockRadius = radius * 0.75; // Уменьшенный радиус циферблата

    function drawClock() {
        drawFace(ctx, clockRadius);
        drawNumbers(ctx, clockRadius);
        drawTime(ctx, clockRadius);
        drawDate(ctx, clockRadius);
    }

    // Нарисовать циферблат
    function drawFace(ctx, radius) {
        ctx.beginPath();
        ctx.arc(0, 0, radius, 0, 2 * Math.PI);
        ctx.fillStyle = '#333'; // Тёмный фон циферблата
        ctx.fill();

        // Ребра циферблата
        ctx.lineWidth = radius * 0.05;
        ctx.strokeStyle = '#fff'; // Белые линии циферблата
        ctx.stroke();

        // Центр циферблата
        ctx.beginPath();
        ctx.arc(0, 0, radius * 0.05, 0, 2 * Math.PI);
        ctx.fillStyle = '#fff'; // Белый центр
        ctx.fill();
    }

    // Нарисовать цифры на циферблате
    function drawNumbers(ctx, radius) {
        ctx.font = `${radius * 0.15}px Arial`;
        ctx.fillStyle = '#fff'; // Белый цвет цифр
        ctx.textBaseline = "middle";
        ctx.textAlign = "center";
        for(let num = 1; num <= 12; num++) {
            const ang = num * Math.PI / 6;
            ctx.rotate(ang);
            ctx.translate(0, -radius * 0.85);
            ctx.rotate(-ang);
            ctx.fillText(num.toString(), 0, 0);
            ctx.rotate(ang);
            ctx.translate(0, radius * 0.85);
            ctx.rotate(-ang);
        }
    }

    // Нарисовать стрелки времени
    function drawTime(ctx, radius) {
        const now = new Date();
        let hour = now.getHours();
        let minute = now.getMinutes();
        let second = now.getSeconds();

        // Часовая стрелка
        hour = hour % 12;
        hour = (hour * Math.PI / 6) +
            (minute * Math.PI / (6 * 60)) +
            (second * Math.PI / (360 * 60));
        drawHand(ctx, hour, radius * 0.5, radius * 0.07);

        // Минутная стрелка
        minute = (minute * Math.PI / 30) + (second * Math.PI / (30 * 60));
        drawHand(ctx, minute, radius * 0.8, radius * 0.07);

        // Секундная стрелка
        second = (second * Math.PI / 30);
        drawHand(ctx, second, radius * 0.9, radius * 0.02, 'red');
    }

    // Функция для рисования одной стрелки
    function drawHand(ctx, pos, length, width, color = '#fff') { // Белый цвет по умолчанию
        ctx.beginPath();
        ctx.lineWidth = width;
        ctx.lineCap = "round";
        ctx.strokeStyle = color;
        ctx.moveTo(0,0);
        ctx.rotate(pos);
        ctx.lineTo(0, -length);
        ctx.stroke();
        ctx.rotate(-pos);
    }

    // Нарисовать дату и время под циферблатом
    function drawDate(ctx, radius) {
        const now = new Date();
        const dateString = now.toLocaleDateString();
        const timeString = now.toLocaleTimeString();

        // Создадим полупрозрачный фон для даты и времени
        const dateBoxHeight = radius * 0.3; // Высота области для даты и времени
        ctx.beginPath();
        ctx.rect(-radius, radius + 10, 2 * radius, dateBoxHeight); // Позиция ниже циферблата
        ctx.fillStyle = 'rgb(77, 77, 77)';
        ctx.fill();

        // Дата
        ctx.font = `${radius * 0.15}px Arial`;
        ctx.fillStyle = '#fff'; // Белый цвет текста
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(dateString, 0, radius + 10 + dateBoxHeight * 0.3); // Смещено ниже циферблата

        // Время
        ctx.font = `${radius * 0.12}px Arial`;
        ctx.fillText(timeString, 0, radius + 10 + dateBoxHeight * 0.7); // Смещено ниже даты
    }

    function updateClock() {
        ctx.clearRect(-radius, -radius, canvas.width, canvas.height);
        drawClock();
    }

    updateClock();
    setInterval(updateClock, 7000);
});
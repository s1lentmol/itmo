<%@ page import="com.example.web_lab2.Result" %>
<%@ page import="java.util.List" %>
<%@ page contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>
<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>main page</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,100;0,300;0,400;0,500;0,700;0,900;1,100;1,300;1,400;1,500;1,700;1,900&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="./styles/general.css">
    <link rel="stylesheet" href="./styles/header.css">
    <link rel="stylesheet" href="./styles/main.css">
  </head>
  <body>
  <header class="header">
    <div class="left-section">
      <img class="itmo-logo-light" src="./images/itmo-logo-light.svg">
      <img class="cs-logo" src="./images/cs-logo.png">
    </div>

    <div class="middle-section">
      Лабораторная работа №2
    </div>
    <div class="right-section">
      <p>Молчанов Артём</p>
      <p>Группа: Р3219</p>
      <p>Вариант: 10253</p>
    </div>
  </header>

  <main class="main">
    <div class="main-left-section">
      <form class="coords-form">
        <label for="x-cord-input">Выберите значение для X</label>
        <select type="text" name="x" id="x-cord-input">
          <option value="-5">-5</option>
          <option value="-4">-4</option>
          <option value="-3">-3</option>
          <option value="-2">-2</option>
          <option value="-1">-1</option>
          <option value="0" selected>0</option>
          <option value="1">1</option>
          <option value="2">2</option>
          <option value="3">3</option>
        </select>

        <label for="y-cord-input">Введите значение для Y</label>
        <p style="font-size: 10px;">Данное значение должно быть в диапазоне (-3,5)</p>

        <input type="text" name="y" id="y-cord-input" placeholder="Input Y coord"/>

        <label for="r-cord-input">Выберите значение для R</label>
        <select type="text" name="r" id="r-cord-input">
          <option value="0" selected>0</option>
          <option value="1">1</option>
          <option value="2">2</option>
          <option value="3">3</option>
          <option value="4">4</option>
          <option value="5">5</option>
        </select>
        <button id="js-submit-button" type="submit">Submit</button>
        <p class="js-validation-message"></p>
      </form>
      <div class="history">
        <h2 class="center">История запросов</h2>
        <table id="response-table" border="1">
          <thead>
          <tr>
            <th>#</th>
            <th>X</th>
            <th>Y</th>
            <th>R</th>
            <th>Попадание</th>
          </tr>
          </thead>
          <tbody>
          <%
            if (session != null) {
              List<Result> results = (List<Result>) session.getAttribute("results");
              if (results != null && !results.isEmpty()) {
                int count = 1;
                for (Result res : results) {
          %>
          <tr>
            <td><%= count++ %></td>
            <td><%= res.getX() %></td>
            <td><%= res.getY() %></td>
            <td><%= res.getR() %></td>
            <td><%= res.isHit() ? "Да" : "Нет" %></td>
          </tr>
          <%
                }
              }
            }
          %>
          </tbody>
        </table>
      </div>
    </div>

    <div class="main-right-section">
      <div class="cord-plane">
        <canvas id="graphCanvas" width="500" height="500"></canvas>
      </div>
    </div>
  </main>
    <script src="./scripts/index.js"></script>
  </body>
</html>

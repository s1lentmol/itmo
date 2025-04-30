<%@ page contentType="text/html; charset=UTF-8" %>
<%@ page import="com.example.web_lab2.Result" %>
<%@ page import="java.util.List" %>
<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="./styles/result.css">
    <meta charset="UTF-8">
    <title>Results</title>
</head>
<body>

<h2 class="center">История запросов</h2>
<%
    if (session != null) {
        String errorMessage = (String) request.getAttribute("errorMessage");
        if (errorMessage != null && !errorMessage.isEmpty()) {
%>
<p class="error-message"><%= errorMessage %></p>
<%
    }

    List<Result> results = (List<Result>) session.getAttribute("results");
    if (results != null && !results.isEmpty()) {
%>
<table>
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
    %>
    </tbody>
</table>
<%
} else {
%>
<p class="center">Нет записей.</p>
<%
        }
    }
%>
<!-- Ссылка на страницу с формой для создания нового запроса -->
<div class="center">
    <a href="<%= request.getContextPath() %>/index.jsp" class="back-button">Создать Новый Запрос</a>
</div>

</body>
</html>

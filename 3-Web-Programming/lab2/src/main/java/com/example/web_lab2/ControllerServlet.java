package com.example.web_lab2;

import java.io.*;
import jakarta.servlet.*;
import jakarta.servlet.http.*;

public class ControllerServlet extends HttpServlet {
    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        request.setCharacterEncoding("UTF-8");
        response.setCharacterEncoding("UTF-8");
        String xParam = request.getParameter("x");
        String yParam = request.getParameter("y");
        String rParam = request.getParameter("r");

        boolean isValid = true;
        String errorMessage = "";
        String requestMethod = request.getMethod();

        if (!("POST".equalsIgnoreCase(requestMethod))) {
            errorMessage = "Обрабатываются только POST запросы!";
            request.setAttribute("errorMessage", errorMessage);
            request.getRequestDispatcher("/result.jsp").forward(request, response);
        }

        try {
            if(xParam == null || yParam == null || rParam == null){
                isValid = false;
                errorMessage = "invalid data";
            }
            if(xParam.isEmpty() || yParam.isEmpty() || rParam.isEmpty()){
                isValid = false;
                errorMessage = "ivalid data";
            }
            float x = Float.parseFloat(xParam);
            float y = Float.parseFloat(yParam);
            int r = Integer.parseInt(rParam);

        } catch (NumberFormatException e) {
            isValid = false;
            errorMessage = errorMessage + " Параметры должны быть числами.";
        }

        if (!isValid) {
            request.setAttribute("errorMessage", errorMessage);
            request.getRequestDispatcher("/result.jsp").forward(request, response);
        }
        else{
            request.getRequestDispatcher("/areaCheck-servlet").forward(request, response);
        }
    }
}

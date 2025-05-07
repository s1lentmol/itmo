package com.example.web_lab2;

import com.google.gson.Gson;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.*;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
public class AreaCheckServlet extends HttpServlet {
    private final Gson gson = new Gson();

    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        request.setCharacterEncoding("UTF-8");
        response.setCharacterEncoding("UTF-8");

        boolean isAjax = "true".equals(request.getParameter("ajax"));

        String xParam = request.getParameter("x");
        String yParam = request.getParameter("y");
        String rParam = request.getParameter("r");

        float x = 0, y = 0;
        int r = 0;
        boolean isValid = true;
        String errorMessage = "";

        try {
            x = Float.parseFloat(xParam);
            y = Float.parseFloat(yParam);
            r = Integer.parseInt(rParam);
            if (r <= 0) {
                isValid = false;
                errorMessage = " Значение R должно быть больше 0.";
            }

        } catch (NumberFormatException e) {
            isValid = false;
            errorMessage = "Параметры должны быть числами.";
        }

        boolean hit = false;
        if (isValid) {
            hit = checkHit(x, y, r);
        }

        Result result = new Result(x, y, r, hit);

        HttpSession session = request.getSession();
        List<Result> results = (List<Result>) session.getAttribute("results");

        if (results == null) {
            results = new ArrayList<>();
        }
        results.add(result);
        session.setAttribute("results", results);


        if (isAjax) {
            response.setContentType("application/json");
            if (isValid) {
                String json = gson.toJson(result);
                response.getWriter().write(json);
            } else {
                ErrorResponse errorResponse = new ErrorResponse(errorMessage);
                String json = gson.toJson(errorResponse);
                response.setStatus(HttpServletResponse.SC_BAD_REQUEST);
                response.getWriter().write(json);
            }

        } else {
            if (y<=-3 || y>=5){
                isValid = false;
                errorMessage = errorMessage + " Значение y должно принадлежать интервалу (-3,5)";
            }
            if (!isValid) {
                request.setAttribute("errorMessage", errorMessage);
            }

            request.setAttribute("results", results);

            request.getRequestDispatcher("/result.jsp").forward(request, response);
        }
    }
    public boolean checkHit(float x, float y, float r){
        return checkInTriangle(x, y, r) || checkInRectangle(x, y, r) || checkInCircle(x, y, r);
    }

    public boolean checkInTriangle(float x, float y, float r){
        return (y <= 0.5 * x + r / 2) && (y >= 0) && (x <= 0);
    }

    public boolean checkInRectangle(float x, float y, float r){
        return (x <= 0) && (x >= -r) && (y >= -r/2) && (y <= 0);
    }

    public boolean checkInCircle(float x, float y, float r){
        return (x*x + y*y <= r*r) && (y >= 0) && (x >= 0);
    }

    // Внутренний класс для обработки ошибок
    private static class ErrorResponse {
        private String error;

        public ErrorResponse(String error) {
            this.error = error;
        }

        public String getError() { return error; }
        public void setError(String error) { this.error = error; }
    }
}

package com.example.web_lab3;

import jakarta.enterprise.context.SessionScoped;
import jakarta.faces.context.FacesContext;
import jakarta.inject.Inject;
import jakarta.inject.Named;
import com.example.web_lab3.jmx.MBeanManager;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;

@Named("pointBean")
@SessionScoped
public class PointBean implements Serializable {
    private static final long serialVersionUID = 1L;
    private Double x;
    private Double y;
    private Integer r;
    private String lastHit;
    private Double lastX;
    private Double lastY;
    private String validationMessage;
    private List<PointResultEntity> results = new ArrayList<>();

    @Inject
    private AreaCheckBean areaCheckBean;
    @Inject
    private PointResultDAO pointResultDAO;

    // Геттеры и сеттеры
    public Double getX() {
        return x;
    }

    public void setX(Double x) {
        this.x = x;
    }

    public Double getY() {
        return y;
    }

    public void setY(Double y) {
        this.y = y;
    }

    public Integer getR() {
        return r;
    }

    public void setR(Integer r) {
        this.r = r;
    }

    public String getValidationMessage() {
        return validationMessage;
    }

    public List<PointResultEntity> getResults() {
        return results;
    }
    public void setResults(List<PointResultEntity> results){
        this.results = results;
    }

    public String getLastHit() {
        return lastHit;
    }

    public void setLastHit(String lastHit) {
        this.lastHit = lastHit;
    }
    public Double getLastX() {
        return lastX;
    }

    public void setLastX(Double lastX) {
        this.lastX = lastX;
    }

    public Double getLastY() {
        return lastY;
    }

    public void setLastY(Double lastY) {
        this.lastY = lastY;
    }
    public void submit() {
        boolean hit = areaCheckBean.checkHit(x.floatValue(), y.floatValue(), r.floatValue());

        // 1) обновляем счётчики MBean
        MBeanManager.getPointsStatistics().recordPoint(x, y, r, hit);
        // 2) обновляем R для area‑MBean
        MBeanManager.getShapeArea().setR(r);

        PointResultEntity result = new PointResultEntity(x, y, r, hit);

        pointResultDAO.save(result);

        results = pointResultDAO.findAll();

        lastHit = String.valueOf(hit);
        lastX = Math.round(x * 100.0) / 100.0;
        lastY = Math.round(y * 100.0) / 100.0;
    }

    public void processCanvasClick() {
        FacesContext fc = FacesContext.getCurrentInstance();
        String rParam = fc.getExternalContext().getRequestParameterMap().get("r");
        String xParam = fc.getExternalContext().getRequestParameterMap().get("x");
        String yParam = fc.getExternalContext().getRequestParameterMap().get("y");
        Double xVal = null;
        Double yVal = null;
        String error = null;
        try {
            xVal = Double.parseDouble(xParam);
            xVal = Math.round(xVal * 100.0) / 100.0;
        } catch (NumberFormatException e) {
            error = "Неверное значение X";
        }

        // Парсинг параметров y
        try {
            yVal = Double.parseDouble(yParam);
            yVal = Math.round(yVal * 100.0) / 100.0;
        } catch (NumberFormatException e) {
            error = "Неверное значение Y";
        }

        if (error == null) {
            int currentR = Integer.parseInt(rParam);
            boolean hit = areaCheckBean.checkHit(xVal.floatValue(), yVal.floatValue(), (float) currentR);
            MBeanManager.getPointsStatistics().recordPoint(xVal, yVal, currentR, hit);
            MBeanManager.getShapeArea().setR(currentR);
            PointResultEntity result = new PointResultEntity(xVal, yVal, currentR, hit);

            pointResultDAO.save(result);

            results = pointResultDAO.findAll();

            lastHit = String.valueOf(hit);
            lastX = xVal;
            lastY = yVal;
        }

        if (error != null) {
            validationMessage = error;
            lastHit = "true";
            lastX = null;
            lastY = null;
        } else {
            validationMessage = "";
        }
    }
}
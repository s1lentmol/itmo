package com.example.web_lab3;

import jakarta.enterprise.context.SessionScoped;
import jakarta.inject.Named;
import java.io.Serializable;

@Named("areaCheckBean")
@SessionScoped
public class AreaCheckBean implements Serializable {

    public boolean checkHit(float x, float y, float r){
        return checkInTriangle(x, y, r) || checkInRectangle(x, y, r) || checkInCircle(x, y, r);
    }

    public boolean checkInTriangle(float x, float y, float r){
        return (y >= -x - r / 2) && (y <= 0) && (x <= 0);
    }

    public boolean checkInRectangle(float x, float y, float r){
        return (x <= 0) && (x >= -r / 2) && (y <= r) && (y >= 0);
    }

    public boolean checkInCircle(float x, float y, float r){
        return (x*x + y*y <= r*r) && (y <= 0) && (x >= 0);
    }
}

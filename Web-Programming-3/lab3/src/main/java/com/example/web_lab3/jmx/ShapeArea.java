package com.example.web_lab3.jmx;

public class ShapeArea implements ShapeAreaMBean {
    private int r;

    @Override
    public int getR() {
        return r;
    }

    @Override
    public void setR(int r) {
        this.r = r;
    }

    @Override
    public double getArea() {
        // Треугольник: r^2/8, прямоугольник: r^2/2, четверть круга: πr^2/4
        return r * r * (5 + 2 * Math.PI) / 8.0;
    }
}

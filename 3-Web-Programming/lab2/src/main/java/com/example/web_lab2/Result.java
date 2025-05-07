package com.example.web_lab2;

public class Result {
    private float x;
    private float y;
    private float r;
    private boolean hit;

    public Result(float x, float y, float r, boolean hit) {
        this.x = x;
        this.y = y;
        this.r = r;
        this.hit = hit;
    }

    // Геттеры и сеттеры
    public float getX() { return x; }
    public void setX(float x) { this.x = x; }

    public float getY() { return y; }
    public void setY(float y) { this.y = y; }

    public float getR() { return r; }
    public void setR(float r) { this.r = r; }

    public boolean isHit() { return hit; }
    public void setHit(boolean hit) { this.hit = hit; }
}

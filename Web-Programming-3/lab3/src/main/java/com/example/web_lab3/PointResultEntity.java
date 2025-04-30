package com.example.web_lab3;

import jakarta.persistence.*;

import java.io.Serializable;

@Entity
@Table(name = "point_results")
public class PointResultEntity implements Serializable {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private Double x;

    @Column(nullable = false)
    private Double y;

    @Column(nullable = false)
    private Integer r;

    @Column(nullable = false)
    private boolean hit;

    public PointResultEntity() {}

    public PointResultEntity(Double x, Double y, Integer r, boolean hit) {
        this.x = x;
        this.y = y;
        this.r = r;
        this.hit = hit;
    }

    // Геттеры и сеттеры
    public Long getId() {
        return id;
    }

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

    public boolean isHit() {
        return hit;
    }

    public void setHit(boolean hit) {
        this.hit = hit;
    }
}

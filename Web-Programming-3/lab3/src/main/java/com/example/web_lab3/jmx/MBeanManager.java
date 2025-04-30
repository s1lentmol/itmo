package com.example.web_lab3.jmx;

public class MBeanManager {
    private static PointsStatistics pointsStatistics;
    private static ShapeArea shapeArea;

    static void setPointsStatistics(PointsStatistics ps) {
        pointsStatistics = ps;
    }
    public static PointsStatistics getPointsStatistics() {
        return pointsStatistics;
    }

    static void setShapeArea(ShapeArea sa) {
        shapeArea = sa;
    }
    public static ShapeArea getShapeArea() {
        return shapeArea;
    }
}

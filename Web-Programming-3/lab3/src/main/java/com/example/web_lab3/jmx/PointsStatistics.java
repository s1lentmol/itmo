package com.example.web_lab3.jmx;

import javax.management.Notification;
import javax.management.NotificationBroadcasterSupport;

public class PointsStatistics extends NotificationBroadcasterSupport implements PointsStatisticsMBean {
    private int totalPoints = 0;
    private int hitPoints = 0;
    private int outOfBoundsCount = 0;
    private long sequenceNumber = 1;

    @Override
    public int getTotalPoints() {
        return totalPoints;
    }

    @Override
    public int getHitPoints() {
        return hitPoints;
    }

    @Override
    public int getOutOfBoundsCount() {
        return outOfBoundsCount;
    }

    /**
     * Вызывается для каждой новой точки.
     * @param x координата X
     * @param y координата Y
     * @param r текущее R
     * @param hit true, если точка попала в область
     */
    public void recordPoint(double x, double y, int r, boolean hit) {
        totalPoints++;
        if (hit) {
            hitPoints++;
        }
        if (x < -6 || x > 6 || y < -6 || y > 6) {
            outOfBoundsCount++;
            Notification n = new Notification(
                    "com.example.web_lab3.jmx.outOfBounds",
                    this,
                    sequenceNumber++,
                    System.currentTimeMillis(),
                    String.format("Point out of bounds: x=%.2f, y=%.2f", x, y)
            );
            sendNotification(n);
        }
    }
}

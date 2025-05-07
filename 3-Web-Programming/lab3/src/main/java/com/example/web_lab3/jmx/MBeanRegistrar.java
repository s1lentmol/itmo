package com.example.web_lab3.jmx;

import jakarta.servlet.ServletContextEvent;
import jakarta.servlet.ServletContextListener;
import jakarta.servlet.annotation.WebListener;

import javax.management.MBeanServer;
import javax.management.ObjectName;
import java.lang.management.ManagementFactory;

@WebListener
public class MBeanRegistrar implements ServletContextListener {

    @Override
    public void contextInitialized(ServletContextEvent sce) {
        try {
            MBeanServer mbs = ManagementFactory.getPlatformMBeanServer();

            PointsStatistics ps = new PointsStatistics();
            ObjectName psName = new ObjectName("com.example.web_lab3.jmx:type=PointsStatistics");
            mbs.registerMBean(ps, psName);
            MBeanManager.setPointsStatistics(ps);

            ShapeArea sa = new ShapeArea();
            ObjectName saName = new ObjectName("com.example.web_lab3.jmx:type=ShapeArea");
            mbs.registerMBean(sa, saName);
            MBeanManager.setShapeArea(sa);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    @Override
    public void contextDestroyed(ServletContextEvent sce) {
        // ничего не делаем
    }
}

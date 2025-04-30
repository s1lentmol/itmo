package com.example.web_lab3;

import jakarta.ejb.Stateless;
import jakarta.persistence.*;

import java.io.Serializable;
import java.util.List;

@Stateless
public class PointResultDAO implements Serializable {

    EntityManagerFactory emf = Persistence.createEntityManagerFactory("PointPU");
    EntityManager em = emf.createEntityManager();

    // Сохранение точки в базу данных
    public void save(PointResultEntity point) {
        em.getTransaction().begin();
        em.persist(point);
        em.getTransaction().commit();
    }

    // Получение всех точек из базы данных
    public List<PointResultEntity> findAll() {
        TypedQuery<PointResultEntity> query = em.createQuery("SELECT p FROM PointResultEntity p", PointResultEntity.class);
        return query.getResultList();
    }
}

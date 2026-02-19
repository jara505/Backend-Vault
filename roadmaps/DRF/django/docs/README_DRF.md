# Plan de Estudio: Django REST Framework — Intermedio a Avanzado

Temario personal de DRF. Nivel principiante ya superado. Enfocado en construir APIs robustas, seguras y listas para producción.

**Referencia Oficial:** [Documentación de Django REST Framework](https://www.django-rest-framework.org/)

---

## Nivel 1: DRF Intermedio — Filtrado, Seguridad y Performance

> Objetivo: APIs robustas, seguras y eficientes.
> Carpeta de apuntes: `learning_units/unidad_1_drf_intermedio/`

- [x] Querysets dinámicos (`get_queryset()`, filtrado por usuario/contexto)
- [x] Serializers avanzados (write-only, read-only, validaciones cross-field, SerializerMethodField)
- [x] Filtrado y búsqueda (django-filter, SearchFilter, OrderingFilter)
- [x] Paginación (LimitOffset, PageNumber, personalización)
- [x] Throttling (rate limit global, por vista, custom throttles)
- [x] Autenticación avanzada (JWT refresh tokens, custom claims, blacklist y revocación)
- [x] Permisos avanzados (get_permissions() dinámico, permisos por acción, object-level)
- [ ] Error handling (response estandarizado, status codes correctos)

---

## Nivel 2: DRF Avanzado — Proyectos Reales y Escalables

> Objetivo: preparar APIs para producción y múltiples clientes.

- [ ] Autenticación multi-cliente (SPA + Mobile + Backend-to-backend, JWT cookies vs header)
- [ ] Integración con terceros (OAuth2, OpenID Connect, social login)
- [ ] Optimización de performance (prefetch/select_related, bulk create/update, serializers eficientes)
- [ ] Testing completo (mocking, test de permisos, auth y edge cases)
- [ ] Versionado de API (URL versioning, header versioning)
- [ ] Documentación (OpenAPI / Swagger con DRF-Spectacular)
- [ ] Arquitectura (API-only backend, modular apps, separación serializers/views/services)

---

## Nivel 3: Extras Profesionales

> Objetivo: temas de especialización y deployment.

- [ ] JWT avanzado (token rotation, refresh token seguro)
- [ ] Microservicios con DRF (serialización para eventos/mensajería)
- [ ] Webhooks
- [ ] Seguridad (CORS, CSRF en APIs, rate-limiting avanzado)
- [ ] Deployment (Gunicorn + Nginx, Docker/Kubernetes, staging/prod)

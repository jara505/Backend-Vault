# Django + Django REST Framework

Stack completo de aprendizaje para construir APIs con Django y DRF, desde fundamentos hasta técnicas avanzadas.

---

## 📚 Plan de Estudio

| Recurso | Descripción |
|---------|-------------|
| [🎯 Django Fundamentos](study-plan/django-fundamentals.md) | Base esencial de Django: modelos, vistas, ORM, templates |
| [🎯 DRF Intermedio → Avanzado](study-plan/drf-roadmap.md) | Roadmap completo de DRF con filtrado, seguridad y performance |

---

## 📖 Topics (Apuntes Teórico-Prácticos)

Cada topic incluye una `explicacion.md` con la teoría y archivos `ejemplo_*.py` con código demostrativo.

| # | Topic | Conceptos Clave |
|---|-------|----------------|
| 01 | [Querysets Dinámicos](topics/01-querysets-dinamicos/) | `get_queryset()`, filtrado por usuario/contexto |
| 02 | [Serializers Avanzados](topics/02-serializers-avanzados/) | Read-only/write-only fields, validaciones cross-field, SerializerMethodField |
| 03 | [Filtrado y Búsqueda](topics/03-filtrado-y-busqueda/) | django-filter, SearchFilter, OrderingFilter |
| 04 | [Paginación](topics/04-paginacion/) | LimitOffsetPagination, PageNumberPagination, CursorPagination |
| 05 | [Throttling](topics/05-throttling/) | Rate limiting global, por vista, custom throttles |
| 06 | [Autenticación Avanzada](topics/06-autenticacion-avanzada/) | JWT refresh tokens, custom claims, blacklist y revocación |
| 07 | [Permisos Avanzados](topics/07-permisos-avanzados/) | Permisos dinámicos por acción, object-level permissions |
| 08 | [Manejo de Errores](topics/08-manejo-de-errores/) | Response estandarizado, excepciones personalizadas, custom exception handler |

---

## 💻 Proyecto de Referencia

El proyecto funcional con todas las implementaciones está en:

```
projects/ticket-system/
├── src/
│   ├── core/       # Configuración de Django (settings, urls, wsgi)
│   └── ticket/     # App de tickets (modelos, views, serializers, filters...)
└── manage.py
```

Para ejecutarlo:

```bash
cd projects/ticket-system
python src/manage.py runserver
```

> Los ejemplos en los topics referencian este proyecto con paths como `projects/ticket-system/src/ticket/views.py`.

---

## 🧠 Cómo Usar Este Stack

1. **Seguí el orden numérico** de los topics (01 → 08).
2. **Leé la `explicacion.md`** de cada topic para entender el concepto.
3. **Revisá los `ejemplo_*.py`** para ver el patrón de código.
4. **Andá al proyecto** y buscá la implementación real en el archivo correspondiente.
5. **Experimentá**: modificá el proyecto, agregá nuevos endpoints, rompelo y arreglalo.

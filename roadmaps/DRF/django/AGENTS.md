# Learning Units — Formato de Apuntes

## Estructura de directorios

learning_units/
└── unidad_N_/
├── README.md
└── /
├── explicacion.md
└── ejemplo_.py   # (1 o más)


## README.md (por unidad)

Secciones en orden: `# Título` → `## Objetivo` → `## Subunidades Cubiertas` (lista con bold) → `## Cómo Usar` (pasos numerados) → `## Próximas Subunidades` → `## Notas`.

## explicacion.md

Formato extenso. Secciones en orden:

1. `# Título descriptivo` — una línea introductoria debajo.
2. `## ¿Por qué usarlo?` — lista con bold (3-4 razones).
3. Secciones numeradas (`## 1. Concepto`, `## 2. Concepto`) — cada una con bloques de código inline usando paths reales del proyecto (`src/ticket/...`).
4. Tablas comparativas cuando hay variantes o decisiones (cuándo usar cuál).
5. `## Ejemplo Integrado al Proyecto` — código aplicado al sistema de tickets.
6. `## Errores Comunes` — lista de errores frecuentes (opcional, si aplica).
7. `## Recursos` — links a documentación oficial.

## ejemplo_*.py

- Línea 1-3: comentarios de cabecera (título, contexto del proyecto, objetivo).
- Bloques separados con `# -------------------------------------------------#` y título `# Ejemplo N: Descripción`.
- Al final: bloque de comentarios `# Cómo probar:` (pasos numerados) y `# Ventajas:` (lista).

## Reglas generales

- Idioma: español.
- Todos los ejemplos de código deben usar el modelo `Ticket` y el dominio del proyecto (no ejemplos genéricos como `User` o `Task`).
- Los imports y paths en código deben reflejar la estructura real: `src/ticket/`, `src/core/settings.py`.
- Choices del proyecto: `TicketStatus` (open, in_progress, resolved, closed), `UserRole` (user, agent, admin).
- Campos del modelo Ticket: `title`, `description`, `created_by`, `assigned_to`, `status`, `priority`, `created_at`, `updated_at`.
- Al crear una subunidad nueva, actualizar el README.md de la unidad padre (agregar a "Subunidades Cubiertas").
- Cuando te pida un nombre para rama utiliza convenciones
- Cuando te pida un commit hazlo de manera profesional pero tampoco que sea extremadamente largo ni corto

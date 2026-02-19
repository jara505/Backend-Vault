# Serializers Avanzados: Read-Only/Write-Only, Cross-Field Validation, SerializerMethodField

## ¿Qué son?
Técnicas para controlar campos en serializers DRF:
- **Read-only/Write-only fields:** Controla qué campos aparecen en request (write) vs response (read).
- **Validaciones cross-field:** Valida relaciones entre campos (ej. si A > B, error).
- **SerializerMethodField:** Campo calculado con método personalizado (obj para lógica).

## Por qué usarlos?
- **Seguridad:** Oculta datos sensibles (ej. passwords write-only).
- **Validación:** Evita estados inválidos (ej. reglas de negocio).
- **Flexibilidad:** Campos dinámicos sin modificar modelo.

## Ejemplo Aplicado a Tickets
Ver `ejemplo_serializer_avanzado.py` para código.

### Cómo integrarlo al proyecto:
1. En `src/ticket/serializers/ticket_serializer.py`, agrega:
   ```python
   extra_kwargs = {'description': {'write_only': True}}
   read_only_fields = ['id', 'created_at']
   def validate(self, attrs): ...  # Validación cross-field
   creator_username = SerializerMethodField()
   def get_creator_username(self, obj): return obj.created_by.username
   ```
2. Prueba: POST con description (no en JSON), GET con creator_username.

### Mejores Prácticas
- Usa `SerializerMethodField` para cálculos simples; para complejos, agrega al modelo.
- `read_only_fields` para campos auto-generados.
- Validaciones en `validate()` para lógica cross-field.

## Recursos
- [DRF Docs: Serializers](https://www.django-rest-framework.org/api-guide/serializers/)
- [Validation](https://www.django-rest-framework.org/api-guide/serializers/#validation)

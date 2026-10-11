<a id="contributing"></a>
# Contribuir

Harneloop está en alfa pública. Se agradecen incidencias y contribuciones específicas mientras se estabilizan la API pública y los formatos de las unidades de harness.

<a id="development-setup"></a>
## Entorno de desarrollo

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -e .
.\.venv\Scripts\python -m unittest discover -s tests
```

En macOS o Linux:

```bash
python3 -m venv .venv
./.venv/bin/python -m pip install -e .
./.venv/bin/python -m unittest discover -s tests
```

<a id="pull-requests"></a>
## Pull requests

Limita cada pull request a un comportamiento o una parte de la arquitectura.

Abre una incidencia antes de realizar trabajo arquitectónico importante para acordar el problema y su impacto en la compatibilidad. Incluye pruebas para los cambios del ciclo de vida y actualiza la documentación para agentes cuando cambie el comportamiento.

Por ahora, no solicites revisiones automáticas de CodeRabbit. Si creas un PR mientras CodeRabbit está configurado, añade la etiqueta o marca CodeRabbit-ignore del repositorio antes de solicitar una revisión.

<a id="standards"></a>
## Normas

- Mantén el núcleo del framework independiente de la familia de tareas.
- No añadas supuestos específicos de Blender a `src/harneloop`.
- Añade o actualiza pruebas del comportamiento del ciclo de vida.
- Mantén legibles los archivos para agentes en Markdown, YAML o JSON.
- No incluyas en commits secretos, artefactos locales de ejecución, entornos virtuales ni paquetes generados.

Al contribuir, aceptas que tu contribución se publique bajo la [Apache License 2.0](../../../LICENSE) del repositorio.

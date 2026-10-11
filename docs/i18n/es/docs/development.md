<a id="development"></a>
# Desarrollo

<a id="repository-layout"></a>
## Estructura del repositorio

```text
src/harneloop/      Python reference implementation
tests/           Unit and behavior tests
docs/            Architecture and development notes
schemas/         Language-neutral data contracts
.github/         CI and repository automation
```

<a id="local-verification"></a>
## Verificación local

Instala una vez el repositorio como herramienta editable a nivel de usuario:

```powershell
uv tool install --editable .
```

El comando `harneloop` seguirá disponible fuera del repositorio y reflejará los cambios del código fuente. Verifica con:

```powershell
uv run python -m compileall src tests
uv run python -m unittest discover -s tests
harneloop doctor
```

<a id="devops-baseline"></a>
## Base de DevOps

El repositorio debe mantener:

- código fuente organizado en `src/`;
- pruebas locales reproducibles;
- CI para las versiones de Python compatibles;
- ningún entorno virtual ni artefacto de ejecución versionado;
- documentación explícita de seguridad y contribución;
- esquemas independientes del lenguaje para los registros principales.

<a id="runtime-data"></a>
## Datos de ejecución

Las trazas de ejecución, artefactos copiados, registros de ejecuciones, planes de intentos y experimentos son datos de trabajo locales. No deben incorporarse a paquetes portátiles thin salvo que un perfil posterior los incluya explícitamente.

<a id="pr-review-note"></a>
## Nota sobre la revisión de PR

No hace falta revisión de CodeRabbit durante el prototipo inicial. Si creas un PR, añade la etiqueta o marca CodeRabbit-ignore configurada.

<a id="target-and-environment-onboarding"></a>
# Incorporación del objetivo y del entorno

Harneloop no debe asumir que es propietario del entorno de pruebas del usuario.

Tampoco debe sugerir que la CLI descubre automáticamente el entorno. Harneloop almacena la correspondencia. El agente debe inspeccionar espacio real, herramientas, servidores MCP, scripts, endpoints, carpetas de salida y rutas de artefactos, y registrar ese mapa en la unidad.

La comprensión de trabajo comienza en `operational-map.md`. Mantén actualizados objetivo de mejora, ejecución y restablecimiento habituales, artefactos útiles, supuestos frágiles y cuestiones por investigar. El mapa debe orientar, no imponer una única receta de evaluación.

Registra también capacidades ausentes. Las herramientas del agente operador son distintas de las de la unidad o entorno del agente objetivo. Un agente restringido puede carecer de terminal, navegador, archivos, MCP, gestor de paquetes, inspección visual, bases de datos o red. Si eso bloquea o debilita la construcción, registra qué falta, por qué importa, herramienta o dependencia útil y alternativa.

El framework debe ayudar primero al agente a entender:

- para qué tarea se construye el harness;
- qué se considera éxito;
- qué artefactos se deben capturar;
- qué patrones de fallo importan;
- si ya existe un entorno de pruebas.

Después crea un plan de intento. No es un comando determinista: es un flujo diseñado por el agente para producir e inspeccionar algo relevante a la tarea objetivo.

<a id="setup-modes"></a>
## Modos de preparación

<a id="existing"></a>
### Existente

Úsalo si el usuario ya tiene un entorno funcional.

Ejemplo: un proyecto Blender ya tiene scripts para ejecutar escenas, capturar pantallas y exportar logs.

El agente debe conectarlo documentando:

- el comando de ejecución;
- las rutas de salida de artefactos;
- capturas, renders, logs o resúmenes estructurados por recopilar;
- cualquier nota específica del entorno.

No reconstruyas el entorno salvo que fallen comprobaciones o lo pida el usuario.

Elimina trabajo manual repetitivo. Si reiniciar servicios, restablecer apps, recoger artefactos o preparar el entorno puede automatizarse con seguridad, impleméntalo o documéntalo. Si resulta arriesgado, incierto o caro, pregunta.

Toda capacidad nueva debe estar respaldada por evidencia. Las herramientas locales de bajo riesgo pueden instalarse, activarse o crearse si se permite. Primero propón dependencias grandes, credenciales, APIs de pago, acceso externo, cuentas del usuario, ampliaciones de red o cambios de seguridad.

La preparación gestionada o asistida no exige construir todo desde cero. Busca en el proyecto y, si ayuda, documentación externa, herramientas abiertas, skills, bibliotecas, validadores, datasets, ejemplos y trabajo previo. Prefiere soluciones mantenidas si mejoran resultados esperados o evitan trabajo innecesario. Registra fuente, versión, propósito, licencia o atribución, compatibilidad y contribución medida. Revisa material ejecutable externo y respeta los permisos habituales sobre riesgo, coste, credenciales, acceso y seguridad.

Los entornos existentes pueden basarse en comandos o herramientas.

Basado en comandos significa disponer de un comando directo. Basado en herramientas significa que el agente actúa mediante MCP, automatización de navegador, plugins de diseño o API de un complemento Blender.

<a id="assisted"></a>
### Asistida

Úsalo si parte del entorno existe pero hay que identificar piezas ausentes.

Propón la mínima preparación que falte para probar una línea base y capturar artefactos.

<a id="managed"></a>
### Gestionada

Úsalo si Harneloop o el agente deben crear más partes del entorno desde cero.

Los cambios de infraestructura deben ser explícitos y respaldados. La preparación gestionada puede ser útil más adelante, pero no debe ser el valor predeterminado para proyectos que ya funcionan.

<a id="attempt-plans"></a>
## Planes de intento

Muchas tareas no se reducen a `run this command`.

El agente objetivo puede necesitar:

- usar herramientas MCP;
- editar archivos;
- crear escenas;
- construir interfaces;
- ejecutar un navegador;
- pedir a un modelo que genere un artefacto;
- inspeccionar visualmente la salida;
- exportar resúmenes estructurados;
- decidir qué evidencia posterior importa.

Harneloop lo registra como un plan de intento:

```powershell
harneloop attempt plan .\unit `
  --goal "Build a Blender scene with a cube on a table." `
  --method "Use Blender MCP tools to create objects, render, and export scene summary." `
  --action "Create table, cube, camera, and light." `
  --action "Render and capture screenshot." `
  --expected-artifact render `
  --expected-artifact scene_summary `
  --success-check "Cube rests on table." `
  --success-check "Objects are visible to camera."
```

Después una ejecución puede referirse al intento:

```powershell
harneloop run start .\unit --task "Baseline Blender spatial scene" --attempt-id attempt-0001
```

Una vez capturados los artefactos, añade observaciones:

```powershell
harneloop attempt observe .\unit attempt-0001 `
  --run-id run-0001 `
  --outcome failed `
  --summary "Render exists but cube floats above the table." `
  --finding "Likely z-coordinate placement issue."
```

Las observaciones pueden convertirse en evidencia candidata o casos de regresión.

<a id="agent-questions"></a>
## Preguntas del agente

Al empezar un harness real, pregunta solo por información ausente:

- ¿Cuál es la familia de tareas objetivo?
- ¿Qué artefactos de salida importan?
- ¿Ya tienes un entorno de pruebas funcional?
- ¿El entorno se basa en comandos, herramientas, pasos manuales o es personalizado?
- Si usa comandos: ¿cuál ejecuta la prueba o tarea?
- Si usa herramientas: ¿cuáles usa el agente?
- ¿Dónde se guardan capturas, renders, logs o resúmenes estructurados?
- ¿Qué fallos habituales deben convertirse en regresiones?

<a id="blender-case"></a>
## Caso Blender

Para el proyecto Blender existente, el modo probable es `existing`.

El modo de interacción puede ser `mcp`, no `command`.

Puede no haber un comando de pruebas directo. El agente objetivo usa Blender MCP y herramientas del complemento para cambiar escenas, renderizar imágenes, capturar pantallas, inspeccionar objetos o exportar resúmenes.

El primer paso no es instalar Blender ni crear un ejecutor nuevo, sino conectar Harneloop a:

- la interfaz MCP o herramientas existente;
- las herramientas que debe usar el agente;
- las rutas de renders, capturas, logs y resúmenes de escena;
- el flujo de línea base para crear escenas y capturar artefactos.

Ejemplo:

```powershell
harneloop environment connect .\blender-unit `
  --name "Existing Blender MCP environment" `
  --mode existing `
  --interaction-mode mcp `
  --description "Agent interacts with Blender through an MCP server and addon tools." `
  --tool create_object `
  --tool render_scene `
  --tool capture_screenshot `
  --tool export_scene_summary `
  --artifact-path "outputs/renders/*.png" `
  --note "Use MCP tools instead of looking for a single run command."
```

Después, Harneloop registra ejecuciones, captura artefactos, guarda evidencia y promueve cambios. El servidor Blender MCP sigue siendo la interfaz de ejecución.

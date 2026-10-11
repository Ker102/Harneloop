<a id="agent-onboarding"></a>
# Incorporación de agentes

Un agente con solo el repositorio y la tarea del usuario debe poder comprender Harneloop. El primer paso no es escribir un validador ni asumir un comando de pruebas: es recopilar contexto suficiente para crear un intento de línea base.

Para una configuración guiada para personas, ejecuta:

```powershell
harneloop setup
```

Para una lista legible por agentes, ejecuta:

```powershell
harneloop onboard
```

o, desde un clon antes de instalar la herramienta de forma persistente:

```powershell
uv run harneloop onboard
```

Para salida legible por máquinas:

```powershell
harneloop onboard --format json
```

Para una unidad creada con una versión anterior, ejecuta `harneloop upgrade-unit <unit>` una vez. Añade archivos de protocolo ausentes sin sustituir el material existente del harness.

<a id="minimal-user-questions"></a>
## Preguntas mínimas al usuario

Úsalas como campos de contexto, no como cuestionario obligatorio. El agente puede crear primero la unidad provisional e inspeccionar el espacio y después preguntar solo lo que siga importando:

1. ¿En qué debe ayudar este harness a mejorar al agente?
2. ¿Dónde se usará: flujo de agente de código, agente de aplicación, investigación o automatización interna?
3. ¿Cómo se gestionan los criterios de éxito?
4. ¿Cómo se validan los resultados?
5. ¿El entorno de pruebas existe, existe en parte, hay que construirlo o aún no está claro?

No conviertas la incorporación en un formulario largo. Los criterios de éxito y artefactos son opciones guiadas, no conocimientos exigidos al usuario. Tras inspeccionar, ejecuta `harneloop intake status <unit>` y clasifica el contexto importante como confirmado, delegado, inferido, desconocido o no aplicable. Nunca conviertas silenciosamente una inferencia en un hecho confirmado.

Antes de la primera ejecución real, resuelve los campos relevantes y registra confirmación o delegación explícita con `harneloop intake acknowledge`. Si una referencia, proyecto, credencial o juicio ausente puede cambiar sustancialmente la prueba, solicítalo directamente o entra en espera; no te limites a mencionarlo después de preparar el entorno.

Harneloop registra el mapa del entorno; no descubre por sí solo endpoints, herramientas MCP, comandos, capturas, renders ni rutas de artefactos. El agente de incorporación debe inspeccionar el proyecto y entorno reales, determinar cómo se producen artefactos y registrar esa correspondencia.

Toda unidad nueva tiene `operational-map.md`. Úsalo como orientación actual: objetivo de mejora, sistemas y herramientas, artefactos y evidencia útiles, ejecución y restablecimiento habituales, restricciones, puntos frágiles, preguntas abiertas, supuestos por revisar y ubicación de ejecuciones o evidencia previas. Actualízalo cuando cambien flujo, necesidades de evidencia, supuestos del entorno o automatización.

El mapa es contexto y navegación, no un procedimiento rígido. El agente debe seguir razonando sobre la tarea, inspeccionar evidencia y elegir la prueba o evaluación adecuada al intento actual.

<a id="capability-gaps"></a>
## Capacidades ausentes

No asumas que todo agente operador tiene capacidades de Codex. Un Hermes, OpenClaw, agente de app o trabajador restringido puede carecer de terminal, archivos, navegador, gestores de paquetes, servidores MCP, inspección visual, bases de datos u otras capacidades necesarias.

Separa dos capas:

- Capacidades del agente operador: lo que realmente puede usar al construir la unidad.
- Herramientas de la unidad o agente objetivo: las diseñadas en la unidad o proporcionadas mediante el contrato del entorno.

Si falta una capacidad útil, regístrala en `operational-map.md`: qué falta, por qué importa, herramienta o dependencia útil, cambios de riesgo, coste, autenticación o seguridad y alternativa si el usuario rechaza.

Las capacidades locales de bajo riesgo pueden instalarse, activarse o crearse si el entorno lo permite. Antes hay que proponer dependencias grandes, credenciales, APIs de pago, cuentas del usuario, acceso externo, ampliación de red o cambios de seguridad.

Justifica capacidades nuevas por obstáculos observados, intentos fallidos, artefactos ausentes o mejora esperada clara; no las añadas por especulación.

<a id="reuse-existing-work"></a>
## Reutilizar trabajo existente

La meta es el mejor harness verificado, no implementarlo desde cero. Antes de crear una capacidad ausente, inspecciona herramientas del proyecto, bibliotecas abiertas, skills, servidores MCP, validadores, datasets, ejemplos, documentación, investigación y material reutilizable. Puedes instalar, adaptar, combinar o aprender de trabajo adecuado si mejora resultados o evita esfuerzo innecesario.

No reutilices a ciegas. Registra fuente, versión o revisión pertinente, propósito, licencia o atribución, compatibilidad y evidencia de valor. Revisa material ejecutable externo antes de confiar. Pregunta primero si añade credenciales, pagos, acceso externo, descargas importantes, licencias restrictivas, ejecución sensible o cambios relevantes del entorno. Si una solución no sirve, documenta por qué antes de sustituirla.

Respuestas sugeridas sobre éxito:

- Que el agente proponga criterios de éxito.
- Sé exactamente cómo es el resultado exitoso.
- Decidir después del primer intento de línea base.

Respuestas sugeridas sobre validación:

- Máxima calidad de validación.
- Validación visual o centrada en artefactos.
- Validación equilibrada.
- Validación eficiente en recursos.
- Que el agente decida por tarea.

Seguimiento opcional:

- ¿Hay restricciones, zonas protegidas, revisiones humanas o límites de coste o tiempo que el harness deba respetar?

<a id="how-answers-map-into-harneloop"></a>
## Cómo se reflejan las respuestas en Harneloop

- Objetivo, estrategia de éxito, preferencia de validación y artefactos sugeridos forman un resumen objetivo: `harneloop target set`.
- El mapa actual de trabajo se registra y revisa en `operational-map.md`.
- Comandos, servidores MCP, pasos manuales o herramientas personalizados forman un contrato del entorno: `harneloop environment connect`.
- El primer flujo real forma un plan de intento: `harneloop attempt plan`.
- Las salidas producidas se convierten en artefactos de ejecución: `harneloop run start`, `harneloop artifact add`, `harneloop run finish`.
- La calidad del resultado y siguiente decisión se registran con `harneloop attempt conclude`.
- Los cambios del harness son candidatos y requieren evidencia antes de promoverse.
- Los valores del usuario se gestionan con `harneloop settings`.
- Las unidades locales se listan o registran con `harneloop units`. Una vez registradas, su ID o nombre sirve desde cualquier directorio.

<a id="important-behavior"></a>
## Comportamiento importante

No toda tarea necesita un comando de pruebas directo. En entornos con herramientas, como Blender MCP o renderizado SVG por agentes, declara herramientas y artefactos en el contrato. El agente escribe un plan para usarlas, producir e inspeccionar artefactos y convertir observaciones en evidencia.

Busca ciclos repetidos sin exigir reinicios manuales de apps, reinstalación de complementos, restablecer servicios o recoger archivos. Si automatizar es razonable, hazlo o documéntalo. Si es arriesgado, incierto o demasiado caro o lento, pregunta antes.

Si se retrasa un artefacto o juicio humano necesario, usa `harneloop state wait`. Si la unidad parece llegar a su límite de capacidades, usa `harneloop state stop` con un motivo concreto y siguiente acción.

Finalizar registra el estado de ejecución, no prueba calidad. Inspecciona artefactos y concluye cada intento con una decisión: aceptar el harness, crear candidato, repetir con plan corregido, pedir información o detenerse. Un buen primer resultado puede aceptarse sin candidato. La evidencia esperada ausente no permite un aprobado sin reservas.

Al entrar o reanudar una unidad, ejecuta `harneloop brief <unit>`. El resumen generado se limita a esa unidad; no afecta a trabajo ajeno de la misma sesión.

<a id="candidate-batching-and-parallel-work"></a>
## Agrupación de candidatos y trabajo paralelo

Un candidato es una hipótesis coherente, no cada edición o commit. Agrupa cambios relacionados de entorno, herramientas, instrucciones o validadores si deben juzgarse juntos. Mantén problemas independientes en candidatos separados; pueden quedar varios abiertos.

Clasifica cada candidato por impacto:

- `target_harness`: cambia lo que recibe o puede hacer el agente objetivo;
- `evaluation`: cambia cómo se observan o juzgan las salidas;
- `infrastructure`: cambia configuración, ejecución, restablecimiento o captura de artefactos;
- `mixed`: solo cuando separar la cuestión le haga perder sentido.

Elige validación proporcional al riesgo de fallo:

- `structural`: análisis, esquemas, comprobaciones estáticas e integridad de metadatos;
- `targeted`: pruebas de humo dirigidas a una herramienta, evaluador o ruta de infraestructura;
- `representative`: intentos reales y regresiones pertinentes para cambios de comportamiento;
- `full`: suites amplias para cambios de gran impacto y controles de versión.

No repitas todo el benchmark tras cada edición de configuración. Acumula el candidato hasta que sea coherente, márcalo `ready` y recopila evidencia del nivel declarado. Separa candidatos de harness objetivo y evaluación si es posible, para que el evaluador modificado no sea el único juez del harness modificado.

Las versiones promovidas siguen una línea. Si un candidato se promueve y otros comparten su base antigua, Harneloop los marca `needs_rebase`. Reconcílialos y haz rebase, luego reúne evidencia nueva contra la base nueva; la anterior sigue como procedencia.

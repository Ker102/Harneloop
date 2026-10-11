<div align="center">

<h1><img src="../../assets/harneloop-mark.svg" alt="" width="56" height="56" align="absmiddle" /> Harneloop</h1>

<p>Evolución del harness para agentes de IA basada en artefactos.</p>

<p><a href="https://harneloop.kaelux.dev/">Sitio web</a> · <a href="#agent-quick-start">Inicio rápido</a> · <a href="#documentation">Documentación</a></p>

</div>

<!-- i18n-switcher:start -->
[English](../../../README.md) | Español | [简体中文](../zh-CN/README.md) | [Français](../fr/README.md) | [日本語](../ja/README.md) | [Deutsch](../de/README.md) | [Português (Brasil)](../pt-BR/README.md)
<!-- i18n-switcher:end -->

**Ayuda a un agente de IA a aprender de lo que salió mal.**

Un agente puede terminar una tarea, afirmar que tuvo éxito y aun así dejar código roto, un render deficiente o un flujo que no funciona. Harneloop da a tu agente actual una forma estructurada de inspeccionar el resultado, revisar sus acciones, localizar el error probable y probar un enfoque mejor.

El agente mejora su **harness**: las instrucciones, herramientas, contexto y comprobaciones alrededor del modelo. No hace falta reentrenar el modelo. Un cambio propuesto solo pasa a ser la versión de trabajo cuando una prueba lo respalda.

<a id="what-can-you-use-it-for"></a>
## ¿Para qué puedes usarlo?

Usa Harneloop cuando un agente repita errores similares y puedas inspeccionar sus resultados. Sirve para código y pruebas, flujos de navegador, documentos generados y tareas visuales. El primer estudio de caso publicado es la construcción de escenas Blender con ViperMesh; otras familias de tareas siguen abiertas a pruebas y contribuciones.

<a id="how-it-works"></a>
## Cómo funciona

1. **Intenta la tarea.** Guarda el resultado y los pasos del agente.
2. **Inspecciona el resultado.** Comprueba el artefacto, no solo el mensaje de finalización.
3. **Revisa lo ocurrido.** Relaciona el problema con una llamada a herramienta, contexto ausente, instrucción o decisión del entorno.
4. **Prueba una mejora.** Deja que el agente proponga un cambio y repita las comprobaciones pertinentes.
5. **Conserva lo que funciona.** Guarda las mejoras respaldadas y una versión restaurable.

<p align="center">
  <a href="https://harneloop.kaelux.dev/media/harneloop-how-it-works.mp4">
    <img src="https://harneloop.kaelux.dev/media/harneloop-video-poster.png" alt="Mira cómo funciona Harneloop: de un objetivo a un harness reutilizable" width="900" />
  </a>
</p>

<p align="center"><a href="https://harneloop.kaelux.dev/media/harneloop-how-it-works.mp4"><img src="../../assets/readme-play.svg" alt="" width="18" height="18" align="absmiddle" /> Mira cómo funciona Harneloop - 3:40</a></p>

Cada familia de tareas tiene una **unidad de harness**: un espacio portátil que reúne objetivo, herramientas, intentos, evidencia y mejoras. Puedes pausarlo y continuar después sin reiniciar la investigación.

<a id="try-harneloop"></a>
## Prueba Harneloop

[Instala desde PyPI](https://pypi.org/project/harneloop/) en un entorno de herramientas aislado:

```bash
uv tool install harneloop
harneloop setup
```

O usa `python -m pip install harneloop` en tu entorno Python. Consulta [Instalar y empezar](#install-and-start) para ver requisitos e instalación desde el código fuente.

Después da a un agente capaz el enlace del repositorio y la tarea que quieras mejorar. El [Inicio rápido para agentes](#agent-quick-start) incluye un prompt listo para usar.

**Estado:** Alfa pública. El ciclo principal funciona; se agradecen validaciones de más tareas y contribuciones. [Informa de un problema o comparte un caso de uso](https://github.com/Ker102/Harneloop/issues).

<a id="evidence-from-a-real-case-study"></a>
## Evidencia de un caso real

Harneloop se usó para desarrollar la unidad personalizada ViperMesh para tareas de razonamiento espacial y construcción de escenas Blender. La comparación mantuvo fijo el modelo ejecutor en **GPT-5.5 High** y probó el harness ViperMesh evolucionado frente a la **línea base del servidor Anthropic x Blender MCP**, aislando el harness como la principal capa modificada.

- ViperMesh fue más rápido en **6 de 7** tareas en vivo comparables, con una **aceleración media de 2.534x**.
- La evaluación visual preliminar por un LLM neutral mejoró **8.19 puntos** en siete pares de renders reales.
- El uso total de tokens del agente ejecutor fue **90.91% menor** en siete benchmarks comparables: unos **175K frente a 1.9M tokens** en total.

Harneloop no generó las escenas. Estructuró el ciclo de evidencia y artefactos que reveló debilidades, guio el desarrollo de herramientas y harness y verificó si los cambios mejoraban el benchmark. Consulta metodología, limitaciones y resultados completos en el [estudio de caso ViperMesh](https://kristoferjussmann.me/case-studies/vipermesh).

Los resultados aportan evidencia empírica directa de que el proceso de Harneloop funciona en un entorno real de agentes con muchos artefactos: el modelo ejecutor no cambió y el harness evolucionado obtuvo mejoras medibles de velocidad, calidad visual y eficiencia de tokens.

<a id="demonstration-vipermesh-mcp"></a>
### Demostración: ViperMesh MCP

[Mira la demostración de Harneloop con ViperMesh MCP](https://www.youtube.com/watch?v=bs74QJ6UD5E&t=2s).

La construcción de escenas Blender es un caso concreto para inspeccionar resultados y mejorar las herramientas e instrucciones del agente. Consulta el [estudio Harneloop](https://kristoferjussmann.me/case-studies/harneloop/#harneloop-demo) para el framework y el [estudio de benchmarks ViperMesh](https://kristoferjussmann.me/case-studies/vipermesh/) para los resultados medidos. El [conector público Blender](https://github.com/Ker102/vipermesh-blender) está disponible por separado del entorno de estudio completo y del harness evaluado.

<a id="start-here"></a>
## Empieza aquí

- **Uso mediante un agente:** [Inicio rápido para agentes](#agent-quick-start)
- **Instalación por tu cuenta:** [Instalar y empezar](#install-and-start)
- **Comprender las unidades:** [¿Qué es una unidad de harness?](#what-is-a-harness-unit)
- **Comprender el ciclo:** [El ciclo de vida simplificado](#the-lifecycle-made-simple)
- **Pruebas medidas:** [Estudio de caso ViperMesh](https://kristoferjussmann.me/case-studies/vipermesh)
- **Conectar un entorno real:** [Configuración del entorno](#environment-setup)
- **Cambiar valores predeterminados:** [Configuración](#configuration)
- **Arquitectura técnica:** [Ciclo principal](docs/architecture/core-lifecycle.md), [capas de ejecución](docs/architecture/runtime-layers.md) y [concurrencia](docs/architecture/concurrency.md)
- **Instrucciones completas para agentes:** [Incorporación de agentes](docs/agent-onboarding.md)
- **Proceso visual:** [Cómo funciona](#how-it-works), [diagrama compacto editable](docs/framework-process-compact.md) y [diagrama detallado](docs/framework-process.md)

<a id="why-harneloop-exists"></a>
## Por qué existe Harneloop

Los modelos repiten fallos porque las lecciones útiles de un intento nunca se convierten en una parte probada de su entorno de trabajo. Un prompt más largo o una puntuación de evaluación no resuelven todo el problema.

El modelo es solo una parte del rendimiento de un agente. Su harness determina el contexto que ve, las herramientas disponibles, cómo interactúa con el entorno, qué recuerda, cómo se inspeccionan resultados y si los errores se convierten en mejoras duraderas. En muchos problemas específicos, el harness es la superficie de mejora de mayor impacto: puede producir grandes avances sin reentrenar el modelo y cada cambio sigue siendo inspeccionable, comprobable, reversible y portátil.

Harneloop estructura ese trabajo y lo hace eficiente. En vez de acumular ediciones aisladas de prompts, permite desarrollar varias unidades independientes, probar cambios mediante intentos reales, conservar evidencia e historial y continuar o exportar cada harness exitoso como un paquete coherente.

Harneloop ofrece al agente operador un ciclo controlado de mejora:

- trabajar en la tarea real, no solo en un benchmark sintético;
- capturar renders, capturas de pantalla, archivos, trazas, logs, estado estructurado u otros artefactos;
- inspeccionar artefactos visual, estructural o conductualmente;
- rastrear resultados débiles hasta instrucciones, herramientas, contexto, recuperación, entorno o límites del modelo;
- desarrollar mejoras como cambios candidatos aislados;
- probar candidatos con nuevos intentos y casos de regresión;
- promover solo cambios respaldados por evidencia válida;
- conservar versiones restaurables y empaquetar el harness resultante para reutilizarlo.

El agente puede razonar y experimentar libremente dentro del espacio del harness. Harneloop controla los límites sensibles a la integridad: registros, estado protegido, evidencia, promoción, instantáneas, reversión y empaquetado.

<details>
<summary>Contexto de investigación: ¿por qué mejorar el harness antes que los pesos?</summary>

<a id="why-improve-the-harness-before-the-weights"></a>
### ¿Por qué mejorar el harness antes que los pesos?

La investigación sobre interfaces de agentes, recuperación, herramientas y feedback iterativo muestra que cambiar el sistema alrededor del modelo puede mejorar notablemente su rendimiento sin modificar sus pesos. Cuando los principales obstáculos son contexto, recuperación, herramientas, feedback o interacción con el entorno, los métodos de harness pueden superar el ajuste fino, a veces ampliamente, conservando las capacidades generales del modelo. Harneloop nació de problemas prácticos al construir harnesses; estos trabajos respaldan de forma independiente su enfoque centrado en el harness:

- [Self-Harness](https://arxiv.org/abs/2606.09498) encontró que los agentes podían extraer debilidades de trazas, proponer cambios del harness, validarlos mediante regresiones y mejorar tasas de aprobación en pruebas reservadas en tres familias de modelos.
- [SWE-agent](https://arxiv.org/abs/2405.15793) mostró que una interfaz agente-ordenador diseñada para el propósito mejoraba sustancialmente la navegación de repositorios, edición de código y ejecución de pruebas por modelos de lenguaje.
- [Reflexion](https://arxiv.org/abs/2303.11366) mejoró agentes mediante ensayo y error, feedback lingüístico y memoria episódica, no mediante actualizaciones de pesos.
- [Self-Refine](https://arxiv.org/abs/2303.17651) informó de una mejora absoluta media de unos 20 puntos porcentuales en siete tareas evaluadas mediante feedback y refinamiento iterativos sin entrenamiento adicional.
- [Fine-Tuning or Retrieval?](https://aclanthology.org/2024.emnlp-main.15/) encontró que RAG superaba sistemáticamente al ajuste fino no supervisado en las tareas de incorporación de conocimiento evaluadas, tanto existente como nuevo.
- [Does Fine-Tuning LLMs on New Knowledge Encourage Hallucinations?](https://arxiv.org/abs/2405.05904) encontró dificultades para adquirir hechos nuevos mediante ajuste fino supervisado y mayor tendencia a alucinar conforme se aprendía ese conocimiento.

Junto con ViperMesh, esto respalda una estrategia práctica: **optimiza primero el harness, mide el resultado y modifica los pesos solo cuando la evidencia muestre que el harness llegó a su límite útil.** Sus cambios son más rápidos de inspeccionar, revertir, reutilizar y validar, y en tareas aplicables pueden lograr mejoras mayores que modificar los pesos sin cambiar permanentemente el modelo base.

Esto no demuestra que un harness siempre supere cualquier método de ajuste fino. Este sigue siendo útil para comportamiento, estilo, latencia, representaciones especializadas o capacidades difíciles de aportar durante la inferencia. Un harness sólido y un ajuste fino bien elegido también pueden complementarse.

</details>

<a id="what-is-a-harness-unit"></a>
## ¿Qué es una unidad de harness?

Una **unidad de harness** es un espacio portátil para mejorar una familia de tareas. Cada unidad evoluciona de manera independiente y conserva definición del objetivo, mapa del entorno, material del harness, experimentos, evidencia, regresiones y versiones promovidas.

Una unidad nueva comienza con esta estructura:

```text
my-harness-unit/
  unit.yaml                 identity and current version
  UNIT_AGENT.md             instructions for agents entering the unit
  operational-map.md        current understanding of tools, artifacts, and workflow
  target/                   task goal and suggested first tests
  environment/              contract for commands, MCP tools, apps, and artifact paths
  agent-facing/             promoted instructions and context
  tools/                    unit-specific helper tools
  observers/                ways to inspect outputs
  validators/               deterministic or agent-driven checks
  regression-cases/         failures that future candidates should not repeat
  candidates/               isolated proposed harness changes
  runtime/                  local runs and captured artifacts
  versions/                 restorable promoted snapshots
  provenance/               human-readable change history
```

No es una plantilla restrictiva. Los agentes pueden añadir investigación, scripts, datos de recuperación, declaraciones de infraestructura, memoria, observadores personalizados o carpetas nuevas. El framework solo protege los archivos y reglas de ciclo de vida necesarios para entender y recuperar la unidad.

<a id="portable-unit-versus-local-working-data"></a>
### Unidad portátil frente a datos de trabajo locales

El material reutilizable pertenece a la unidad portátil. No así las trazas brutas, experimentos temporales, cachés, secretos, candidatos no promovidos y todos los renders históricos.

El paquete `thin` predeterminado contiene conocimiento promovido y contratos para reconstruir o integrar el harness. La evidencia de ejecución permanece local salvo que un perfil futuro la incluya explícitamente.

<a id="the-lifecycle-made-simple"></a>
## El ciclo de vida simplificado

1. **Describe el objetivo.** El usuario explica qué debe mejorar el agente.
2. **Mapea el entorno.** El agente operador descubre cómo se realiza la tarea real y de dónde sale la evidencia útil.
3. **Reconciliar supuestos.** Antes de la primera ejecución real, el contexto importante se confirma, delega o marca claramente como inferido.
4. **Ejecuta una línea base.** El agente intenta la tarea antes de cambiar el harness.
5. **Inspecciona y concluye.** Evalúa artefactos y acepta, cambia, repite, pide información o se detiene explícitamente.
6. **Crea o amplía candidatos cuando haga falta.** Los cambios relacionados se acumulan en lotes coherentes aislados; los problemas independientes pueden tener candidatos paralelos.
7. **Valida según el riesgo.** Usa comprobaciones estructurales, dirigidas, representativas o completas y adjunta evidencia.
8. **Promueve, revisa, espera o detente.** Las mejoras respaldadas se convierten en una versión. Los candidatos débiles se revisan o rechazan.
9. **Exporta o empaqueta.** El harness promovido puede aplicarse a un agente de código, de aplicaciones u otro entorno compatible.

Las ejecuciones terminadas son inmutables. La evidencia candidata se comprueba al adjuntarla y de nuevo al promoverla, por lo que ejecuciones borradas, artefactos ausentes o archivos de evidencia faltantes no pueden respaldar una versión.

No hay que crear un candidato por commit. Un candidato de configuración o herramientas puede reunir cambios relacionados y recibir una prueba de humo específica; uno que cambie el comportamiento puede requerir intentos con artefactos reales y regresiones. Los cambios del harness objetivo, evaluación e infraestructura pueden avanzar de forma independiente. Si se promueve uno, los candidatos paralelos con la base anterior deben hacer rebase y aportar evidencia nueva antes de promoverse.

El vídeo al principio explica el ciclo. El [documento compacto](docs/framework-process-compact.md) contiene un diagrama Mermaid editable. El [diagrama detallado](docs/framework-process.md) cubre capacidades ausentes, aportación humana, espera, parada y el ciclo completo basado en artefactos.

<a id="what-makes-it-different"></a>
## ¿Qué lo diferencia?

<a id="artifact-aware"></a>
### <img src="../../assets/readme-observe.svg" alt="" width="18" height="18" align="absmiddle" /> Basado en artefactos

Harneloop trata lo producido como evidencia. El agente puede inspeccionar imágenes, escenas, interfaces, documentos, repositorios generados, trazas, estado de bases de datos o cualquier salida útil, en vez de confiar en su propio informe textual.

<a id="harness-building-not-only-scoring"></a>
### <img src="../../assets/readme-improve.svg" alt="" width="18" height="18" align="absmiddle" /> Construir harnesses, no solo puntuar

El fin no es solo informar de que un agente falló. El agente operador diagnostica el fallo y desarrolla un cambio concreto que puede incluir prompts, principios, ejemplos, recuperación, herramientas, observadores, validadores, regresiones o automatización del entorno.

<a id="evidence-gated-self-improvement"></a>
### <img src="../../assets/readme-verify.svg" alt="" width="18" height="18" align="absmiddle" /> Automejora condicionada por evidencia

El agente activo no puede reescribir libremente el harness promovido. Crea un candidato, lo prueba, adjunta evidencia y lo promueve mediante el framework. Cada versión promovida es inspeccionable y restaurable.

<a id="environment-agnostic"></a>
### Independiente del entorno

El núcleo no depende de Blender, SVG, agentes Python ni de un proveedor de modelos específico. Una unidad puede usar comandos de terminal, servidores MCP, automatización de navegador, apps de escritorio, APIs, pasos manuales o una interfaz personalizada.

<a id="reasoning-remains-open-ended"></a>
### El razonamiento sigue abierto

Harneloop estructura el ciclo sin convertir al agente operador en un script fijo. El agente sigue eligiendo pruebas, artefactos, estrategia de evaluación, herramientas y punto de parada apropiados.

<a id="agent-quick-start"></a>
## Inicio rápido para agentes

Harneloop está diseñado para usarse principalmente conversando con un agente con acceso a archivos y terminal.

Dale el repositorio y un prompt como este:

```text
Read this repository's README.md and docs/agent-onboarding.md.
Use Harneloop to create a harness unit that improves an agent at: [describe the task].

Inspect my existing environment before deciding how to test it. Ask only for context
that can materially change the work, and do not silently treat assumptions as confirmed.
Run a baseline, inspect its artifacts, and conclude the attempt before deciding whether
a candidate is needed. Do not promote a candidate without evidence.
```

El agente debe entonces:

1. Instalar Harneloop si hace falta y ejecutar `harneloop doctor`.
2. Leer `harneloop onboard --format json` o [la guía de incorporación](docs/agent-onboarding.md).
3. Crear o continuar una unidad provisional e inspeccionar el entorno real.
4. Reconciliar el contexto confirmado, delegado, inferido y desconocido mediante el control de recopilación adaptativa.
5. Actualizar `operational-map.md` con la comprensión actual.
6. Ejecutar la línea base e inspeccionar los artefactos resultantes.
7. Concluir el intento antes de aceptar el harness actual o proponer mejoras.

<a id="instructions-for-agents-reading-this-repository"></a>
### Instrucciones para agentes que lean este repositorio

Si eres el agente operador:

- No asumas que toda tarea tiene un comando de pruebas.
- No asumas que Harneloop descubre por ti endpoints, herramientas, capturas o rutas de artefactos.
- Ejecuta `harneloop brief <unit>` y lee `AGENTS.md`, `UNIT_AGENT.md` y `operational-map.md` al entrar en una unidad o recuperar el contexto.
- Aplica el resumen de la unidad solo mientras trabajes en ella; el trabajo ajeno queda fuera.
- Usa `harneloop intake status` para mostrar solo preguntas pendientes que puedan cambiar sustancialmente el trabajo.
- Usa `harneloop candidate list <unit>` para recuperar todo el trabajo abierto; una unidad puede tener varios candidatos activos.
- Agrupa cambios relacionados en candidatos coherentes y ajusta la validación al impacto en lugar de ejecutar todo el benchmark tras cada edición de configuración.
- Separa los cambios del evaluador y del harness objetivo cuando sea posible para mantener la evidencia fiable.
- Inspecciona el entorno real y documéntalo en `target/` y `environment/`.
- Prefiere inspeccionar artefactos reales si las comprobaciones deterministas no bastan para establecer calidad.
- Separa tus capacidades de las herramientas diseñadas para el agente objetivo.
- Busca el mejor resultado verificado, no reconstruirlo todo: investiga y reutiliza herramientas, skills, bibliotecas, ejemplos y trabajo previo adecuados; registra procedencia y respeta licencias, seguridad, costes y permisos.
- Pon los cambios propuestos en un espacio candidato.
- Usa comandos Harneloop para ejecuciones, artefactos, evidencia, promoción, reversión, espera, parada y reanudación.
- Pregunta antes de añadir credenciales, servicios de pago, acceso externo, herramientas sensibles a la seguridad o infraestructura cara.
- Actualiza el mapa operativo cuando cambien supuestos, rutas de artefactos, herramientas o automatización.
- Nunca te detengas al terminar la ejecución: inspecciona artefactos y registra una decisión explícita con `harneloop attempt conclude`.

La incorporación legible por máquinas está disponible con:

```bash
harneloop onboard --format json
```

<a id="install-and-start"></a>
## Instalar y empezar

Harneloop está [publicado en PyPI](https://pypi.org/project/harneloop/). Instálalo como herramienta aislada mediante [uv](https://docs.astral.sh/uv/getting-started/installation/) o usa `python -m pip install harneloop` en tu entorno Python. El comando `harneloop` está diseñado para Windows, macOS y Linux.

```bash
uv tool install harneloop
harneloop doctor
harneloop setup
```

Para una compilación del código fuente no publicada, usa `uv tool install git+https://github.com/Ker102/Harneloop.git`.

Si `uv` indica que su directorio de herramientas no está en `PATH`, ejecuta `uv tool update-shell` y abre otro terminal. Quienes contribuyan desde un clon pueden instalar el checkout activo con `uv tool install --editable .`; consulta [el entorno de desarrollo](docs/development.md).

`harneloop setup` abre la CLI guiada para personas. Ejecutar `harneloop` sin un comando abre el menú interactivo más amplio en un terminal. Los agentes pueden usar directamente comandos explícitos no interactivos.

Primeros comandos útiles:

```bash
harneloop onboard
harneloop template list
harneloop units list
harneloop settings show
```

Las unidades creadas mediante `harneloop setup` o `harneloop init-unit` se registran automáticamente. Las existentes pueden añadirse una vez con:

```bash
harneloop units register /path/to/my-unit
```

Tras registrarla, usa su ID o nombre desde cualquier directorio en lugar de una ruta relativa:

```bash
harneloop units list
harneloop status my-unit --format markdown
harneloop environment status my-unit
```

<a id="what-the-agent-asks-you"></a>
## Qué te pregunta el agente

La incorporación de nuevas unidades es breve a propósito. El agente debe recopilar cinco datos:

1. ¿En qué debe ayudar este harness a mejorar al agente?
2. ¿Dónde se usará el harness?
3. ¿Defines tú el éxito, lo propone el agente o se decide después de la línea base?
4. ¿La validación prioriza calidad, evidencia visual, equilibrio o eficiencia de recursos?
5. ¿El entorno de pruebas existe, existe en parte o hay que construirlo?

No necesitas conocer de antemano las pruebas o artefactos perfectos. Cuando corresponda, el agente debe proponerlos tras inspeccionar la tarea y el entorno. Solo preguntará por restricciones, áreas protegidas, costes o revisión humana cuando importen.

<a id="environment-setup"></a>
## Configuración del entorno

Harneloop registra el mapa del entorno; lo crea el agente operador.

La CLI no puede adivinar qué herramienta MCP controla una app, dónde se guarda un render, cómo se restablece un flujo de navegador o qué estado de base de datos demuestra éxito. El agente debe inspeccionar el espacio real y vincular esos detalles a la unidad.

Se admiten tres modos de preparación:

| Modo | Cuándo usarlo | Comportamiento del agente |
|---|---|---|
| `existing` | El entorno ya funciona | Conectarlo y documentarlo; no reconstruirlo sin motivo |
| `assisted` | Algunas piezas existen | Identificar y añadir lo mínimo que falta para una línea base |
| `managed` | Hay que crear el entorno | Construirlo explícitamente y documentar cambios de infraestructura |

El entorno puede basarse en comandos, MCP, pasos manuales o ser totalmente personalizado. Un harness Blender, por ejemplo, puede usar un servidor MCP existente sin un único comando de ejecución. El agente llama herramientas, renderiza, captura pantallas y estado estructurado de la escena y adjunta las salidas a una ejecución Harneloop.

Lee [la incorporación del entorno](docs/environment-onboarding.md) para ejemplos detallados.

<a id="configuration"></a>
## Configuración

La mayoría debe empezar con los valores predeterminados. La primera configuración útil suele estar dentro de la unidad, no en los ajustes globales.

<a id="harness-unit-configuration"></a>
### Configuración de la unidad de harness

| Archivo o área | Cuándo cambiarlo |
|---|---|
| `operational-map.md` | Cambian herramientas, ubicaciones de artefactos, supuestos, restricciones o flujo |
| `target/brief.yaml` | Cambian la familia de tareas, definición de éxito, artefactos esperados o riesgos |
| `environment/contract.yaml` | Cambian comandos, herramientas MCP, modos de preparación e interacción o rutas de salida |
| `agent-facing/` | Un candidato probado promueve instrucciones nuevas o contexto reutilizable |
| `observers/` y `validators/` | Hace falta mejor inspección de artefactos o comprobaciones deterministas |
| `regression-cases/` | Un fallo descubierto debe probarse en futuras iteraciones |
| `tools/` y `infrastructure/` | El mejor rendimiento requiere capacidades o servicios específicos de la unidad |

No edites manualmente `.evolve/`, `versions/`, `provenance/`, `runtime/` ni metadatos candidatos propiedad del framework. Usa los comandos de ciclo de vida.

<a id="global-preferences"></a>
### Preferencias globales

Consulta las preferencias con `harneloop settings show` y cambia una con:

```bash
harneloop settings set validation.prefer_visual_artifacts true
harneloop settings set agent_behavior.autonomy_level balanced
harneloop settings set runtime.token_efficiency_mode false
```

Grupos importantes de preferencias:

- `agent_behavior`: autonomía, confirmación de acciones arriesgadas y rigor de promoción;
- `validation`: validación decidida por agentes, preferencia visual y modo de recursos;
- `export`: adaptador objetivo y perfil de paquete predeterminados;
- `runtime`: detalle de telemetría, eficiencia de tokens y comportamiento del registro local de unidades.

En la alfa, las preferencias son valores duraderos y orientación para la CLI y el agente operador. Aún no todos los comandos del motor imponen automáticamente todas las preferencias. La promoción exige evidencia salvo que se use la excepción explícita de desarrollo.

<a id="example-use-cases"></a>
## Ejemplos de uso

- Mejorar razonamiento espacial y construcción de escenas de un agente Blender o CAD.
- Mejorar generación de SVG, imágenes, diapositivas, documentos o interfaces mediante revisión de artefactos renderizados.
- Construir un harness de agente de código para un repositorio con fallos recurrentes de implementación o depuración.
- Mejorar automatización del navegador con capturas, estado DOM, trazas y resultados.
- Desarrollar mejor selección de herramientas y recuperación de fallos para agentes MCP.
- Evolucionar recuperación, ejemplos, validadores y contexto para investigación o procesamiento de datos.
- Crear un harness interno reutilizable y exportarlo a Codex, Cursor o un agente de aplicación personalizado.

Harneloop resulta más útil cuando la tarea se repite, las salidas son inspeccionables y los fallos pueden convertirse en mejoras duraderas. No hace falta para una tarea única sin aprendizaje reutilizable.

<a id="core-cli-lifecycle"></a>
## Ciclo principal de la CLI

Los comandos explícitos están pensados para agentes, automatización y usuarios técnicos:

```bash
harneloop init-unit ./my-unit --id my-unit --name "My Harness Unit" --template artifact-review
harneloop target set my-unit --task "..." --success "..."
harneloop environment connect my-unit --name "..." --mode existing --description "..."
harneloop attempt plan my-unit --goal "..." --method "..."
harneloop run start my-unit --task "Baseline attempt"
harneloop artifact add my-unit run-0001 ./output.png --kind image
harneloop run finish my-unit run-0001 --status succeeded --summary "Baseline captured"
harneloop candidate create my-unit --summary "Improve artifact construction" --plane target_harness --validation-tier representative
harneloop run start my-unit --task "Test candidate improvement" --candidate-id cand-0001
harneloop artifact add my-unit run-0002 ./improved-output.png --kind image
harneloop run finish my-unit run-0002 --status succeeded --summary "Candidate result captured"
harneloop candidate evidence add my-unit cand-0001 --kind artifact_review --summary "..." --run-id run-0002 --artifact-id artifact-0001 --validation-tier representative
harneloop candidate stage my-unit cand-0001 ready
harneloop promote my-unit cand-0001 --version 0.1.0
harneloop export my-unit --adapter codex
harneloop package my-unit --output ./my-unit-0.1.0.tar.gz
```

La secuencia es ilustrativa, no una receta fija. Los agentes con herramientas pueden realizar muchas acciones entre `run start` y `run finish`, capturar varios artefactos, crear varios intentos o esperar resultados externos.

<a id="safety-and-integrity"></a>
## Seguridad e integridad

- Los archivos de control YAML y JSON se escriben atómicamente.
- La asignación concurrente de IDs y lectura-modificación-escritura usan bloqueos locales del harness.
- Una ejecución terminada no puede modificarse ni finalizarse de nuevo.
- Las capas candidatas no pueden modificar el estado protegido del framework.
- Las referencias de evidencia deben existir al adjuntarse y al promoverse.
- La evidencia debe coincidir con la versión base actual y el nivel de validación declarado del candidato.
- Los candidatos paralelos sobreviven a otra promoción, pero deben hacer rebase y reunir evidencia nueva antes de promoverse.
- Las versiones promovidas se guardan como instantáneas restaurables.
- La reversión es una acción registrada del framework.
- Los paquetes thin excluyen datos de ejecución, candidatos, cachés y archivos habituales de secretos.

<a id="documentation"></a>
## Documentación

- [Cómo funciona Harneloop](docs/framework-process.md)
- [Incorporación de agentes](docs/agent-onboarding.md)
- [Incorporación del entorno](docs/environment-onboarding.md)
- [Ciclo de vida principal](docs/architecture/core-lifecycle.md)
- [Capas de ejecución y futuro límite Rust](docs/architecture/runtime-layers.md)
- [Concurrencia y seguridad de archivos](docs/architecture/concurrency.md)
- [Principios del producto](docs/product-principles.md)
- [Demostración local](docs/demo-first-test.md)
- [Notas de desarrollo](docs/development.md)

<a id="contributing"></a>
## Contribuir

Se agradecen contribuciones, incidencias y estudios independientes de unidades. Son especialmente útiles:

- probar Harneloop en familias de tareas distintas al estudio actual;
- informar de fallos reproducibles de ciclo de vida, portabilidad o incorporación;
- mejorar adaptadores de agentes objetivo, validadores, empaquetado y comportamiento multiplataforma;
- aportar documentación, ejemplos o cobertura de regresión centrados.

Lee [CONTRIBUTING.md](CONTRIBUTING.md) antes de cambios importantes. Para arquitectura, abre una incidencia primero para discutir alcance y compatibilidad. Los problemas de seguridad deben seguir [SECURITY.md](SECURITY.md), no una incidencia pública.

<a id="development"></a>
## Desarrollo

Ejecuta las pruebas desde el repositorio:

```bash
python -m unittest discover -s tests
```

El proyecto usa actualmente Python 3.11 o posterior. Cuando se estabilice el producto, un futuro runtime Rust podría asumir mayores responsabilidades protegidas de ciclo de vida, empaquetado, vigilancia de archivos o distribución de escritorio.

Harneloop es la identidad elegida para la alfa y el lanzamiento público. El paquete, CLI, metadatos, documentación y repositorio usan el mismo nombre.

<a id="license"></a>
## Licencia

Harneloop está disponible bajo la [Apache License 2.0](../../../LICENSE).

<a id="runtime-layers"></a>
# Capas de ejecución

<a id="current-decision"></a>
## Decisión actual

Usar Python para la primera implementación de referencia.

Preferir Rust a Go más adelante si Harneloop necesita un runtime nativo protegido.

<a id="why-rust-later"></a>
## Por qué Rust más adelante

La capa nativa solo debe existir si el framework necesita garantías locales más fuertes sobre:

- integridad del ciclo de vida;
- límites del estado protegido;
- instantáneas de versiones;
- reversión;
- almacenamiento direccionado por contenido;
- empaquetado de artefactos;
- vigilancia de archivos;
- supervisión de subprocesos;
- distribución de escritorio.

Rust encaja mejor que Go en ese papel de núcleo protegido para este tipo de producto.

<a id="agent-boundary"></a>
## Límite del agente

Rust no debe convertirse en el espacio abierto del agente para diseñar el harness.

Los agentes deben seguir trabajando mediante:

- instrucciones Markdown;
- manifiestos YAML y JSON;
- esquemas;
- directorios de candidatos;
- comandos CLI;
- contratos de artefactos.

La regla sigue siendo:

> Los agentes pueden explorar libremente dentro de los candidatos. El motor controla la promoción.

<a id="where-go-could-still-fit"></a>
## Dónde podría encajar Go

Go sigue siendo una buena opción para futuros servicios alojados, coordinación de trabajadores remotos o infraestructura de registro si Harneloop crece en esa dirección.

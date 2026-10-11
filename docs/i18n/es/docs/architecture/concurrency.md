<a id="concurrency-and-file-safety"></a>
# Concurrencia y seguridad de archivos

Los agentes pueden ejecutar comandos de Harneloop en rápida sucesión o en paralelo. Todo comando que lea un archivo de control, calcule un ID secuencial y vuelva a escribir el archivo debe proteger toda esa sección de lectura-modificación-escritura.

<a id="current-rule"></a>
## Regla actual

- Usa un archivo de bloqueo de la unidad de harness para las secciones compartidas del ciclo de vida.
- Vuelve a leer el archivo YAML o JSON pertinente dentro del bloqueo.
- Asigna el siguiente ID secuencial dentro del bloqueo.
- Escribe YAML y JSON mediante sustitución atómica de archivos temporales.
- Libera el bloqueo solo cuando la actualización del archivo termine.

<a id="implemented-locks"></a>
## Bloqueos implementados

- `runs`: asigna IDs de ejecución.
- `run-<id>`: añade artefactos y finaliza una ejecución.
- `attempts`: asigna IDs de intento.
- `attempt-<id>`: añade observaciones de intentos.
- `candidates`: asigna IDs de candidato.
- `candidate-<id>-evidence`: asigna IDs de evidencia.
- `lifecycle`: promueve candidatos y revierte versiones.
- `state`: actualiza `.evolve/state.json` y los archivos de estado derivados.

Los bloqueos están en `.evolve/locks/`, un estado de ejecución propiedad del framework que se excluye de los paquetes portátiles.

<a id="rust-runtime-note"></a>
## Nota sobre el runtime Rust

Esto todavía no requiere Rust. Los bloqueos de archivos y la sustitución atómica de Python bastan para la CLI alfa. Cuando se estabilice el producto, un futuro runtime Rust podría encargarse de un aislamiento más estricto, supervisión de procesos y coordinación concurrente de archivos con mayores garantías.

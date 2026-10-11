<a id="security"></a>
# Seguridad

Harneloop es un framework de prioridad local para unidades de harness construidas por agentes. Los límites de seguridad importan porque los agentes pueden crear herramientas, ejecutar comandos y empaquetar unidades reutilizables.

<a id="current-status"></a>
## Estado actual

Es una alfa pública temprana. No consideres Harneloop ni una unidad de harness como un sandbox reforzado o un límite de seguridad.

<a id="rules"></a>
## Reglas

- Nunca almacenes secretos dentro de las unidades de harness.
- No empaquetes por defecto archivos `.env`, claves privadas, credenciales, cachés ni trazas de ejecución sin procesar.
- Trata las herramientas de candidatos generadas como no confiables hasta inspeccionarlas.
- Usa los comandos del framework para promover, revertir y empaquetar.
- Exige la aprobación explícita del usuario antes de acciones destructivas.

<a id="reporting"></a>
## Notificación

No reveles posibles vulnerabilidades en una incidencia pública. Usa el formulario privado de notificación de vulnerabilidades de GitHub cuando esté disponible para este repositorio. Si no lo está, contacta en privado con el propietario mediante el perfil de GitHub enlazado e incluye pasos para reproducir el problema, versiones afectadas y posible impacto.

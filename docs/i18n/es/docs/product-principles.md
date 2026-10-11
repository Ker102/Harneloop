<a id="product-principles"></a>
# Principios del producto

Harneloop es la identidad de producto elegida. La arquitectura sigue siendo independiente de cualquier benchmark o familia de tareas particular.

<a id="what-this-is"></a>
## Qué es

Harneloop es un framework que los agentes usan para construir y mejorar el harness que los rodea a ellos mismos o a otro agente objetivo.

El framework debe ayudar a los agentes a:

- realizar intentos de tareas;
- inspeccionar artefactos reales;
- vincular los fallos con las ejecuciones;
- mantener un mapa operativo local de la unidad con el flujo de trabajo, la evidencia, los supuestos del entorno y las preguntas abiertas;
- distinguir las capacidades ausentes del agente operador de las herramientas de la unidad o del agente objetivo;
- investigar y reutilizar herramientas, skills, bibliotecas, conjuntos de datos, ejemplos y trabajos previos adecuados;
- proponer cambios candidatos del harness;
- probar los cambios candidatos;
- promover solo mejoras respaldadas por evidencia;
- empaquetar unidades de harness portátiles.

<a id="what-this-is-not"></a>
## Qué no es

Harneloop no es:

- un panel genérico de evaluación;
- un framework de grafos de agentes fijos;
- un sistema específico de Blender;
- un sistema de entrenamiento o ajuste fino de modelos;
- una carpeta informal de prompts sin ciclo de vida.

<a id="core-design-tension"></a>
## Tensión principal del diseño

El sistema está pensado para modelos de IA generativa, así que debe permitir razonamiento y exploración. Al mismo tiempo, el framework debe proteger la integridad del ciclo de vida.

La regla:

> Los agentes pueden explorar libremente dentro de los candidatos. El motor controla la promoción.

`operational-map.md` conserva la comprensión actual del agente sobre una unidad de harness sin convertirla en un script fijo. El agente debe usarlo para orientarse, actualizarlo cuando cambie la evidencia y seguir razonando a partir de la tarea y los artefactos actuales.

El framework no debe asumir que el agente que construye una unidad de harness puede hacerlo todo. Identifica las capacidades ausentes del agente operador, justifícalas con evidencia o una mejora esperada clara y respeta los permisos adecuados antes de añadir herramientas, dependencias, credenciales, servicios de pago o mayor acceso externo.

Harneloop busca el mejor rendimiento verificado de la tarea, no reconstruir cada capacidad desde cero. El agente operador debe inspeccionar soluciones existentes y puede adoptarlas, adaptarlas, combinarlas o aprender de ellas si mejoran el harness. La reutilización debe poder inspeccionarse: registra qué se usó y por qué, verifica compatibilidad y valor observado, respeta licencias y atribución, y aplica los permisos habituales para seguridad, credenciales, acceso externo, coste o cambios importantes de infraestructura.

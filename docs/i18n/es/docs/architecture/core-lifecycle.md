<a id="core-lifecycle"></a>
# Ciclo de vida principal

<a id="harness-unit"></a>
## Unidad de harness

Una unidad de harness es un directorio portátil con material reutilizable del harness y archivos de control del framework.

Archivos obligatorios:

```text
unit/
  unit.yaml
  UNIT_AGENT.md
  operational-map.md
  candidates/
  versions/
  provenance/
```

`operational-map.md` es el documento de orientación local de la unidad. Registra la comprensión actual del agente: qué mejora la unidad, cómo se usa el entorno objetivo, qué artefactos o evidencia son útiles, cómo se ejecuta y restablece normalmente, capacidades ausentes del agente operador, herramientas de la unidad o del agente objetivo, puntos frágiles, supuestos, preguntas abiertas y ubicación de la evidencia anterior. Debe orientar al agente sin convertirse en un procedimiento rígido.

Carpetas opcionales habituales:

```text
agent-facing/
observers/
validators/
regression-cases/
infrastructure/
exports/
tools/
memory/
experiments/
```

<a id="candidates"></a>
## Candidatos

Un candidato es un lote coherente de cambios o una hipótesis, no una edición de archivo ni un commit de Git. Los cambios relacionados de configuración, herramientas, instrucciones o validadores pueden acumularse en un candidato si deben probarse y promoverse juntos. Los agentes pueden mantener varios candidatos abiertos para problemas independientes, como una mejora del harness objetivo y una reparación separada de la evaluación.

```text
candidates/cand-0001/
  candidate.yaml
  rationale.md
  changes/
  validation/
  evidence/
  notes.md
```

Los cambios del candidato se aplican mediante el framework. Las capas de cambios no pueden editar rutas protegidas como `unit.yaml`, `versions/`, `provenance/`, `.evolve/` o `candidates/`.

Cada candidato actual declara:

- un plano de impacto: `target_harness`, `evaluation`, `infrastructure` o `mixed`;
- un nivel de validación: `structural`, `targeted`, `representative` o `full`;
- una etapa del ciclo de vida: `accumulating`, `ready`, `validating`, `needs_rebase`, `promoted` o `rejected`;
- la versión promovida del harness en la que se basa.

La validación es proporcional al riesgo. Las comprobaciones estructurales sirven para cambios solo de metadatos; las dirigidas, para reparaciones aisladas de infraestructura o evaluadores; las ejecuciones representativas, para cambios de comportamiento del harness. Las regresiones completas se reservan para cambios amplios y controles de versiones. El agente puede elegir un nivel más fuerte, pero no debe repetir todo el benchmark de artefactos por cada edición incremental de configuración.

Los cambios de evaluación y del harness objetivo normalmente deben seguir en candidatos separados para que un juez modificado no sea la única prueba de que un harness modificado mejoró. Un candidato puede seguir `accumulating` mientras agrupa trabajo relacionado y pasar a `ready` cuando sea lo bastante coherente para validarlo.

<a id="promotion"></a>
## Promoción

La promoción aplica a la unidad una capa de cambios candidata lista, crea una instantánea restaurable en `versions/` y actualiza la procedencia. Las versiones promovidas siguen siendo lineales aunque el trabajo candidato sea paralelo.

Si dos candidatos abiertos comparten base, promover uno marca el otro como `needs_rebase`. Conserva archivos e historial, pero debe reconciliarse con la versión nueva y reunir evidencia reciente antes de promoverse. La evidencia anterior queda como procedencia y no satisface la barrera de la nueva versión base.

La integridad de las referencias de evidencia se comprueba al adjuntarlas y de nuevo al promover. Deben existir la ejecución y el artefacto declarados, el archivo almacenado del artefacto y cualquier archivo de evidencia referido directamente. La evidencia narrativa puede omitir esas referencias.

<a id="run-integrity"></a>
## Integridad de las ejecuciones

Una ejecución solo es modificable mientras tenga estado `running`; en esa fase pueden adjuntarse artefactos. La primera transición `run finish` exitosa es terminal: se rechazan artefactos posteriores y finalizaciones repetidas para impedir reescribir silenciosamente el resultado original.

<a id="rollback"></a>
## Reversión

La reversión restaura una instantánea promovida anterior. Debe ser una acción del framework con procedencia, no una copia manual.

<a id="wait-and-stop"></a>
## Esperar y detener

El ciclo de vida de ejecución admite espera y parada explícitas.

La espera cubre artefactos retrasados, revisión humana, trabajos en cola, periodos de espera y reconstrucciones de infraestructura.

La parada cubre evidencia suficiente, estancamiento, límites de capacidades, necesidades de permisos o casos en que el siguiente paso útil depende de una persona o un sistema externo.

Consulta [Cómo funciona Harneloop](../framework-process.md) para el ciclo completo de evolución basado en artefactos.

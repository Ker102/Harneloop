<a id="core-lifecycle"></a>
# Ciclo de vida central

<a id="harness-unit"></a>
## Unidade de harness

Uma unidade de harness é um diretório portátil com material reutilizável do harness e arquivos de controle do framework.

Arquivos obrigatórios:

```text
unit/
  unit.yaml
  UNIT_AGENT.md
  operational-map.md
  candidates/
  versions/
  provenance/
```

`operational-map.md` é o documento de orientação local da unidade. Registra o entendimento atual do agente: o que a unidade melhora, como usar o ambiente-alvo, quais artefatos ou evidências são úteis, como executar e reinicializar normalmente, lacunas de capacidade do agente operador, ferramentas da unidade ou do agente-alvo, pontos frágeis, premissas, questões em aberto e onde ficam as evidências anteriores. Deve orientar sem virar um procedimento rígido.

Pastas opcionais comuns:

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

Um candidato é um lote coerente de mudanças ou uma hipótese, não uma edição de arquivo nem um commit Git. Mudanças relacionadas de configuração, ferramentas, instruções ou validadores podem se acumular em um candidato quando devem ser testadas e promovidas juntas. Agentes podem manter vários candidatos abertos para problemas independentes, como uma melhoria do harness-alvo e um reparo separado da avaliação.

```text
candidates/cand-0001/
  candidate.yaml
  rationale.md
  changes/
  validation/
  evidence/
  notes.md
```

Mudanças candidatas são aplicadas pelo framework. Overlays de candidatos não podem editar caminhos protegidos como `unit.yaml`, `versions/`, `provenance/`, `.evolve/` ou `candidates/`.

Cada candidato atual declara:

- um plano de impacto: `target_harness`, `evaluation`, `infrastructure` ou `mixed`;
- um nível de validação: `structural`, `targeted`, `representative` ou `full`;
- uma etapa do ciclo de vida: `accumulating`, `ready`, `validating`, `needs_rebase`, `promoted` ou `rejected`;
- a versão promovida do harness na qual se baseia.

A validação é proporcional ao risco. Verificações estruturais servem para mudanças apenas de metadados; direcionadas, para reparos isolados de infraestrutura ou avaliadores; execuções representativas, para mudanças de comportamento do harness. Suítes completas de regressão ficam para mudanças amplas e marcos de lançamento. O agente pode escolher um nível mais forte, mas não deve repetir todo o benchmark de artefatos a cada edição incremental de configuração.

Mudanças na avaliação e no harness-alvo normalmente devem permanecer em candidatos separados, para que um juiz modificado não seja a única prova de melhoria de um harness modificado. Um candidato pode ficar em `accumulating` enquanto agrupa trabalho relacionado e passar a `ready` quando estiver coerente o bastante para validar.

<a id="promotion"></a>
## Promoção

A promoção aplica um overlay candidato pronto à unidade, cria um snapshot restaurável em `versions/` e atualiza a procedência. Versões promovidas permanecem lineares, mesmo quando o trabalho com candidatos é paralelo.

Se dois candidatos abertos compartilham a mesma base, promover um marca o outro como `needs_rebase`. Seus arquivos e histórico permanecem intactos, mas ele deve ser reconciliado com a nova versão e reunir evidências novas antes da promoção. Evidências anteriores permanecem como procedência e não atendem ao controle da nova versão-base.

A integridade das referências de evidências é verificada ao anexá-las e novamente na promoção. A execução e o artefato declarados devem existir, o arquivo armazenado do artefato deve continuar presente e qualquer arquivo de evidência diretamente referenciado deve existir. Evidências narrativas podem omitir essas referências.

<a id="run-integrity"></a>
## Integridade das execuções

Uma execução só é mutável enquanto seu status é `running`; artefatos podem ser anexados nessa fase. A primeira transição `run finish` bem-sucedida é terminal: adições posteriores de artefatos e tentativas repetidas de finalização são rejeitadas para impedir a reescrita silenciosa do resultado original.

<a id="rollback"></a>
## Reversão

A reversão restaura um snapshot promovido anterior. Deve ser uma ação do framework com procedência, não uma cópia manual.

<a id="wait-and-stop"></a>
## Aguardar e parar

O ciclo de vida de execução suporta espera e parada explícitas.

A espera cobre artefatos atrasados, revisão humana, trabalhos em fila, períodos de espera e reconstruções de infraestrutura.

A parada cobre evidências suficientes, estagnação, limites de capacidade, necessidades de permissão ou casos em que o próximo passo útil depende de uma pessoa ou sistema externo.

Veja [Como o Harneloop funciona](../framework-process.md) para o ciclo completo de evolução orientada por artefatos.

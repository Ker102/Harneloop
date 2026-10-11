<div align="center">

<h1><img src="../../assets/harneloop-mark.svg" alt="" width="56" height="56" align="absmiddle" /> Harneloop</h1>

<p>Evolução do harness para agentes de IA orientada por artefatos.</p>

<p><a href="https://harneloop.kaelux.dev/">Site</a> · <a href="#agent-quick-start">Início rápido</a> · <a href="#documentation">Documentação</a></p>

</div>

<!-- i18n-switcher:start -->
[English](../../../README.md) | [Español](../es/README.md) | [简体中文](../zh-CN/README.md) | [Français](../fr/README.md) | [日本語](../ja/README.md) | [Deutsch](../de/README.md) | Português (Brasil)
<!-- i18n-switcher:end -->

**Ajude um agente de IA a aprender com o que deu errado.**

Um agente pode terminar uma tarefa, dizer que teve sucesso e ainda deixar código quebrado, um render ruim ou um fluxo que não funciona. O Harneloop oferece ao seu agente atual uma forma estruturada de inspecionar o resultado, rever suas ações, encontrar o provável erro e testar uma abordagem melhor.

O agente melhora seu **harness**: instruções, ferramentas, contexto e verificações ao redor do modelo. O modelo em si não precisa ser treinado novamente. Uma mudança proposta só se torna a versão de trabalho depois que um teste a sustenta.

<a id="what-can-you-use-it-for"></a>
## Para que você pode usar?

Use o Harneloop quando um agente repete erros semelhantes e você consegue inspecionar o que ele produz. Exemplos incluem código e testes, fluxos de navegador, documentos gerados e tarefas visuais. O primeiro estudo publicado é a construção de cenas Blender com ViperMesh; outras famílias de tarefas continuam abertas a testes e contribuições.

<a id="how-it-works"></a>
## Como funciona

1. **Tente a tarefa.** Guarde a saída e os passos do agente.
2. **Inspecione o resultado.** Verifique o artefato em si, sem confiar apenas na mensagem de conclusão.
3. **Reveja o processo.** Relacione o problema a uma chamada de ferramenta, contexto ausente, instrução ou decisão do ambiente.
4. **Teste uma melhoria.** Deixe o agente propor uma mudança e repetir as verificações relevantes.
5. **Mantenha o que funciona.** Preserve melhorias sustentadas e uma versão que possa restaurar.

<p align="center">
  <a href="https://harneloop.kaelux.dev/media/harneloop-how-it-works.mp4">
    <img src="https://harneloop.kaelux.dev/media/harneloop-video-poster.png" alt="Veja como o Harneloop funciona: de um objetivo a um harness reutilizável" width="900" />
  </a>
</p>

<p align="center"><a href="https://harneloop.kaelux.dev/media/harneloop-how-it-works.mp4"><img src="../../assets/readme-play.svg" alt="" width="18" height="18" align="absmiddle" /> Veja como o Harneloop funciona - 3:40</a></p>

Cada família de tarefas tem uma **unidade de harness**: um espaço portátil que reúne objetivo, ferramentas, tentativas, evidências e melhorias. Você pode pausar e continuar depois sem reiniciar a investigação.

<a id="try-harneloop"></a>
## Experimente o Harneloop

[Instale pelo PyPI](https://pypi.org/project/harneloop/) em um ambiente isolado de ferramentas:

```bash
uv tool install harneloop
harneloop setup
```

Ou use `python -m pip install harneloop` no seu ambiente Python. Veja [Instalar e iniciar](#install-and-start) para requisitos e instalação pelo código-fonte.

Depois, dê a um agente capaz o link do repositório e a tarefa que deseja melhorar. O [Início rápido para agentes](#agent-quick-start) inclui um prompt pronto para uso.

**Estado:** Alfa pública. O ciclo central funciona; validação em mais tarefas e contribuições são bem-vindas. [Relate um problema ou compartilhe um caso de uso](https://github.com/Ker102/Harneloop/issues).

<a id="evidence-from-a-real-case-study"></a>
## Evidências de um estudo real

O Harneloop foi usado para desenvolver a unidade personalizada ViperMesh para raciocínio espacial e construção de cenas Blender. A comparação manteve o modelo executor fixo em **GPT-5.5 High** e testou o harness ViperMesh evoluído contra a **linha de base do servidor Anthropic x Blender MCP**, isolando o harness como a principal camada alterada do sistema.

- O ViperMesh foi mais rápido em **6 de 7** tarefas ao vivo comparáveis, com **aceleração média de 2.534x**.
- A avaliação visual preliminar por um LLM neutro melhorou **8.19 pontos** em sete pares de renders ao vivo.
- O uso agregado de tokens do agente executor foi **90.91% menor** em sete benchmarks comparáveis, aproximadamente **175K contra 1.9M tokens** no total.

O Harneloop não gerou as cenas. Ele estruturou o ciclo de evidências e artefatos que expôs fraquezas, orientou o desenvolvimento de ferramentas e do harness e verificou se as mudanças melhoraram o benchmark. Leia metodologia, limitações e resultados completos no [estudo ViperMesh](https://kristoferjussmann.me/case-studies/vipermesh).

Esses resultados fornecem evidência empírica direta de que o processo do Harneloop funciona em um ambiente real de agentes rico em artefatos: o modelo executor permaneceu igual, enquanto o harness evoluído trouxe ganhos mensuráveis de velocidade, desempenho visual e eficiência de tokens.

<a id="demonstration-vipermesh-mcp"></a>
### Demonstração: ViperMesh MCP

[Assista à demonstração do Harneloop com ViperMesh MCP](https://www.youtube.com/watch?v=bs74QJ6UD5E&t=2s).

A construção de cenas Blender é um caso concreto para inspecionar o que um agente produziu e melhorar suas ferramentas e instruções. Leia o [estudo Harneloop](https://kristoferjussmann.me/case-studies/harneloop/#harneloop-demo) para o framework e o [benchmark ViperMesh](https://kristoferjussmann.me/case-studies/vipermesh/) para os resultados medidos. O [conector público do Blender](https://github.com/Ker102/vipermesh-blender) está disponível separadamente do estúdio completo e do harness avaliado.

<a id="start-here"></a>
## Comece aqui

- **Usar por meio de um agente:** [Início rápido para agentes](#agent-quick-start)
- **Instalar por conta própria:** [Instalar e iniciar](#install-and-start)
- **Entender as unidades:** [O que é uma unidade de harness?](#what-is-a-harness-unit)
- **Entender o ciclo:** [O ciclo de vida simplificado](#the-lifecycle-made-simple)
- **Evidências medidas:** [Estudo ViperMesh](https://kristoferjussmann.me/case-studies/vipermesh)
- **Conectar um ambiente real:** [Configuração do ambiente](#environment-setup)
- **Alterar padrões:** [Configuração](#configuration)
- **Arquitetura técnica:** [Ciclo central](docs/architecture/core-lifecycle.md), [camadas de execução](docs/architecture/runtime-layers.md) e [concorrência](docs/architecture/concurrency.md)
- **Instruções completas para agentes:** [Introdução de agentes](docs/agent-onboarding.md)
- **Processo visual:** [Como funciona](#how-it-works), [diagrama compacto editável](docs/framework-process-compact.md) e [diagrama detalhado](docs/framework-process.md)

<a id="why-harneloop-exists"></a>
## Por que o Harneloop existe

Modelos frequentemente repetem as mesmas falhas porque as lições úteis de uma tentativa nunca se tornam parte testada do ambiente de trabalho. Um prompt maior ou uma pontuação de avaliação não resolve o problema inteiro.

O modelo é só uma parte do desempenho de um agente. O harness determina o contexto que vê, as ferramentas disponíveis, como interage com o ambiente, o que lembra, como os resultados são inspecionados e se erros viram melhorias duradouras. Em muitos problemas específicos, isso torna o harness o maior ponto de alavancagem: ganhos significativos sem treinar novamente o modelo, com mudanças inspecionáveis, testáveis, reversíveis e portáteis.

O Harneloop torna esse trabalho estruturado e eficiente. Em vez de acumular edições pontuais de prompts, permite desenvolver várias unidades independentes, testar mudanças em tentativas reais, preservar evidências e histórico e continuar ou exportar cada harness bem-sucedido como um pacote coerente.

O Harneloop oferece ao agente operador um ciclo controlado de melhoria:

- trabalhar na tarefa real, não apenas em um benchmark sintético;
- capturar renders, capturas de tela, arquivos, rastros, logs, estado estruturado ou outros artefatos;
- inspecionar os artefatos visualmente, estruturalmente ou pelo comportamento;
- rastrear resultados fracos até instruções, ferramentas, contexto, recuperação, ambiente ou limites do modelo;
- desenvolver melhorias como patches candidatos isolados;
- testar candidatos em novas tentativas e casos de regressão;
- promover apenas mudanças sustentadas por evidências válidas;
- preservar versões restauráveis e empacotar o harness resultante para reutilização.

O agente pode raciocinar e experimentar livremente no espaço do harness. O Harneloop controla os limites sensíveis à integridade: registros, estado protegido, evidências, promoção, snapshots, reversão e empacotamento.

<details>
<summary>Contexto de pesquisa: por que melhorar o harness antes dos pesos?</summary>

<a id="why-improve-the-harness-before-the-weights"></a>
### Por que melhorar o harness antes dos pesos?

Pesquisas sobre interfaces de agentes, recuperação, ferramentas e feedback iterativo mostram que mudar o sistema ao redor de um modelo pode melhorar bastante o desempenho sem alterar seus pesos. Quando contexto, recuperação, ferramentas, feedback ou interação com o ambiente são os principais gargalos, métodos no nível do harness podem superar o ajuste fino, às vezes substancialmente, preservando as capacidades gerais do modelo. O Harneloop surgiu de problemas práticos de construção de harnesses; os trabalhos abaixo sustentam independentemente essa direção:

- [Self-Harness](https://arxiv.org/abs/2606.09498) mostrou que agentes podiam extrair fraquezas de rastros de execução, propor mudanças no harness, validá-las com regressões e melhorar taxas de aprovação em testes reservados em três famílias de modelos.
- [SWE-agent](https://arxiv.org/abs/2405.15793) mostrou que uma interface agente-computador específica melhorou substancialmente a navegação em repositórios, a edição de código e a execução de testes por modelos de linguagem.
- [Reflexion](https://arxiv.org/abs/2303.11366) melhorou agentes por tentativa e erro, feedback linguístico e memória episódica, em vez de atualizações dos pesos.
- [Self-Refine](https://arxiv.org/abs/2303.17651) relatou melhoria absoluta média de cerca de 20 pontos percentuais em sete tarefas avaliadas, com feedback e refinamento iterativos sem treinamento adicional.
- [Fine-Tuning or Retrieval?](https://aclanthology.org/2024.emnlp-main.15/) constatou que RAG superou consistentemente o ajuste fino não supervisionado nas tarefas de injeção de conhecimento avaliadas, incluindo conhecimento existente e novo.
- [Does Fine-Tuning LLMs on New Knowledge Encourage Hallucinations?](https://arxiv.org/abs/2405.05904) constatou dificuldade para adquirir fatos novos por ajuste fino supervisionado e maior propensão a alucinações à medida que esse conhecimento era aprendido.

Junto com o estudo ViperMesh, isso sustenta uma estratégia prática: **otimize primeiro o harness, meça o resultado e altere os pesos somente quando evidências mostrarem que o harness atingiu seu limite útil.** Mudanças no harness são mais rápidas de inspecionar, reverter, reutilizar e validar e, em tarefas aplicáveis, podem trazer ganhos maiores que mudanças de pesos sem alterar permanentemente o modelo-base.

Isso não estabelece que um harness sempre superará qualquer método de ajuste fino. O ajuste fino ainda pode ser útil para comportamento, estilo, latência, representações especializadas ou capacidades difíceis de fornecer na inferência. Um harness forte e um ajuste fino bem escolhido também podem se complementar.

</details>

<a id="what-is-a-harness-unit"></a>
## O que é uma unidade de harness?

Uma **unidade de harness** é um espaço portátil para melhorar uma família de tarefas. Cada unidade evolui independentemente e mantém definição do alvo, mapa do ambiente, material do harness, experimentos, evidências, casos de regressão e versões promovidas.

Uma unidade nova começa com esta estrutura:

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

Não é um template restritivo. Agentes podem adicionar pesquisa, scripts, dados de recuperação, declarações de infraestrutura, memória, observadores personalizados ou pastas novas. O framework protege apenas arquivos e regras do ciclo de vida necessários para manter a unidade compreensível e recuperável.

<a id="portable-unit-versus-local-working-data"></a>
### Unidade portátil versus dados locais de trabalho

O material reutilizável pertence à unidade portátil. Rastros brutos, experimentos temporários, caches, segredos, candidatos não promovidos e todos os renders históricos não.

O pacote `thin` padrão contém conhecimento promovido e contratos necessários para reconstruir ou integrar o harness. Evidências de execução ficam locais, salvo inclusão explícita por um perfil futuro.

<a id="the-lifecycle-made-simple"></a>
## O ciclo de vida simplificado

1. **Descreva o objetivo.** O usuário explica no que o agente deve melhorar.
2. **Mapeie o ambiente.** O agente operador descobre como a tarefa real é executada e de onde vêm evidências úteis.
3. **Reconcilie premissas.** Antes da primeira execução real, o contexto importante é confirmado, delegado ou marcado claramente como inferido.
4. **Execute uma linha de base.** O agente tenta a tarefa antes de alterar o harness.
5. **Inspecione e conclua.** Avalia artefatos e aceita, muda, repete, solicita informações ou para explicitamente.
6. **Crie ou amplie candidatos quando necessário.** Mudanças relacionadas se acumulam em lotes coerentes isolados; problemas independentes podem ter candidatos paralelos.
7. **Valide proporcionalmente ao risco.** Usa verificações estruturais, direcionadas, representativas ou completas e anexa evidências.
8. **Promova, revise, aguarde ou pare.** Melhorias sustentadas viram uma versão; candidatos fracos são revisados ou rejeitados.
9. **Exporte ou empacote.** O harness promovido pode ser aplicado a um agente de código, de aplicações ou outro ambiente compatível.

Execuções finalizadas são imutáveis. Evidências candidatas são verificadas ao anexar e novamente na promoção; execuções excluídas, artefatos ausentes ou arquivos de evidências faltantes não podem sustentar um lançamento.

Candidatos não são wrappers por commit. Um candidato de configuração ou ferramentas pode reunir mudanças relacionadas e receber um teste de fumaça focado; um candidato que altera comportamento pode exigir tentativas com artefatos reais e regressões. Harness-alvo, avaliação e infraestrutura podem avançar independentemente. Se um for promovido, os candidatos paralelos na base antiga precisam de rebase e novas evidências antes de seguir.

O vídeo no início explica o ciclo. O [documento compacto](docs/framework-process-compact.md) contém um diagrama Mermaid editável. O [diagrama detalhado](docs/framework-process.md) cobre lacunas de capacidade, entrada humana, espera, parada e o ciclo completo orientado por artefatos.

<a id="what-makes-it-different"></a>
## O que o diferencia?

<a id="artifact-aware"></a>
### <img src="../../assets/readme-observe.svg" alt="" width="18" height="18" align="absmiddle" /> Orientado por artefatos

O Harneloop trata o que foi produzido como evidência. O agente pode inspecionar imagem, cena, UI, documento, repositório gerado, rastro de execução, estado de banco de dados ou outra saída útil, em vez de confiar no próprio relato textual.

<a id="harness-building-not-only-scoring"></a>
### <img src="../../assets/readme-improve.svg" alt="" width="18" height="18" align="absmiddle" /> Construir harnesses, não apenas pontuar

O objetivo não é só relatar que um agente falhou. O agente operador diagnostica a falha e desenvolve uma mudança concreta no harness, incluindo prompts, princípios, exemplos, recuperação, ferramentas, observadores, validadores, regressões ou automação do ambiente.

<a id="evidence-gated-self-improvement"></a>
### <img src="../../assets/readme-verify.svg" alt="" width="18" height="18" align="absmiddle" /> Autoaperfeiçoamento condicionado por evidências

O agente ativo não pode reescrever livremente o harness promovido. Ele cria um candidato, testa, anexa evidências e promove pelo framework. Cada versão promovida pode ser inspecionada e restaurada.

<a id="environment-agnostic"></a>
### Independente do ambiente

O núcleo não depende de Blender, SVG, agentes Python ou de um fornecedor específico de modelos. Uma unidade pode usar comandos de terminal, servidores MCP, automação de navegador, apps de desktop, APIs, passos manuais ou uma interface personalizada.

<a id="reasoning-remains-open-ended"></a>
### O raciocínio permanece aberto

O Harneloop estrutura o ciclo sem transformar o agente operador em um script fixo. O agente continua escolhendo testes, artefatos, estratégia de avaliação, ferramentas e ponto de parada adequados à tarefa.

<a id="agent-quick-start"></a>
## Início rápido para agentes

O Harneloop foi projetado para ser usado principalmente conversando com um agente com acesso ao sistema de arquivos e ao terminal.

Dê ao agente o repositório e um prompt como este:

```text
Read this repository's README.md and docs/agent-onboarding.md.
Use Harneloop to create a harness unit that improves an agent at: [describe the task].

Inspect my existing environment before deciding how to test it. Ask only for context
that can materially change the work, and do not silently treat assumptions as confirmed.
Run a baseline, inspect its artifacts, and conclude the attempt before deciding whether
a candidate is needed. Do not promote a candidate without evidence.
```

O agente deve então:

1. Instalar o Harneloop se necessário e executar `harneloop doctor`.
2. Ler `harneloop onboard --format json` ou [o guia de introdução](docs/agent-onboarding.md).
3. Criar ou continuar uma unidade provisória e inspecionar o ambiente real.
4. Reconciliar contexto confirmado, delegado, inferido e desconhecido pelo ponto de controle de coleta adaptativa.
5. Atualizar `operational-map.md` com o entendimento atual.
6. Executar uma linha de base e inspecionar os artefatos resultantes.
7. Concluir a tentativa antes de aceitar o harness atual ou propor melhorias.

<a id="instructions-for-agents-reading-this-repository"></a>
### Instruções para agentes que leem este repositório

Se você é o agente operador:

- Não presuma que toda tarefa tem um comando de teste.
- Não presuma que o Harneloop descobre endpoints, ferramentas, capturas de tela ou caminhos de artefatos por você.
- Execute `harneloop brief <unit>` e leia `AGENTS.md`, `UNIT_AGENT.md` e `operational-map.md` ao entrar em uma unidade ou recuperar contexto perdido.
- Aplique o resumo da unidade só ao trabalhar nela; trabalho não relacionado fica fora do escopo.
- Use `harneloop intake status` para expor apenas questões pendentes que possam alterar materialmente o trabalho.
- Use `harneloop candidate list <unit>` para recuperar todo o trabalho aberto; não presuma que a unidade só pode ter um candidato ativo.
- Agrupe mudanças relacionadas em candidatos coerentes e ajuste a validação ao impacto, sem executar todo o benchmark após cada edição de configuração.
- Separe mudanças do avaliador e do harness-alvo quando possível para manter evidências confiáveis.
- Inspecione o ambiente real e mapeie-o em `target/` e `environment/`.
- Prefira inspecionar artefatos reais quando verificações determinísticas não estabelecem qualidade.
- Separe suas capacidades das ferramentas projetadas para o agente-alvo.
- Busque o melhor resultado verificado, não reconstruir tudo: pesquise e reutilize ferramentas, skills, bibliotecas, exemplos e trabalho anterior adequados, registrando procedência e respeitando licenças, segurança, custos e permissões.
- Coloque mudanças propostas no harness em um espaço candidato.
- Use comandos Harneloop para execuções, artefatos, evidências, promoção, reversão, espera, parada e retomada.
- Pergunte antes de adicionar credenciais, serviços pagos, acesso externo, ferramentas sensíveis à segurança ou infraestrutura cara.
- Atualize o mapa operacional quando premissas, caminhos de artefatos, ferramentas ou automação mudarem.
- Nunca pare só na conclusão da execução: inspecione artefatos e registre uma decisão explícita com `harneloop attempt conclude`.

A introdução legível por máquina está disponível com:

```bash
harneloop onboard --format json
```

<a id="install-and-start"></a>
## Instalar e iniciar

O Harneloop está [publicado no PyPI](https://pypi.org/project/harneloop/). Instale como ferramenta isolada por [uv](https://docs.astral.sh/uv/getting-started/installation/) ou use `python -m pip install harneloop` no seu ambiente Python. O comando `harneloop` foi projetado para Windows, macOS e Linux.

```bash
uv tool install harneloop
harneloop doctor
harneloop setup
```

Para uma versão não lançada pelo código-fonte, use `uv tool install git+https://github.com/Ker102/Harneloop.git`.

Se `uv` informar que seu diretório de ferramentas não está no `PATH`, execute `uv tool update-shell` e abra outro terminal. Colaboradores em um clone podem instalar o checkout ativo com `uv tool install --editable .`; veja [o ambiente de desenvolvimento](docs/development.md).

`harneloop setup` abre a CLI guiada para pessoas. Executar `harneloop` sem comando abre o menu interativo mais amplo no terminal. Agentes podem usar diretamente comandos explícitos não interativos.

Primeiros comandos úteis:

```bash
harneloop onboard
harneloop template list
harneloop units list
harneloop settings show
```

Unidades criadas por `harneloop setup` ou `harneloop init-unit` são registradas automaticamente. Unidades existentes podem ser adicionadas uma vez com:

```bash
harneloop units register /path/to/my-unit
```

Após registrar, use o ID ou nome da unidade de qualquer diretório em vez de um caminho relativo:

```bash
harneloop units list
harneloop status my-unit --format markdown
harneloop environment status my-unit
```

<a id="what-the-agent-asks-you"></a>
## O que o agente pergunta

A introdução de novas unidades é intencionalmente curta. O agente deve coletar cinco informações:

1. No que este harness deve ajudar o agente a melhorar?
2. Onde o harness será usado?
3. Você define o sucesso, o agente propõe ou isso é decidido após a linha de base?
4. A validação prioriza qualidade, evidências visuais, equilíbrio ou eficiência de recursos?
5. O ambiente de testes já existe, existe em parte ou precisa ser construído?

Você não precisa conhecer de antemão os testes ou artefatos perfeitos. Quando apropriado, o agente deve propô-los após inspecionar tarefa e ambiente. Só pergunta sobre restrições, áreas protegidas, limites de custo ou revisão humana quando esses detalhes importam.

<a id="environment-setup"></a>
## Configuração do ambiente

O Harneloop registra o mapeamento do ambiente; o agente operador o cria.

A CLI não pode adivinhar qual ferramenta MCP controla um app, onde um render é salvo, como reiniciar um fluxo de navegador ou qual estado de banco prova sucesso. O agente deve inspecionar o espaço real e ligar esses detalhes à unidade.

São suportados três modos de configuração:

| Modo | Quando usar | Comportamento do agente |
|---|---|---|
| `existing` | O ambiente já funciona | Conectar e documentar; não reconstruir sem motivo |
| `assisted` | Algumas partes existem | Identificar e adicionar o mínimo faltante para uma linha de base |
| `managed` | O ambiente precisa ser criado | Construir explicitamente e documentar mudanças de infraestrutura |

Um ambiente pode ser orientado por comandos, MCP, passos manuais ou totalmente personalizado. Um harness Blender pode usar um servidor MCP existente sem um único comando de execução. O agente chama ferramentas, renderiza, captura telas e estado estruturado da cena e anexa as saídas a uma execução Harneloop.

Leia [a introdução do ambiente](docs/environment-onboarding.md) para exemplos detalhados.

<a id="configuration"></a>
## Configuração

A maioria dos usuários deve começar com os padrões. A primeira configuração útil geralmente fica na unidade, não nos ajustes globais.

<a id="harness-unit-configuration"></a>
### Configuração da unidade de harness

| Arquivo ou área | Quando alterar |
|---|---|
| `operational-map.md` | Ferramentas, locais de artefatos, premissas, restrições ou fluxo mudam |
| `target/brief.yaml` | Família de tarefas, definição de sucesso, artefatos esperados ou riscos mudam |
| `environment/contract.yaml` | Comandos, ferramentas MCP, modos de configuração e interação ou caminhos de saída mudam |
| `agent-facing/` | Um candidato testado promove instruções novas ou contexto reutilizável |
| `observers/` e `validators/` | A unidade precisa de melhor inspeção ou verificações determinísticas |
| `regression-cases/` | Uma falha descoberta deve ser testada nas próximas iterações |
| `tools/` e `infrastructure/` | Melhor desempenho exige capacidades ou serviços específicos da unidade |

Não edite manualmente `.evolve/`, `versions/`, `provenance/`, `runtime/` ou metadados de candidatos controlados pelo framework. Use comandos CLI do ciclo de vida.

<a id="global-preferences"></a>
### Preferências globais

Consulte preferências com `harneloop settings show` e altere uma com:

```bash
harneloop settings set validation.prefer_visual_artifacts true
harneloop settings set agent_behavior.autonomy_level balanced
harneloop settings set runtime.token_efficiency_mode false
```

Grupos importantes de preferências:

- `agent_behavior`: autonomia, confirmação de ações arriscadas e rigor da promoção;
- `validation`: validação decidida pelo agente, preferência por artefatos visuais e modo de recursos;
- `export`: adaptador-alvo e perfil de pacote padrão;
- `runtime`: detalhes de telemetria, modo de eficiência de tokens e comportamento do registro local de unidades.

Na alfa, preferências são padrões persistentes e orientação para a CLI e o agente operador. Nem toda preferência é aplicada automaticamente por todo comando do motor. A promoção exige evidências, salvo uso da exceção explícita de desenvolvimento.

<a id="example-use-cases"></a>
## Exemplos de uso

- Melhorar raciocínio espacial e construção de cenas de um agente Blender ou CAD.
- Melhorar geração de SVG, imagens, slides, documentos ou UI pela revisão de artefatos renderizados.
- Criar um harness de agente de código para um repositório com falhas recorrentes de implementação ou depuração.
- Melhorar automação de navegador com capturas, estado DOM, rastros e resultados.
- Desenvolver melhor seleção de ferramentas e recuperação de falhas para um agente MCP.
- Evoluir recuperação, exemplos, validadores e contexto para pesquisa ou processamento de dados.
- Criar um harness interno reutilizável e exportá-lo para Codex, Cursor ou um agente de aplicação personalizado.

O Harneloop é mais útil quando a tarefa se repete, as saídas podem ser inspecionadas e falhas podem virar melhorias duradouras. Não é necessário para uma tarefa única sem aprendizado reutilizável.

<a id="core-cli-lifecycle"></a>
## Ciclo central da CLI

Os comandos explícitos são voltados a agentes, automação e usuários técnicos:

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

A sequência é ilustrativa, não uma receita fixa. Agentes com ferramentas podem fazer várias ações entre `run start` e `run finish`, capturar vários artefatos, criar várias tentativas ou aguardar resultados externos.

<a id="safety-and-integrity"></a>
## Segurança e integridade

- Arquivos de controle YAML e JSON são gravados atomicamente.
- Alocação concorrente de IDs e operações de leitura-modificação-gravação usam bloqueios locais do harness.
- Execuções finalizadas não podem ser alteradas nem finalizadas novamente.
- Overlays de candidatos não podem alterar o estado protegido do framework.
- Referências de evidências devem existir ao anexar e na promoção.
- Evidências devem corresponder à versão-base atual e ao nível de validação declarado do candidato.
- Candidatos paralelos sobrevivem a outra promoção, mas precisam de rebase e novas evidências antes de serem promovidos.
- Versões promovidas são armazenadas como snapshots restauráveis.
- A reversão é uma ação registrada do framework.
- Pacotes thin excluem dados de execução, candidatos, caches e arquivos comuns de segredos.

<a id="documentation"></a>
## Documentação

- [Como o Harneloop funciona](docs/framework-process.md)
- [Introdução de agentes](docs/agent-onboarding.md)
- [Introdução do ambiente](docs/environment-onboarding.md)
- [Ciclo de vida central](docs/architecture/core-lifecycle.md)
- [Camadas de execução e futuro limite Rust](docs/architecture/runtime-layers.md)
- [Concorrência e segurança de arquivos](docs/architecture/concurrency.md)
- [Princípios do produto](docs/product-principles.md)
- [Demonstração local](docs/demo-first-test.md)
- [Notas de desenvolvimento](docs/development.md)

<a id="contributing"></a>
## Contribuindo

Contribuições, relatos de problemas e estudos independentes de unidades são bem-vindos. Especialmente úteis:

- testar o Harneloop em outras famílias de tarefas;
- relatar falhas reproduzíveis de ciclo de vida, portabilidade ou introdução de agentes;
- melhorar adaptadores de agentes-alvo, validadores, empacotamento e comportamento multiplataforma;
- contribuir com documentação focada, exemplos ou cobertura de regressão.

Leia [CONTRIBUTING.md](CONTRIBUTING.md) antes de mudanças importantes. Para arquitetura, abra uma issue primeiro para discutir escopo e compatibilidade. Problemas de segurança devem seguir [SECURITY.md](SECURITY.md), não uma issue pública.

<a id="development"></a>
## Desenvolvimento

Execute a suíte de testes no repositório:

```bash
python -m unittest discover -s tests
```

O projeto usa atualmente Python 3.11 ou mais recente. Um runtime Rust futuro poderá assumir responsabilidades mais fortes de ciclo de vida protegido, empacotamento, monitoramento de arquivos ou distribuição desktop após a estabilização do produto.

Harneloop é a identidade escolhida para a alfa e o lançamento público. Pacote, CLI, metadados das unidades, documentação e repositório usam o mesmo nome.

<a id="license"></a>
## Licença

O Harneloop está disponível sob a [Apache License 2.0](../../../LICENSE).

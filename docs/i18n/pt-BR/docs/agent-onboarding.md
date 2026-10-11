<a id="agent-onboarding"></a>
# Introdução de agentes

Um agente com apenas o repositório e a tarefa-alvo deve conseguir entender o Harneloop. O primeiro passo não é escrever um validador nem presumir um comando de teste, mas coletar contexto suficiente para criar uma tentativa de linha de base.

Para configuração guiada voltada a pessoas, execute:

```powershell
harneloop setup
```

Para uma lista legível por agentes, execute:

```powershell
harneloop onboard
```

ou, em um clone antes de instalar a ferramenta de forma persistente:

```powershell
uv run harneloop onboard
```

Para saída legível por máquina:

```powershell
harneloop onboard --format json
```

Para uma unidade criada por uma versão anterior, execute `harneloop upgrade-unit <unit>` uma vez. Isso adiciona arquivos de protocolo ausentes sem substituir o material existente.

<a id="minimal-user-questions"></a>
## Perguntas mínimas ao usuário

Use como campos de contexto, não como questionário obrigatório. O agente pode criar a unidade provisória e inspecionar o espaço primeiro, depois perguntar só o que ainda importa:

1. No que este harness deve ajudar o agente a melhorar?
2. Onde será usado: fluxo de agente de código, agente de aplicação, pesquisa ou automação interna?
3. Como tratar os critérios de sucesso?
4. Como validar os resultados?
5. O ambiente de testes já existe, existe em parte, precisa ser construído ou ainda não está claro?

Não transforme a introdução em um formulário longo. Critérios de sucesso e artefatos são escolhas guiadas, não conhecimento exigido do usuário. Após inspecionar, execute `harneloop intake status <unit>` e classifique o contexto como confirmado, delegado, inferido, desconhecido ou não aplicável. Não transforme silenciosamente inferências em fatos confirmados.

Antes da primeira execução real, resolva campos relevantes e registre confirmação ou delegação explícita com `harneloop intake acknowledge`. Se uma referência, projeto-alvo, credencial ou julgamento ausente puder alterar materialmente o teste, peça diretamente ou entre em espera, em vez de só mencionar depois da configuração.

O Harneloop registra o mapeamento; não descobre sozinho endpoints, ferramentas MCP, comandos, capturas, renders ou caminhos de artefatos. O agente de introdução deve inspecionar projeto e ambiente reais, determinar como produzir artefatos e registrar esse mapeamento.

Toda unidade nova tem `operational-map.md`. Use como orientação atual: objetivo, sistemas e ferramentas, artefatos e evidências úteis, execução e reinicialização habituais, restrições, pontos frágeis, questões abertas, premissas a rever e locais de execuções ou evidências anteriores. Atualize quando fluxo, necessidades de evidência, premissas do ambiente ou automação mudarem.

O mapa é contexto e navegação, não procedimento rígido. O agente deve continuar raciocinando a partir da tarefa, inspecionar evidências e escolher a estratégia adequada à tentativa atual.

<a id="capability-gaps"></a>
## Lacunas de capacidade

Não presuma capacidades de Codex em todo agente operador. Um Hermes, OpenClaw, agente de app ou worker restrito pode não ter terminal, arquivos, navegador, gerenciadores de pacotes, servidores MCP, inspeção visual, banco de dados ou outras capacidades necessárias.

Separe duas camadas:

- Capacidades do agente operador: o que pode realmente usar ao construir a unidade.
- Ferramentas da unidade ou agente-alvo: projetadas na unidade ou fornecidas pelo contrato do ambiente.

Se faltar uma capacidade útil, registre em `operational-map.md`: o que falta, por quê, ferramenta ou dependência útil, mudanças de risco, custo, autenticação ou segurança e alternativa se o usuário recusar.

Capacidades locais de baixo risco podem ser instaladas, ativadas ou criadas se o ambiente permitir. Dependências maiores, credenciais, APIs pagas, contas do usuário, acesso externo, expansão de rede ou mudanças de segurança devem ser propostas primeiro.

Justifique adições por gargalos observados, tentativas falhas, artefatos ausentes ou melhoria esperada clara, não por especulação.

<a id="reuse-existing-work"></a>
## Reutilizar trabalho existente

O objetivo é o melhor harness verificado, não implementar do zero. Antes de criar uma capacidade, examine ferramentas do projeto, bibliotecas abertas, skills, servidores MCP, validadores, datasets, exemplos, documentação, pesquisa e material reutilizável. O agente pode instalar, adaptar, combinar ou aprender de trabalho adequado se melhorar resultados ou evitar esforço desnecessário.

Não reutilize cegamente. Registre fonte, versão ou revisão relevante, finalidade, licença ou atribuição, compatibilidade e evidências de valor. Revise material executável externo antes de confiar. Pergunte primeiro se introduzir credenciais, pagamentos, acesso externo, downloads relevantes, licenças restritivas, execução sensível ou mudanças importantes no ambiente. Se uma solução não servir, documente o motivo antes de substituí-la.

Respostas sugeridas sobre sucesso:

- Deixar o agente propor critérios de sucesso.
- Conheço o resultado exato de sucesso.
- Decidir após a primeira tentativa de linha de base.

Respostas sugeridas sobre validação:

- Melhor qualidade de validação.
- Validação visual ou orientada por artefatos.
- Validação equilibrada.
- Validação eficiente em recursos.
- Deixar o agente decidir por tarefa.

Pergunta adicional opcional:

- Há restrições, áreas protegidas, pontos de revisão humana ou limites de custo e tempo a respeitar?

<a id="how-answers-map-into-harneloop"></a>
## Como as respostas são mapeadas no Harneloop

- Objetivo, estratégia de sucesso, preferência de validação e artefatos sugeridos viram um resumo-alvo: `harneloop target set`.
- O mapa atual de trabalho é registrado e revisado em `operational-map.md`.
- Comandos, servidores MCP, passos manuais ou ferramentas personalizadas viram um contrato do ambiente: `harneloop environment connect`.
- O primeiro fluxo real vira um plano de tentativa: `harneloop attempt plan`.
- Saídas produzidas viram artefatos de execução: `harneloop run start`, `harneloop artifact add`, `harneloop run finish`.
- Qualidade do resultado e próxima decisão são registradas com `harneloop attempt conclude`.
- Mudanças no harness viram candidatos e exigem evidências antes da promoção.
- Padrões do usuário são gerenciados com `harneloop settings`.
- Unidades locais são listadas ou registradas com `harneloop units`. Depois, ID ou nome funciona nos comandos da unidade de qualquer diretório.

<a id="important-behavior"></a>
## Comportamento importante

Nem toda tarefa precisa de comando direto de teste. Em ambientes com ferramentas, como Blender MCP ou renderização SVG por agentes, declare ferramentas e artefatos no contrato. O agente planeja seu uso, a produção e inspeção de artefatos e a conversão de observações em evidências.

Busque ciclos repetidos sem exigir reinícios manuais de apps, reinstalação de addons, reinicialização de serviços ou coleta de arquivos. Automatize ou documente se for razoável; pergunte se houver risco, incerteza, custo ou tempo excessivo.

Se um artefato ou julgamento necessário atrasar, use `harneloop state wait`. Se a unidade parecer atingir um limite de capacidade, use `harneloop state stop` com motivo concreto e próxima ação.

Finalizar registra status, não prova qualidade. Inspecione artefatos e conclua cada tentativa: aceitar o harness, criar candidato, repetir com plano corrigido, pedir informações ou parar. Um bom primeiro resultado pode ser aceito sem candidato. Evidência esperada ausente não permite aprovação sem ressalvas.

Ao entrar ou retomar uma unidade, execute `harneloop brief <unit>`. O resumo gerado se limita a ela e não afeta trabalho não relacionado na mesma sessão.

<a id="candidate-batching-and-parallel-work"></a>
## Agrupamento de candidatos e trabalho paralelo

Um candidato é uma hipótese coerente, não cada edição ou commit. Agrupe mudanças relacionadas de ambiente, ferramentas, instruções ou validadores a julgar juntas. Separe problemas independentes; vários candidatos podem ficar abertos.

Classifique cada candidato pelo impacto:

- `target_harness`: muda o que o agente-alvo recebe ou pode fazer;
- `evaluation`: muda como saídas são observadas ou julgadas;
- `infrastructure`: muda configuração, execução, reinicialização ou coleta de artefatos;
- `mixed`: use só quando separar a questão fizer perder o sentido.

Escolha validação proporcional ao risco de falha:

- `structural`: parsing, schemas, verificações estáticas e integridade de metadados;
- `targeted`: testes de fumaça focados em ferramenta, avaliador ou caminho de infraestrutura;
- `representative`: tentativas reais e regressões relevantes para mudanças de comportamento;
- `full`: suítes amplas para mudanças de alto impacto e marcos de lançamento.

Não repita o benchmark completo após cada configuração. Acumule um candidato coerente, marque `ready` e colete evidências no nível declarado. Separe harness-alvo e avaliação quando possível para que o avaliador modificado não seja o único juiz do harness modificado.

Versões promovidas permanecem lineares. Ao promover um candidato, o Harneloop marca os demais na base antiga como `needs_rebase`. Reconcilie, faça rebase e reúna novas evidências na nova base; as antigas ficam como procedência.

<a id="target-and-environment-onboarding"></a>
# Introdução do alvo e do ambiente

O Harneloop não deve presumir que é dono do ambiente de testes do usuário.

Também não deve sugerir que a CLI descobre o ambiente automaticamente. O Harneloop armazena o mapeamento. O agente deve inspecionar espaço real, ferramentas, servidores MCP, scripts, endpoints, pastas de saída e caminhos de artefatos e registrar o mapa na unidade.

O entendimento de trabalho começa em `operational-map.md`. Mantenha atualizados objetivo, execução e reinicialização habituais, artefatos úteis, premissas frágeis e pontos a investigar. O mapa deve orientar, não prender a uma única receita de avaliação.

Registre também lacunas de capacidade. Ferramentas do agente operador são separadas das projetadas na unidade ou ambiente-alvo. Um agente restrito pode não ter terminal, navegador, arquivos, MCP, gerenciador de pacotes, inspeção visual, banco ou rede. Se isso bloquear ou enfraquecer a construção, registre o que falta, por quê, ferramenta ou dependência útil e alternativa.

O framework deve primeiro ajudar o agente a entender:

- para qual tarefa o harness é construído;
- o que conta como sucesso;
- quais artefatos coletar;
- quais padrões de falha importam;
- se já existe um ambiente de testes.

Depois, o agente cria um plano de tentativa. Não é um comando determinístico de teste, mas um fluxo escrito pelo agente para produzir e inspecionar algo relevante à tarefa-alvo.

<a id="setup-modes"></a>
## Modos de configuração

<a id="existing"></a>
### Existente

Use quando o usuário já tem um ambiente funcional.

Exemplo: um projeto Blender já tem scripts para executar cenas, capturar telas e exportar logs.

O agente deve conectar documentando:

- o comando de execução;
- caminhos de saída de artefatos;
- capturas, renders, logs ou resumos estruturados a coletar;
- notas específicas do ambiente.

Não reconstrua o ambiente salvo falha nas verificações ou pedido do usuário.

Reduza trabalho manual repetido. Se reiniciar serviços, redefinir apps, coletar artefatos ou preparar o ambiente puder ser automatizado com segurança, implemente ou documente. Pergunte se houver risco, incerteza ou custo elevado.

Adições devem ter evidências. Ferramentas locais de baixo risco podem ser instaladas, ativadas ou criadas se permitido. Proponha primeiro dependências maiores, credenciais, APIs pagas, acesso externo, contas do usuário, expansão de rede ou mudanças de segurança.

Configuração gerenciada ou assistida não exige construir tudo do zero. Busque no projeto e, se útil, documentação externa, ferramentas abertas, skills, bibliotecas, validadores, datasets, exemplos e trabalho anterior. Prefira soluções mantidas se melhorarem resultados esperados ou evitarem trabalho. Registre fonte, versão, finalidade, licença ou atribuição, compatibilidade e contribuição medida. Revise executáveis externos e respeite permissões normais de risco, custo, credenciais, acesso e segurança.

Ambientes existentes podem ser orientados por comandos ou ferramentas.

Orientado por comandos significa ter um comando direto. Orientado por ferramentas significa agir por servidor MCP, automação de navegador, plugin de design ou API de addon Blender.

<a id="assisted"></a>
### Assistida

Use se parte do ambiente existe, mas é preciso identificar o que falta.

Proponha o mínimo faltante para executar uma linha de base e capturar artefatos.

<a id="managed"></a>
### Gerenciada

Use se Harneloop ou o agente deve criar mais partes do ambiente do zero.

Mudanças de infraestrutura devem ser explícitas e sustentadas. A configuração gerenciada pode ser útil depois, mas não deve ser padrão em projetos que já funcionam.

<a id="attempt-plans"></a>
## Planos de tentativa

Muitas tarefas não se reduzem a `run this command`.

O agente-alvo pode precisar:

- usar ferramentas MCP;
- editar arquivos;
- criar cenas;
- construir UI;
- executar um navegador;
- pedir a um modelo para gerar um artefato;
- inspecionar visualmente a saída;
- exportar resumos estruturados;
- decidir quais evidências adicionais importam.

O Harneloop registra isso como plano de tentativa:

```powershell
harneloop attempt plan .\unit `
  --goal "Build a Blender scene with a cube on a table." `
  --method "Use Blender MCP tools to create objects, render, and export scene summary." `
  --action "Create table, cube, camera, and light." `
  --action "Render and capture screenshot." `
  --expected-artifact render `
  --expected-artifact scene_summary `
  --success-check "Cube rests on table." `
  --success-check "Objects are visible to camera."
```

Depois, uma execução pode referenciar a tentativa:

```powershell
harneloop run start .\unit --task "Baseline Blender spatial scene" --attempt-id attempt-0001
```

Após capturar artefatos, adicione observações:

```powershell
harneloop attempt observe .\unit attempt-0001 `
  --run-id run-0001 `
  --outcome failed `
  --summary "Render exists but cube floats above the table." `
  --finding "Likely z-coordinate placement issue."
```

Essas observações podem virar evidências candidatas ou casos de regressão.

<a id="agent-questions"></a>
## Perguntas do agente

Ao iniciar um harness real, pergunte apenas pelas informações ausentes:

- Qual é a família de tarefas-alvo?
- Quais artefatos de saída importam?
- Já existe um ambiente de testes funcional?
- O ambiente é orientado por comandos, ferramentas, manual ou personalizado?
- Se por comandos: qual executa o teste ou tarefa?
- Se por ferramentas: quais o agente usa?
- Onde são gravados capturas, renders, logs ou resumos estruturados?
- Quais falhas comuns devem virar casos de regressão?

<a id="blender-case"></a>
## Caso Blender

Para o projeto Blender existente, o modo provável é `existing`.

O modo de interação pode ser `mcp`, não `command`.

Pode não haver comando direto de teste. O agente-alvo usa Blender MCP e ferramentas de addon para mudar cenas, renderizar imagens, capturar telas, inspecionar objetos ou exportar resumos.

O primeiro passo não é instalar Blender nem criar um executor novo, mas conectar Harneloop a:

- à interface MCP ou ferramentas existente;
- às ferramentas que o agente deve usar;
- aos caminhos de renders, capturas, logs e resumos de cena;
- ao fluxo de linha de base para criar cenas e capturar artefatos.

Exemplo:

```powershell
harneloop environment connect .\blender-unit `
  --name "Existing Blender MCP environment" `
  --mode existing `
  --interaction-mode mcp `
  --description "Agent interacts with Blender through an MCP server and addon tools." `
  --tool create_object `
  --tool render_scene `
  --tool capture_screenshot `
  --tool export_scene_summary `
  --artifact-path "outputs/renders/*.png" `
  --note "Use MCP tools instead of looking for a single run command."
```

Depois, o Harneloop registra execuções, captura artefatos, armazena evidências e promove mudanças. O servidor Blender MCP continua sendo a interface de execução.

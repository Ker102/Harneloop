<a id="product-principles"></a>
# Princípios do produto

Harneloop é a identidade de produto escolhida. A arquitetura permanece independente de qualquer benchmark ou família de tarefas específica.

<a id="what-this-is"></a>
## O que é

O Harneloop é um framework que agentes usam para construir e melhorar o harness ao redor de si mesmos ou de outro agente-alvo.

O framework deve ajudar os agentes a:

- executar tentativas de tarefas;
- inspecionar artefatos reais;
- rastrear falhas até as execuções;
- manter um mapa operacional local da unidade com fluxo de trabalho, evidências, premissas do ambiente e questões em aberto;
- identificar lacunas de capacidade do agente operador separadamente das ferramentas da unidade ou do agente-alvo;
- pesquisar e reutilizar ferramentas, skills, bibliotecas, conjuntos de dados, exemplos e trabalhos anteriores adequados;
- propor patches candidatos para o harness;
- testar patches candidatos;
- promover apenas melhorias sustentadas por evidências;
- empacotar unidades de harness portáteis.

<a id="what-this-is-not"></a>
## O que não é

O Harneloop não é:

- um painel genérico de avaliação;
- um framework de grafos fixos de agentes;
- um sistema específico do Blender;
- um sistema de treinamento ou ajuste fino de modelos;
- uma pasta avulsa de prompts sem ciclo de vida.

<a id="core-design-tension"></a>
## Tensão central do projeto

O sistema é feito para modelos de IA generativa, portanto deve permitir raciocínio e exploração. Ao mesmo tempo, o framework precisa proteger a integridade do ciclo de vida.

A regra:

> Os agentes podem explorar livremente dentro dos candidatos. O motor controla a promoção.

`operational-map.md` preserva o entendimento atual do agente sobre uma unidade de harness sem transformá-lo em um script fixo. O agente deve usá-lo para se orientar, atualizá-lo conforme as evidências mudam e continuar raciocinando a partir da tarefa e dos artefatos atuais.

O framework não deve presumir que o agente que constrói uma unidade de harness pode tudo. Capacidades ausentes do agente operador devem ser identificadas, justificadas por evidências ou melhoria esperada clara e tratadas dentro dos limites de permissão apropriados antes de adicionar ferramentas, dependências, credenciais, serviços pagos ou acesso externo mais amplo.

O Harneloop otimiza o melhor desempenho verificado da tarefa, não a reconstrução de cada capacidade do zero. O agente operador deve examinar soluções existentes e pode adotá-las, adaptá-las, combiná-las ou aprender com elas quando melhorarem o harness. A reutilização deve permanecer verificável: registre o que foi usado e por quê, confira compatibilidade e valor observado, respeite licenças e atribuição e aplique os controles normais de permissão para segurança, credenciais, acesso externo, custo ou mudanças relevantes de infraestrutura.

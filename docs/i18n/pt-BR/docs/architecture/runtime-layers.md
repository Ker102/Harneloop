<a id="runtime-layers"></a>
# Camadas de execução

<a id="current-decision"></a>
## Decisão atual

Usar Python na primeira implementação de referência.

Preferir Rust a Go no futuro se o Harneloop precisar de um runtime nativo protegido.

<a id="why-rust-later"></a>
## Por que Rust no futuro

A camada nativa só deve existir se o framework precisar de garantias locais mais fortes quanto a:

- integridade do ciclo de vida;
- limites do estado protegido;
- snapshots de versões;
- reversão;
- armazenamento endereçado por conteúdo;
- empacotamento de artefatos;
- monitoramento de arquivos;
- supervisão de subprocessos;
- empacotamento para desktop.

Rust se encaixa melhor que Go no papel de núcleo protegido para esse tipo de produto.

<a id="agent-boundary"></a>
## Limite do agente

Rust não deve se tornar o espaço aberto de projeto do harness para o agente.

Os agentes devem continuar trabalhando por meio de:

- instruções em Markdown;
- manifestos YAML e JSON;
- schemas;
- diretórios de candidatos;
- comandos da CLI;
- contratos de artefatos.

A regra continua sendo:

> Os agentes podem explorar livremente dentro dos candidatos. O motor controla a promoção.

<a id="where-go-could-still-fit"></a>
## Onde Go ainda pode se encaixar

Go continua sendo uma boa opção para serviços hospedados futuros, coordenação de workers remotos ou infraestrutura de registro se o Harneloop crescer nessa direção.

<a id="concurrency-and-file-safety"></a>
# Concorrência e segurança de arquivos

Agentes podem iniciar comandos do Harneloop rapidamente em sequência ou em paralelo. Todo comando que lê um arquivo de controle, calcula um ID sequencial e grava o arquivo de volta deve proteger toda essa seção de leitura-modificação-gravação.

<a id="current-rule"></a>
## Regra atual

- Use um arquivo de bloqueio da unidade de harness para seções compartilhadas do ciclo de vida.
- Releia o arquivo YAML ou JSON relevante dentro do bloqueio.
- Aloque o próximo ID sequencial dentro do bloqueio.
- Grave YAML e JSON por substituição atômica de arquivos temporários.
- Libere o bloqueio somente após concluir a atualização do arquivo.

<a id="implemented-locks"></a>
## Bloqueios implementados

- `runs`: aloca IDs de execução.
- `run-<id>`: adiciona artefatos e finaliza uma execução.
- `attempts`: aloca IDs de tentativas.
- `attempt-<id>`: acrescenta observações de tentativas.
- `candidates`: aloca IDs de candidatos.
- `candidate-<id>-evidence`: aloca IDs de evidências.
- `lifecycle`: promove candidatos e reverte versões.
- `state`: atualiza `.evolve/state.json` e os arquivos de estado derivados.

Os bloqueios ficam em `.evolve/locks/`, um estado de execução controlado pelo framework e excluído dos pacotes portáteis.

<a id="rust-runtime-note"></a>
## Nota sobre o runtime Rust

Isso ainda não exige Rust. Bloqueios de arquivos e substituição atômica em Python são suficientes para a CLI alfa. Um runtime Rust futuro poderá cuidar de isolamento mais rigoroso, supervisão de processos e coordenação concorrente de arquivos mais confiável quando a superfície do produto se estabilizar.

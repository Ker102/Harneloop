<a id="development"></a>
# Desenvolvimento

<a id="repository-layout"></a>
## Estrutura do repositório

```text
src/harneloop/      Python reference implementation
tests/           Unit and behavior tests
docs/            Architecture and development notes
schemas/         Language-neutral data contracts
.github/         CI and repository automation
```

<a id="local-verification"></a>
## Verificação local

Instale o checkout uma vez como ferramenta editável no nível do usuário:

```powershell
uv tool install --editable .
```

O comando `harneloop` continuará disponível fora do repositório, refletindo alterações no código-fonte. Execute a verificação com:

```powershell
uv run python -m compileall src tests
uv run python -m unittest discover -s tests
harneloop doctor
```

<a id="devops-baseline"></a>
## Base de DevOps

O repositório deve manter:

- organização do código-fonte com `src/`;
- testes locais reproduzíveis;
- CI para versões suportadas do Python;
- nenhum ambiente virtual ou artefato de execução versionado;
- documentação explícita de segurança e contribuição;
- schemas independentes de linguagem para os registros centrais.

<a id="runtime-data"></a>
## Dados de execução

Rastros de execução, artefatos copiados, registros de execuções, planos de tentativas e experimentos são dados locais de trabalho. Não devem ser incluídos em pacotes portáteis thin, salvo quando um perfil de empacotamento posterior os incluir explicitamente.

<a id="pr-review-note"></a>
## Nota sobre revisão de PR

A revisão do CodeRabbit não é necessária durante o protótipo inicial. Se criar um PR, adicione a tag ou o label CodeRabbit-ignore configurado.

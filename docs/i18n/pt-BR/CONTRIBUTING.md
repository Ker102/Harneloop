<a id="contributing"></a>
# Contribuindo

O Harneloop está em alfa pública. Issues e contribuições com foco específico são bem-vindas enquanto a API pública e os formatos das unidades de harness se estabilizam.

<a id="development-setup"></a>
## Ambiente de desenvolvimento

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -e .
.\.venv\Scripts\python -m unittest discover -s tests
```

No macOS ou Linux:

```bash
python3 -m venv .venv
./.venv/bin/python -m pip install -e .
./.venv/bin/python -m unittest discover -s tests
```

<a id="pull-requests"></a>
## Pull requests

Limite cada pull request a um comportamento ou a uma parte da arquitetura.

Abra uma issue antes de um trabalho arquitetural significativo para alinhar o problema e o impacto na compatibilidade. Inclua testes para mudanças no ciclo de vida e atualize a documentação voltada a agentes quando o comportamento mudar.

Por enquanto, não solicite revisão automatizada do CodeRabbit. Se criar um PR enquanto o CodeRabbit estiver configurado, adicione o label ou a tag CodeRabbit-ignore do repositório antes de solicitar revisão.

<a id="standards"></a>
## Padrões

- Mantenha o núcleo do framework independente da família de tarefas.
- Não adicione premissas específicas do Blender a `src/harneloop`.
- Adicione ou atualize testes do comportamento do ciclo de vida.
- Mantenha os arquivos voltados a agentes legíveis em Markdown, YAML ou JSON.
- Não faça commits de segredos, artefatos locais de execução, ambientes virtuais ou pacotes gerados.

Ao contribuir, você concorda que sua contribuição seja licenciada sob a [Apache License 2.0](../../../LICENSE) do repositório.

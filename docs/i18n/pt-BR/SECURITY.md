<a id="security"></a>
# Segurança

O Harneloop é um framework que prioriza o uso local para unidades de harness criadas por agentes. Os limites de segurança importam porque agentes podem criar ferramentas, executar comandos e empacotar unidades reutilizáveis.

<a id="current-status"></a>
## Estado atual

Esta é uma alfa pública inicial. Não trate o Harneloop nem uma unidade de harness como um sandbox reforçado ou um limite de segurança.

<a id="rules"></a>
## Regras

- Nunca armazene segredos dentro das unidades de harness.
- Por padrão, não empacote arquivos `.env`, chaves privadas, credenciais, caches ou rastros brutos de execução.
- Trate ferramentas geradas para candidatos como não confiáveis até inspecioná-las.
- Use os comandos do framework para promoção, reversão e empacotamento.
- Exija aprovação explícita do usuário antes de ações destrutivas.

<a id="reporting"></a>
## Relato

Não divulgue suspeitas de vulnerabilidades em uma issue pública. Use o formulário privado de relato de vulnerabilidades do GitHub quando estiver disponível para este repositório. Caso contrário, contate o proprietário em privado pelo perfil do GitHub vinculado e inclua detalhes de reprodução, versões afetadas e impacto potencial.

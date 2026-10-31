# Contribuindo

Contribuições para a skill de apresentação de vendas são bem-vindas.

- Mantenha separados fatos, números com fonte, hipóteses, recomendações e pendências. A skill nunca afirma além do que os materiais, a coleta e a pesquisa sustentam.
- Não inclua nomes de clientes ou de pessoas, decisões comerciais reais, credenciais, URLs privadas, caminhos da sua máquina nem trechos de código de produtos privados. Exemplos têm de ser fictícios.
- Preserve as seis etapas e a parada na validação do documento de conteúdo, antes de qualquer plano ou código.
- Mantenha o `SKILL.md` em no máximo 600 palavras. O detalhe mora em `references/`.
- Não edite as quatro cópias da metodologia (`references/00-analise.md` a `references/03-direcao-criacao.md`) nem a linha de crédito na primeira linha de cada uma.
- Scripts usam só a biblioteca padrão do Python e nenhuma rede.
- Escreva em português do Brasil, sem travessão como separador, com títulos em sentence case.
- Antes de enviar, rode `python3 -m unittest discover -s tests -v` e `python3 scripts/verificar_pacote.py`. O segundo precisa imprimir `OK`.
- Quando a mudança alterar o comportamento da skill, explique o efeito para quem a usa e, se possível, registre uma rodada do cenário de `tests/cenario/` em `tests/resultados/`.
- Envie mudanças focadas, com uma explicação clara do efeito para o usuário.

Ao enviar uma contribuição, você concorda que ela pode ser distribuída sob a licença MIT do repositório.

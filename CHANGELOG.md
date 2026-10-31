# Changelog

Todas as mudanças relevantes deste pacote ficam registradas aqui. O formato segue o [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/) e as versões seguem o [versionamento semântico](https://semver.org/lang/pt-BR/).

## [1.0.0] - 2026-10-30

Primeira versão pública.

### Adicionado

- Skill `apresentacao-vendas` com seis etapas: destino e leitura, coleta com uma pergunta por mensagem, análise e pesquisa, conteúdo com revisão e validação, construção, e verificação com publicação. A skill para na validação do documento de conteúdo antes de qualquer plano ou código.
- Referências da skill: formato do documento de conteúdo, contrato de comportamento da apresentação, armadilhas de construção, revisão contra conteúdo superficial e as quatro cópias da metodologia Oferta Sexy (análise, copy, design system e direção de criação), cada uma com a linha de crédito na primeira linha.
- Validador do documento de conteúdo (`scripts/validar_conteudo.py`), só com a biblioteca padrão, que confere seções, campos de cada slide, ids, objeções, termos proibidos e dicas de formato.
- Plugin para o Claude Code (`plugin.json`, marketplace e agente coordenador) e metadados da skill para o Codex (`agents/openai.yaml`).
- Verificador do pacote (`scripts/verificar_pacote.py`), que confere o `SKILL.md`, links, JSON, versão contra este arquivo, caminhos locais, segredos, travessão nos textos autorais, linha de crédito e uma lista local opcional de termos privados.
- Testes unitários, cenário de teste fictício com prompt do avaliador cego e os resultados da linha de base sem a skill e da rodada com a skill, em `tests/resultados/`.
- README bilíngue, CONTRIBUTING e licença MIT.

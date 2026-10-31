---
name: apresentacao-vendas
description: Use quando o usuário pedir uma apresentação de vendas, deck comercial, slides para reunião de vendas no Meet ou presencial, demonstração guiada com roteiro para o vendedor, ou quiser replicar o modelo da apresentação de vendas do Vitio em outro produto.
---

# Apresentação de vendas

Slides para o cliente e roteiro automatizado do vendedor, com conteúdo 100% da Oferta Sexy. Entrega método, conteúdo e contrato, não motor de slides.

**Quando não usar.** Proposta comercial e landing page.

Regras do usuário e do projeto (`CLAUDE.md`, `AGENTS.md`) prevalecem sobre esta skill. Com o Superpowers, use `superpowers:brainstorming` na etapa 2 e `superpowers:subagent-driven-development` na etapa 5. Sem ele, as etapas bastam.

## As seis etapas

Código só a partir da etapa 5.

1. **Destino e leitura.** Pergunte o produto e onde a apresentação vai morar. Antes de outra pergunta, leia regras, memória, landing, análise, copy e design system do projeto.
2. **Coleta, uma pergunta por mensagem.** Espere cada resposta e grave-a com a pergunta, nas palavras do usuário, em `docs/apresentacao/coleta-<deck>.md`. Cubra a Fase 1 de `01-copy.md`, duração, formato, quem conduz e quem decide, números do diagnóstico, fórmula da conta, o que não falar, telas reais e segmentos. Pule o que os materiais respondem.
3. **Análise e pesquisa.** Sem análise estratégica, faça a de `00-analise.md` em `docs/apresentacao/analise-<deck>.md` e escolha o ângulo com o usuário. Número dos materiais com fonte entra como veio, registrando fonte, amostra e o que mede; o resto vem de fonte primária, em `docs/pesquisa/AAAA-MM-DD-numeros-de-apoio.md`. Sem fonte nem como pesquisar, fica fora dos slides.
4. **Conteúdo, revisão e validação.** Escreva `docs/apresentacao/conteudo-<deck>.md` no formato de `conteudo.md`, passe no validador e revise com `revisao.md` num subagente separado. **Pare aqui**, mostre o documento e só siga quando o usuário validar. Com o Superpowers, o documento substitui o spec do brainstorming, e o `superpowers:writing-plans` só vem depois que validador, revisão e usuário aprovam.
5. **Construção.** Plano e tarefas revisadas na stack do site, seguindo `contrato.md` e `armadilhas.md`. Use o design system do produto ou, sem ele, `02-design-system.md` e `03-direcao-criacao.md` adaptados para slide.
6. **Verificação e publicação.** `contrato.md` conferido num navegador visível. PR e deploy pelo fluxo do produto, com autorização do usuário.

## O que não pode faltar

- Roteiro que anda com os slides, põe os números do cliente nas falas, mostra a objeção do momento com resposta e slide de prova e cronometra slide e reunião.
- Meet, presencial e PDF depois, sem nada do roteiro.
- Revisão contra conteúdo superficial.

## Erros comuns

- **Afirmar além do material.** Todo fato sai dos materiais, da coleta ou da pesquisa; o que faltar, pergunte.
- **Slide sem pergunta.** Todo slide pergunta algo ao cliente.
- **Objeções só no fim.** Cada slide do meio liga as objeções do momento.
- **Objeção sem prova.** Toda objeção aponta o slide que prova o que ela questiona.
- **Tela só para olhar.** No Meet, o cliente escolhe e o vendedor clica; presencial, o cliente pode tocar.
- **Prova que vale para o jeito de hoje.** Se vale também para a alternativa gratuita, mostre o que só o produto faz.
- **Pergunta do comprador sem resposta.** Responda também confiança, casos, segurança dos dados e risco, com o compromisso total do contrato.
- **Slides antes da análise.** O mapa liga cada parte da análise a uma peça.
- **Conta sem plano para dado faltando.** Diga o que tela e fala fazem sem esse número.

## Referências

| Etapa | Arquivos |
|---|---|
| 2 | [01-copy.md](references/01-copy.md) |
| 3 | [00-analise.md](references/00-analise.md) |
| 4 | [conteudo.md](references/conteudo.md), [validar_conteudo.py](scripts/validar_conteudo.py), [revisao.md](references/revisao.md) |
| 5 | [contrato.md](references/contrato.md), [armadilhas.md](references/armadilhas.md), [02-design-system.md](references/02-design-system.md), [03-direcao-criacao.md](references/03-direcao-criacao.md) |

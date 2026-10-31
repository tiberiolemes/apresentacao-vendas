# Conteúdo da apresentação: Painel Padaria

Fixture de teste com produto fictício. Os números e a fonte abaixo não são dados reais.

## Mapa da Oferta Sexy
| Parte da análise | Onde entra |
|---|---|
| Ângulo | Fio da reunião. A sobra de pão é dinheiro que sai do caixa todo dia, e todo slide volta a ela. |
| Problema na voz do cliente | Slide `problema`, com a frase "Eu assei demais e joguei fora de novo" e o custo da sobra no mês. |
| Inimigo do resultado | Slide `problema`, onde o caderno e o palpite do padeiro aparecem como o jeito de hoje que não mostra a sobra por horário. |
| Mecanismo único | Slide `como-funciona`, com a sugestão de fornada que cruza a venda dos últimos dias com o dia da semana. |
| Diferenciais | Slide `como-funciona`, onde o cliente clica no produto e no horário e vê a sugestão mudar. |
| Verdades | Falas do roteiro nos slides `problema` e `conta`. |
| Objeções | Painel de objeções, com oito entradas e os slides de prova. |
| Proibições | Seção "O que não falar". |

## Slides
### `capa` Painel Padaria, a fornada certa para cada hora
- **Cliente vê:** O nome do produto, a frase "A fornada certa para cada hora do dia" e o nome da padaria do cliente.
- **Interação:** Nenhuma. O vendedor avança com a seta.
- **Tempo:** 1 min
- **Análise:** Ângulo.
- **Falar:**
  - Obrigado por separar esse tempo.
  - Somos uma equipe que só trabalha com padaria.
  - Vou mostrar uma coisa só, e você me diz se faz sentido para a sua padaria.
- **Pergunta:** O que você precisa levar desta conversa para valer o seu tempo?
- **Dica:** Comece pelo que o cliente quer levar, não pelo produto.
- **Objeções:** nenhuma

### `combinado` Como vamos usar os próximos minutos
- **Cliente vê:** Três itens do combinado, com o que vamos fazer, quanto tempo leva e como terminamos.
- **Interação:** O cliente toca em cada item para confirmar.
- **Tempo:** 2 min
- **Análise:** Ângulo.
- **Falar:**
  - Primeiro eu pergunto da sua rotina.
  - Depois mostro o painel com os seus números.
  - No fim, a gente decide juntos se faz sentido ou não.
- **Pergunta:** Pode ser assim, e você me interrompe se algo não bater com a sua padaria?
- **Dica:** Peça o combinado em voz alta e espere o sim antes de seguir.
- **Objeções:** nenhuma

### `problema` Eu assei demais e joguei fora de novo
- **Cliente vê:** A frase do dono, o custo da sobra no mês com os números do cliente e o caderno como jeito de hoje.
- **Interação:** O cliente informa a sobra média por dia e o custo do mês aparece na hora.
- **Tempo:** 4 min
- **Análise:** Problema na voz do cliente e inimigo do resultado.
- **Falar:**
  - Quase toda padaria assa um pouco a mais para não deixar o balcão vazio.
  - Essa sobra de {perda_diaria} reais por dia vira {perda_mensal} reais no mês.
  - O caderno e a experiência do padeiro seguram o negócio. O que eles não mostram é a sobra por horário.
- **Pergunta:** Quanto sobra, em média, no fim de um dia normal?
- **Dica:** Escute mais do que fala.
- **Objeções:** `ja-controlo-no-caderno`

### `como-funciona` Veja a próxima fornada antes de acender o forno
- **Cliente vê:** A tela de fornadas, com a venda por horário e a sugestão da próxima fornada para cada produto.
- **Interação:** O cliente escolhe um produto e um horário, e a sugestão da fornada muda na hora.
- **Tempo:** 5 min
- **Análise:** Mecanismo único e diferenciais.
- **Falar:**
  - Escolha o produto que mais sobra na sua padaria.
  - Repare que o painel olha a venda dos últimos dias no mesmo horário.
  - A sugestão é um ponto de partida. A decisão da fornada continua sendo do padeiro.
- **Pergunta:** Qual produto sobra mais na sua padaria?
- **Dica:** Deixe o cliente clicar sozinho antes de explicar a tela.
- **Objeções:** `preco-alto`

### `conta` Quanto a sobra precisa cair para o painel se pagar
- **Cliente vê:** Campos de sobra por dia, dias abertos no mês e mensalidade, e o percentual da sobra que precisa cair.
- **Interação:** O cliente digita os três números e o percentual atualiza a cada tecla.
- **Tempo:** 3 min
- **Análise:** Verdades e a conta.
- **Falar:**
  - Com {perda_diaria} reais de sobra por dia, a padaria perde {perda_mensal} reais no mês.
  - A mensalidade de {mensalidade} reais se paga se a sobra cair {percentual} por cento.
  - Não prometemos esse resultado. Mostramos o tamanho do desafio.
- **Falar sem comparação:**
  - Sem a sobra do dia, não dá para calcular o percentual.
  - Vamos pesar a sobra por três dias e voltar a esta tela.
- **Pergunta:** Esse percentual parece alcançável para a sua padaria?
- **Pergunta sem comparação:** Você consegue pesar a sobra por três dias?
- **Dica:** Depois de mostrar o percentual, fique em silêncio e espere a reação do cliente.
- **Objeções:** `resultado-garantido`

### `proximo-passo` Instalação com data marcada
- **Cliente vê:** A data e a hora marcadas para a instalação e a lista do que a padaria separa antes.
- **Interação:** O cliente escolhe uma data no calendário e confirma.
- **Tempo:** 2 min
- **Análise:** Ângulo e implantação.
- **Falar:**
  - A instalação leva uma manhã e não para o balcão.
  - Você só separa a lista de produtos e o acesso ao caixa.
  - Se não fizer sentido, você cancela e leva os seus dados.
  - Que dia desta semana é melhor para você?
- **Pergunta:** Qual dia da semana fica melhor para instalar?
- **Dica:** Saia da reunião com a data escolhida, mesmo que provisória.
- **Objeções:** `nao-tenho-tempo`, `preciso-pensar`

## Objeções
### `preco-alto` Caro para o meu tamanho.
- **Resposta:** Mostre a conta com a sobra dele. O painel se paga quando a sobra cai o percentual que a tela mostra.
- **Quem levanta:** Dono de padaria pequena.
- **Alerta:** Não prometa que a sobra vai cair. Mostre só quanto precisa cair.
- **Slides:** `conta`

### `ja-controlo-no-caderno` Eu já controlo no caderno e funciona.
- **Resposta:** O caderno mostra o que saiu no dia. O painel mostra a sobra por horário, que o caderno não separa.
- **Quem levanta:** Dono com muitos anos de padaria.
- **Slides:** `problema`

### `equipe-nao-usa` Meu pessoal não vai usar sistema.
- **Resposta:** O padeiro só olha a sugestão da fornada. Não há digitação extra no balcão.
- **Quem levanta:** Gerente de turno.
- **Slides:** `como-funciona`

### `integra-com-caixa` Isso conversa com o meu caixa?
- **Resposta:** O painel lê a venda que o caixa já registra. Confirme o modelo do caixa antes de responder sim.
- **Quem levanta:** Gerente ou responsável por compras.
- **Alerta:** Só diga que integra com o caixa depois de conferir a lista de caixas compatíveis.
- **Slides:** `como-funciona`

### `dados-seguros` Onde ficam os meus dados de venda?
- **Resposta:** Ficam na conta da padaria, e só quem ela autoriza vê. Ela pode exportar tudo quando quiser.
- **Quem levanta:** Dono ou sócio.
- **Slides:** `como-funciona`

### `nao-tenho-tempo` Não tenho tempo para implantar.
- **Resposta:** A instalação leva uma manhã, com data marcada agora, e não para o balcão.
- **Quem levanta:** Dono que também trabalha no balcão.
- **Slides:** `proximo-passo`

### `preciso-pensar` Preciso pensar e falar com o meu sócio.
- **Resposta:** Faz sentido. Marque agora a data da próxima conversa, com o sócio presente, e deixe a instalação provisória.
- **Quem levanta:** Dono com sócio.
- **Slides:** `proximo-passo`

### `resultado-garantido` Vocês garantem que a sobra cai?
- **Resposta:** Não garantimos. A conta mostra quanto a sobra precisa cair para a mensalidade se pagar, e o resultado depende da rotina da padaria.
- **Quem levanta:** Dono mais cauteloso.
- **Alerta:** Nunca aceite prometer percentual de redução.
- **Slides:** `conta`

## O que não falar
- Não prometer que a sobra vai cair, nem dar percentual de redução como certo.
- Não dizer que o painel integra com um caixa que não está na lista de compatíveis.
- Não criticar o caderno nem o jeito de trabalhar do padeiro.
- Não falar de concorrente pelo nome.

## A conta
- **Entradas:** `{perda_diaria}` (sobra média por dia, em reais), `{dias}` (dias abertos no mês) e `{mensalidade}` (valor do plano, em reais).
- **Fórmula:** `{perda_mensal}` = perda_diaria * dias; `{percentual}` = mensalidade / perda_mensal * 100, com uma casa decimal.
- **Exemplos:**
  - Sobra de 100 reais por dia, 30 dias abertos e mensalidade de 180 reais dão perda de 3.000 reais no mês e 6,0 por cento.
  - Sobra de 60 reais por dia, 25 dias abertos e mensalidade de 150 reais dão perda de 1.500 reais no mês e 10,0 por cento.
  - Sobra de 5 reais por dia, 20 dias abertos e mensalidade de 180 reais dão perda de 100 reais no mês e 180,0 por cento, e a tela avisa que a sobra sozinha não paga a mensalidade.
- **Dado vazio ou zero:** Com qualquer entrada vazia ou zero, a perda do mês e o percentual não aparecem, nunca há divisão por zero e a tela mostra só a mensalidade e pede o número que falta.

## Números de apoio
### `sobra-media` Padarias de exemplo perdem parte do que assam todo dia
- **Fonte:** Estudo fictício de exemplo, usado só nos testes desta skill.
- **Amostra:** 400 padarias fictícias de cidades médias.
- **O que mede:** Percentual da produção diária que não foi vendido no mesmo dia, declarado pelo dono.
- **Uso:** slide `problema`

## PDF
- Entram os slides `capa`, `problema`, `como-funciona`, `conta` e `proximo-passo`. O `combinado` fica de fora.
- Cada interação aparece parada no estado final, com os números do cliente preenchidos.
- O roteiro, a dica e a lista do que não falar nunca entram no PDF.

## As 14 perguntas do comprador
| # | Pergunta | Onde responde |
|---|---|---|
| 1 | Eu entendi o que esse produto faz? | `capa` |
| 2 | Isso resolve um problema que eu tenho agora? | `problema` |
| 3 | É para uma empresa como a minha? | `capa` |
| 4 | Como exatamente funciona? | `como-funciona` |
| 5 | Integra com o que eu já uso? | fala de `como-funciona` e objeção `integra-com-caixa` (`como-funciona`) |
| 6 | Meu time vai realmente adotar? | objeção `equipe-nao-usa` (`como-funciona`) |
| 7 | Quanto trabalho dá para implementar? | `proximo-passo` |
| 8 | Eu confio nessa empresa? | fala da `capa` |
| 9 | Outras empresas como a minha usam e têm resultado? | número `sobra-media` no `problema` |
| 10 | Meus dados estão seguros? | objeção `dados-seguros` (`como-funciona`) |
| 11 | Quanto custa? | `conta` |
| 12 | Vale o investimento? | `conta` |
| 13 | Qual o risco se eu testar? | fala de `proximo-passo` |
| 14 | Qual o próximo passo e o que acontece depois? | `proximo-passo` |

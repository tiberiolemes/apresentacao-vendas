# Documento de conteúdo

Leia este arquivo na etapa 4, antes de escrever o documento de conteúdo. Esse documento é o design escrito da apresentação. Nenhuma linha de código nasce antes de ele estar completo, revisado e validado por quem pediu a apresentação.

No projeto do produto, ele se chama `docs/apresentacao/conteudo-<deck>.md`. Depois de escrever, rode o validador da skill e corrija cada linha que ele devolver.

```bash
python3 <pasta-da-skill>/scripts/validar_conteudo.py docs/apresentacao/conteudo-<deck>.md
```

O script mora na pasta da skill, e o documento mora no projeto do produto. Rode o comando a partir da raiz do projeto, trocando `<pasta-da-skill>` pelo caminho da skill instalada.

Com tudo certo, o script imprime `OK (N slides, M objeções)` e sai com 0. Com problema, imprime um por linha e sai com 1. O validador confere forma, não profundidade. Passar nele é o piso. Frase que serviria para qualquer produto, número que diz mais do que a fonte mede e slide que só se olha continuam sendo trabalho da revisão em `references/revisao.md`.

## Estrutura do documento

O documento começa com ``# Conteúdo da apresentação: <produto>`` e tem estas oito seções `##`, com estes nomes exatos, nesta ordem.

1. `## Mapa da Oferta Sexy`
2. `## Slides`
3. `## Objeções`
4. `## O que não falar`
5. `## A conta`
6. `## Números de apoio`
7. `## PDF`
8. `## As 14 perguntas do comprador`

O roteiro não é uma seção à parte. Ele mora dentro de cada slide.

Regras de escrita que valem para o documento inteiro:

- cada campo ocupa uma linha no formato ``- **Nome:** texto``, e o texto fica na mesma linha do rótulo;
- subitens usam recuo de dois espaços ou mais, ou um tab, depois um traço e um espaço (``  - frase``), sempre logo abaixo do campo a que pertencem;
- slides, objeções e números de apoio começam por um título ``### `id` texto``, com o id entre crases, em minúsculas, sem acento, só letras, números e hífen (`proximo-passo`, nunca `Próximo passo`). Cada id aparece uma vez dentro da sua seção;
- campo com rótulo e sem texto vale como campo faltando;
- sem travessão em lugar nenhum, nem na lista do que não falar. Separe ideias com ponto, vírgula ou ponto e vírgula;
- os termos a seguir ficam fora do documento, com uma exceção. Na seção "O que não falar" eles podem aparecer, porque ali a lista existe para dizer o que o vendedor evita. Em qualquer outro lugar, o validador acusa. Os termos são solução completa, revolucionário, líder de mercado, potencialize, transforme seu negócio, próximo nível, tudo em um só lugar e disruptivo. O validador confere só esses oito; a revisão cobra por inteiro a seção "Proibições absolutas" de `references/01-copy.md`.

## Mapa da Oferta Sexy

Tabela com duas colunas, "Parte da análise" e "Onde entra". Ela prova que a análise estratégica chegou inteira à apresentação. A primeira coluna usa exatamente os nomes da tabela abaixo, e a segunda diz qual peça da apresentação usa aquela parte.

| Parte da análise | Peça da apresentação que a usa |
|---|---|
| Ângulo | O ângulo escolhido é o fio da reunião. Todo slide volta a ele. |
| Problema na voz do cliente | Abre a conversa, junto com o custo de conviver com o problema. |
| Inimigo do resultado | Vira o slide do jeito de hoje que não resolve, validando o que o cliente já faz. |
| Mecanismo único | É o momento marcante da reunião. |
| Diferenciais | Viram telas que o cliente clica, não telas que ele só olha. |
| Verdades | Viram falas do roteiro. |
| Objeções | Viram o painel do vendedor. |
| Proibições | Viram a lista do que o vendedor não pode falar. |

Parte da análise sem peça correspondente não pode ficar com a linha vazia. Escreva na própria linha a justificativa, que explica por que aquela parte não tem lugar nesta apresentação. A revisão julga se a justificativa se sustenta.

## Slides

Um bloco por slide, na ordem em que aparecem na reunião. O título do bloco é o texto que aparece na tela. Cada bloco traz os oito campos abaixo, todos com texto.

| Campo | O que escrever |
|---|---|
| `Cliente vê` | O que está na tela, em uma frase. Inclui os números do cliente quando houver. |
| `Interação` | O que o cliente faz na tela. Slide de produto que só se olha não passa na revisão. Se não há interação, escreva "Nenhuma" e diga por quê. |
| `Tempo` | Minutos previstos, no formato `2 min` ou `1,5 min`. |
| `Análise` | Qual parte da análise o slide carrega. |
| `Falar` | Subitens com as frases do vendedor (veja o roteiro, abaixo). |
| `Pergunta` | A pergunta que o vendedor faz neste momento. |
| `Dica` | Como conduzir o momento. |
| `Objeções` | Os ids das objeções prováveis aqui, entre crases e separados por vírgula, ou a palavra nenhuma. |

O esqueleto padrão, que se ajusta ao produto, tem capa, combinado, diagnóstico, o problema, o jeito de hoje, como funciona, telas do produto, pesquisa com fonte, preço, a conta com os números do cliente, implantação e próximo passo com data marcada. Tire o que o produto não pede e acrescente o que ele exige.

Sobre ``Objeções: nenhuma``:

- só vale no primeiro slide, no segundo e no último;
- um slide do meio da reunião sempre tem objeção provável. Se parece não ter, falta pensar no que quem decide teme naquele ponto.

## Roteiro por slide

O roteiro vive nos campos `Falar`, `Pergunta`, `Dica` e `Objeções` de cada slide.

- `Falar` usa frases curtas, uma ideia por frase, escritas para serem ditas em voz alta.
- Fala que usa número do cliente leva marcador entre chaves, em minúsculas e com sublinhado, como `{alunos}` ou `{perda_diaria}`. O marcador é o nome de uma entrada ou de um resultado da conta, o mesmo que aparece na seção "A conta".
- Marcador de nome não leva artigo nem depende de gênero, porque o mesmo marcador recebe nomes de qualquer gênero. Escreva "para {cliente}" ou "com os números de {cliente}", nunca "da {cliente}" nem "o {pet}".
- Quando a frase ficaria absurda, escreva a variante sem comparação. Isso acontece com dado faltando (o cliente não sabe o número) e com comparação invertida (o número dele já está melhor que a referência). Os dois campos abaixo são opcionais e entram logo depois do campo original.

```markdown
- **Falar sem comparação:**
  - Frase que funciona sem o número.
- **Pergunta sem comparação:** Pergunta que funciona sem o número.
```

O vendedor usa a variante quando o dado falta ou a comparação não faz sentido. Toda fala com marcador que pode ficar sem valor ou sair do esperado merece a sua variante.

## Painel de objeções

Por volta de dez objeções, nunca menos de oito. O título é a fala do cliente, como ele diria.

| Campo | O que escrever |
|---|---|
| `Resposta` | A resposta curta que o vendedor dá. |
| `Quem levanta` | Quem costuma levantar a objeção (cargo ou papel, não nome de pessoa). |
| `Alerta` | Opcional. O que o vendedor não pode deixar escapar nessa resposta. |
| `Slides` | Os ids dos slides de prova, entre crases. Pelo menos um, e todos existem. |

Toda objeção citada em `Objeções` de um slide precisa existir nesta seção, com o mesmo id.

## O que não falar

Lista simples, com pelo menos um item. As regras vêm de duas fontes, as proibições da análise estratégica e as decisões de oferta do produto, como promessa que ele não confirmou, desconto que não existe e concorrente que não se cita. Cada item é uma regra que o vendedor entende de relance.

## A conta

A conta mostra quanto precisa acontecer para o produto se pagar. Ela nunca promete resultado.

| Campo | O que escrever |
|---|---|
| `Entradas` | Os números que o diagnóstico pede ao cliente, na mesma linha, com o marcador de cada um. |
| `Fórmula` | A fórmula em uma linha, com o marcador de cada resultado que as falas usam. |
| `Exemplos` | Subitens com casos numéricos completos (entradas e resultado). Eles viram teste na construção, então use números que dão resultado exato. Inclua um caso de borda. |
| `Dado vazio ou zero` | O que a tela mostra quando falta entrada ou ela vale zero. Nunca divide por zero e nunca mostra um resultado inventado. |

## Números de apoio

Um bloco por número, com o id e a frase que aparece no slide ou no roteiro.

| Campo | O que escrever |
|---|---|
| `Fonte` | Para número dos materiais do produto, o material que traz o número, como veio (por exemplo, a pesquisa interna que esse material cita), sem dizer sobre a fonte nada que o material não diga. Para número pesquisado, a fonte primária, com título e ano. Escrever "pendente" vale como fonte faltando, então termine a pesquisa antes de validar. |
| `Amostra` | Quem ou o que a fonte mediu, e quantos. |
| `O que mede` | O texto exato do que a fonte mede. A frase do slide não pode dizer mais do que isso. |
| `Uso` | ``slide `id` `` para o número que vai à tela, ou `reserva` para o que fica só no roteiro, pronto para quando o cliente perguntar. |

## PDF

Lista com pelo menos um item. Diga quais slides entram no PDF e como cada interação aparece parada. A regra geral é mostrar o estado final, com os números do cliente preenchidos. O roteiro, a dica e a lista do que não falar nunca entram no PDF.

## As 14 perguntas do comprador

Tabela com três colunas e as 14 linhas, na ordem abaixo. Em "Onde responde", cite entre crases o slide que responde. A pergunta que não cabe na tela fica numa fala do roteiro, e a linha cita o slide cuja fala traz a resposta.

| # | Pergunta |
|---|---|
| 1 | Eu entendi o que esse produto faz? |
| 2 | Isso resolve um problema que eu tenho agora? |
| 3 | É para uma empresa como a minha? |
| 4 | Como exatamente funciona? |
| 5 | Integra com o que eu já uso? |
| 6 | Meu time vai realmente adotar? |
| 7 | Quanto trabalho dá para implementar? |
| 8 | Eu confio nessa empresa? |
| 9 | Outras empresas como a minha usam e têm resultado? |
| 10 | Meus dados estão seguros? |
| 11 | Quanto custa? |
| 12 | Vale o investimento? |
| 13 | Qual o risco se eu testar? |
| 14 | Qual o próximo passo e o que acontece depois? |

A tabela do documento fica assim.

```markdown
| # | Pergunta | Onde responde |
|---|---|---|
| 1 | Eu entendi o que esse produto faz? | `capa` |
| 4 | Como exatamente funciona? | `como-funciona` |
```

## O que o validador confere

Cada problema impresso começa por um destes trechos. Depois do trecho pode vir uma dica entre parênteses, que diz como corrigir.

| Trecho | Quando aparece |
|---|---|
| ``seção faltando: <nome>`` | Uma das oito seções não existe. |
| ``slide `<id>`: <campo>`` | O slide não tem o campo, ou o campo está sem texto. Em `Falar`, falta pelo menos um subitem. |
| ``slide `<id>`: Tempo`` | O tempo não segue `2 min` ou `1,5 min`. |
| ``id inválido: <id>`` | O id tem maiúscula, acento, espaço ou símbolo, ou se repete na seção. |
| ``slide `<id>`: sem objeção`` | Slide do meio com a palavra nenhuma. |
| ``objeção inexistente: <id>`` | Um slide cita uma objeção que não está no painel. |
| ``objeções: <n>`` | O painel tem menos de oito objeções. |
| ``objeção `<id>`: <campo>`` | Falta `Resposta`, `Quem levanta` ou um slide de prova que exista. |
| ``o que não falar vazio`` | A seção não tem item. |
| ``conta: <campo>`` | Falta `Entradas`, `Fórmula`, `Dado vazio ou zero` ou um exemplo. |
| ``número `<id>`: <campo>`` | Falta `Fonte` (ou ela é "pendente"), `Amostra`, `O que mede` ou `Uso`, ou o slide citado em `Uso` não existe. |
| ``mapa: <parte>`` | O mapa não tem linha com texto para essa parte. |
| ``pergunta <n>`` | A linha da pergunta não existe ou não cita nenhum slide existente entre crases. |
| ``PDF vazio`` | A seção não tem item. |
| ``travessão`` | O documento tem um travessão. |
| ``termo proibido: <termo>`` | O documento tem um dos termos proibidos fora da seção "O que não falar", com qualquer combinação de maiúsculas e minúsculas. |

Os campos opcionais `Alerta`, `Falar sem comparação` e `Pergunta sem comparação` são aceitos e nunca exigidos.

## Exemplo curto

Trecho de um documento para um produto fictício, o Estoque Certo, que ajuda lojas de material de construção a controlar o estoque. Os números e a fonte são inventados para o exemplo. O documento real traz as oito seções completas, com os slides do esqueleto e pelo menos oito objeções.

````markdown
# Conteúdo da apresentação: Estoque Certo

## Mapa da Oferta Sexy
| Parte da análise | Onde entra |
|---|---|
| Ângulo | Fio da reunião. Cliente que pede e a loja não tem é venda que vai para o vizinho. |
| Mecanismo único | Slide `como-funciona`, com o alerta de reposição que olha a venda dos últimos 90 dias. |
| Proibições | Sem peça nesta apresentação, porque a análise não registrou nenhuma proibição do produto. |

## Slides
### `problema` O cliente pediu e a prateleira estava vazia
- **Cliente vê:** A frase do dono, o número de pedidos perdidos no mês e o caderno de compras como jeito de hoje.
- **Interação:** O cliente informa quantos pedidos por semana ficam sem produto e o valor do mês aparece.
- **Tempo:** 4 min
- **Análise:** Problema na voz do cliente.
- **Falar:**
  - Todo dono de loja já ouviu "não tem" do próprio balcão.
  - {pedidos_perdidos} pedidos por semana, a {ticket} reais cada, são {perda_mensal} reais por mês.
- **Falar sem comparação:**
  - Sem o número de pedidos perdidos, vamos contar durante uma semana e voltar aqui.
- **Pergunta:** Quantas vezes por semana alguém pede algo que você não tem?
- **Dica:** Deixe o cliente chegar ao número sozinho.
- **Objeções:** `conheco-minha-loja`

## Objeções
### `conheco-minha-loja` Eu conheço a minha loja, não preciso de sistema.
- **Resposta:** O conhecimento do dono continua valendo. O alerta só mostra o que a memória não alcança, como o item que vende pouco e acaba de repente.
- **Quem levanta:** Dono com muitos anos de loja.
- **Alerta:** Não critique o jeito de comprar de hoje.
- **Slides:** `problema`

## A conta
- **Entradas:** `{pedidos_perdidos}` (pedidos sem produto por semana), `{ticket}` (valor médio do pedido, em reais) e `{mensalidade}` (plano, em reais).
- **Fórmula:** `{perda_mensal}` = pedidos_perdidos * ticket * 4, contando quatro semanas no mês; `{pedidos_a_recuperar}` = mensalidade / ticket, arredondado para cima.
- **Exemplos:**
  - 3 pedidos perdidos por semana, ticket de 150 reais e mensalidade de 300 reais dão perda de 1.800 reais no mês e pedem 2 pedidos recuperados por mês.
  - 5 pedidos perdidos por semana, ticket de 70 reais e mensalidade de 300 reais dão perda de 1.400 reais no mês e pedem 5 pedidos recuperados por mês.
- **Dado vazio ou zero:** Com ticket vazio ou zero, a tela mostra só a mensalidade e pede o valor médio do pedido.

## Números de apoio
### `venda-perdida` Parte das vendas de lojas de exemplo se perde por falta de produto
- **Fonte:** Pesquisa inventada para este exemplo, 2026.
- **Amostra:** 300 lojas fictícias de material de construção.
- **O que mede:** Percentual de pedidos que o balcão não atendeu por falta do item, segundo o dono.
- **Uso:** slide `problema`
````

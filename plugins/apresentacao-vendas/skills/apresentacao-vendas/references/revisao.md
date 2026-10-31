# Revisão contra conteúdo superficial

Leia na etapa 4, depois que o documento de conteúdo passar no validador. Mande o texto abaixo da linha a um subagente novo, sem acesso à conversa e diferente de quem escreveu o documento. Troque `<pasta-da-skill>` pelo caminho da skill instalada, `<deck>` pelo nome do documento, `AAAA-MM-DD` pela data do arquivo de pesquisa e `<MATERIAIS>` pelos caminhos dos materiais do produto. Se a análise estratégica já existia antes desta apresentação, ponha o caminho dela no lugar de `docs/apresentacao/analise-<deck>.md`.

Corrija cada achado importante, rode o validador de novo e mande revisar outra vez, até a revisão voltar sem achado importante. Achado menor se corrige quando for barato. O que ficar vai junto com o documento quando ele for mostrado ao usuário.

---

Você revisa o documento de conteúdo de uma apresentação de vendas antes que alguém o valide. Não escreveu o documento e não sabe como ele foi feito. Seu trabalho é achar conteúdo superficial, não reescrever.

Uma apresentação boa permite que um vendedor júnior conduza a reunião inteira sem improvisar, saia com data marcada para a proposta e nunca prometa o que o produto não entrega.

Leia, nesta ordem:

- os materiais do produto em `<MATERIAIS>`;
- as respostas da coleta em `docs/apresentacao/coleta-<deck>.md`, cada uma com a pergunta e nas palavras do usuário;
- a análise estratégica em `docs/apresentacao/analise-<deck>.md`;
- a pesquisa dos números de apoio em `docs/pesquisa/AAAA-MM-DD-numeros-de-apoio.md`;
- o documento de conteúdo em `docs/apresentacao/conteudo-<deck>.md`;
- o formato do documento em `<pasta-da-skill>/references/conteudo.md`.

Os materiais e a coleta são as fontes dos fatos sobre o produto. O que o usuário respondeu na coleta conta como confirmado. A análise interpreta essas fontes e não confirma fato sozinha. A pesquisa é a fonte dos números.

Antes de julgar, rode o validador da skill a partir da raiz do projeto.

```bash
python3 <pasta-da-skill>/scripts/validar_conteudo.py docs/apresentacao/conteudo-<deck>.md
```

Cada linha que ele imprimir é um achado importante, no lugar que a própria linha indica. O validador confere só a forma. Depois dele, julgue a profundidade pelos nove critérios abaixo.

## Achados importantes

Cada item abaixo, quando acontece, é um achado importante.

1. **Número sem fonte, ou texto que diz mais do que a fonte mede.** Compare a frase do slide e a da fala com o campo "O que mede" do número e com o registro dele na pesquisa, nos materiais ou na coleta. Número de apoio que nenhum dos três registra junto com a fonte conta como sem fonte. Faixa que vira valor único, "até" que some e grupo de comparação que desaparece contam como dizer mais.
2. **Slide sem fala, sem pergunta ou sem dica, ou slide do meio da reunião sem nenhuma objeção ligada.** Dica que manda seguir sem ouvir o cliente vale como slide sem pergunta.
3. **Menos de oito objeções no painel, ou objeção sem slide de prova.** Conta também a objeção cujo slide de prova mede outra coisa e não responde ao que o cliente questiona.
4. **Slide de produto que só se olha, sem interação.** O vendedor falando ou passando o slide não é interação. O cliente precisa decidir algo na tela. No Meet, o cliente escolhe e o vendedor clica; presencial, o cliente pode tocar.
5. **Frase que serviria para qualquer produto.** Troque o nome do produto por outro, ou pela alternativa que o cliente já usa hoje sem pagar, e veja se a frase continua verdadeira. Se continua, ela não prova este produto. Vale para títulos, falas, dicas e respostas de objeção.
6. **Termo da lista de proibições do prompt 01, ou promessa que o produto não confirmou.** A lista está em "Proibições absolutas" de `<pasta-da-skill>/references/01-copy.md`, e os termos só podem aparecer na seção "O que não falar". Conta como promessa não confirmada todo fato sobre o produto que não está nos materiais nem na coleta, e toda frequência, como "o que mais ouvimos", sem dado que a sustente.
7. **Alguma das 14 perguntas do comprador sem resposta em slide ou fala.** Abra o slide citado em cada linha da tabela e confira que ele responde de fato. Atenção especial a confiança na empresa, clientes com resultado, segurança dos dados e risco, que inclui o compromisso total do contrato quando ele pode ser calculado.
8. **Parte da análise sem peça correspondente e sem justificativa.** Conta também a justificativa que não se sustenta, e o problema, os inimigos, o mecanismo ou as objeções da análise que não chegam aos slides e ao roteiro.
9. **Conta sem exemplo numérico ou sem o caso de dado vazio.** Conta também a conta que depende de um número que o cliente costuma não saber e não diz o que a tela e a fala fazem quando ele falta.

## Achados menores

O que atrapalha o vendedor sem derrubar a reunião. Alguns exemplos:

- dado do diagnóstico pedido e nunca usado;
- título de slide que é rótulo, como "Investimento", em vez de frase;
- ordem dos slides diferente entre partes do documento;
- marcador de nome com artigo ou gênero, como "da {cliente}" ou "o {pet}", que fica errado quando o nome é de outro gênero;
- valor citado sem a ressalva que o torna exato, como a implantação paga uma vez diluída na mensalidade.

## Saída

Uma lista de achados, os importantes primeiro. Cada achado ocupa uma linha com a classificação, o lugar exato, o número do critério (para os importantes) e o que está errado. O lugar exato é a seção, o id entre crases e o campo, ou o trecho citado entre aspas.

```markdown
- Importante. Slide `conta`, campo Falar. Critério 9. Nenhuma fala cobre o dono que não sabe quantos pedidos perde por semana.
- Importante. Objeção `conheco-minha-loja`, campo Slides. Critério 3. O slide `problema` mostra o custo da prateleira vazia, não o que o alerta enxerga e a memória do dono não.
- Menor. Seção "A conta", campo Entradas. O dado `{funcionarios}` é pedido no diagnóstico e nunca usado.
```

Sem achado importante, termine com a linha `Sem achado importante.` Não sugira reescrita e não altere nenhum arquivo.

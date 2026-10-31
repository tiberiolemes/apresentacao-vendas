# Contrato de comportamento

Leia na etapa 5, antes de escrever o plano, e de novo na etapa 6. Este contrato diz o que toda apresentação construída pela skill faz, em qualquer stack. Como implementar fica com quem constrói. Cada item abaixo vira requisito do plano, e a seção "Verificação antes de dar como pronta" diz como provar que ele se cumpre.

A apresentação tem duas janelas. Os slides são o que o cliente vê. O roteiro é o que o vendedor vê. As duas andam juntas.

## Regras gerais

- Tudo o que a apresentação diz vem do documento de conteúdo validado na etapa 4 (`docs/apresentacao/conteudo-<deck>.md`). A construção não inventa fala, número nem objeção.
- Nada que venha de documento confidencial do produto vai para a página pública ou para o PDF sem o usuário confirmar.
- Nenhum pedido a serviço de terceiros na página. Fontes, ícones e imagens ficam no próprio site. A única exceção é o canal de tempo real que o produto já usa, descrito em "Sincronia".

## Slides

- Palco 16:9 desenhado em 1920×1080 e escalado para caber na janela, sem cortar nada.
- Legível no Meet e na TV. Nenhum texto abaixo de 28 px na escala de 1920×1080, no máximo cerca de 25 palavras por slide e contraste AA medido.
- Passos dentro do slide. Clique, seta para a direita, espaço e PageDown revelam primeiro os passos e só depois passam ao próximo slide. As teclas de voltar fazem o caminho inverso.
- Barra de controles com anterior, próximo, contador, tela cheia e modo apresentador, que abre o roteiro.
- Um momento marcante, no slide do mecanismo único.
- Transições de 0,5 a 0,8 s. Com `prefers-reduced-motion`, tudo aparece parado, já no estado final.
- Telas do produto com interação de verdade. O que não for tela real do produto leva a palavra "Ilustração" visível.
- O diagnóstico é digitado na própria tela. Ele alimenta a conta e o nome do cliente na capa e no fim. Os dados ficam só no navegador; o que pode passar pelo servidor durante a reunião está em "Sincronia".
- Endereço aberto, com `noindex, nofollow` e fora do sitemap. O HTML público nunca contém texto do roteiro, e um teste automático confere isso.
- Versões por segmento existem só quando a coleta previu segmentos. Cada versão declara apenas a diferença em relação à base (remover, trocar ou inserir depois de um `id`), para slides e roteiro, e a mescla tem teste. Sem segmento previsto, a mescla não se constrói.

## Roteiro

- Abre com uma senha única do time comercial, uma por site de produto.
- A senha fica só como hash, num segredo de deploy do produto, cadastrada por um script que lê sem eco (veja a armadilha do script de senha em [armadilhas.md](armadilhas.md)). Limite de tentativas por IP, sessão em cookie `HttpOnly`, `Secure` e `SameSite=Strict`, e o conteúdo do roteiro só chega depois da sessão válida.
- Funciona no notebook e no celular.
- A tela do roteiro mostra:
  - o slide atual e o próximo em miniatura;
  - o cronômetro da reunião e o tempo previsto do slide, com aviso quando passa;
  - o que falar, a pergunta destacada e a dica;
  - as objeções do momento, cada uma com a resposta e um botão para o slide de prova;
  - o painel com todas as objeções;
  - a lista do que não falar, fixa no topo;
  - o botão "Nova reunião", que limpa o diagnóstico.
- Os marcadores das falas, como `{alunos}`, trocam pelos números e pelo nome do cliente assim que o diagnóstico é digitado. A variante sem comparação aparece pela mesma condição que esconde a comparação no slide.
- Os botões de avançar e voltar do roteiro passam os slides passo a passo, como as teclas nos slides. Ir ao slide de prova abre o slide com todos os passos visíveis.

## Sincronia

- **Mesmo computador.** É o Meet com só a guia dos slides compartilhada, ou a TV com os slides e o notebook com o roteiro, o caso mais comum no presencial. As duas janelas conversam pelo navegador, sem servidor, por exemplo com `BroadcastChannel`.
- **Outro aparelho.** Slides no notebook virado para o cliente e roteiro no celular. O roteiro também anda sozinho e funciona como controle remoto. A troca passa pelo servidor do produto. Se o produto já usa um serviço de tempo real, como o Realtime do Supabase, use o canal dele, sem tabela nova. Nos outros casos, use uma consulta curta a um endereço do próprio site.
- **Pareamento.**
  - O celular encontra os slides daquela reunião em menos de 30 segundos, sem digitar código longo.
  - Quem só vê o código não controla nada, porque o celular ainda pede a senha do time.
  - O código expira junto com a sessão.
- **Dados no servidor.** Posição do slide, nome e números do cliente que passam pelo servidor na sincronia não ficam gravados além da sessão da reunião.
- **Uma guia ativa.** Quando uma guia nova de slides assume, as antigas param de responder e mostram um aviso discreto. Recarregar qualquer janela preserva o slide, o diagnóstico e o cronômetro.

## PDF para o cliente

- O vendedor gera o PDF no fim da reunião, a partir do roteiro, com o nome e os números daquele cliente.
- O PDF nunca leva nada do roteiro (falas, perguntas, dicas, objeções e a lista do que não falar).
- Gerar o PDF nunca mostra diálogo nem tela nova na guia que está sendo compartilhada.
- Cada slide vira uma página no estado final, com todos os passos visíveis e a conta preenchida, sem a barra de controles. Os campos aparecem como texto.
- O nome do arquivo leva o produto e o cliente.
- Sem serviço de terceiros. A impressão do próprio navegador, com folha de estilo de impressão, resolve. Troque só se ela não couber na stack.

## Verificação antes de dar como pronta

Confira num navegador com a janela visível, como o Playwright com a janela aberta. Aba oculta ou em segundo plano pausa animações e temporizadores e dá resultado falso. A conferência cobre:

- todos os slides em 1920×1080 e 1280×720;
- cada interação;
- as duas janelas sincronizadas no mesmo computador;
- o celular sincronizado com os slides em outro aparelho;
- o login com a senha certa e com a errada;
- o PDF gerado com os números do cliente e sem nada do roteiro;
- o contraste;
- o movimento reduzido;
- o console limpo e nenhum pedido a terceiros.

Os testes automáticos cobrem:

- as rotas e o `noindex`;
- a ausência do roteiro no HTML público;
- o login e o limite de tentativas;
- a mescla de segmento, quando houver;
- a fórmula da conta, com os exemplos do documento de conteúdo, inclusive o caso de dado vazio ou zero.

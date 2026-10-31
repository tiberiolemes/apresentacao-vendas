# Armadilhas

Leia na etapa 5, antes de escrever o plano. Cada armadilha abaixo aconteceu na primeira implementação deste modelo e passou pela verificação de tarefa daquela construção, até a revisão final achar. O sintoma é o que o cliente ou o vendedor vê. A regra é o que evita. Leve cada regra para o plano como requisito ou como teste.

## 1. Roteiro que pula os passos do slide

**Sintoma.** O vendedor avança pela janela do roteiro, que é a que ele está olhando. O cliente vê no Meet um slide só com o título, enquanto ouve a fala sobre o conteúdo que não apareceu. O momento marcante nunca dispara.

**Regra.** Avançar e voltar no roteiro mandam o comando de avançar ou voltar, e os slides tratam esse comando como a tecla, passo a passo. O roteiro nunca manda "vá ao slide N no passo 0". Ele só troca de slide quando o estado que volta dos slides traz outro slide, o que também evita o pisca para trás no clique duplo. Ir a um slide pela lista ou pelo botão de prova abre o slide com todos os passos visíveis. Na verificação, confira os passos que aparecem, não só o número do slide.

## 2. Número do slide maior do que a fonte sustenta

**Sintoma.** No slide de credibilidade, o cliente vê o maior valor da pesquisa como se fosse o único, sem o "até" e sem o grupo de comparação. A fala do roteiro diz a versão certa, e a tela diz outra.

**Regra.** A tela e a fala dizem o mesmo que o campo "O que mede" do número, com a faixa, a base de comparação e a amostra que a fonte usa. O maior valor de uma faixa nunca vira número único. Confira a tela e a fala lado a lado, e confira que o texto completo cabe em 1280×720.

## 3. Fala de fechamento absurda

**Sintoma.** No fechamento, o vendedor júnior lê palavra por palavra uma pergunta como "dá para recuperar 8 dos 3 clientes que vocês perdem por mês?", porque o número calculado passou do número informado. Ou a fala diz "vocês perdem (sem dado)" quando o cliente informou zero. A conta desmonta na frente de quem decide.

**Regra.** Toda fala com marcador que pode ficar vazio ou inverter a comparação tem a variante sem comparação do documento de conteúdo. O roteiro escolhe a variante pela mesma condição que o slide usa para esconder a frase, numa função só, com teste. Zero informado é dado, nunca "sem dado".

## 4. Duas guias de slides disputando o roteiro

**Sintoma.** Com uma guia de slides esquecida de outra reunião ainda aberta, o roteiro pula de slide sozinho. O nome do cliente alterna entre a reunião antiga e a de agora, e o vendedor pode ler em voz alta o nome errado no fechamento. "Nova reunião" mexe nas duas guias.

**Regra.** Cada guia de slides gera uma identidade ao abrir e anuncia que assumiu. As guias mais antigas param de responder e mostram um aviso discreto, como "Os slides estão abertos em outra guia". O roteiro ignora o estado de qualquer guia que não seja a última que assumiu.

## 5. Limite de tentativas travando o escritório inteiro

**Sintoma.** O time comercial trabalha atrás do mesmo IP. Cinco senhas erradas de um colega bloqueiam todos, inclusive quem digita a senha certa. Se o servidor não enxerga o IP real do visitante, o limite vira global, e qualquer pessoa na internet trava o time.

**Regra.** No primeiro uso real, confira que o IP que chega ao limite é o do visitante. Atrás de proxy, leia só o cabeçalho que o próprio host garante. Um acerto zera a contagem daquele IP.

## 6. Botão desabilitado que solta o foco

**Sintoma.** O vendedor aciona pelo teclado o botão de uma tela interativa até ele ficar desabilitado. O foco cai no corpo da página, e o espaço seguinte passa o slide sem ninguém querer. Parece que o slide avançou sozinho.

**Regra.** Ao desabilitar um controle que tem o foco, mova o foco para a seção do slide. Quando um slide parecer avançar sozinho, registre teclas, mudanças de endereço e mensagens do canal, além dos cliques, antes de procurar a causa.

## 7. Janela nova com o diagnóstico velho

**Sintoma.** A janela do roteiro, ou uma guia de slides aberta a partir dele, nasce com o nome e os números da reunião anterior. "Nova reunião" limpa uma janela e deixa a cópia na outra.

**Regra.** Quem abre uma janela com `window.open` copia para ela o armazenamento da sessão (`sessionStorage`). A janela do roteiro descarta o diagnóstico herdado ao iniciar e ao confirmar "Nova reunião", e recebe o diagnóstico atual da guia ativa dos slides.

## 8. Nome do cliente sem concordância

**Sintoma.** O slide ou a fala diz "da Studio Forma" ou "do Padaria Central", e o cliente percebe que está lendo um modelo.

**Regra.** Frase com o marcador do nome do cliente não depende de artigo nem de gênero. Escreva "para {cliente}", "com os números de {cliente}" ou use o nome sozinho.

## 9. Script de senha sem terminal interativo

**Sintoma.** O cadastro da senha do roteiro falha sem explicação. O agente rodou o script pelo próprio shell, ou o usuário rodou pela linha de comando do assistente, e a leitura sem eco não tem terminal para ler. Em outro caso, a leitura cortou um espaço na ponta da senha, e o hash gravado nunca bate com o que o navegador envia.

**Regra.** O script só lê a senha num terminal interativo. Sem terminal, ele para com uma mensagem que manda rodar no aplicativo de terminal do computador, e a instrução ao usuário já diz isso antes. A leitura guarda a linha exatamente como foi digitada, sem cortar espaços, e a senha nunca é gravada em claro, nem em log.

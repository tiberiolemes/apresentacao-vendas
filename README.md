<div align="center">

```text
╔══════════════════════════════════════════════════════════════════╗
║  APRESENTAÇÃO DE VENDAS · SLIDES + ROTEIRO DO VENDEDOR           ║
║  coleta → análise → conteúdo validado → construção → verificação ║
║  Codex · Claude Code · MIT                                       ║
╚══════════════════════════════════════════════════════════════════╝
```

**Skill para montar a apresentação de vendas de um produto, com slides para o cliente e roteiro automatizado para o vendedor.**

[![Version](https://img.shields.io/badge/version-1.0.0-2563eb?style=for-the-badge)](plugins/apresentacao-vendas/.claude-plugin/plugin.json)
[![License](https://img.shields.io/badge/license-MIT-16a34a?style=for-the-badge)](LICENSE)
![Codex](https://img.shields.io/badge/Codex-supported-111827?style=for-the-badge)
![Claude Code](https://img.shields.io/badge/Claude%20Code-supported-111827?style=for-the-badge)

[English version below](#english)

</div>

## O que faz

A skill conduz, em seis etapas, a apresentação de vendas de um produto para reunião no Meet ou presencial, com PDF para mandar depois. Os slides são o que o cliente vê. O roteiro é o que o vendedor vê, com fala, tempo, pergunta para o cliente, objeção do momento com a resposta e o slide que prova. Ela replica para outros produtos o modelo da apresentação de vendas do Vitio, com o conteúdo construído sobre a metodologia Oferta Sexy.

As etapas são destino e leitura, coleta com uma pergunta por mensagem, análise e pesquisa, conteúdo com revisão e validação, construção, e verificação com publicação. A skill para na validação do documento de conteúdo e só segue para plano e código depois que o usuário valida.

## O que entrega e o que não entrega

Entrega:

- o método, em seis etapas, com as regras de cada uma;
- o conteúdo, com o formato do documento `docs/apresentacao/conteudo-<deck>.md`, um validador que confere a forma desse documento e uma revisão contra conteúdo superficial;
- o contrato de comportamento da apresentação construída, com palco 16:9, passos dentro do slide, modo apresentador, sincronia, PDF sem o roteiro e a verificação antes de dar como pronta;
- as armadilhas de construção já encontradas em uso real.

Não entrega um motor de slides. Não há template, biblioteca nem site pronto. A construção acontece na stack do produto, e o contrato diz o que ela precisa cumprir, não como programar. A skill também não faz proposta comercial nem landing page.

## Instalação no Codex

Clone este repositório e copie a pasta da skill para seu diretório pessoal:

```bash
git clone https://github.com/tiberiolemes/apresentacao-vendas.git
mkdir -p ~/.agents/skills
cp -R apresentacao-vendas/plugins/apresentacao-vendas/skills/apresentacao-vendas ~/.agents/skills/
```

Abra ou recarregue o Codex e invoque:

```text
$apresentacao-vendas
```

Para instalação apenas no projeto, copie para `.agents/skills/` na raiz do repositório.

## Instalação no Claude Code

Adicione o marketplace público e instale o plugin em escopo de usuário:

```text
/plugin marketplace add tiberiolemes/apresentacao-vendas
/plugin install apresentacao-vendas@tiberio-apresentacao-vendas
```

A skill aparece como `/apresentacao-vendas:apresentacao-vendas`. Para uso apenas em uma sessão local de desenvolvimento, clone o repositório e inicie o Claude Code com `--plugin-dir ./plugins/apresentacao-vendas`.

## Uso

Dentro do projeto do produto, peça a apresentação:

```text
Use $apresentacao-vendas para montar a apresentação de vendas do meu produto.
```

A skill pergunta o produto e onde a apresentação vai morar, lê o que o projeto já tem (regras, landing, análise, copy e design system) e só então começa a coleta. Cada resposta sua é gravada, com a pergunta, em `docs/apresentacao/coleta-<deck>.md`. Os números de apoio com fonte vão para `docs/pesquisa/AAAA-MM-DD-numeros-de-apoio.md`. O que nenhum material sustenta, ela pergunta e não inventa.

Na etapa 4 nasce `docs/apresentacao/conteudo-<deck>.md`. Depois de escrever, a skill roda o validador, que também pode ser rodado à mão a partir da raiz do projeto:

```bash
python3 <pasta-da-skill>/scripts/validar_conteudo.py docs/apresentacao/conteudo-<deck>.md
```

Com tudo certo, o validador imprime `OK (N slides, M objeções)`. Ele confere a forma. A profundidade fica com a revisão feita por um subagente separado. Código só começa depois que você valida o documento.

## Como rodar os testes e a verificação do pacote

Os testes e o verificador usam só a biblioteca padrão do Python, sem rede. A partir da raiz do repositório:

```bash
python3 -m unittest discover -s tests -v
python3 scripts/verificar_pacote.py
```

O verificador imprime `OK` quando o pacote está em ordem e, senão, um problema por linha com saída 1. Ele confere o `SKILL.md` (nome igual ao da pasta, descrição começando por "Use quando", no máximo 600 palavras), links quebrados, JSON e versão do plugin contra o `CHANGELOG.md`, caminhos locais, segredos, travessão nos textos autorais e a linha de crédito nas cópias da metodologia.

Quem mantém o repositório pode manter fora dele uma lista de termos que não podem aparecer na skill. O verificador lê essa lista de `~/.config/apresentacao-vendas/termos-privados.txt` (um termo por linha; linhas começando por `#` são comentário) ou da variável de ambiente `VERIFICAR_TERMOS_PRIVADOS` (termos separados por vírgula). Sem nenhuma das duas, essa checagem é pulada e o verificador avisa na saída de erro. Nenhum termo mora no pacote.

## Resultado do teste

O teste usa um produto fictício e um briefing que deixa de propósito fatos de fora. Um avaliador cego comparou duas versões da mesma entrega. A versão sem a skill teve 9 achados importantes, 7 deles evitáveis. A versão com a skill teve 2, e os dois vêm de fatos que faltavam no briefing do teste. Nesses casos a skill diz só o que o briefing sustenta, promete resposta por escrito e registra a lacuna, sem inventar. O avaliador reprovou as duas versões. O registro completo, inclusive os achados menores que ficaram para a próxima iteração, está em [tests/resultados/](tests/resultados/).

## Estrutura

```text
plugins/apresentacao-vendas/
├── .claude-plugin/plugin.json
├── agents/apresentacao-vendas-agent.md
└── skills/apresentacao-vendas/
    ├── SKILL.md
    ├── agents/openai.yaml
    ├── references/
    └── scripts/validar_conteudo.py
scripts/verificar_pacote.py
tests/
```

## Crédito da metodologia

A metodologia Oferta Sexy é de Gabriel Rodrigues, ARR.Academy. Os quatro arquivos `references/00-analise.md` a `references/03-direcao-criacao.md` são cópias sem edição dos prompts originais, com a linha de crédito na primeira linha, e servem de referência para as etapas de análise, copy, design e direção de criação.

## Licença e contribuição

Este pacote é público sob MIT; consulte [LICENSE](LICENSE). As quatro cópias da metodologia continuam dos seus autores e vão com crédito, sem relicenciamento pela MIT. Contribuições e correções são bem-vindas conforme [CONTRIBUTING.md](CONTRIBUTING.md). O histórico de versões está em [CHANGELOG.md](CHANGELOG.md).

---

<a id="english"></a>

## English

**A skill for building a product's sales presentation, with slides for the customer and an automated script for the salesperson.** It guides six stages for a presentation delivered on a video call or in person, with a PDF to send afterwards. The slides are what the customer sees. The script is what the salesperson sees, with what to say, timing, a question for the customer, the objection of the moment with its answer, and the slide that proves it. The content is built on the Oferta Sexy methodology. The skill stops at the validation of the content document and moves on to planning and code only after the user approves it.

### What it delivers and what it does not

It delivers the method (six stages), the content (the format of `docs/apresentacao/conteudo-<deck>.md`, a validator for that document's form, and a review against shallow content), a behavior contract for the finished presentation (16:9 stage, steps inside a slide, presenter mode, sync, a PDF without the script, and checks before calling it done), and the build pitfalls found in real use.

It does not ship a slide engine. There is no template, library, or ready-made site. The build happens in the product's own stack, and the contract states what it must satisfy, not how to code it. It does not write commercial proposals or landing pages either.

### Install for Codex

```bash
git clone https://github.com/tiberiolemes/apresentacao-vendas.git
mkdir -p ~/.agents/skills
cp -R apresentacao-vendas/plugins/apresentacao-vendas/skills/apresentacao-vendas ~/.agents/skills/
```

Reload Codex if needed, then invoke `$apresentacao-vendas`. For project-only use, copy it to `.agents/skills/` at your repository root.

### Install for Claude Code

```text
/plugin marketplace add tiberiolemes/apresentacao-vendas
/plugin install apresentacao-vendas@tiberio-apresentacao-vendas
```

Invoke `/apresentacao-vendas:apresentacao-vendas`. For one local development session, clone the repository and start Claude Code with `--plugin-dir ./plugins/apresentacao-vendas`.

### Use

From the product's project, ask for the presentation:

```text
Use $apresentacao-vendas to build the sales presentation for my product.
```

The skill asks for the product and the destination, reads what the project already has, then collects answers one question per message and saves them in `docs/apresentacao/`. It records missing facts instead of inventing them. After writing the content document it runs the validator, which you can also run from the project root:

```bash
python3 <skill-folder>/scripts/validar_conteudo.py docs/apresentacao/conteudo-<deck>.md
```

### Tests and package check

Tests and the checker use only the Python standard library and no network. From the repository root:

```bash
python3 -m unittest discover -s tests -v
python3 scripts/verificar_pacote.py
```

The checker prints `OK` when the package is in order, or one problem per line with exit code 1. Maintainers can keep a list of terms that must not appear in the skill outside the repository. The checker reads it from `~/.config/apresentacao-vendas/termos-privados.txt` (one term per line, lines starting with `#` are comments) or from the `VERIFICAR_TERMOS_PRIVADOS` environment variable (comma-separated). Without either, that check is skipped and the checker prints a notice on stderr. No term lives in the package.

### Test result

The test uses a fictional product and a briefing that deliberately leaves facts out. A blind evaluator compared two versions of the same deliverable. The version without the skill had 9 important findings, 7 of them avoidable. The version with the skill had 2, both caused by facts missing from the test briefing. In those cases the skill states only what the briefing supports, promises a written answer, and records the gap without inventing anything. The evaluator failed both versions. The full record, including the minor findings left for the next iteration, is in [tests/resultados/](tests/resultados/).

### Methodology credit

The Oferta Sexy methodology is by Gabriel Rodrigues, ARR.Academy. The four files `references/00-analise.md` to `references/03-direcao-criacao.md` are unedited copies of the original prompts, with a credit line on the first line.

### License and contribution

This public package is licensed under MIT; see [LICENSE](LICENSE). The four methodology copies remain their authors' work and ship with credit; they are not relicensed under MIT. Contributions are welcome under [CONTRIBUTING.md](CONTRIBUTING.md). Version history is in [CHANGELOG.md](CHANGELOG.md).

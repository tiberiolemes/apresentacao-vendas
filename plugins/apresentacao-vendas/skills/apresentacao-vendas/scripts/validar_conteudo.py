#!/usr/bin/env python3
"""Valida o documento de conteúdo da apresentação (formato em references/conteudo.md).

Só biblioteca padrão, sem rede. Uso: python3 validar_conteudo.py <arquivo>
Imprime `OK (N slides, M objeções)` com saída 0, ou um problema por linha com saída 1.
"""
import re
import sys
from pathlib import Path

SECOES = ("Mapa da Oferta Sexy", "Slides", "Objeções", "O que não falar", "A conta",
          "Números de apoio", "PDF", "As 14 perguntas do comprador")
CAMPOS_DO_SLIDE = ("Cliente vê", "Interação", "Tempo", "Análise", "Falar", "Pergunta", "Dica", "Objeções")
PARTES_DO_MAPA = ("Ângulo", "Problema na voz do cliente", "Inimigo do resultado", "Mecanismo único",
                  "Diferenciais", "Verdades", "Objeções", "Proibições")
TERMOS_PROIBIDOS = ("solução completa", "revolucionário", "líder de mercado", "potencialize",
                    "transforme seu negócio", "próximo nível", "tudo em um só lugar", "disruptivo")
MINIMO_DE_OBJECOES = 8

ID = re.compile(r"[a-z0-9-]+")
TEMPO = re.compile(r"\d+(,\d+)? min")
SECAO = re.compile(r"^## ", re.M)
BLOCO = re.compile(r"^### `([^`]+)`")
CAMPO = re.compile(r"^- \*\*(.+?)(?::\*\*|\*\*:)[ \t]*(.*)$")  # aceita também `- **Campo**:`
SUBITEM = re.compile(r"^(?:\t| {2})[ \t]*- (.+)$")  # dois espaços ou mais, ou tab
ITEM = re.compile(r"^- (.+)$")
TABELA = re.compile(r"^\|\s*([^|]+?)\s*\|\s*([^|]*?)\s*\|(?:\s*([^|]*?)\s*\|)?\s*$")
CRASES = re.compile(r"`([^`]+)`")
DICA_MESMA_LINHA = " (escreva o texto na mesma linha do rótulo)"
DICA_SUBITENS = " (use subitens com hífen, recuados)"
SECAO_SEM_TERMOS = "O que não falar"  # lista o que evitar, então pode citar os termos proibidos


def _secoes(texto):
    """Nome da seção `##` -> corpo."""
    secoes = {}
    for parte in SECAO.split(texto.replace("\r\n", "\n"))[1:]:
        nome, _, corpo = parte.partition("\n")
        secoes[nome.strip()] = corpo
    return secoes


def _blocos(corpo):
    """[(id, linhas)] dos títulos `###`. Título sem id entre crases vira id com o texto dele, que o ID recusa."""
    blocos = []
    for linha in corpo.split("\n"):
        achado = BLOCO.match(linha)
        if achado:
            blocos.append((achado.group(1), []))
        elif linha.startswith("### "):
            blocos.append((linha[4:].strip(), []))
        elif blocos:
            blocos[-1][1].append(linha)
    return blocos


def _campos(linhas):
    """Nome do campo -> (texto, subitens). Subitem pertence ao último campo lido."""
    campos, atual = {}, None
    for linha in linhas:
        campo, subitem = CAMPO.match(linha), SUBITEM.match(linha)
        if campo:
            atual = campos[campo.group(1)] = (campo.group(2).strip(), [])
        elif subitem and atual and subitem.group(1).strip():
            atual[1].append(subitem.group(1).strip())
    return campos


def _itens(corpo):
    return [m.group(1) for m in map(ITEM.match, corpo.split("\n")) if m and m.group(1).strip()]


def _tabela(corpo):
    return [m.groups() for m in map(TABELA.match, corpo.split("\n")) if m]


def _texto(campos, nome):
    return campos.get(nome, ("", []))[0]


def _ids(blocos):
    """Ids existentes (inclusive os inválidos, para não gerar problema em cascata) e os problemas de id."""
    vistos, problemas = set(), []
    for id_, _ in blocos:
        if not ID.fullmatch(id_):
            problemas.append(f"id inválido: {id_}")
        elif id_ in vistos:
            problemas.append(f"id inválido: {id_} (repetido)")
        vistos.add(id_)
    return vistos, problemas


def _inexistentes(texto, existentes):
    return [i for i in CRASES.findall(texto) if i not in existentes]


def _slides(blocos, ids_objecoes):
    problemas = []
    for posicao, (id_, linhas) in enumerate(blocos):
        campos, prefixo = _campos(linhas), f"slide `{id_}`: "
        for nome in CAMPOS_DO_SLIDE:
            texto, subitens = campos.get(nome, ("", []))
            if nome == "Falar" and not subitens:
                problemas.append(prefixo + nome + DICA_SUBITENS)
            elif nome != "Falar" and not texto:
                problemas.append(prefixo + nome)
        tempo = _texto(campos, "Tempo")
        if tempo and not TEMPO.fullmatch(tempo):
            problemas.append(prefixo + "Tempo (use 2 min ou 1,5 min)")
        objecoes = _texto(campos, "Objeções")
        if objecoes:
            nenhuma = objecoes.replace("`", "").strip(" .").lower() == "nenhuma"
            citadas = [] if nenhuma else CRASES.findall(objecoes)
            if not citadas and not nenhuma:
                problemas.append(prefixo + "Objeções (cite os ids entre crases ou escreva nenhuma)")
            elif nenhuma and 1 < posicao < len(blocos) - 1:
                problemas.append(prefixo + "sem objeção")
            problemas += [f"objeção inexistente: {i}" for i in citadas if i not in ids_objecoes]
    return problemas


def _objecoes(blocos, ids_slides):
    problemas = [f"objeções: {len(blocos)} (mínimo {MINIMO_DE_OBJECOES})"] if len(blocos) < MINIMO_DE_OBJECOES else []
    for id_, linhas in blocos:
        campos, prefixo = _campos(linhas), f"objeção `{id_}`: "
        problemas += [prefixo + nome for nome in ("Resposta", "Quem levanta") if not _texto(campos, nome)]
        slides = _texto(campos, "Slides")
        if not CRASES.search(slides):
            problemas.append(prefixo + "Slides")
        problemas += [f"{prefixo}Slides (slide inexistente: {i})" for i in _inexistentes(slides, ids_slides)]
    return problemas


def _conta(corpo):
    campos = _campos(corpo.split("\n"))
    problemas = []
    for nome in ("Entradas", "Fórmula", "Dado vazio ou zero"):
        if not _texto(campos, nome):
            problemas.append(f"conta: {nome}" + (DICA_MESMA_LINHA if nome in campos else ""))
    if not campos.get("Exemplos", ("", []))[1]:
        problemas.append("conta: Exemplos" + DICA_SUBITENS)
    return problemas


def _numeros(blocos, ids_slides):
    problemas = []
    for id_, linhas in blocos:
        campos, prefixo = _campos(linhas), f"número `{id_}`: "
        fonte = _texto(campos, "Fonte")
        if not fonte or fonte.lower().startswith("pendente"):
            problemas.append(prefixo + "Fonte")
        problemas += [prefixo + nome for nome in ("Amostra", "O que mede") if not _texto(campos, nome)]
        uso = _texto(campos, "Uso")
        if not CRASES.search(uso) and not uso.lower().startswith("reserva"):
            problemas.append(prefixo + "Uso")
        problemas += [f"{prefixo}Uso (slide inexistente: {i})" for i in _inexistentes(uso, ids_slides)]
    return problemas


def _mapa(corpo):
    linhas = {parte.casefold(): texto for parte, texto, _ in _tabela(corpo)}
    return [f"mapa: {parte}" for parte in PARTES_DO_MAPA if not linhas.get(parte.casefold())]


def _perguntas(corpo, ids_slides):
    onde = {}
    for numero, _, resposta in _tabela(corpo):
        if numero.isdecimal():  # isdigit aceita '²', que int() recusa
            onde.setdefault(int(numero), resposta or "")
    problemas = []
    for n in range(1, 15):
        if n not in onde:
            problemas.append(f"pergunta {n}: linha ausente")
        elif not any(i in ids_slides for i in CRASES.findall(onde[n])):
            problemas.append(f"pergunta {n}: cite entre crases um slide que existe")
    return problemas


def _proibidos(texto):
    """Travessão vale no documento todo; os termos proibidos, fora da seção que lista o que evitar."""
    problemas, secao = [], ""
    for numero, linha in enumerate(texto.splitlines(), 1):
        if linha.startswith("## "):
            secao = linha[3:].strip()
        if "—" in linha:
            problemas.append(f"travessão (linha {numero})")
        if secao != SECAO_SEM_TERMOS:
            problemas += [f"termo proibido: {t} (linha {numero})" for t in TERMOS_PROIBIDOS if t in linha.lower()]
    return problemas


def validar(texto):
    """Problemas do documento, um por item; lista vazia quando está tudo certo."""
    secoes = _secoes(texto)
    problemas = [f"seção faltando: {nome}" for nome in SECOES if nome not in secoes]
    slides, objecoes = _blocos(secoes.get("Slides", "")), _blocos(secoes.get("Objeções", ""))
    numeros = _blocos(secoes.get("Números de apoio", ""))
    ids_slides, problemas_de_id = _ids(slides)
    ids_objecoes, problemas_de_id_objecao = _ids(objecoes)
    _, problemas_de_id_numero = _ids(numeros)
    problemas += problemas_de_id + problemas_de_id_objecao + problemas_de_id_numero

    if "Mapa da Oferta Sexy" in secoes:
        problemas += _mapa(secoes["Mapa da Oferta Sexy"])
    if "Slides" in secoes:
        problemas += _slides(slides, ids_objecoes)
    if "Objeções" in secoes:
        problemas += _objecoes(objecoes, ids_slides)
    if "O que não falar" in secoes and not _itens(secoes["O que não falar"]):
        problemas.append("o que não falar vazio")
    if "A conta" in secoes:
        problemas += _conta(secoes["A conta"])
    if "Números de apoio" in secoes:
        problemas += _numeros(numeros, ids_slides)
    if "PDF" in secoes and not _itens(secoes["PDF"]):
        problemas.append("PDF vazio")
    if "As 14 perguntas do comprador" in secoes:
        problemas += _perguntas(secoes["As 14 perguntas do comprador"], ids_slides)
    return problemas + _proibidos(texto)


def main(argv):
    if len(argv) != 2:
        print("arquivo: informe o caminho do documento de conteúdo")
        return 1
    try:
        texto = Path(argv[1]).read_text(encoding="utf-8")
    except (OSError, ValueError) as erro:  # ValueError cobre UnicodeDecodeError
        print(f"arquivo: {erro}")
        return 1
    problemas = validar(texto)
    if problemas:
        print("\n".join(problemas))
        return 1
    secoes = _secoes(texto)
    print(f"OK ({len(_blocos(secoes['Slides']))} slides, {len(_blocos(secoes['Objeções']))} objeções)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

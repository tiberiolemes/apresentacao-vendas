#!/usr/bin/env python3
"""Verifica o pacote da skill antes do uso e da publicação. Só biblioteca padrão, sem rede.

Os termos privados não moram no pacote: vêm de ~/.config/apresentacao-vendas/termos-privados.txt
(um por linha, `#` comenta) e da variável de ambiente VERIFICAR_TERMOS_PRIVADOS (separados por vírgula).
"""
import fnmatch
import json
import os
import re
import sys
from pathlib import Path
from urllib.parse import unquote

SKILL = "plugins/apresentacao-vendas/skills/apresentacao-vendas"
PLUGIN_JSON = "plugins/apresentacao-vendas/.claude-plugin/plugin.json"
MARKETPLACE_JSON = ".claude-plugin/marketplace.json"
CREDITO = (
    "> Metodologia Gabriel Rodrigues, ARR.Academy. "
    "Cópia sem edição do prompt original, usada como referência por esta skill."
)
IGNORADAS = {".git", ".superpowers", "__pycache__"}
SEM_VARREDURA_DE_SEGREDO = ("scripts/verificar_pacote.py", "tests/test_*.py")
ARQUIVOS_AUTORAIS = (
    f"{SKILL}/SKILL.md",
    *(f"{SKILL}/references/{n}.md" for n in ("conteudo", "contrato", "revisao", "armadilhas")),
    "README.md",
    "CONTRIBUTING.md",
    "CHANGELOG.md",
    "tests/cenario/*.md",
)
ARQUIVO_TERMOS = ".config/apresentacao-vendas/termos-privados.txt"
VAR_TERMOS = "VERIFICAR_TERMOS_PRIVADOS"
CAMINHO_LOCAL = re.compile(r"/Users/|/home/|~/(Documents|Desktop|Downloads|\.claude/projects)")
SEGREDOS = (
    re.compile(r"sk-[A-Za-z0-9]{20,}"),
    re.compile(r"ghp_[A-Za-z0-9]{20,}"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"(?i:senha|password|secret|token)\s*[:=]\s*['\"]?[A-Za-z0-9$./+=_-]{12,}"),
)
LINK = re.compile(r"\]\(([^)]*)\)")
VERSAO_CHANGELOG = re.compile(r"^## \[(\d[^\]]*)\]", re.M)


def _termos_privados():
    """Lista local de termos privados; sem arquivo e sem variável, devolve lista vazia."""
    arquivo = Path.home() / ARQUIVO_TERMOS
    linhas = arquivo.read_text(encoding="utf-8").splitlines() if arquivo.is_file() else []
    termos = [x.strip() for x in linhas if x.strip() and not x.lstrip().startswith("#")]
    return termos + [t.strip() for t in os.environ.get(VAR_TERMOS, "").split(",") if t.strip()]


def _ler_textos(raiz):
    """Todos os arquivos de texto UTF-8 do repositório, por caminho relativo."""
    textos = {}
    for pasta, subpastas, nomes in os.walk(raiz):
        subpastas[:] = sorted(d for d in subpastas if d not in IGNORADAS)
        for nome in sorted(n for n in nomes if n not in IGNORADAS):  # .git também é arquivo em worktree e submódulo
            caminho = Path(pasta, nome)
            try:
                textos[caminho.relative_to(raiz).as_posix()] = caminho.read_text(encoding="utf-8")
            except (UnicodeDecodeError, FileNotFoundError):
                pass  # binário (imagem, fonte) e atalho quebrado não entram na verificação
    return textos


def _campos(frontmatter):
    """Lê `chave: valor` de nível zero; linhas indentadas continuam o valor anterior."""
    # shortcut: sem YAML, cobre texto simples, entre aspas e dobrado (>), trocar por parser se os campos ficarem complexos
    campos, chave = {}, None
    for linha in frontmatter.split("\n"):
        achado = re.match(r"([\w-]+):\s*(.*)$", linha)
        if achado and not linha[0].isspace():
            chave = achado.group(1)
            campos[chave] = [achado.group(2)]
        elif chave:
            campos[chave].append(linha.strip())
    resultado = {}
    for chave, partes in campos.items():
        valor = " ".join(p for p in partes if p and p not in (">", "|", ">-", "|-")).strip()
        resultado[chave] = valor[1:-1] if len(valor) > 1 and valor[0] == valor[-1] and valor[0] in "\"'" else valor
    return resultado


def _problemas_skill_md(texto, nome_da_pasta):
    achado = re.match(r"---\n(.*?)\n---(?:\n|$)", texto, re.S) if texto is not None else None
    if not achado:
        motivo = "arquivo ausente" if texto is None else "sem frontmatter"
        return [f"SKILL.md: name ausente ({motivo})", f"SKILL.md: description ausente ({motivo})"]
    frontmatter = achado.group(1)
    campos = _campos(frontmatter)
    problemas = []
    if campos.get("name") != nome_da_pasta:
        problemas.append(f'SKILL.md: name "{campos.get("name", "")}" diferente da pasta "{nome_da_pasta}"')
    if not campos.get("description", "").startswith("Use quando"):
        problemas.append('SKILL.md: description deve começar por "Use quando"')
    if len(frontmatter) > 1024:
        problemas.append(f"SKILL.md: description, frontmatter com {len(frontmatter)} caracteres (máximo 1024)")
    palavras = len(texto.split())
    if palavras > 600:
        problemas.append(f"SKILL.md: palavras, {palavras} (máximo 600)")
    return problemas


def _problemas_links(raiz, textos):
    problemas = []
    for rel, texto in textos.items():
        if not rel.endswith(".md"):
            continue
        for bruto in LINK.findall(texto):
            partes = bruto.split()
            destino = unquote(partes[0].split("#")[0]) if partes else ""
            if not destino or re.match(r"(https?|mailto):", destino):
                continue
            if not (raiz / rel).parent.joinpath(destino).exists():
                problemas.append(f"link quebrado: {rel} -> {bruto.strip()}")
    return problemas


def _problemas_json_e_versao(textos):
    problemas, plugin = [], None
    for rel in (MARKETPLACE_JSON, PLUGIN_JSON):
        if rel not in textos:
            problemas.append(f"json: {rel} não encontrado")
            continue
        try:
            dados = json.loads(textos[rel])
        except ValueError as erro:
            problemas.append(f"json: {rel} inválido ({erro})")
            continue
        if rel == PLUGIN_JSON:
            plugin = dados
    if plugin is None:
        return problemas
    versao_do_plugin = plugin.get("version") if isinstance(plugin, dict) else None
    achado = VERSAO_CHANGELOG.search(textos.get("CHANGELOG.md", ""))
    if not versao_do_plugin or not achado:
        problemas.append("versão: faltam `version` no plugin.json ou `## [x.y.z]` no CHANGELOG.md")
    elif versao_do_plugin != achado.group(1):
        problemas.append(f"versão: plugin.json {versao_do_plugin} diferente do CHANGELOG.md {achado.group(1)}")
    return problemas


def verificar(raiz, termos=None):
    raiz = Path(raiz).resolve()
    if termos is None:
        termos = _termos_privados()
    padroes = [(t, re.compile(rf"\b{re.escape(t)}\b", re.I)) for t in termos]
    textos = _ler_textos(raiz)
    skill = f"{SKILL}/"
    problemas = _problemas_skill_md(textos.get(f"{SKILL}/SKILL.md"), Path(SKILL).name)
    problemas += _problemas_links(raiz, textos)

    for rel, texto in textos.items():
        if not any(fnmatch.fnmatchcase(rel, padrao) for padrao in SEM_VARREDURA_DE_SEGREDO):
            if CAMINHO_LOCAL.search(texto):
                problemas.append(f"caminho local: {rel}")
            if any(padrao.search(texto) for padrao in SEGREDOS):
                problemas.append(f"segredo: {rel}")
        if "—" in texto and any(fnmatch.fnmatchcase(rel, padrao) for padrao in ARQUIVOS_AUTORAIS):
            problemas.append(f"travessão: {rel}")
        if rel == f"{skill}SKILL.md" or (rel.startswith(f"{skill}references/") and rel.endswith(".md")):
            problemas += [f"termo privado: {rel} ({t})" for t, padrao in padroes if padrao.search(texto)]
        if fnmatch.fnmatchcase(rel, f"{skill}references/0[0-3]-*.md") and texto.split("\n", 1)[0] != CREDITO:
            problemas.append(f"crédito: {rel} sem a linha de crédito exata na primeira linha")

    return problemas + _problemas_json_e_versao(textos)


def main(argv):
    raiz = Path(argv[1]) if len(argv) > 1 else Path(__file__).resolve().parent.parent
    termos = _termos_privados()
    problemas = verificar(raiz, termos)
    if not termos:
        print("termos privados: nenhuma lista local", file=sys.stderr)
    print("\n".join(problemas) if problemas else "OK")
    return 1 if problemas else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

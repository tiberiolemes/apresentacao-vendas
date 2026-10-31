import contextlib
import io
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from verificar_pacote import main, verificar  # noqa: E402

SKILL = "plugins/apresentacao-vendas/skills/apresentacao-vendas"
CREDITO = (
    "> Metodologia Gabriel Rodrigues, ARR.Academy. "
    "Cópia sem edição do prompt original, usada como referência por esta skill."
)
SKILL_MD = """---
name: apresentacao-vendas
description: Use quando o usuário pedir uma apresentação de vendas.
---

# Apresentação de vendas

Veja a [análise](references/00-analise.md).
"""
CAMINHO_LOCAL = "/Us" + "ers/fulano"
TRAVESSAO = "—"
VAR_TERMOS = "VERIFICAR_TERMOS_PRIVADOS"


class VerificarPacoteTest(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.pasta = Path(tmp.name)
        self.com_home()
        self.escrever(f"{SKILL}/SKILL.md", SKILL_MD)
        self.escrever(f"{SKILL}/references/00-analise.md", f"{CREDITO}\n\nTexto.\n")
        self.escrever("plugins/apresentacao-vendas/.claude-plugin/plugin.json", '{"version": "1.0.0"}')
        self.escrever(".claude-plugin/marketplace.json", '{"plugins": []}')
        self.escrever("CHANGELOG.md", "## [1.0.0] - 2026-10-30\n\n- Primeira versão.\n")

    def escrever(self, rel, texto):
        caminho = self.pasta / rel
        caminho.parent.mkdir(parents=True, exist_ok=True)
        caminho.write_text(texto, encoding="utf-8")

    def acrescentar(self, rel, texto):
        caminho = self.pasta / rel
        caminho.write_text(caminho.read_text(encoding="utf-8") + texto, encoding="utf-8")

    def com_home(self, termos_no_arquivo=None, termos_no_env=None):
        """HOME temporário, para nunca ler a configuração real de quem roda os testes."""
        home = tempfile.TemporaryDirectory()
        self.addCleanup(home.cleanup)
        if termos_no_arquivo is not None:
            arquivo = Path(home.name) / ".config/apresentacao-vendas/termos-privados.txt"
            arquivo.parent.mkdir(parents=True)
            arquivo.write_text(termos_no_arquivo, encoding="utf-8")
        ambiente = mock.patch.dict(os.environ, {"HOME": home.name})
        ambiente.start()
        self.addCleanup(ambiente.stop)
        os.environ.pop(VAR_TERMOS, None)
        if termos_no_env is not None:
            os.environ[VAR_TERMOS] = termos_no_env

    def assertUmProblema(self, prefixo, **opcoes):
        problemas = verificar(self.pasta, **opcoes)
        self.assertEqual(len(problemas), 1, problemas)
        self.assertTrue(problemas[0].startswith(prefixo), problemas)

    def test_pacote_valido_passa(self):
        self.assertEqual(verificar(self.pasta), [])

    def test_name_diferente_da_pasta(self):
        self.escrever(f"{SKILL}/SKILL.md", SKILL_MD.replace("name: apresentacao-vendas", "name: outra-coisa"))
        self.assertUmProblema("SKILL.md: name")

    def test_description_sem_use_quando(self):
        self.escrever(f"{SKILL}/SKILL.md", SKILL_MD.replace("Use quando o usuário pedir", "Ajuda a montar"))
        self.assertUmProblema("SKILL.md: description")

    def test_frontmatter_acima_de_1024_caracteres(self):
        self.escrever(f"{SKILL}/SKILL.md", SKILL_MD.replace("vendas.\n---", "vendas. " + "x" * 1100 + "\n---"))
        self.assertUmProblema("SKILL.md: description")

    def test_description_em_varias_linhas_e_com_aspas_passa(self):
        dobrada = "description: >\n  Use quando o usuário pedir\n  uma apresentação de vendas.\n"
        entre_aspas = 'description: "Use quando o usuário pedir uma apresentação."\n'
        for descricao in (dobrada, entre_aspas):
            with self.subTest(descricao=descricao):
                texto = SKILL_MD.replace("description: Use quando o usuário pedir uma apresentação de vendas.\n", descricao)
                self.escrever(f"{SKILL}/SKILL.md", texto)
                self.assertEqual(verificar(self.pasta), [])

    def test_skill_md_acima_de_600_palavras(self):
        self.acrescentar(f"{SKILL}/SKILL.md", "palavra " * 600)
        self.assertUmProblema("SKILL.md: palavras")

    def test_skill_md_ausente_nao_quebra(self):
        (self.pasta / SKILL / "SKILL.md").unlink()
        problemas = verificar(self.pasta)
        self.assertTrue(problemas and problemas[0].startswith("SKILL.md: name"), problemas)

    def test_link_relativo_quebrado(self):
        self.acrescentar(f"{SKILL}/SKILL.md", "\n[x](references/nao-existe.md)\n")
        self.assertUmProblema("link quebrado")

    def test_link_externo_e_ancora_nao_contam(self):
        self.acrescentar(
            f"{SKILL}/SKILL.md",
            "\n[a](https://exemplo.com) [b](#secao) [c](mailto:a@b.co) [d](references/00-analise.md#topo)\n",
        )
        self.assertEqual(verificar(self.pasta), [])

    def test_caminho_local(self):
        self.escrever(f"{SKILL}/references/contrato.md", f"Veja {CAMINHO_LOCAL}/projeto.\n")
        self.assertUmProblema("caminho local")

    def test_caminho_local_na_pasta_do_usuario(self):
        for pasta in ("~/Desktop", "~/Downloads"):
            with self.subTest(pasta=pasta):
                self.escrever(f"{SKILL}/references/contrato.md", f"Veja {pasta}/projeto.\n")
                self.assertUmProblema("caminho local")

    def test_travessao_em_arquivo_autoral(self):
        self.acrescentar(f"{SKILL}/SKILL.md", f"\nUma ideia {TRAVESSAO} outra ideia.\n")
        self.assertUmProblema("travessão")

    def test_travessao_no_readme(self):
        self.escrever("README.md", f"Uma ideia {TRAVESSAO} outra ideia.\n")
        self.assertUmProblema("travessão")

    def test_travessao_permitido_na_copia_00(self):
        self.escrever(f"{SKILL}/references/00-analise.md", f"{CREDITO}\n\nUma ideia {TRAVESSAO} outra.\n")
        self.assertEqual(verificar(self.pasta), [])

    def test_termo_privado_sem_diferenca_de_maiuscula(self):
        self.escrever(f"{SKILL}/references/contrato.md", "Cliente TERMOFALSOX Tech.\n")
        self.assertUmProblema("termo privado", termos=["TermoFalsoX"])

    def test_termo_privado_so_palavra_inteira(self):
        self.escrever(f"{SKILL}/references/contrato.md", "TermoFalsoXis e preTermoFalsoX.\n")
        self.assertEqual(verificar(self.pasta, termos=["TermoFalsoX"]), [])

    def test_termo_privado_so_nos_arquivos_da_skill(self):
        self.escrever("README.md", "Autor TermoFalsoX.\n")
        self.assertEqual(verificar(self.pasta, termos=["TermoFalsoX"]), [])

    def test_termo_privado_lista_vazia_nao_roda_a_checagem(self):
        self.escrever(f"{SKILL}/references/contrato.md", "Cliente TermoFalsoX Tech.\n")
        self.assertEqual(verificar(self.pasta, termos=[]), [])

    def test_termos_privados_vindos_da_variavel_de_ambiente(self):
        self.com_home(termos_no_env=" TermoFalsoX , ,OutroFalsoY")
        self.escrever(f"{SKILL}/references/contrato.md", "Cliente OutroFalsoY Tech.\n")
        self.assertUmProblema("termo privado")

    def test_termos_privados_vindos_do_arquivo_de_configuracao(self):
        self.com_home(termos_no_arquivo="# comentário\n\nTermoFalsoX\n")
        self.escrever(f"{SKILL}/references/contrato.md", "Cliente TermoFalsoX Tech.\n")
        self.assertUmProblema("termo privado")

    def test_sem_arquivo_nem_variavel_a_checagem_nao_roda_e_nao_da_erro(self):
        self.escrever(f"{SKILL}/references/contrato.md", "Cliente TermoFalsoX Tech.\n")
        self.assertEqual(verificar(self.pasta), [])

    def test_cli_avisa_no_stderr_quando_nao_ha_lista_e_continua_ok(self):
        saida, erro = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(saida), contextlib.redirect_stderr(erro):
            codigo = main(["verificar_pacote.py", str(self.pasta)])
        self.assertEqual((codigo, saida.getvalue(), erro.getvalue()), (0, "OK\n", "termos privados: nenhuma lista local\n"))

    def test_cli_nao_avisa_quando_ha_lista(self):
        self.com_home(termos_no_env="TermoFalsoX")
        saida, erro = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(saida), contextlib.redirect_stderr(erro):
            codigo = main(["verificar_pacote.py", str(self.pasta)])
        self.assertEqual((codigo, saida.getvalue(), erro.getvalue()), (0, "OK\n", ""))

    def test_segredo(self):
        self.escrever(f"{SKILL}/references/contrato.md", "senha=" + "Abc123456789xyz\n")
        self.assertUmProblema("segredo")

    def test_copia_sem_credito(self):
        self.escrever(f"{SKILL}/references/01-copy.md", "# Copy\n\n" + CREDITO + "\n")
        self.assertUmProblema("crédito")

    def test_json_invalido(self):
        self.escrever("plugins/apresentacao-vendas/.claude-plugin/plugin.json", '{"version": "1.0.0"')
        self.assertUmProblema("json")

    def test_versao_do_plugin_diferente_do_changelog(self):
        self.escrever("plugins/apresentacao-vendas/.claude-plugin/plugin.json", '{"version": "1.0.1"}')
        self.assertUmProblema("versão")

    def test_pastas_ignoradas_e_arquivo_binario(self):
        sujeira = f"{CAMINHO_LOCAL}/x {TRAVESSAO} [x](nao-existe.md) senha=" + "Abc123456789xyz\n"
        self.escrever(".superpowers/sdd/x.md", sujeira)
        self.escrever(".git/x.md", sujeira)
        (self.pasta / "imagem.png").write_bytes(b"\xff\xd8\xff\xe0 " + CAMINHO_LOCAL.encode())
        self.assertEqual(verificar(self.pasta), [])

    def test_git_como_arquivo_e_ignorado(self):
        self.escrever(".git", f"gitdir: {CAMINHO_LOCAL}/repo/.git/worktrees/x\n")
        self.assertEqual(verificar(self.pasta), [])

    def test_link_simbolico_quebrado_dentro_do_repositorio_nao_quebra(self):
        os.symlink(self.pasta / "nao-existe", self.pasta / "atalho-quebrado")
        self.assertEqual(verificar(self.pasta), [])

    def test_link_simbolico_mesmo_resultado(self):
        self.acrescentar(f"{SKILL}/SKILL.md", "\n[x](references/nao-existe.md)\n")
        com_link = tempfile.TemporaryDirectory()
        self.addCleanup(com_link.cleanup)
        atalho = Path(com_link.name) / "atalho"
        os.symlink(self.pasta, atalho)
        esperado = verificar(self.pasta)
        self.assertEqual(len(esperado), 1, esperado)
        self.assertEqual(verificar(atalho), esperado)


if __name__ == "__main__":
    unittest.main()

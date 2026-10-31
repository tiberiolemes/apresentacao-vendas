import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SCRIPTS = RAIZ / "plugins/apresentacao-vendas/skills/apresentacao-vendas/scripts"
SCRIPT = SCRIPTS / "validar_conteudo.py"
FIXTURE = Path(__file__).resolve().parent / "fixtures/conteudo-valido.md"

sys.path.insert(0, str(SCRIPTS))
from validar_conteudo import validar  # noqa: E402

TRAVESSAO = "—"


class ValidarConteudoTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ok = FIXTURE.read_text(encoding="utf-8")

    def trocar(self, antigo, novo):
        """Troca a primeira ocorrência e garante que a fixture ainda tem o trecho."""
        self.assertIn(antigo, self.ok)
        return self.ok.replace(antigo, novo, 1)

    def trocar_linha(self, prefixo, nova):
        linhas = self.ok.split("\n")
        i = next(i for i, linha in enumerate(linhas) if linha.startswith(prefixo))
        linhas[i] = nova
        return "\n".join(linhas)

    def sem_linha(self, prefixo):
        return "\n".join(x for x in self.ok.split("\n") if not x.startswith(prefixo))

    def sem_itens(self, secao):
        """Esvazia uma seção feita só de itens `- ...`."""
        texto = re.sub(rf"(^## {secao}\n)(?:- .*\n)+", r"\1", self.ok, flags=re.M)
        self.assertNotEqual(texto, self.ok)
        return texto

    def assertProblema(self, texto, prefixo):
        problemas = validar(texto)
        self.assertTrue(any(p.startswith(prefixo) for p in problemas), f"{prefixo!r} não está em {problemas}")

    def assertSemProblema(self, texto, prefixo):
        problemas = validar(texto)
        self.assertFalse(any(p.startswith(prefixo) for p in problemas), f"{prefixo!r} está em {problemas}")

    def test_fixture_valida(self):
        self.assertEqual(validar(self.ok), [])

    def test_secao_faltando(self):
        texto = re.sub(r"^## PDF\n.*?(?=^## )", "", self.ok, flags=re.M | re.S)
        self.assertEqual(validar(texto), ["seção faltando: PDF"])

    def test_slide_sem_dica(self):
        self.assertProblema(self.sem_linha("- **Dica:** Escute mais do que fala."), "slide `problema`: Dica")

    def test_campo_vazio_conta_como_faltando(self):
        texto = self.trocar("- **Dica:** Escute mais do que fala.", "- **Dica:**")
        self.assertProblema(texto, "slide `problema`: Dica")

    def test_falar_sem_subitem(self):
        # os subitens passam a pertencer a outro campo, e o Falar fica só com texto solto
        texto = self.trocar("- **Falar:**\n", "- **Falar:** frase solta\n- **Roteiro:**\n")
        self.assertProblema(texto, "slide `capa`: Falar")

    def test_tempo_fora_do_formato(self):
        self.assertProblema(self.trocar("- **Tempo:** 1 min", "- **Tempo:** dois minutos"), "slide `capa`: Tempo")

    def test_tempo_com_virgula_vale(self):
        self.assertEqual(validar(self.trocar("- **Tempo:** 1 min", "- **Tempo:** 1,5 min")), [])

    def test_id_invalido(self):
        problemas = validar(self.ok.replace("`problema`", "`Problema`"))
        self.assertIn("id inválido: Problema", problemas)

    def test_id_com_acento(self):
        problemas = validar(self.ok.replace("`proximo-passo`", "`próximo-passo`"))
        self.assertIn("id inválido: próximo-passo", problemas)

    def test_id_repetido(self):
        self.assertProblema(self.trocar("### `combinado`", "### `capa`"), "id inválido: capa")

    def test_titulo_sem_id_entre_crases(self):
        self.assertProblema(self.trocar("### `combinado` ", "### "), "id inválido: Como vamos")

    def test_slide_do_meio_sem_objecao(self):
        texto = self.trocar("- **Objeções:** `preco-alto`", "- **Objeções:** nenhuma")
        self.assertProblema(texto, "slide `como-funciona`: sem objeção")

    def test_slide_do_meio_com_ids_sem_crases_recebe_a_dica_das_crases(self):
        problemas = validar(self.trocar("- **Objeções:** `preco-alto`", "- **Objeções:** preco-alto"))
        self.assertEqual(problemas, ["slide `como-funciona`: Objeções (cite os ids entre crases ou escreva nenhuma)"])

    def test_capa_pode_ficar_sem_objecao(self):
        self.assertIn("- **Objeções:** nenhuma", self.ok)
        self.assertSemProblema(self.ok, "slide `capa`: sem objeção")

    def test_objecao_inexistente_citada(self):
        texto = self.trocar("- **Objeções:** `preco-alto`", "- **Objeções:** `nao-existe`")
        self.assertProblema(texto, "objeção inexistente: nao-existe")

    def test_menos_de_oito_objecoes(self):
        texto = re.sub(r"^### `resultado-garantido`.*?(?=^## )", "", self.ok, flags=re.M | re.S)
        texto = texto.replace("- **Objeções:** `resultado-garantido`", "- **Objeções:** `preco-alto`")
        problemas = validar(texto)
        self.assertEqual(len(problemas), 1)
        self.assertTrue(problemas[0].startswith("objeções: 7"), problemas)

    def test_objecao_sem_resposta(self):
        self.assertProblema(self.trocar_linha("- **Resposta:** Mostre a conta", "- **Resposta:**"), "objeção `preco-alto`: Resposta")

    def test_objecao_sem_quem_levanta(self):
        self.assertProblema(self.sem_linha("- **Quem levanta:** Dono de padaria pequena."), "objeção `preco-alto`: Quem levanta")

    def test_objecao_sem_slide_de_prova(self):
        self.assertProblema(self.trocar("- **Slides:** `conta`", "- **Slides:** nenhum"), "objeção `preco-alto`: Slides")

    def test_objecao_com_slide_inexistente(self):
        self.assertProblema(self.trocar("- **Slides:** `conta`", "- **Slides:** `sumiu`"), "objeção `preco-alto`: Slides")

    def test_o_que_nao_falar_vazio(self):
        self.assertEqual(validar(self.sem_itens("O que não falar")), ["o que não falar vazio"])

    def test_numero_com_fonte_pendente(self):
        texto = self.trocar_linha("- **Fonte:**", "- **Fonte:** Pendente, buscar na entidade do setor.")
        self.assertProblema(texto, "número `sobra-media`: Fonte")

    def test_numero_sem_amostra(self):
        self.assertProblema(self.sem_linha("- **Amostra:**"), "número `sobra-media`: Amostra")

    def test_numero_sem_o_que_mede(self):
        self.assertProblema(self.trocar_linha("- **O que mede:**", "- **O que mede:**"), "número `sobra-media`: O que mede")

    def test_numero_com_uso_em_slide_inexistente(self):
        self.assertProblema(self.trocar("- **Uso:** slide `problema`", "- **Uso:** slide `sumiu`"), "número `sobra-media`: Uso")

    def test_numero_de_reserva_vale(self):
        self.assertEqual(validar(self.trocar("- **Uso:** slide `problema`", "- **Uso:** reserva")), [])

    def test_conta_sem_exemplo(self):
        self.assertProblema(self.trocar("- **Exemplos:**", "- **Casos:**"), "conta: Exemplos")

    def test_conta_sem_formula(self):
        self.assertProblema(self.sem_linha("- **Fórmula:**"), "conta: Fórmula")

    def test_conta_sem_dado_vazio(self):
        self.assertProblema(self.trocar_linha("- **Dado vazio ou zero:**", "- **Dado vazio ou zero:**"), "conta: Dado vazio ou zero")

    def test_mapa_sem_mecanismo(self):
        self.assertProblema(self.sem_linha("| Mecanismo único"), "mapa: Mecanismo único")

    def test_mapa_com_parte_sem_texto(self):
        self.assertProblema(self.trocar_linha("| Verdades", "| Verdades | |"), "mapa: Verdades")

    def test_pergunta_do_comprador_sem_slide(self):
        texto = self.trocar_linha("| 9 |", "| 9 | Outras empresas usam? | número sem crase |")
        self.assertProblema(texto, "pergunta 9")

    def test_pergunta_do_comprador_com_slide_inexistente(self):
        self.assertProblema(self.trocar_linha("| 9 |", "| 9 | Outras empresas usam? | `sumiu` |"), "pergunta 9")

    def test_pergunta_do_comprador_ausente(self):
        self.assertProblema(self.sem_linha("| 14 |"), "pergunta 14")

    def test_termo_proibido_vale_na_lista_do_que_nao_falar(self):
        texto = self.trocar("- Não falar de concorrente pelo nome.", "- Não dizer que o painel é revolucionário.")
        self.assertEqual(validar(texto), [])

    def test_termo_proibido_em_slide_continua_acusado_com_o_mesmo_texto(self):
        texto = self.trocar("Escute mais do que fala.", "Não dizer que o painel é revolucionário.")
        self.assertProblema(texto, "termo proibido: revolucionário")

    def test_travessao_na_lista_do_que_nao_falar_continua_acusado(self):
        texto = self.trocar("- Não falar de concorrente pelo nome.", f"- Não falar {TRAVESSAO} de concorrente.")
        self.assertProblema(texto, "travessão")

    def test_dica_quando_o_campo_da_conta_tem_rotulo_sem_texto(self):
        texto = self.trocar_linha("- **Entradas:**", "- **Entradas:**\n  - `{perda_diaria}`")
        self.assertIn("conta: Entradas (escreva o texto na mesma linha do rótulo)", validar(texto))

    def test_sem_dica_quando_o_campo_da_conta_nem_existe(self):
        self.assertEqual(validar(self.sem_linha("- **Fórmula:**")), ["conta: Fórmula"])

    def test_dica_quando_falar_e_exemplos_nao_tem_subitens(self):
        problemas = validar(self.trocar("- **Falar:**\n", "- **Falar:** frase solta\n- **Roteiro:**\n"))
        self.assertIn("slide `capa`: Falar (use subitens com hífen, recuados)", problemas)
        self.assertIn("conta: Exemplos (use subitens com hífen, recuados)", validar(self.trocar("- **Exemplos:**", "- **Casos:**")))

    def test_subitem_com_quatro_espacos_ou_tab(self):
        quatro = re.sub(r"^  - ", "    - ", self.ok, flags=re.M)
        tab = re.sub(r"^  - ", "\t- ", self.ok, flags=re.M)
        self.assertNotEqual(quatro, self.ok)
        self.assertEqual(validar(quatro), [])
        self.assertEqual(validar(tab), [])

    def test_dois_pontos_fora_do_negrito_valem(self):
        texto = re.sub(r"^- \*\*(.+?):\*\*", r"- **\1**:", self.ok, flags=re.M)
        self.assertNotEqual(texto, self.ok)
        self.assertEqual(validar(texto), [])

    def test_nenhuma_entre_crases_vale(self):
        self.assertEqual(validar(self.trocar("- **Objeções:** nenhuma", "- **Objeções:** `nenhuma`")), [])

    def test_nenhuma_entre_crases_no_meio_ainda_e_sem_objecao(self):
        problemas = validar(self.trocar("- **Objeções:** `preco-alto`", "- **Objeções:** `nenhuma`"))
        self.assertEqual(problemas, ["slide `como-funciona`: sem objeção"])

    def test_numero_da_pergunta_estranho_nao_quebra(self):
        texto = self.trocar_linha("| 9 |", "| ² | Outras empresas usam? | `capa` |")
        self.assertProblema(texto, "pergunta 9")

    def test_pdf_vazio(self):
        self.assertEqual(validar(self.sem_itens("PDF")), ["PDF vazio"])

    def test_travessao(self):
        self.assertProblema(self.trocar("Escute mais do que fala.", f"Escute mais {TRAVESSAO} fala."), "travessão")

    def test_termo_proibido(self):
        self.assertProblema(self.trocar("Escute mais do que fala.", "Potencialize a escuta."), "termo proibido: potencialize")

    def test_termo_proibido_com_acento_e_caixa(self):
        self.assertProblema(self.trocar("Escute mais do que fala.", "Um produto REVOLUCIONÁRIO."), "termo proibido: revolucionário")

    def test_crlf_igual_lf(self):
        self.assertEqual(validar(self.ok.replace("\n", "\r\n")), [])


class CliTest(unittest.TestCase):
    def rodar(self, caminho):
        return subprocess.run(
            [sys.executable, "-I", str(SCRIPT), str(caminho)], capture_output=True, text=True, encoding="utf-8"
        )

    def test_cli_arquivo_inexistente(self):
        with tempfile.TemporaryDirectory() as pasta:
            r = self.rodar(Path(pasta) / "nao-existe.md")
        self.assertEqual(r.returncode, 1)
        self.assertNotIn("Traceback", r.stdout + r.stderr)
        self.assertTrue(r.stdout.startswith("arquivo:"))

    def test_cli_arquivo_vazio(self):
        with tempfile.TemporaryDirectory() as pasta:
            vazio = Path(pasta) / "vazio.md"
            vazio.write_text("", encoding="utf-8")
            r = self.rodar(vazio)
        self.assertEqual(r.returncode, 1)
        self.assertIn("seção faltando", r.stdout)
        self.assertNotIn("Traceback", r.stdout + r.stderr)

    def test_cli_arquivo_que_nao_e_utf8(self):
        with tempfile.TemporaryDirectory() as pasta:
            binario = Path(pasta) / "binario.md"
            binario.write_bytes(b"\xff\xfe\x00")
            r = self.rodar(binario)
        self.assertEqual(r.returncode, 1)
        self.assertNotIn("Traceback", r.stdout + r.stderr)
        self.assertTrue(r.stdout.startswith("arquivo:"))

    def test_cli_sem_argumento(self):
        r = subprocess.run([sys.executable, "-I", str(SCRIPT)], capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(r.returncode, 1)
        self.assertNotIn("Traceback", r.stdout + r.stderr)

    def test_cli_valido_imprime_ok(self):
        r = self.rodar(FIXTURE)
        self.assertEqual((r.returncode, r.stdout.strip()), (0, "OK (6 slides, 8 objeções)"))

    def test_cli_problema_sai_com_1_e_um_por_linha(self):
        with tempfile.TemporaryDirectory() as pasta:
            ruim = Path(pasta) / "ruim.md"
            ruim.write_text(FIXTURE.read_text(encoding="utf-8").replace("- **Tempo:** 1 min", "- **Tempo:** logo"), encoding="utf-8")
            r = self.rodar(ruim)
        self.assertEqual(r.returncode, 1)
        self.assertEqual(len(r.stdout.strip().split("\n")), 1)
        self.assertTrue(r.stdout.startswith("slide `capa`: Tempo"), r.stdout)


if __name__ == "__main__":
    unittest.main()

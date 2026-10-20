# Arquivos do projeto de indutores acoplados

Leia primeiro [o guia em PDF](pdf/01_Guia_de_Projeto.pdf), depois [o exemplo resolvido](pdf/02_Projeto_Exemplo_Resolvido.pdf) e, para a análise dos anexos, [a memória de cálculo](pdf/03_Memoria_de_Calculo.pdf).

O exemplo resolvido usa **36/24 espiras** e uma geometria maior **hipotética**. A memória conserva o estudo inicial de **24/16** para mostrar a revisão do dimensionamento. Essas hipóteses não são especificações aprovadas dos núcleos do laboratório.

## Conteúdo

- `pdf/`: os três PDFs com texto selecionável e sumário.
- `GUIA_PROJETO.md`, `EXEMPLO_RESOLVIDO.md`, `PROJETO.md`: fontes editáveis dos documentos.
- `LEIA_AQUI_Guia_e_Projeto.md` e `.txt`: guia e exemplo completos reunidos para leitura/cópia.
- `calculo.py`: conferência das correntes de 50 kHz, com o estudo inicial de 24/16.
- `exemplo_completo.py`: exemplo ampliado de 36/24, camadas, comprimentos por camada, resistência, ocupação e orçamento térmico.
- `parametros_exemplo.json`: parâmetros do estudo inicial.
- `parametros_projeto_exemplo.json`: parâmetros do exemplo ampliado.
- `dados/CorrenteIndutor.txt`: dados fornecidos pelo usuário necessários à reprodução.
- `resultados/` e `resultados_exemplo/`: resultados JSON/CSV e gráfico SVG.
- `figuras/`: desenhos e gráficos incluídos no exemplo.
- `verificacao/`: registros visuais dos PDFs e fonte LaTeX intermediária de verificação.
- `historico/`: primeira entrega preliminar preservada, com parâmetros e documentos daquela etapa.
- `gerar_figuras.py`, `escrever_exemplo.py`, `gerar_pdfs.py`, `cabecalho_pdf.tex`: reprodução de figuras e documentos.
- `empacotar.py`: cria o ZIP e o manifesto SHA-256 a partir desta pasta.
- `pacotes/Projeto_Indutores_Pacote_Completo.zip`: arquivos gerados para baixar.
- `MANIFESTO_SHA256.txt`: integridade dos arquivos atuais do pacote.

## Reproduzir as contas

Requer **Python 3.11 ou posterior** por causa da versão fixada do NumPy; validado com Python 3.12.14, NumPy 2.3.5 e Matplotlib 3.10.8. O exemplo ampliado usa apenas a biblioteca padrão de Python. NumPy serve à análise das curvas; Matplotlib regenera as figuras.

Dentro desta pasta:

```sh
python -m venv .venv
# Linux/macOS:
. .venv/bin/activate
# Windows PowerShell, em vez da linha anterior:
# .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python calculo.py --correntes dados/CorrenteIndutor.txt --saida resultados
python exemplo_completo.py --config parametros_projeto_exemplo.json --saida resultados_exemplo
```

A análise de `calculo.py` é específica dos dados de 50 kHz recebidos. Não alterar a frequência do arquivo para simular 100 kHz: são necessários novos dados. O código valida a coerência de `n` com `Ns/Np`.

Para regenerar o exemplo escrito, as figuras e o pacote:

```sh
python escrever_exemplo.py
python gerar_figuras.py
python empacotar.py
```

Os PDFs já estão prontos para leitura. Para regenerá-los são necessários Pandoc, XeLaTeX/TeX Live, fontes DejaVu e os pacotes LaTeX usados no cabeçalho:

```sh
python gerar_pdfs.py
python empacotar.py
```

Ao alterar parâmetros, revise também as passagens explicativas que contêm escolhas fixas e números no texto. O gerador de documentos não substitui a revisão de engenharia.

## Referências e limitações

As referências metodológicas são os arquivos `PROJETO_INDUTOR.pdf` e `McLyman.pdf` fornecidos pelo usuário. **Os originais, suas extrações integrais de texto e suas imagens não integram esta publicação nem o ZIP atual.** Utilize as cópias originais que já possui.

O arquivo PSIM `.smv` excedeu o limite de transferência de 32 MiB e não pôde ser aberto. A planilha de estoque e `PROJETO_INDUTOR(1).pdf` não foram recebidos. Os datasheets oficiais não foram acessados devido ao bloqueio de rede. Não há dados simulados de 100 kHz, transientes ou correntes físicas dos quatro enrolamentos.

As perdas DC dos exemplos usam RMS e temperatura explicitamente hipotéticos. As perdas AC, de ferrite e a temperatura real não foram validadas. O orçamento térmico é uma condição de aceitação de estudo. Fringing, polarização CC, isolação e ensaios precisam ser verificados antes da fabricação/energização nominal.

O conteúdo do ZIP é o estado dos documentos quando `empacotar.py` foi executado. O histórico conserva resultados preliminares antigos; os documentos atuais e esta página são a referência da entrega.

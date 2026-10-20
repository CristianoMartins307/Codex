# Projeto de indutores acoplados — conversor CC-CC de 2 kW

Documentos e cálculos gerados para o estudo de dois indutores acoplados a **50 kHz e 100 kHz**.

## Arquivos para baixar

- **[Pacote completo dos arquivos gerados — ZIP](indutores/pacotes/Projeto_Indutores_Pacote_Completo.zip)**
- [Guia: como fazer o projeto — PDF, 15 páginas](indutores/pdf/01_Guia_de_Projeto.pdf)
- [Projeto resolvido como exemplo — PDF, 11 páginas](indutores/pdf/02_Projeto_Exemplo_Resolvido.pdf)
- [Memória de cálculo — PDF, 14 páginas](indutores/pdf/03_Memoria_de_Calculo.pdf)

Abra o arquivo desejado no GitHub e utilize a opção de baixar o arquivo. O ZIP contém os documentos, fontes editáveis, códigos, dados de corrente, resultados, desenhos e registros de verificação.

## Ler e reproduzir

- [Instruções completas e reprodução dos cálculos](indutores/README.md)
- [Guia e exemplo reunidos para leitura no navegador](indutores/LEIA_AQUI_Guia_e_Projeto.md)
- [Análise das correntes de 50 kHz](indutores/calculo.py)
- [Código do exemplo de 36/24 espiras](indutores/exemplo_completo.py)
- [Resultados numéricos do exemplo](indutores/resultados_exemplo/exemplo_resultados.json)

## Situação técnica

As correntes magnetizantes de 50 kHz foram recalculadas a partir do arquivo recebido. O exemplo resolvido usa geometria e correntes físicas hipotéticas identificadas nos documentos; não é uma liberação para fabricação e operação nominal. Faltam, entre outros dados, as correntes físicas dos enrolamentos, curvas oficiais dos materiais, transientes e a simulação de 100 kHz.

Os PDFs de referência enviados originalmente pelo usuário não são publicados neste repositório. A pasta `historico` conserva a primeira entrega preliminar apenas para rastreabilidade; para leitura e construção do exemplo, utilize os documentos atuais em `indutores/pdf/`.

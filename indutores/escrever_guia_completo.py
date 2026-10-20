#!/usr/bin/env python3
"""Reúne guia, exemplo resolvido e fluxogramas em uma fonte Markdown."""
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parent


def sections(filename):
    text = (ROOT/filename).read_text(encoding='utf-8')
    text = text.split('\n', 1)[1].lstrip() if text.startswith('# ') else text
    # Rebaixa os títulos para que as partes do documento tenham hierarquia própria.
    return re.sub(r'(?m)^(#{2,5}) ', lambda m: '#'+m.group(1)+' ', text)


def main():
    data = json.loads((ROOT/'resultados_exemplo/exemplo_resultados.json').read_text())
    r = data['resultados']
    body = '''# Guia completo: projeto de indutores acoplados com exemplo e fluxograma

## Como utilizar este documento

Este PDF reúne o procedimento de projeto, um exemplo numérico resolvido e dois fluxogramas. Foi preparado para estudar dois componentes magnéticos idênticos de um conversor CC-CC de 2 kW nas frequências de 50 kHz e 100 kHz.

O objetivo é permitir refazer os cálculos e preparar uma ficha de fabricação. O caso de 50 kHz tem dados numéricos de magnetização verificados. O exemplo de construção utiliza hipóteses explícitas de geometria, correntes físicas e envelope de corrente. **Essas hipóteses não representam um núcleo comercial homologado nem uma liberação para energizar o conversor em potência nominal.**

### Sequência recomendada de leitura

1. Use os fluxogramas para entender a sequência e os retornos de revisão.
2. Leia o método para identificar os dados necessários e a origem das equações.
3. Refaça o exemplo numérico, comparando cada resultado com o código Python.
4. Substitua as hipóteses pelos dados reais do laboratório e da simulação.
5. Execute a validação elétrica, magnética e térmica antes de concluir a fabricação.

### Ficha rápida do exemplo resolvido

| Item | Valor adotado ou calculado | Natureza |
|---|---:|---|
| Lm por componente | 209 µH | Requisito, referência primária a confirmar no modelo |
| Np / Ns | 36 / 24 espiras | Escolha didática, razão 2/3 |
| Arranjo | P1=18, S=24, P2=18 | Primário em série aditiva |
| Correntes físicas RMS P / S | 8 A / 6 A | Hipóteses, não correntes extraídas de iM |
| Envelope de corrente | 10 A | Hipótese de estudo, não transiente medido |
| Ae / Aw | 354 mm² / 400 mm² | Geometria hipotética maior |
| Condutores P / S | 53 / 40 fios AWG30 em paralelo | Exemplo de dimensionamento |
| Gap equivalente inicial | 2,69849 mm | Sem espraiamento; não gap físico aprovado |
| B no envelope e com tolerâncias | 0,181262 T | L+5%, Ae−5%; ainda requer material quente |
| Ocupação geométrica estimada | 0,75188 | Feixes e isolamento hipotéticos |
| Referência de perdas de cobre DC | 4,75776 W | RMS hipotéticos e cobre a 100 °C |

Os dois indutores são unidades separadas, cada uma com P e S. Não confundir Lm1/Lm2 com os dois enrolamentos de um único componente. Não multiplicar a potência total pelo número de referências de saída do barramento.

As perdas AC, de ferrite, a dispersão real e a temperatura final dependem de dados e ensaios ainda pendentes. O orçamento térmico mostrado no exemplo é uma condição de aceitação de estudo, não um resultado experimental.

## Parte 1 — Fluxograma do projeto

### Dimensionamento eletromagnético e térmico

O primeiro fluxo organiza os dados, esforços, seleção, espiras, janela e perdas. Os ramos laterais indicam pendências ou revisões. Se faltar evidência, o estudo continua condicional e não libera fabricação nominal.

![Fluxograma de dimensionamento: dados, esforços, núcleo, espiras, condutores e perdas.](figuras/fluxograma_1.png){width=100%}

### Construção e validação experimental

O segundo fluxo organiza bobinamento, montagem, LCR, ensaios sob corrente, isolação, aquecimento e comparação de frequências. LCR em pequeno sinal não verifica saturação nominal sozinho.

![Fluxograma de fabricação e validação experimental dos dois componentes.](figuras/fluxograma_2.png){width=100%}

## Parte 2 — Como fazer o projeto, passo a passo

'''
    body += sections('GUIA_PROJETO.md')
    body += '\n\n## Parte 3 — Projeto resolvido como exemplo numérico\n\n'
    body += sections('EXEMPLO_RESOLVIDO.md')
    body += '\n\n## Parte 4 — Arquivos para reproduzir e conferir\n\n'
    body += '''Os arquivos editáveis, códigos, resultados, PDFs e imagens estão publicados no repositório GitHub autorizado pelo usuário:

https://github.com/CristianoMartins307/Codex/tree/main/indutores

O fluxograma também é entregue em PDF separado (`pdf/05_Fluxograma_Projeto.pdf`) e em PNG/SVG na pasta `figuras/`. Para reproduzir os cálculos, consulte `README.md`, `calculo.py` e `exemplo_completo.py`.

A memória original de análise dos anexos permanece em `pdf/03_Memoria_de_Calculo.pdf`. O exemplo resolvido atual usa 36/24 espiras; os 24/16 da análise inicial mostram uma etapa de revisão, sem aprovação para o envelope de 10 A.
'''
    path = ROOT/'GUIA_COM_EXEMPLO_E_FLUXOGRAMA.md'
    path.write_text(body, encoding='utf-8')
    print('Guia completo escrito:', len(body.split()), 'palavras')


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Gera os fluxogramas de dimensionamento e validação em PDF, PNG e SVG."""
import os
os.environ.setdefault('MPLCONFIGDIR', '/tmp/mpl_indutores')
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon, FancyArrowPatch
from matplotlib.backends.backend_pdf import PdfPages

ROOT = Path(__file__).resolve().parent
FIG = ROOT / 'figuras'
FIG.mkdir(exist_ok=True)
(ROOT / 'pdf').mkdir(exist_ok=True)
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 9})


def page(title, subtitle, nodes, notes, returns, footer):
    fig, ax = plt.subplots(figsize=(8.27, 11.69))
    fig.subplots_adjust(left=.035, right=.965, top=.96, bottom=.035)
    ax.set(xlim=(0, 15), ylim=(0, 20.8))
    ax.axis('off')
    ax.text(.5, 20.5, title, fontsize=16, fontweight='bold', color='#164b6b', va='top')
    ax.text(.5, 19.76, subtitle, fontsize=9, color='#586a76', va='top')
    cx, width = 6.1, 9.1
    ys = [18.6 - i*1.45 for i in range(len(nodes))]
    heights = []
    for i, ((kind, text), y) in enumerate(zip(nodes, ys)):
        h = 1.04 if kind != 'decision' else 1.25
        heights.append(h)
        if kind == 'decision':
            ax.add_patch(Polygon([(cx-width/2, y), (cx, y+h/2),
                                  (cx+width/2, y), (cx, y-h/2)],
                                 closed=True, fc='#fff1d6', ec='#a56b00', lw=1.1))
        else:
            color = '#d8ebf6' if kind == 'box' else '#d9efdf'
            ax.add_patch(FancyBboxPatch((cx-width/2, y-h/2), width, h,
                                        boxstyle='round,pad=0.035,rounding_size=.14',
                                        fc=color, ec='#164b6b', lw=1))
        ax.text(cx, y, text, ha='center', va='center', fontsize=8.8)
        if i:
            start = (cx, ys[i-1]-heights[i-1]/2)
            end = (cx, y+h/2)
            ax.add_patch(FancyArrowPatch(start, end, arrowstyle='-|>',
                                         mutation_scale=10, lw=1, color='#164b6b'))
            if nodes[i-1][0] == 'decision':
                ax.text(cx+.17, (start[1]+end[1])/2, 'Sim', fontsize=7.6, va='center')
    for idx, text in notes.items():
        y = ys[idx]
        ax.add_patch(FancyArrowPatch((cx+width/2, y), (11.3, y),
                                    arrowstyle='-|>', mutation_scale=9, color='#a56b00', lw=1))
        ax.text(11.0, y+.18, 'Não', fontsize=6.7, ha='center', color='#875600')
        ax.add_patch(FancyBboxPatch((11.42, y-.55), 3.0, 1.1,
                                   boxstyle='round,pad=.04', fc='#fff7e7', ec='#a56b00', lw=.8))
        ax.text(12.92, y, text, ha='center', va='center', fontsize=7.0)
    for idx, destination, label in returns:
        y, target = ys[idx], ys[destination]
        xret = .55
        ax.plot([cx-width/2, xret, xret], [y, y, target], color='#a56b00', lw=.8)
        ax.add_patch(FancyArrowPatch((xret, target), (cx-width/2, target),
                                    arrowstyle='-|>', mutation_scale=9, color='#a56b00', lw=.8))
        ax.text(.25, (y+target)/2, label, fontsize=6.3, rotation=90,
                ha='center', va='center', color='#875600')
    ax.text(.55, .64, footer, fontsize=8.0, color='#444', va='bottom',
            bbox=dict(boxstyle='round,pad=.4', fc='#f2f5f7', ec='#ccd4da'))
    return fig


def main():
    nodes1 = [
        ('box', '1. Definir requisitos e confirmar circuito\n2 kW totais; dois componentes; pontos; referência de Lm/Lk'),
        ('box', '2. Obter simulações e materiais reais\niM(t), iP(t), iS(t), vM(t); transientes; 50/100 kHz; estoque'),
        ('decision', '3. Dados suficientes e rastreáveis?'),
        ('box', '4. Calcular esforços e conferir ondulação\nRMS físicos, picos, volt-segundos e energia\nPropor mudanças de Lm em estudo separado'),
        ('box', '5. Comparar núcleo e carretel\nAe, Amin, Aw útil, material, quantidade e método AeAw'),
        ('box', '6. Escolher Np/Ns inteiros e calcular gap\nFluxo CC + excursão AC; tolerâncias; fringing'),
        ('decision', '7. Margem magnética suficiente?'),
        ('box', '8. Dimensionar fios, isolamento e camadas\nCorrentes de cada enrolamento; paralelos/Litz; proximidade'),
        ('decision', '9. Janela e construção viáveis?'),
        ('box', '10. Avaliar perdas e resfriamento\nCobre AC, ferrite, campo do gap e ponto quente'),
        ('decision', '11. Limites comprovados?'),
        ('end', '12. Preparar ficha e protótipo\nSem comprovação: manter estudo condicional\nSem liberação para potência nominal'),
    ]
    fig1 = page('1 | Dimensionamento do projeto',
                'Azul: cálculo/ação. Losango: decisão. Ramo lateral: pendência ou revisão.',
                nodes1,
                {2: 'Registrar pendências.\nSó calcular cenários\ncondicionais.',
                 6: 'Rever espiras,\nnúcleo e envelope.\nRetornar à etapa 5.',
                 8: 'Rever feixes,\ndisposição ou núcleo.\nRetornar à etapa 5/8.',
                 10: 'Rever perdas e gap.\nSem evidência:\nsem liberação nominal.'},
                [(6, 4, 'Revisar magnetismo')],
                '209 µH é o projeto original. A mudança para 20% de ondulação deve ser estudada separadamente.\nSem dados de 100 kHz, a comparação nessa frequência permanece condicional.')
    nodes2 = [
        ('box', '1. Conferir materiais e geometria\nNúcleo, carretel, fios, margens e sistema de isolamento'),
        ('box', '2. Preparar feixes e bobinar\nP1–S–P2; contar espiras; identificar inícios/fins; P em série aditiva'),
        ('box', '3. Montar núcleo e gap provisórios\nFixação reversível; pressão repetível; evitar espira em curto'),
        ('box', '4. Ensaiar com LCR\nLp/Ls, polaridade, relação, M, k e dispersão na mesma referência'),
        ('decision', '5. Indutâncias e dispersão atendem?'),
        ('box', '6. Validar com corrente e temperatura reais\nL incremental, reset e margem de saturação; instrumentação adicional'),
        ('decision', '7. Margem sob corrente comprovada?'),
        ('box', '8. Ensaiar isolação e aquecimento\nProteção, potência progressiva e monitoramento do ponto quente'),
        ('decision', '9. Todos os ensaios aprovados?'),
        ('box', '10. Construir e conferir a segunda unidade\nMesma ficha; verificar pareamento e polaridades de cada ramo'),
        ('box', '11. Comparar 50 e 100 kHz\nMesmas cargas, potência total, montagem e condições térmicas'),
        ('end', '12. Registrar resultados e concluir\nMateriais, tolerâncias, perdas, limites e condições de operação'),
    ]
    fig2 = page('2 | Fabricação e validação',
                'O fluxo só termina após ensaios que comprovem as condições de operação.',
                nodes2,
                {4: 'Ajustar gap ou\nrever bobinamento.\nRepetir LCR.',
                 6: 'Rever projeto\nmagnético e limites\nde proteção.',
                 8: 'Rever construção,\nisolamento, perdas\ne resfriamento.'},
                [(4, 2, 'Ajustar e repetir')],
                'LCR sozinho não comprova saturação nem aptidão térmica. Ensaios em potência exigem proteção.\nOs 10 A e a geometria do exemplo são hipóteses didáticas, não condições já validadas.')
    path = ROOT/'pdf'/'05_Fluxograma_Projeto.pdf'
    with PdfPages(path) as pdf:
        for number, fig in enumerate([fig1, fig2], 1):
            pdf.savefig(fig)
            fig.savefig(FIG/f'fluxograma_{number}.png', dpi=220)
            fig.savefig(FIG/f'fluxograma_{number}.svg')
            plt.close(fig)
    print('Fluxograma gerado:', path)


if __name__ == '__main__':
    main()

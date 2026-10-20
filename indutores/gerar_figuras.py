#!/usr/bin/env python3
import os
os.environ.setdefault('MPLCONFIGDIR','/tmp/mpl_indutores')
from pathlib import Path
import json, numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
p=Path(__file__).resolve().parent;o=p/'figuras';o.mkdir(exist_ok=True)
x=np.loadtxt(p/'dados/CorrenteIndutor.txt',skiprows=1)
mask=(x[:,0]>=.03494)&(x[:,0]<=.03504)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10})
fig,ax=plt.subplots(figsize=(9.3,3.7),layout='constrained')
for j,col in [(1,'#0868ac'),(2,'#d94801')]:ax.plot((x[mask,0]-.03494)*1e6,x[mask,j],label=f'I(Lm{j})',color=col,lw=1.7)
ax.set(xlabel='Tempo após 34,940 ms (µs)',ylabel='Corrente magnetizante (A)',title='Cinco períodos a 50 kHz — dados do arquivo fornecido',xlim=(0,100))
ax.grid(alpha=.25);ax.legend(ncol=2);fig.savefig(o/'correntes_50k.png',dpi=180);plt.close(fig)
# Corte radial hipotético; não é um desenho do núcleo comercial.
fig,ax=plt.subplots(figsize=(9.3,5.3),layout='constrained');ax.set_xlim(-2,28);ax.set_ylim(-1,18)
ax.add_patch(Rectangle((0,0),25,16,fill=False,ec='#263238',lw=1.5))
sections=[(.2,4.6,'P1: 18 espiras (7 + 7 + 4)\n53 fios AWG30 em paralelo','#b5d9f1'),(5.3,3.7,'S: 24 espiras (8 + 8 + 8)\n40 fios AWG30 em paralelo','#ffd39e'),(9.5,4.6,'P2: 18 espiras (7 + 7 + 4)\n53 fios AWG30 em paralelo','#b5d9f1')]
for y,h,label,color in sections:
 ax.add_patch(Rectangle((0,y),25,h,fc=color,ec='#444',lw=.7));ax.text(12.5,y+h/2,label,ha='center',va='center',fontsize=10)
ax.text(12.5,15.1,'Isolamento externo + folga residual',ha='center',va='center',fontsize=9)
ax.annotate('',(26,0),(26,16),arrowprops={'arrowstyle':'<->','lw':1});ax.text(26.5,8,'16 mm úteis',rotation=90,va='center')
ax.annotate('',(0,-.5),(25,-.5),arrowprops={'arrowstyle':'<->','lw':1});ax.text(12.5,-.8,'25 mm úteis; margens elétricas fora desta largura',ha='center',va='top',fontsize=9)
ax.set_title('Janela hipotética — corte radial do enrolamento P1–S–P2',fontsize=12,pad=12);ax.axis('off');fig.savefig(o/'arranjo_exemplo.png',dpi=180);plt.close(fig)
fig,ax=plt.subplots(figsize=(9.3,3.3),layout='constrained');ax.axis('off');ax.set_xlim(0,10);ax.set_ylim(0,3)
ax.plot([.8,9.2],[2,2],color='#0868ac',lw=2)
for left,title in [(1.6,'P1 — 18 espiras'),(5.9,'P2 — 18 espiras')]:
 ax.add_patch(Rectangle((left,1.55),2.5,.9,fc='#d7e9f5',ec='#0868ac'));ax.text(left+1.25,2,title,ha='center',va='center',fontsize=10)
ax.text(.8,2.35,'P início •',ha='center');ax.text(9.2,2.35,'P fim',ha='center');ax.text(5.05,1.2,'Emenda: fim de P1 com início de P2\nConfirmar série aditiva antes de isolar',ha='center',fontsize=10)
ax.add_patch(Rectangle((3.7,.05),2.5,.65,fc='#ffe1b8',ec='#d94801'));ax.text(4.95,.37,'S — 24 espiras',ha='center',va='center')
ax.text(3.3,.37,'S início •',ha='right',va='center');ax.text(6.6,.37,'S fim',ha='left',va='center');ax.set_title('Terminais do exemplo: a polaridade final deve ser ensaiada')
fig.savefig(o/'terminais_exemplo.png',dpi=180);plt.close(fig)
print('Três figuras geradas.')

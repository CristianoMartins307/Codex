#!/usr/bin/env python3
from pathlib import Path
import subprocess,os
from concurrent.futures import ThreadPoolExecutor
p=Path(__file__).resolve().parent
os.environ['XDG_CACHE_HOME']='/tmp/indutores_cache'
os.environ['TEXMFVAR']='/tmp/indutores_texvar'
os.environ['TEXMFCONFIG']='/tmp/indutores_texconfig'
for x in ['pdf','.build']:(p/x).mkdir(exist_ok=True)
items=[('GUIA_PROJETO.md','01_Guia_de_Projeto.pdf','Como projetar indutores acoplados','Método, construção e ensaios — 50 kHz e 100 kHz'),('EXEMPLO_RESOLVIDO.md','02_Projeto_Exemplo_Resolvido.pdf','Projeto resolvido como exemplo','Cálculos reproduzíveis — geometria hipotética de 36/24 espiras'),('PROJETO.md','03_Memoria_de_Calculo.pdf','Memória de cálculo e análise dos anexos','Dados verificados, pré-dimensionamento e pendências')]
def build(it):
 src,dest,title,sub=it
 s=(p/src).read_text();s=s.split('\n',1)[1].lstrip() if s.startswith('# ') else s
 tmp=p/'.build'/src;tmp.write_text(s.replace('ℓ','l'))
 cmd=['pandoc',str(tmp),'--from=markdown','--pdf-engine=xelatex','--resource-path='+str(p),'--standalone','--toc','--toc-depth=2','--metadata','toc-title=Conteúdo','--metadata','lang=pt-BR','--metadata','title='+title,'--metadata','subtitle='+sub,'--metadata','date=20 de outubro de 2026','-V','documentclass=article','-V','fontsize=10pt','-V','papersize=a4','-V','geometry:top=24mm,bottom=23mm,left=20mm,right=20mm','-V','mainfont=DejaVu Sans','-V','sansfont=DejaVu Sans','-V','monofont=DejaVu Sans Mono','--highlight-style=tango','--include-in-header='+str(p/'cabecalho_pdf.tex'),'-o',str(p/'pdf'/dest)]
 r=subprocess.run(cmd,cwd=p,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
 (p/'.build'/(dest+'.log')).write_text(r.stdout)
 print(dest,'status',r.returncode,'bytes',(p/'pdf'/dest).stat().st_size if (p/'pdf'/dest).exists() else 0)
 if r.returncode:print(r.stdout[-6000:]);raise RuntimeError(dest)
 return dest
with ThreadPoolExecutor(max_workers=3) as ex:list(ex.map(build,items))

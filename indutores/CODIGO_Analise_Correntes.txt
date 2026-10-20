#!/usr/bin/env python3
"""Análise reproduzível. Exemplo geométrico NÃO equivale a núcleo homologado.
Uso: python calculo.py --correntes ARQUIVO --saida DIRETORIO [--config JSON]
Config JSON sobrescreve os parâmetros exibidos em resultados.json.
Dependência: numpy (ambiente validado: 2.3.5).
"""
import argparse, json, math, csv
from pathlib import Path
import numpy as np

def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--correntes',required=True);p.add_argument('--saida',default='resultados');p.add_argument('--config')
 a=p.parse_args(); out=Path(a.saida);out.mkdir(parents=True,exist_ok=True)
 c=dict(L_H=209e-6,n=2/3,f_Hz=50000,t_inicio_s=.03494,periodos=5,
        Ae_mm2=354,Aw_mm2=250,le_mm=120,mu_r=2000,Np=24,Ns=16,
        I_projeto_A=7.83,B_lim_T=.20,J_A_mm2=3,ku=.25,
        Ip_rms_exemplo_A=8,Is_rms_exemplo_A=6,MLT_p_mm=116,MLT_s_mm=116,
        temperatura_cobre_C=100,terminais_p_m=.20,terminais_s_m=.20,
        fio_AWG=30,fios_p=53,fios_s=40,diametro_esmalte_mm=.30,
        empacotamento=.785,area_isolamentos_mm2=20)
 if a.config:c.update(json.loads(Path(a.config).read_text()))
 if c['f_Hz']!=50000:raise ValueError('Este analisador usa dados de 50 kHz; a extrapolação de 100 kHz é separada. Não redefina a frequência do arquivo.')
 if not math.isclose(c['n'],c['Ns']/c['Np'],rel_tol=1e-9):raise ValueError('n deve ser coerente com Ns/Np; ajuste todos os parâmetros relacionados.')
 x=np.loadtxt(a.correntes,skiprows=1)
 if x.ndim!=2 or x.shape[1]!=3 or not np.all(np.isfinite(x)) or np.any(np.diff(x[:,0])<=0):raise ValueError('Dados inválidos')
 t0=c['t_inicio_s'];t1=t0+c['periodos']/c['f_Hz']
 if t0<x[0,0] or t1>x[-1,0]:raise ValueError('Janela fora do arquivo')
 t=np.r_[t0,x[(x[:,0]>t0)&(x[:,0]<t1),0],t1]; results={}
 for j in (1,2):
  y=np.interp(t,x[:,0],x[:,j]);mean=float(np.trapezoid(y,t)/(t1-t0))
  # Integral exata do quadrado de interpolação linear, não média de amostras.
  rms=float(np.sqrt(np.sum(np.diff(t)*(y[:-1]**2+y[:-1]*y[1:]+y[1:]**2)/3)/(t1-t0)))
  lo=float(y.min());hi=float(y.max()); pp=hi-lo
  results[f'Lm{j}']=dict(media_A=mean,rms_A=rms,min_A=lo,max_A=hi,pp_A=pp,ripple_pct=100*pp/mean,
   min_arquivo_A=float(x[:,j].min()),max_arquivo_A=float(x[:,j].max()),
   L_para_20pct_uH=c['L_H']*pp/(.2*mean)*1e6,
   ripple_100k_condicional_pct=100*pp/(2*mean),
   volts_segundos_Vs=c['L_H']*pp,
   tensao_derivada_p10_V=float(np.quantile(np.diff(x[:,j])/np.diff(x[:,0]),.1)*c['L_H']),
   tensao_derivada_p90_V=float(np.quantile(np.diff(x[:,j])/np.diff(x[:,0]),.9)*c['L_H']))
 L=c['L_H'];Ae=c['Ae_mm2']*1e-6;Np=c['Np'];Ns=c['Ns'];ip=c['I_projeto_A'];mu0=4*math.pi*1e-7
 awg=c['fio_AWG'];d=.127*92**((36-awg)/39);area=math.pi*d*d/4
 ap=area*c['fios_p'];ass=area*c['fios_s'];rho=.01724*(1+.00393*(c['temperatura_cobre_C']-20))
 lp=Np*c['MLT_p_mm']/1000+c['terminais_p_m'];ls=Ns*c['MLT_s_mm']/1000+c['terminais_s_m'];rp=rho*lp/ap;rs=rho*ls/ass
 Pdc=c['Ip_rms_exemplo_A']**2*rp+c['Is_rms_exemplo_A']**2*rs
 wire_window=(Np*c['fios_p']+Ns*c['fios_s'])*math.pi*c['diametro_esmalte_mm']**2/4
 ex=dict(AVISO='EXEMPLO HIPOTETICO; NÃO LIBERADO PARA FABRICAÇÃO',
  B_pico_T=L*ip/(Np*Ae),B_10A_T=L*10/(Np*Ae),
  delta_B_50_T=L*results['Lm1']['pp_A']/(Np*Ae),
  delta_B_100_condicional_T=L*results['Lm1']['pp_A']/(2*Np*Ae),
  energia_pico_J=.5*L*ip**2,AL_nH=L/Np**2*1e9,Ls_ideal_uH=L*(Ns/Np)**2*1e6,
  gap_ideal_total_mm=mu0*Np*Np*Ae/L*1000,
  gap_sem_fringing_mm=(mu0*Np*Np*Ae/L-c['le_mm']/1000/c['mu_r'])*1000,
  produto_areas_requerido_cm4=L*ip*(c['Ip_rms_exemplo_A']+c['n']*c['Is_rms_exemplo_A'])/(c['B_lim_T']*c['J_A_mm2']*1e6*c['ku'])*1e8,
  diametro_cobre_mm=d,area_fio_mm2=area,area_p_mm2=ap,area_s_mm2=ass,
  Jp_A_mm2=c['Ip_rms_exemplo_A']/ap,Js_A_mm2=c['Is_rms_exemplo_A']/ass,
  comprimento_p_m=lp,comprimento_s_m=ls,Rp_ohm=rp,Rs_ohm=rs,
  perda_DC_exemplo_W=Pdc,
  FE_anexo=wire_window/c['Aw_mm2'],
  FE_geometrico_estimado=(wire_window/c['empacotamento']+c['area_isolamentos_mm2'])/c['Aw_mm2'],
  sensibilidade_perda_cobre_fatores_1p5_2_3_W=[Pdc*k for k in [1.5,2,3]],
  delta_cobre_50_mm=math.sqrt(.01724*1e-6/(math.pi*50000*mu0))*1000,
  delta_cobre_100_mm=math.sqrt(.01724*1e-6/(math.pi*100000*mu0))*1000)
 result=dict(parametros=c,arquivo=dict(amostras=len(x),inicio_s=float(x[0,0]),fim_s=float(x[-1,0])),janela_s=[t0,t1],correntes=results,exemplo=ex)
 (out/'resultados.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
 with (out/'correntes_resumo.csv').open('w') as f:
  w=csv.writer(f);w.writerow(['componente',*next(iter(results.values())).keys()])
  for k,v in results.items():w.writerow([k,*v.values()])
 # Gráfico SVG independente de bibliotecas gráficas.
 colors=['#0868ac','#d94801']; lines=[]
 for j in (1,2):
  y=np.interp(t,x[:,0],x[:,j]);pts=' '.join(f'{65+(tt-t0)/(t1-t0)*900:.2f},{330-(yy-4)*65:.2f}' for tt,yy in zip(t,y))
  lines.append(f'<polyline points="{pts}" fill="none" stroke="{colors[j-1]}" stroke-width="1.7"/>')
 svg='<svg xmlns="http://www.w3.org/2000/svg" width="1040" height="410" viewBox="0 0 1040 410"><rect width="1040" height="410" fill="white"/><g font-family="sans-serif" font-size="15"><text x="65" y="25">Correntes magnetizantes — 50 kHz — cinco períodos</text>'
 for val in range(4,9):
  yy=330-(val-4)*65;svg+=f'<path d="M65 {yy}H965" stroke="#ddd"/><text x="30" y="{yy+5}">{val} A</text>'
 svg+=''.join(lines)+'<text x="65" y="370">34,940 ms</text><text x="875" y="370">35,040 ms</text><text x="350" y="400" fill="#0868ac">I(Lm1)</text><text x="500" y="400" fill="#d94801">I(Lm2)</text></g></svg>'
 (out/'correntes.svg').write_text(svg)
 print(json.dumps(result,indent=2,ensure_ascii=False))
if __name__=='__main__':main()

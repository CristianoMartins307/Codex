#!/usr/bin/env python3
"""Exemplo didático: geometria maior hipotética, sem catálogo/ensaio de validação.
As hipóteses não são especificações dos núcleos do laboratório.
Uso: python exemplo_completo.py [--config parametros_projeto_exemplo.json] [--saida resultados_exemplo]
"""
import argparse,json,math,csv
from pathlib import Path

BASE=dict(L_uH=209,L_tolerancia_pct=5,Ae_mm2=354,Ae_tolerancia_pct=5,Aw_mm2=400,
 le_mm=120,mu_r=2000,Np=36,Ns=24,I_envelope_A=10,I_referencia_A=7.83,
 B_lim_T=.20,J_lim_A_mm2=3,ku_projeto=.35,Ip_rms_hipotetico_A=8,Is_rms_hipotetico_A=6,
 AWG=30,fios_p=53,fios_s=40,d_externo_mm=.30,
 perimetro_base_mm=114,terminais_p_m=.20,terminais_s_m=.20,
 T_cobre_C=100,empacotamento=.785,reserva_area_extra_mm2=0,
 largura_util_mm=25,altura_util_mm=16,feixe_p_largura_mm=3.3,feixe_p_altura_mm=1.5,
 feixe_s_largura_mm=3,feixe_s_altura_mm=1.2,
 Im1_media_50_A=6.099703167946442,Im2_media_50_A=5.966344864362196,
 delta_Im1_50_A=3.4501192595111414,delta_Im2_50_A=3.4530835326838742,
 T_amb_C=25,T_lim_exemplo_C=80,Rtheta_meta_K_W=5,
 espessura_inicial_mm=.20,espessura_barreira_PS_mm=.50,
 espessura_fita_entre_camadas_mm=.05,espessura_externa_mm=.20,
 Pcore_orcamento_W=3,fator_cobre_orcamento=1.5)

def calcular(c):
 mu0=4*math.pi*1e-7;L=c['L_uH']*1e-6;Ae=c['Ae_mm2']*1e-6;n=c['Ns']/c['Np'];N=c['Np'];Ns=c['Ns']
 diam=.127*92**((36-c['AWG'])/39);Afio=math.pi*diam**2/4;Ap=c['fios_p']*Afio;As=c['fios_s']*Afio
 rho20=.01724;rhoT=rho20*(1+.00393*(c['T_cobre_C']-20))
 # Modelo geométrico de curvas paralelas convexas: C(r)=C0+2*pi*r.
 # Alturas incluem fitas entre camadas, barreiras e isolamento inicial.
 ep0=math.floor(c['largura_util_mm']/c['feixe_p_largura_mm']);es0=math.floor(c['largura_util_mm']/c['feixe_s_largura_mm'])
 if ep0<1 or es0<1 or N%2:raise ValueError('Gabarito incompatível com o exemplo')
 def distribuir(total,cap):
  return [min(cap,total-i) for i in range(0,total,cap)]
 dp=distribuir(N//2,ep0);ds=distribuir(Ns,es0)
 def secao(contagens,h,inicio):
  pos=inicio;comprimento=0;raios=[]
  for z,q in enumerate(contagens):
   centro=pos+h/2;raios.append(centro)
   comprimento+=q*(c['perimetro_base_mm']+2*math.pi*centro)/1000
   pos+=h
   if z<len(contagens)-1:pos+=c['espessura_fita_entre_camadas_mm']
  return comprimento,pos,raios
 lp1,pos,rp1=secao(dp,c['feixe_p_altura_mm'],c['espessura_inicial_mm'])
 lss,pos,rsr=secao(ds,c['feixe_s_altura_mm'],pos+c['espessura_barreira_PS_mm'])
 lp2,pos,rp2=secao(dp,c['feixe_p_altura_mm'],pos+c['espessura_barreira_PS_mm'])
 lp=lp1+lp2+c['terminais_p_m'];ls=lss+c['terminais_s_m']
 Rp=rhoT*lp/Ap;Rs=rhoT*ls/As;Pdc=c['Ip_rms_hipotetico_A']**2*Rp+c['Is_rms_hipotetico_A']**2*Rs
 Aexterna=math.pi*c['d_externo_mm']**2/4
 area_fios=(N*c['fios_p']+Ns*c['fios_s'])*Aexterna
 isolamento_total=c['espessura_inicial_mm']+2*c['espessura_barreira_PS_mm']+(2*(len(dp)-1)+len(ds)-1)*c['espessura_fita_entre_camadas_mm']+c['espessura_externa_mm']
 reserva_area=c['largura_util_mm']*isolamento_total+c['reserva_area_extra_mm2']
 ftot=area_fios/c['empacotamento']+reserva_area
 ep=math.floor(c['largura_util_mm']/c['feixe_p_largura_mm']);es=math.floor(c['largura_util_mm']/c['feixe_s_largura_mm'])
 if N%2:raise ValueError('Exemplo exige duas metades P iguais')
 cp=math.ceil(N/2/ep);cs=math.ceil(Ns/es)
 hr=pos+c['espessura_externa_mm']
 ap_req=L*c['I_envelope_A']*(c['Ip_rms_hipotetico_A']+n*c['Is_rms_hipotetico_A'])/(c['B_lim_T']*c['J_lim_A_mm2']*1e6*c['ku_projeto'])*1e8
 r=dict(AVISO='EXEMPLO DIDÁTICO HIPOTÉTICO; NÃO É PROJETO HOMOLOGADO DO CONVERSOR',
 n=n,Np=N,Ns=Ns,AL_alvo_nH=L/N**2*1e9,Ls_mag_ideal_uH=c['L_uH']*n*n,
 B_referencia_T=L*c['I_referencia_A']/(N*Ae),B_envelope_T=L*c['I_envelope_A']/(N*Ae),
 B_pior_tolerancias_T=L*(1+c['L_tolerancia_pct']/100)*c['I_envelope_A']/(N*Ae*(1-c['Ae_tolerancia_pct']/100)),
 energia_envelope_mJ=.5*L*c['I_envelope_A']**2*1000,
 gap_equivalente_sem_fringing_mm=(mu0*Ae*N*N/L-c['le_mm']/1000/c['mu_r'])*1000,
 AeAw_disponivel_cm4=c['Ae_mm2']*c['Aw_mm2']*1e-4,AeAw_requerido_cm4=ap_req,
 diametro_cobre_mm=diam,area_fio_mm2=Afio,area_P_mm2=Ap,area_S_mm2=As,
 Jp_A_mm2=c['Ip_rms_hipotetico_A']/Ap,Js_A_mm2=c['Is_rms_hipotetico_A']/As,
 comprimento_P_por_filamento_m=lp,comprimento_S_por_filamento_m=ls,
 MLT_P1_mm=lp1/(N/2)*1000,MLT_P2_mm=lp2/(N/2)*1000,MLT_S_mm=lss/Ns*1000,
 distribuicao_P1=dp,distribuicao_S=ds,distribuicao_P2=dp,
 raios_camadas_P1_mm=rp1,raios_camadas_S_mm=rsr,raios_camadas_P2_mm=rp2,
 Rp_T_ohm=Rp,Rs_T_ohm=Rs,Pcu_DC_W=Pdc,
 FE_anexo=area_fios/c['Aw_mm2'],FE_geometrico=ftot/c['Aw_mm2'],
 isolamento_radial_total_mm=isolamento_total,reserva_area_mm2=reserva_area,
 ku_cobre_real=(N*Ap+Ns*As)/c['Aw_mm2'],
 espiras_por_camada_P=ep,espiras_por_camada_S=es,
 camadas_P1=cp,camadas_S=cs,camadas_P2=cp,
 altura_radial_total_mm=hr,folga_radial_mm=c['altura_util_mm']-hr,
 fio_total_duas_unidades_m=2*(c['fios_p']*lp+c['fios_s']*ls),
 Ve_efetivo_hipotetico_cm3=Ae*c['le_mm']/1000*1e6)
 cen=[]
 for f in [50000,100000]:
  escala=50000/f
  v=dict(aviso_RMS_triangular='RMS e pico pela aproximação triangular, não RMS integrado nem correntes físicas dos fios',f_Hz=f,estado='50 kHz medido para iM; demais hipóteses' if f==50000 else '100 kHz: extrapolação condicional, sem nova simulação')
  for j in [1,2]:
   avg=c[f'Im{j}_media_50_A'];di=c[f'delta_Im{j}_50_A']*escala
   v[f'delta_Im{j}_A']=di;v[f'ripple_Im{j}_pct']=100*di/avg
   v[f'Bpp{j}_T']=L*di/(N*Ae)
   v[f'Im{j}_pico_triangular_A']=avg+di/2
   v[f'Im{j}_rms_triangular_A']=math.sqrt(avg*avg+di*di/12)
  cen.append(v)
 r['frequencias']=cen
 # Não atribuir cenários inventados a uma frequência ou material.
 r['orcamento_termico']=dict(AVISO='METAS HIPOTÉTICAS; EXIGEM COMPROVAÇÃO EM ENSAIO',
  Pcu_limite_W=Pdc*c['fator_cobre_orcamento'],Pcore_limite_W=c['Pcore_orcamento_W'],
  Rtheta_meta_K_W=c['Rtheta_meta_K_W'])
 o=r['orcamento_termico'];o['Ptotal_limite_W']=o['Pcu_limite_W']+o['Pcore_limite_W']
 o['T_condicional_C']=c['T_amb_C']+o['Ptotal_limite_W']*c['Rtheta_meta_K_W']
 o['Rtheta_max_para_Tlim_K_W']=(c['T_lim_exemplo_C']-c['T_amb_C'])/o['Ptotal_limite_W']
 r['sensibilidade']=[]
 for fator in [1.3,1.5,2.0]:
  for pc in [1,3,5]:
   pt=Pdc*fator+pc
   r['sensibilidade'].append(dict(AVISO='CENÁRIO HIPOTÉTICO, SEM FREQUÊNCIA ATRIBUÍDA',fator_cobre=fator,Pcore_W=pc,Ptotal_W=pt,T_se_Rtheta_5_C=c['T_amb_C']+5*pt,T_se_Rtheta_10_C=c['T_amb_C']+10*pt))
 return r

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--config');p.add_argument('--saida',default='resultados_exemplo');a=p.parse_args()
 c=BASE.copy()
 if a.config:c.update(json.loads(Path(a.config).read_text()))
 r=calcular(c);out=Path(a.saida);out.mkdir(parents=True,exist_ok=True)
 (out/'exemplo_resultados.json').write_text(json.dumps(dict(parametros=c,resultados=r),ensure_ascii=False,indent=2)+'\n')
 with (out/'comparacao_cenarios.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=r['frequencias'][0].keys());w.writeheader();w.writerows(r['frequencias'])
 print(json.dumps(r,ensure_ascii=False,indent=2))
if __name__=='__main__':main()

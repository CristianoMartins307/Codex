# Projeto resolvido como exemplo

## 1. Finalidade e limites do exemplo

Este documento resolve um exemplo de dois indutores acoplados idênticos para estudar o conversor de 2 kW, com Lm=209 µH e relação Ns/Np=2/3. Os cenários A (50 kHz) e B (100 kHz) são comparados sem transformar hipóteses em resultados de simulação.

**O exemplo usa uma geometria hipotética maior. Não corresponde a um E55, PQ40 ou outro núcleo de estoque confirmado. Não é uma liberação para construir e energizar os componentes nominais do conversor.** Ele mostra como fechar uma ficha numérica, reprovar tentativas, ajustar espiras/janela e definir os ensaios que faltam. A seleção comercial e a operação em potência exigem os dados ausentes.

O objetivo didático é avançar além de uma lista de fórmulas: escolher valores explícitos, executar cada substituição e montar uma sequência física coerente, mantendo a distinção entre dados medidos, requisitos e escolhas de estudo.

## 2. O que é dado e o que foi adotado

| Parâmetro | Valor | Situação |
|---|---:|---|
| Potência nominal total | 2.000 W | Requisito do conversor; não multiplicar pelas saídas |
| Entrada | 56 Vcc | Requisito |
| Barramento | 340 V / +170 V / −170 V | Conexões e cargas ainda precisam de esquema completo |
| Lm por componente | 209 µH | Requisito; referência primária ainda a confirmar no PSIM |
| Ns/Np | 2/3 | Aproxima 0,667 |
| Ipk de referência | 7,83 A | Arredondamento do maior pico do arquivo |
| Envelope de estudo | 10 A | Hipótese de projeto, não transiente simulado |
| Ip,rms / Is,rms físicos | 8 A / 6 A | Hipóteses didáticas; não extraídas de iM |
| Ae / Aw úteis | 354 mm² / 400 mm² | Geometria fictícia; não dado de catálogo |
| le / μr | 120 mm / 2.000 | Hipóteses para relutância |
| Janela útil | 25 mm × 16 mm | Gabarito hipotético, com convenção de uma passagem das espiras |
| Blim | 0,20 T | Meta de estudo; não Bsat do material |
| Jmáx / ku de projeto | 3 A/mm² / 0,35 | Critérios preliminares |
| Tolerâncias de fluxo | L +5%; Ae −5% | Hipóteses de robustez a verificar no catálogo |
| Temperatura do cobre para R | 100 °C | Condição de cálculo da resistência, não previsão térmica |
| Material ferrítico | Não especificado | Seleção depende de curvas oficiais e estoque |

Ae é seção magnética efetiva; Aw é a seção útil de uma janela atravessada por todos os condutores do desenho. Se um fabricante publicar a soma de duas janelas, converter antes de comparar. Não contar o mesmo cobre duas vezes nem duplicar área útil.

## 3. Confirmar o circuito antes do bobinamento

O recorte recebido sugere dois componentes independentes, cada um com P e S, ramo Lm e dispersão Lk. A imagem parcial não confirma o modelo completo ou os sentidos dos pontos. Para o exemplo, cada conjunto é construído separadamente e usa a mesma ficha; a ligação no conversor deve seguir o esquema completo.

Com correntes definidas entrando nos pontos, adotar iM=iP+n·iS. Portanto iP=iM−n·iS. A corrente eficaz física exige integrar iP(t) e iS(t), incluindo seus intervalos de condução. Não usar 6,18 A de iM como se fosse automaticamente a corrente do primário.

Os valores 8/6 A deste documento apenas permitem demonstrar o cálculo de cobre. Não são garantia de atendimento ao conversor de 2 kW. Uma vez exportadas as correntes físicas, substituí-las no código; a contagem de fios e a janela podem mudar.

## 4. Conferência das correntes fornecidas

Janela de cinco períodos: 34,940 a 35,040 ms. O arquivo tem 1.504 amostras e o período nominal é 20 µs. O programa integra no tempo, interpola os limites e calcula o RMS pelo quadrado de cada trecho linear.

| Grandeza | Lm1 | Lm2 |
|---|---:|---:|
| Média (A) | 6,099703 | 5,966345 |
| RMS magnetizante (A) | 6,180803 | 6,049461 |
| Máximo na janela (A) | 7,823397 | 7,691064 |
| Mínimo na janela (A) | 4,373278 | 4,237980 |
| Pico a pico (A) | 3,450119 | 3,453084 |
| Ondulação (%) | 56,5621 | 57,8760 |

Maior valor de todo o arquivo: 7,827687 A. Não é máximo garantido de partida ou desequilíbrio.

![Correntes magnetizantes medidas na exportação do PSIM.](figuras/correntes_50k.png)

A área de tensão de uma rampa é aproximadamente L·Δi. Para Lm1: 209×10⁻⁶×3,450119=721,075×10⁻⁶ V·s. O valor usa o envelope de cinco ciclos; exportar vM(t) e analisar cada ciclo para o fechamento definitivo.

## 5. Por que o exemplo inicial 24/16 foi revisto

Np≥L·Ipk/(Ae·Blim). Com apenas o pico 7,83 A:

`Np≥209×10⁻⁶×7,83/(354×10⁻⁶×0,20)=23,115`.

24/16 satisfaz a razão, mas B≈0,1926 T e há pouca folga até a meta de 0,20 T. A 10 A, B≈0,2460 T. Essa tentativa não é adequada ao envelope didático escolhido.

Para 10 A e sem tolerâncias: Np≥29,52; a opção 30/20 chega a 0,1968 T. Com L+5% e Ae−5%, sobe a 0,2175 T e reprova a meta. A opção 33/22 reduz o fluxo, mas não permite duas metades iguais de P. Para facilitar intercalamento simétrico e manter folga, escolher **Np=36 e Ns=24**.

Na janela antiga hipotética de 250 mm², 36/24 com os mesmos feixes não cabe no critério de ocupação usado. O exemplo aumenta Aw para 400 mm². Isso é uma decisão geométrica de estudo, não uma alteração presumida de um núcleo comercial.

## 6. Seleção por AeAw

O cobre exige:

`Aw·ku≥Np·Ip,rms/J+Ns·Is,rms/J`.

Como Ns=n·Np e Np≥L·Ipk/(Ae·Blim):

`Ae·Aw≥L·Ipk·(Ip,rms+n·Is,rms)/(Blim·J·ku)`.

Substituição SI:

`AeAw_req = (209×10⁻⁶×10×(8+(2/3)×6))/(0,20×3×10⁶×0,35)`.

Resultado: **11,9429 cm⁴**.

Área disponível: 354×400=141.600 mm⁴=**14,16 cm⁴**. A triagem passa: 14,16>11,9429. O cálculo de camadas, a margem magnética e o calor continuam obrigatórios.

O método foi derivado do fluxo e da área de cobre, sem usar a fórmula de potência de um Flyback. A corrente de pico é magnetizante; as correntes do somatório são as dos enrolamentos físicos. ku já representa a utilização global de cobre nu no critério.

## 7. Espiras, fluxo e energia

Escolha inteira: P=36 espiras; S=24; n=24/36=0,666667. Primário dividido em P1=18 e P2=18 em série aditiva.

`AL_alvo=L/Np²=209 µH/1.296=161,265432 nH/espira²`.

`Ls,mag=(24/36)²×209=92,888889 µH`.

O entreferro será ajustado para esse AL. O arredondamento das espiras sem ajuste de AL não garante 209 µH.

| Condição | Cálculo | B |
|---|---|---:|
| Pico do arquivo arredondado | 209 µH×7,83/(36×354 mm²) | 0,128411 T |
| Envelope hipotético | 209 µH×10/(36×354 mm²) | 0,163999 T |
| Envelope, L+5%, Ae−5% | 219,45 µH×10/(36×336,3 mm²) | 0,181262 T |

O último valor é inferior à meta 0,20 T. Ainda falta verificar Bsat mínimo a quente e fluxo local com Amin da peça real. Ae efetivo não substitui a menor seção local, e μ não foi comprovado em polarização CC.

Energia no envelope: `W=½×209×10⁻⁶×10²=10,45 mJ` por unidade. No pico de referência, 6,407 mJ. Não somar novamente a energia dos dois enrolamentos como se fossem dois núcleos independentes: ambos compartilham a energia do mesmo componente.

A energia do modelo de dois indutores acoplados pode ser escrita `½Lp ip²+½Ls is²+M ip is`, respeitando sentidos. O modelo Lm mais dispersões distribui essa energia em ramo magnetizante e fluxos de dispersão.

## 8. Comparação magnética entre frequências

A 50 kHz, `ΔB=L·Δi/(Np·Ae)`:

`ΔB1=209×10⁻⁶×3,450119/(36×354×10⁻⁶)=56,5815 mT`.

B é unipolar com forte polarização CC; a amplitude AC aproximadamente metade de ΔB não é igual a Bpk total.

Para 100 kHz, apenas se tensões por estado, duty e médias se mantiverem, Δi e ΔB cairiam à metade. O projeto B mantém 36/24 e 209 µH neste exemplo comparativo; não se divide N por dois.

| Grandeza magnetizante | A — 50 kHz | B — 100 kHz, condicional |
|---|---:|---:|
| Δi1 (A) | 3,450119 | 1,725060 |
| Δi2 (A) | 3,453084 | 1,726542 |
| Ondulação 1 (%) | 56,5621 | 28,2810 |
| Ondulação 2 (%) | 57,8760 | 28,9380 |
| ΔB1 (mT) | 56,5815 | 28,2908 |
| ΔB2 (mT) | 56,6301 | 28,3151 |
| Irms magnetizante 1 (A) | 6,180803 do arquivo | 6,119997 pela aproximação triangular |
| Irms magnetizante 2 (A) | 6,049461 do arquivo | 5,987126 pela aproximação triangular |

O programa também calcula uma aproximação triangular a 50 kHz, ligeiramente diferente do RMS integrado. Essa diferença não é erro de integração: são métodos/dados distintos. Para a conferência do PSIM usar os valores integrados.

**209 µH continua sem atender 20%**. A 50 kHz, o cálculo estático daria 591,1/604,8 µH; a 100 kHz condicional, 295,5/302,4 µH. Não incorporar essas alterações ao exemplo sem refazer energia, controle, fluxo, espiras e janela.

## 9. Entreferro calculado e significado físico

`Rtotal=Np²/Lm=1.296/(209×10⁻⁶)=6,20096×10⁶ A/Wb`.

`g_eq=μ0 Ae Np²/Lm−le/μr`.

`g_eq=(4π×10⁻⁷×354×10⁻⁶×1.296)/(209×10⁻⁶)−0,120/2.000`.

Resultado: **2,698493 mm** sem espraiamento.

A relutância do núcleo foi incluída, mas le/μr e a geometria são hipotéticos. Com gap apenas na coluna central e faces externas encostadas, esse é aproximadamente o comprimento central somado. Com espaçamento uniforme de toda a junta e áreas externas totais equivalentes à central, o fluxo cruza duas juntas em série; a espessura inicial de espaçador seria aproximadamente **1,34925 mm**, não 2,69849 mm em cada face.

Esse gap é grande o suficiente para tornar o fringing uma pendência relevante. Não se propõe simplesmente colocá-lo ao lado do cobre e declarar perdas baixas. Para uma peça real, procurar gap central/distribuído apropriado do fabricante, prever distância do cobre e avaliar aquecimento local; o tamanho físico pode mudar ao incluir Agap efetiva. Se o fringing impedir a margem térmica, a construção proposta deve ser rejeitada ou reformulada.

AL é ajustado medindo com S aberto e pressão de montagem reproduzível, depois verificando a relação entre indutância própria e Lm do modelo. Pequeno sinal em i≈0 não comprova a indutância incremental entre 4 e 10 A.

## 10. Cobre: área e quantidade de filamentos

Com J≤3 A/mm²: AcuP≥8/3=2,6667 mm² e AcuS≥6/3=2,0000 mm².

AWG30: `d=0,127×92^((36−30)/39)=0,254639 mm`.

`Afio=πd²/4=0,050926 mm²`.

Número mínimo de fios: `mP=ceil(2,6667/0,050926)=53`; `mS=ceil(2/0,050926)=40`.

Áreas finais P=2,699079 mm², S=2,037041 mm². Densidades P=2,9640 A/mm² e S=2,9454 A/mm².

Fios esmaltados em paralelo precisam ter comprimentos e percursos semelhantes, transposição das posições e conexão de todos os filamentos. Litz exige construção e terminação apropriadas. Muitos fios não garantem Rac baixo se não houver controle de proximidade e divisão de corrente.

A profundidade do cobre a 20 °C é cerca de 0,296 mm a 50 kHz e 0,209 mm a 100 kHz. O raio do AWG30 é 0,127 mm, inferior a ambas. Isso ajuda no efeito pelicular individual, mas as três camadas de cada seção ainda estão sujeitas a proximidade.

Comparar AWG28 (33/25 fios para as mesmas hipóteses), AWG30 (53/40) e AWG32 (84/63). AWG32 pode reduzir perdas de campo em certas condições, mas aumenta esmalte e dificuldade de fabricação. Testar feixe real antes de comprar toda a metragem.

## 11. Janela, camadas e desenho do carretel

Adotar diâmetro externo máximo hipotético de 0,30 mm. Feixe P: 53 fios organizados em retângulo aproximado de 3,3×1,5 mm (55 posições, duas vazias). Feixe S: 40 fios, 3,0×1,2 mm. Essas dimensões são de gabarito ordenado, não de feixe circular solto.

Largura axial útil=25 mm. Então P comporta floor(25/3,3)=7 espiras/camada; S comporta floor(25/3,0)=8.

| Seção radial | Espiras | Fios paralelos | Distribuição por camada |
|---|---:|---:|---|
| P1, interna | 18 | 53×AWG30 | 7 + 7 + 4 |
| S, intermediária | 24 | 40×AWG30 | 8 + 8 + 8 |
| P2, externa | 18 | 53×AWG30 | 7 + 7 + 4 |

Fios: 3×1,5+3×1,2+3×1,5=12,6 mm radiais. Reservas didáticas: 0,20 mm inicial; duas barreiras P/S de 0,50 mm; seis fitas entre camadas de 0,05 mm; 0,20 mm externo. Total=1,70 mm. Altura final=**14,30 mm**; folga até 16 mm=**1,70 mm**.

**Essas espessuras são hipóteses geométricas, não uma especificação de isolação aprovada.** A largura de 25 mm já deve excluir margens elétricas e mecânicas. O recorte não determina se existe isolação de segurança requerida entre P e S. As distâncias e a classe do sistema devem ser definidas pela aplicação, picos e norma pertinente.

![Corte radial do exemplo, com uma janela útil hipotética.](figuras/arranjo_exemplo.png)

P1 e P2 ficam em série aditiva. Marcar todos os inícios e fins e confirmar com LCR ou gerador isolado. A ligação dos pontos em Lm1/Lm2 no conversor pode diferir; o desenho abaixo é de um componente isolado, não o esquema completo do conversor.

![Identificação didática dos terminais e da emenda do primário.](figuras/terminais_exemplo.png)

## 12. Fator de execução e verificação de área

A definição da aula é FE=Aw_min/Aw, incluindo o esmalte:

`Aw_min=(36×53+24×40)×π×0,30²/4=202,727 mm²`.

`FE_anexo=202,727/400=0,506817`.

Para empacotamento 0,785 e reserva de 42,5 mm² equivalente às fitas/barreiras da hipótese:

`FE_geom=(202,727/0,785+42,5)/400=0,751877`.

Cobre nu real na janela: `(36×2,699079+24×2,037041)/400=0,365140`. É maior que o ku de triagem 0,35, mas inferior à capacidade geométrica assumida com isolantes. Além da área, a contagem de camadas demonstrou folga radial.

As embalagens retangulares dos feixes ocupam aproximadamente 264,6 mm², ligeiramente mais que o cálculo circular corrigido. Somando as reservas de 42,5 mm² resulta 307,1/400=0,76775. O retângulo envolvente de toda a altura ocupa 25×14,3/400=0,89375, incluindo vazios nas camadas incompletas. São métricas diferentes; não misturar seus valores.

A aprovação é apenas do gabarito ideal. Se o feixe real aumentar de largura/altura, as camadas podem mudar de forma descontínua. Medir uma amostra transposta e rever sem apertar o esmalte.

## 13. Comprimentos por camada e resistência

Usar o mesmo MLT para a seção interna e externa subestima a resistência externa. O exemplo utiliza contorno convexo hipotético com perímetro base C0=114 mm. A linha paralela a uma distância radial r tem perímetro aproximado:

`C(r)=114+2πr mm`.

O contorno é um modelo didático; na peça real o perímetro deve ser medido ou obtido do desenho. Os centros das camadas incluem fita inicial, barreiras e fitas entre camadas.

| Seção | Raios das camadas (mm) | MLT médio ponderado (mm) |
|---|---|---:|
| P1 | 0,95; 2,50; 4,05 | 128,084807 |
| S | 5,90; 7,15; 8,40 | 158,924775 |
| P2 | 10,25; 11,80; 13,35 | 186,518430 |

Por exemplo, MLT_P1=[7C(0,95)+7C(2,50)+4C(4,05)]/18. Comprimento de P inclui as duas seções e 0,20 m de terminais por filamento; S inclui 24 espiras e 0,20 m.

Resultados: ℓP=**5,862858 m**, ℓS=**4,014195 m** por filamento. A emenda P1/P2 pode exigir reserva adicional real.

A 100 °C: `ρ=0,01724×[1+0,00393×(100−20)]=0,022660256 Ω·mm²/m`.

`RP=ρℓP/AcuP=49,221926 mΩ`.

`RS=ρℓS/AcuS=44,654323 mΩ`.

`Pcu,DC=8²RP+6²RS=4,757759 W` por componente, sob as hipóteses de corrente e temperatura. Esse é o valor que seria dissipado pelas mesmas correntes RMS se a resistência fosse Rdc; não é a perda real em alta frequência.

## 14. Perdas, orçamento térmico e resultado condicional

Sem curvas de ferrite, espectro dos fios ou montagem térmica, não se determina a perda total real. Para executar um exemplo completo sem atribuir números falsos a N87/N97, estabelecer **metas de aceitação**, que devem ser demonstradas:

- Perda de cobre total ≤1,5×Pcu,DC=7,136638 W por unidade.
- Perda de núcleo ≤3,0 W por unidade.
- Resistência térmica efetiva para o ponto quente ≤5 K/W.
- Ambiente 25 °C e limite de estudo 80 °C.

Se todas essas metas forem satisfeitas:

`Ptotal≤10,136638 W` por unidade.

`Tquente≤25+5×10,136638=75,683 °C`.

O orçamento passaria a meta de 80 °C, mas **não é previsão medida ou estimativa oficial do ferrite**. A resistência foi calculada a 100 °C como hipótese conservadora em relação a esse limite de estudo. Resistência térmica e temperatura de ponto quente exigem ensaio; a ferrite e o cobre podem ter temperaturas diferentes.

Para duas unidades: perda combinada ≤20,273 W se os orçamentos forem demonstrados. A parcela seria cerca de 1,014% dos 2 kW, sem incluir semicondutores, capacitores e conexões. Não chamar isso de eficiência do conversor.

Volume magnético efetivo hipotético Ve≈Ae·le=42,48 cm³. A meta Pcore≤3 W equivale a Pv≤3/(42,48×10⁻⁶)=70,62 kW/m³, a verificar na forma de onda e polarização reais. O número é limite permitido, não perda específica do material.

O cálculo correto do cobre é `Pcu=Idc²Rdc+ΣIh,rms²Rac(hf,T)`. A perda de núcleo é `Pcore=Pv×Ve`, com f, ΔB, forma de onda, Bdc e temperatura apropriados. Para curvas senoidais, usar amplitude AC, sem confundir ΔB pico a pico com Bpk da curva. A iGSE e as correções de polarização só são úteis com parâmetros válidos.

A tabela seguinte é uma sensibilidade SEM associação com 50 ou 100 kHz; mostra quanto os ensaios precisam controlar as perdas.

| Fator de cobre sobre referência DC | Pcore adotada (W) | Ptotal (W) | T se Rθ=5 K/W (°C) | T se Rθ=10 K/W (°C) |
|---|---:|---:|---:|---:|
| 1,3 | 1,0 | 7,185 | 60,93 | 96,85 |
| 1,3 | 3,0 | 9,185 | 70,93 | 116,85 |
| 1,3 | 5,0 | 11,185 | 80,93 | 136,85 |
| 1,5 | 1,0 | 8,137 | 65,68 | 106,37 |
| 1,5 | 3,0 | 10,137 | 75,68 | 126,37 |
| 1,5 | 5,0 | 12,137 | 85,68 | 146,37 |
| 2,0 | 1,0 | 10,516 | 77,58 | 130,16 |
| 2,0 | 3,0 | 12,516 | 87,58 | 150,16 |
| 2,0 | 5,0 | 14,516 | 97,58 | 170,16 |

Esses cenários não escolhem a melhor frequência. Se a meta térmica falhar, revisar área de cobre, geometria do gap, distribuição do campo, janela, material e ventilação. Não compensar apenas elevando o limite de temperatura sem uma justificativa de sistema.

## 15. Dispersão e capacitância

O intercalamento P1–S–P2 foi escolhido para reduzir a separação média das ampère-espiras. Isso não prova um Lk numérico. Faltam forma do carretel real, campos do gap e medições; não usar um percentual arbitrário como resultado calculado.

Metas referidas a P: Lk≤10,45 µH e máximo 20,9 µH. No S: ≤4,644 µH e máximo 9,289 µH. O secundário tem menos espiras e a referência se transforma por n², não por n.

No modelo de duas indutâncias próprias, Lsc,P=Lp−M²/Ls=Lp(1−k²). Se Lp≈Lm, meta de 5% implica k≥0,97468; para 10%, k≥0,94868. Confirmar o modelo antes de aplicar esses números ao PSIM.

Aproximar os enrolamentos aumenta capacitância e corrente de deslocamento `i=C dv/dt`. As duas barreiras P/S e os múltiplos planos tornam a resposta de alta frequência um compromisso. Uma frequência maior pode elevar efeitos de modo comum. Isolação adequada tem prioridade sobre a tentativa de reduzir Lk.

## 16. Fabricação do exemplo, sem ligação ao conversor nominal

Fazer primeiro uma bobina de prova, desenergizada, usando o gabarito de 25×16 mm. O modelo fictício não pode ser comprado por nome; para uso real deve ser substituído por um conjunto comercial e verificado.

1. Conferir os desenhos e separar dois conjuntos completos de ferrite e carretéis compatíveis, quando identificados. Sem essa seleção, o passo físico limita-se ao gabarito de prova.
2. Medir largura útil, altura radial, perímetro da primeira camada e localização do gap. Confirmar convenção de Aw, margens e distância do cobre ao gap.
3. Inspecionar trincas e arestas. Preparar fitas, mangas, espaçadores calibrados, contador de espiras e folha de registro.
4. Confirmar AWG30 pelo diâmetro do cobre e o esmalte máximo. Ensaiar feixes com 53 e 40 filamentos; medir suas dimensões transpostas.
5. Reservar por filamento aproximadamente 5,863 m para o primário completo e 4,014 m para o secundário, antes de margens extras de manuseio/emenda. Separar P1 e P2 considerando seus MLT diferentes.
6. Preparar todos os filamentos de cada feixe com comprimentos semelhantes, identificação e transposição. Todas as pontas precisam ser soldadas; contar e inspecionar.
7. Aplicar 0,20 mm inicial apenas no gabarito geométrico. Para uma peça nominal, usar o sistema de isolação aprovado e recalcular espessuras.
8. Enrolar P1: 18 espiras, 53 fios paralelos; primeira camada 7, segunda 7, terceira 4. Fitas intermediárias conforme a ficha. Contar espiras, não filamentos.
9. Isolar e encaminhar terminais P1i/P1f sem cruzamentos na região ativa. Registrar o sentido visto de uma face de referência fixa.
10. Aplicar a barreira P/S do plano de isolação; no modelo de espaço ela tem 0,50 mm. A fita não pode suprimir margens de escoamento.
11. Enrolar S: 24 espiras de 40 fios, distribuídas 8+8+8. Marcar Si/Sf e proteger terminais.
12. Aplicar a segunda barreira de 0,50 mm no gabarito ou a espessura real homologada.
13. Enrolar P2: 18 espiras de 53 fios, 7+7+4. Manter convenção e terminais acessíveis para verificar a série aditiva.
14. Aplicar isolamento externo, mangas e alívio mecânico. Conferir altura final: 14,30 mm no modelo. Se exceder a folga disponível, não pressionar para fechar.
15. Fazer emenda aditiva P1f–P2i após confirmar polaridade. P tem 36 espiras totais; não colocar P1/P2 em paralelo.
16. Montar o núcleo real com gap preliminar somente após avaliar a equivalência e o fringing. Não transferir a lâmina de 1,34925 mm para qualquer junta comercial sem conferir a geometria.
17. Fixar provisoriamente com pressão uniforme e sem formar uma espira condutiva fechada ao redor do fluxo. Não colar antes do ajuste.
18. Medir relação, polaridade, indutâncias próprias, dispersão e resistência. Ajustar gap com pequenos passos e repetir as medições na mesma montagem.
19. Após aprovação de pequeno sinal, aplicar fixação definitiva e medir novamente. O ensaio sob corrente e o térmico ainda são obrigatórios.
20. Repetir o processo para o segundo componente e comparar os resultados. Só conectar ao circuito depois de confirmar a ligação de cada ponto no esquema completo.

## 17. Plano de ensaios com valores de referência

### 17.1 LCR e identificação

Com componente desconectado e capacitores descarregados: compensar aberto/curto, registrar frequência/amplitude/modelo série ou paralelo e temperatura. Medir P com S aberto, depois S com P aberto. Pequena excitação não deve produzir fluxo elevado.

O modelo ideal sem dispersão daria Lp=209 µH e Ls=92,889 µH. Com dispersão, são indutâncias próprias diferentes do ramo Lm. Se o PSIM tiver Lσ em série com o lado medido, não ajustar cegamente a leitura aberta para 209 µH.

Associar P e S em série aditiva/subtrativa e medir L+ e L−. `M=(L+−L−)/4`; `k=M/√(LpLs)`. Valores ideais: M=139,333 µH; L+=580,556 µH; L−=23,222 µH. As espiras 36/24 mantêm a mesma razão e os mesmos valores de indutância ideais após ajuste do gap.

Curto-circuitar S com conexão de baixa impedância e medir no P; comparar a grandeza de dispersão equivalente com a meta de 10,45 µH depois de mapear o modelo. Repetir no outro lado e referir por n². Usar frequências do instrumento abaixo da ressonância própria.

Medir DCR por quatro fios. O parâmetro Rs em 100 kHz inclui perdas e não substitui DCR. Para comparar com este exemplo, corrigir resistência pela temperatura. Os valores calculados a 100 °C são P=49,222 mΩ e S=44,654 mΩ, sem resistência de emenda extra.

### 17.2 Indutância sob corrente e saturação

Com fonte limitada, circuito pulsado com reset e clamp, sonda de corrente/shunt e osciloscópio diferencial, medir v(t) e i(t). Calcular Linc≈(v−Ri)/(di/dt) e λ=∫(v−Ri)dt. Aceleração abrupta de di/dt indica queda de L. Começar com pulsos curtos e baixa energia, garantir desmagnetização e elevar a corrente em etapas dentro da proteção.

10 A é o envelope didático deste exemplo, não um limite aprovado do circuito. O teste deve ser definido e supervisionado no laboratório. Repetir a quente e nos extremos de tolerância. LCR sozinho não executa essa validação.

### 17.3 Isolação e aquecimento

Tensão e duração de hipot dependem da norma e do sistema de isolação; não deduzi-las somente de 340 V. Medir isolação com equipamento adequado e o componente fora da eletrônica.

Operar progressivamente com carga controlada, barreiras e proteção. Registrar temperatura de núcleo, cobre, terminais e ambiente; acompanhar equilíbrio dos barramentos e picos de corrente. O objetivo de estudo é demonstrar Pcu≤7,137 W, Pcore≤3 W e Rθ efetiva≤5 K/W, ou refazer o orçamento com valores medidos. A leitura externa de um termopar não representa automaticamente o ponto quente.

Em 340 Vcc há risco letal e energia armazenada; usar desligamento, descarga e confirmação de ausência de tensão antes de qualquer intervenção. Ensaios em potência e de isolação exigem pessoal habilitado e montagem protegida.

## 18. Lista de materiais do exemplo para duas unidades

| Item | Quantidade ou condição |
|---|---|
| Núcleos | 2 conjuntos completos (4 metades), código ainda não selecionado |
| Carretéis | 2, geometria real a confirmar |
| AWG30 para P | 2×53×5,862858=621,463 m de filamento |
| AWG30 para S | 2×40×4,014195=321,136 m de filamento |
| AWG30 total | 942,599 m sem reserva adicional |
| AWG30 com 15% adicional | 1083,988 m, aproximadamente 1,084 km |
| Cobre nu sem reserva | Aproximadamente 0,430 kg |
| Fixação | 2 conjuntos adequados, sem espira em curto |
| Gap | Jogo de espaçadores/gap de fábrica; valor real ajustado |
| Fitas/mangas | Pelo plano de isolação e área real; estoque a confirmar |
| Terminais | 8 externos e 2 emendas internas P1/P2 |

A reserva de 15% é hipótese de planejamento e não substitui a metragem medida de terminações e transposição. Não comprar núcleos por estes números sem conferir datasheet e fabricante.

## 19. Comparação final A/B e decisão

| Parâmetro | A — 50 kHz | B — 100 kHz |
|---|---|---|
| Geometria didática | Ae354/Aw400 mm² | A mesma |
| Material | A selecionar | A selecionar |
| Np/Ns | 36/24 | 36/24 para comparação |
| Lm | 209 µH | 209 µH |
| Entreferro equivalente sem fringing | 2,69849 mm | O mesmo |
| Condutores do exemplo | P53/S40 AWG30 | Mesmos, somente sob hipóteses de RMS |
| Envelope e B máximo com tolerâncias | 10 A; 0,181262 T | Mesmo envelope de estudo |
| ΔB1 | 56,5815 mT | 28,2908 mT condicional |
| FE anexo / geométrico | 0,50682 / 0,75188 | Os mesmos |
| Referência DC de cobre | 4,75776 W a 100 °C e 8/6 A | A mesma se os RMS forem iguais; hipótese |
| Perda AC/núcleo/temperatura real | A medir/calcular com dados oficiais | A medir/calcular com nova simulação |
| Dispersão | Meta≤10,45 µH, sem previsão aprovada | Mesma meta, dependência frequencial a medir |
| Conclusão de eficiência real | Não disponível | Não disponível |

O exemplo fecha os números geométricos e define um orçamento térmico verificável. Não fecha a seleção comercial, o fringing, a polarização real ou a eficiência do conversor. O fato de o gabarito caber não assegura aptidão do núcleo do laboratório.

A decisão prática é validar primeiro o caso de 50 kHz, porque existem dados numéricos. A comparação a 100 kHz continua necessária; aumento de frequência pode diminuir excursão/perda de núcleo e aumentar perda AC e de comutação. A escolha deve usar a mesma potência total, mesmas cargas e condições de temperatura.

## 20. Reprodução e substituição das hipóteses

No diretório do pacote, executar:

```sh
python -m pip install -r requirements.txt
python calculo.py --correntes dados/CorrenteIndutor.txt --saida resultados
python exemplo_completo.py --config parametros_projeto_exemplo.json --saida resultados_exemplo
```

`calculo.py` confere o arquivo de 50 kHz e mantém o exemplo inicial de 24/16 para rastreabilidade. `exemplo_completo.py` é o cálculo deste documento, com 36/24 e geometria ampliada hipotética. O JSON contém todos os valores adotados e os resultados.

Ao receber dados reais: substituir RMS, envelope, Ae/Aw/le, material, tolerâncias, diâmetros e dimensões; medir o perímetro por camada; atualizar plano de isolação; introduzir perdas do material e espectro; executar validações. Se uma condição de aceitação falhar, repetir o dimensionamento antes da fabricação nominal.

Referências disponíveis: PROJETO_INDUTOR.pdf (método, espiras, gap, condutores e fator de execução), McLyman.pdf (componentes magnéticos, ocupação e espraiamento) e CorrenteIndutor.txt (dados numéricos de 50 kHz). Os datasheets de fabricantes e o modelo PSIM completo não foram acessados nesta análise.

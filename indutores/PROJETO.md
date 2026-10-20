# Indutores acoplados de um conversor de 2 kW — memória de engenharia

**Situação: análise verificável e pré-dimensionamento condicional. Não é uma liberação de fabricação dos componentes nominais.** Os dados disponíveis permitem conferir as correntes magnetizantes, quantificar a incompatibilidade com a ondulação de 20%, desenvolver o método e preparar ensaios. Não permitem especificar definitivamente os fios, o núcleo, a dispersão e a temperatura. Os exemplos numéricos abaixo têm hipóteses explícitas e não substituem esses dados.

## 1. Documentos efetivamente examinados e impedimentos

Recebidos e lidos: `CorrenteIndutor.txt` (1.504 linhas numéricas); `PROJETO_INDUTOR.pdf` (44 páginas, aula DCG 2021/2, metodologia AeAw e exemplo Flyback); `McLyman.pdf` (texto extraído; discussão de relutância, espraiamento, perdas e ocupação); imagem parcial do esquema no pedido.

O arquivo `Etapas_operacaoVGanhosDefinidos.smv` foi recebido pela plataforma, mas sua transferência para esta máquina foi recusada por ultrapassar 32 MiB. Portanto **não foi aberto nem analisado**. Não foram recebidos o esquema completo, a planilha de estoque/datasheets nem `PROJETO_INDUTOR(1).pdf`. McLyman é uma referência distinta; não há base para afirmar que substitui ou duplica esse segundo PDF.

Tentativas HTTPS aos PDFs oficiais da TDK em `www.tdk-electronics.tdk.com` retornaram `Tunnel connection failed: 403 Forbidden`. Nenhuma característica oficial de N87/N97 ou dos núcleos foi validada por esse acesso. O domínio foi acrescentado ao rascunho de rede, preservando os destinos dos presets. É necessário revisar/salvar nas configurações e publicar o ambiente; salvar o rascunho não liberou a conexão atual.

| Informação faltante | Consequência | Como obter |
|---|---|---|
| Modelo completo, bloco magnético e seus parâmetros | Não confirma qual lado é primário nem referência dos 209 µH | Esquema legível, propriedades dos elementos e netlist/exportação textual do PSIM |
| iP(t), iS(t), vP(t), vS(t) dos dois componentes, simultâneos | Impede cobre, perdas AC, polaridades e isolação definitivos | Exportar CSV com tempo e unidades; incluir sentidos de medição |
| PWM, D, defasagem, condução dos diodos | Impede enumerar com segurança os estados de comutação | Esquema completo e sinais das chaves |
| 100 kHz estabilizado e transientes | Impede projeto B confirmado | Simular mantendo controle/cargas reais e exportar as mesmas variáveis |
| Cargas entre +, zero e −; potência de cada carga | Impede confirmar barramento, equilíbrio e pior caso | Valores resistivos/controle de carga e tensões dos capacitores |
| Partida, limite de corrente, cargas extremas, desequilíbrio | Pico de 7,83 A não é máximo garantido | Simulações de envelope e especificação de proteção |
| Códigos, quantidades e desenhos dos núcleos/carretéis | Impede escolha, estoque e encaixe | Planilha ausente e PDFs oficiais |
| Estoque de fios e classe de esmalte | Impede lista final de compra | Diâmetro de cobre, diâmetro externo máximo, metragem e classe térmica |
| Resfriamento, montagem e limite de temperatura | Impede temperatura final | Dimensões externas, gabinete, fluxo de ar, pontos quentes permitidos |
| Modelo do LCR e sua frequência/excitação | Impede precisão e frequência final dos ensaios | Manual do instrumento |

Solicitar os arquivos ausentes e uma exportação menor do PSIM. Não é necessário aguardar para executar os cálculos e o roteiro abaixo.

## 2. Interpretação do circuito e potência

A imagem mostra **dois símbolos de transformador/indutor acoplado separados**, um em cada ramo, cada qual com Lm em paralelo com um lado e Lk em série. A interpretação preliminar é de dois componentes magnéticos independentes, com dois enrolamentos cada: total de dois conjuntos de núcleo e quatro enrolamentos. Não há indicação gráfica de um núcleo compartilhado. O recorte, contudo, não comprova o modelo completo nem uma construção em núcleo multicoluna.

O enrolamento à direita de cada símbolo está associado à Lm e a Lk; por isso é candidato a lado de referência. Não o declarar primário somente por sua posição. Os pontos/polaridades de Lm1 e Lm2 aparecem em extremidades distintas do desenho; não copiar a ligação de um ramo para o outro por simetria visual. Confirmar no símbolo original. A coordenada do ponto no desenho é referência elétrica, não o sentido físico de giro isoladamente.

Modelo por componente: transformador ideal n=Ns/Np; ramo Lm no lado P; resistência RP e dispersão LσP em série com P; resistência RS e dispersão LσS em série com S; perdas do núcleo representadas por resistência não linear/frequencial em paralelo com Lm. No circuito magnético: força magnetomotriz Np·iP ± Ns·iS alimenta Rcore + Rgap e produz Φ. Os sinais dependem de sentidos entrando nos pontos.

Adotando ambas as correntes entrando nos pontos, vS=n·vP e iM=iP+n·iS no modelo ideal referido ao primário. Se uma sonda usa sentido oposto, o sinal muda. Logo iP=iM−n·iS: **iM RMS não determina iP RMS**. É necessário o valor temporal da corrente secundária e sua correlação com iM, não apenas seu RMS:

`Ip,rms² = Im,rms² + n² Is,rms² − 2n <iM iS>`.

Equações fundamentais:

- vM=Np·dΦ/dt=Np·Ae·dB/dt=Lm·diM/dt no modelo linear.
- B≈Lm·iM/(Np·Ae), sem remanência inicial e antes de saturação.
- Wm=½ Lm·iM²; Eσ=½ Lσ·i_comutação². A corrente da dispersão é a corrente do enrolamento correspondente, não automaticamente iM.
- ΔB=∫vM dt/(Np Ae); em regime periódico ∮vM dt≈0. Tensões medidas nos terminais incluem quedas de cobre/dispersão, que devem ser separadas quando relevantes.

Não se adotam os estados ou a razão cíclica de um Flyback. A aula usa esse conversor como exemplo; a derivação por energia, fluxo e janela aplica-se ao componente acoplado sem assumir transferência descontínua de energia.

Se os terminais +170, 0, −170 pertencem ao mesmo barramento, V(+−)=340 V: são referências distintas da mesma estrutura, e a potência é `P=340 I_+− +170 I_+0 +170 I_0−`, com correntes positivas definidas como consumo de cada carga. Não somar novamente uma medição de potência total que já contenha essas cargas. Para só uma carga de 2 kW entre + e −, I=2000/340=5,882 A e R=57,8 Ω. Para duas cargas equilibradas de 1 kW entre cada polo e zero, cada uma consome 5,882 A e R=28,9 Ω. Estes são exemplos de carregamento, não condições confirmadas.

Potência de entrada ideal: 2000/56=35,714 A; real: 35,714/η A. A média magnetizante de aproximadamente 6 A não representa a corrente total de entrada, nem prova incompatibilidade com 2 kW. É necessário conferir correntes de ramo e divisão real da potência. Não pressupor que cada magnético processa exatamente 1 kW.

## 3. Correntes recalculadas

Intervalo total: 34,9178 a 35,0681 ms, passo aproximadamente 0,1 µs, duração 150,3 µs, ou 7,515 períodos a 50 kHz. Não usar todo o arquivo como se contivesse um número inteiro de ciclos.

A janela **34,940 a 35,040 ms** contém exatamente cinco períodos nominais (100 µs). Interpolação linear nos limites. Média por integração no tempo; RMS pela integral analítica do quadrado de cada trecho linear. Assim não há viés por simplesmente contar amostras de borda duas vezes.

`Iavg=(1/Δt)∫i dt`; `Irms=√[(1/Δt)∫i²dt]`; `ripple=100(Imax−Imin)/Iavg`.

| Grandeza | Lm1 | Lm2 |
|---|---:|---:|
| Média (A) | 6,099703 | 5,966345 |
| RMS (A) | 6,180803 | 6,049461 |
| Mínimo (A) | 4,373278 | 4,237980 |
| Máximo (A) | 7,823397 | 7,691064 |
| Pico a pico (A) | 3,450119 | 3,453084 |
| Ondulação (%) | 56,562084 | 57,876030 |
| Maior valor em TODO o arquivo (A) | 7,827687 | 7,694950 |
| Menor valor em TODO o arquivo (A) | 4,362525 | 4,232882 |

Os valores do pedido são confirmados pelo arredondamento. Os extremos do arquivo completo diferem dos extremos da janela. Há leve evolução temporal entre janelas; o trecho não estabelece estabilização completa nem inclui a partida.

**Correção de uma atualização preliminar:** os máximos corretos do arquivo são 7,827687 e 7,694950 A, não 7,832/7,699 A. O valor arredondado conservador de referência inicial permanece **7,83 A**, sem margem de transiente comprovada.

Energia máxima inicial de cada unidade, usando o envelope comum:

`W=0,5×209×10⁻⁶×7,83²=0,00640678 J=6,407 mJ`.

Dois componentes nesse mesmo pico simultâneo armazenariam 12,814 mJ; simultaneidade real não foi confirmada.

## 4. Ondulação e volt-segundos

Para os mesmos estados, tensões e tempos: Δi=∫vMdt/Lm. A 50 kHz os dados dão:

- Lm1: ∫vMdt≈209 µH×3,450119 A=721,075 µV·s.
- Lm2: ∫vMdt≈721,694 µV·s.

Esses valores combinam extremos ao longo de cinco ciclos, não necessariamente pertencentes ao mesmo ciclo. São uma estimativa de envelope; o fechamento rigoroso deve usar cada rampa e as tensões exportadas.

A derivada numérica das curvas, multiplicada por 209 µH, indica patamares aproximados de **+54,3 V e −108,1 V**. Como verificação física: tempos aproximados de subida 3,45/(54,3/209 µH)=13,28 µs e descida 6,67 µs, somando cerca de 20 µs. Isso sugere uma fração de subida próxima de 2/3; **não estabelece D da chave**. Não usar 56 V diretamente como tensão de cada enrolamento em todos os estados.

### Alteração separada para alcançar 20%

Mantendo provisoriamente corrente média e volt-segundos:

`Lnovo=Loriginal × Δi_atual/(0,20 Iavg)`.

- Lm1: `209×3,450119/(0,2×6,099703)=591,074 µH`.
- Lm2: `209×3,453084/(0,2×5,966345)=604,805 µH`.

Para componentes idênticos, um alvo inicial de aproximadamente **605 µH** cobriria ambos neste cálculo estático; controle, médias e dinâmica mudam e precisam ser simulados. O projeto original permanece **209 µH**.

Com 605 µH e média de 6,10 A, Δi estimada ≈1,192 A, pico ≈6,696 A, energia ≈13,56 mJ. Em Ae=354 mm² e B≤0,20 T, Np≥605e−6×6,696/(354e−6×0,20)=57,2; para razão 3:2 usar no mínimo 60/40, sob essas hipóteses. Não conservar 24/16: produziria aproximadamente 0,477 T. A janela, cobre e resposta dinâmica devem ser reprojetados.

### 100 kHz — extrapolação expressamente condicional

Somente se as tensões por estado, a razão cíclica, a topologia de condução e as médias permanecerem iguais, duplicar f reduz Δi à metade:

- Δi1≈1,72506 A; ripple≈28,281%.
- Δi2≈1,72654 A; ripple≈28,938%.

Ainda não atende 20%. A mesma hipótese daria L requerido de 295,537/302,402 µH. Não é uma recomendação de alteração sem nova simulação.

Para rampa triangular centrada nas médias atuais, Ipk≈6,962 A no ramo 1 e 6,830 A no ramo 2; Irms≈√(Iavg²+Δi²/12), aproximadamente 6,120/5,987 A. Esses valores NÃO são novos resultados do PSIM e NÃO são correntes físicas dos fios.

Aumentar f não permite reduzir automaticamente Np pela metade: com L e componente CC mantidos, Bdc=L·Idc/(Np Ae) permanece. A excursão AC pode cair; o armazenamento de energia continua impondo núcleo/espiras/entreferro.

## 5. Método AeAw adaptado aos dois enrolamentos

A aula, p.4 e p.6, apresenta `AeAw=L·Ipk·Irms/(Bmax J K)` e `Np=L·Ipk/(Ae Bmax)`, com K≈0,5 para uma bobina e 0,25 para duas ou mais. No acoplado, distinguir a corrente que produz fluxo da corrente que ocupa cobre.

Definindo ku como **fração total de cobre nu utilizável na janela**, temos:

`Aw ku ≥ Np AcuP + Ns AcuS ≥ (Np Ip,rms + Ns Is,rms)/J`.

Com Ns=nNp e Np≥Lm IMpk/(Ae Blim):

`AeAw ≥ Lm IMpk (Ip,rms+n Is,rms)/(Blim J ku)`.

Dimensões SI: H·A·A/[T·(A/m²)]=m⁴. Converter m⁴ para cm⁴ multiplicando por 10⁸. A fórmula decorre de fluxo e espaço de cobre, sem relação de potência típica de Flyback. Não multiplicar arbitrariamente pelo número de saídas. Não combinar um ku total conservador com uma penalização idêntica novamente sem explicitar a dupla margem.

Escolhas preliminares de estudo: Blim=0,20 T e J=3 A/mm², mais conservadoras que 0,3–0,35 T e 3,5–4,5 A/mm² da aula. São metas de projeto, não propriedades oficiais do material nem garantia térmica. Com ku=0,25:

`AeAw_req=1,09098×(Ip,rms+0,666667 Is,rms) cm⁴`.

**Sem Ip,rms e Is,rms físicos não há AeAw final.** Usar 6,18 A nas duas bobinas seria uma hipótese inventada.

Exemplo aritmético independente, não resultado elétrico: se Ip,rms=8 A e Is,rms=6 A, então `AeAw_req=1,09098×12=13,0918 cm⁴`.

Com a tabela DIDÁTICA da aula, E55 tem Ae=3,54 cm² e Aw=2,50 cm², produto=8,85 cm⁴, inferior a 13,09 cm⁴ nesse critério ku=0,25. Isso reprova a triagem conservadora para esse exemplo; não prova inviabilidade dos componentes reais. Se um arranjo real comprovar ku≈0,40, o produto requerido cai a 8,18 cm⁴. É necessário justificar a ocupação geometricamente e testar temperatura; não alterar ku apenas para aprovar o cálculo.

## 6. Comparação dos núcleos e disponibilidade

| Candidato informado | Material informado | Avaliação possível agora | Pendências decisivas |
|---|---|---|---|
| PQ40/40 | N97 | Candidato para comparar perdas e janela | Código completo, Ae/Aw/Ve/le, carretel e número de metades |
| E42/21/20 | N87OL | Candidato, possivelmente mais restritivo para feixes volumosos | Confirmar grafia/código N87OL e carretel E42/20 |
| E55/28/25 | N87OL | Primeiro candidato a investigar pela janela e montagem acessível | Identificar variante, Aw útil, encaixe E55/26 e perdas oficiais |
| PQ32/20 | N87 | Candidato compacto, sem aprovação de capacidade | Quantidade, janela, margens de cobre e calor |

Não atribuir números da tabela genérica E-42/20 ou E-55 da aula aos modelos comerciais específicos sem conferir o desenho. Particularmente a tabela didática traz um valor de le aparentemente inconsistente para E55; não utilizá-lo como especificação de fabricante.

Comparar, quando os datasheets estiverem disponíveis: Ae mínimo e efetivo; Aw do carretel com margens; le; Ve; AL sem/com gap e tolerâncias; μi e curva de polarização; Bsat na temperatura máxima; perdas vs f, B e T; acabamento do gap; montagem; número de metades e carretéis. AL ungapped não é AL de projeto com entreferro.

São necessários **quatro meios-núcleos compatíveis (ou dois conjuntos completos), dois carretéis e duas fixações**, não dois meios-núcleos. A palavra “quantidade” da planilha precisa distinguir peça de par. `Core SH B65884E` é identificação incompleta para validar encaixe. E30/15/14 não deve ser adaptado a E42/E55 sem desenho dimensional. E55/26 e E55/28/25 não se tornam compatíveis pela semelhança dos nomes.

**Escolha final para A e B: pendente.** O E55 é candidato de bancada por facilitar feixes e intercalamento; não foi selecionado como solução aprovada. N97 pode ter vantagens em determinado ponto de perda, mas sem curvas oficiais e formato de onda não há classificação quantitativa defensável.

## 7. Exemplo magnético numérico comum a A e B

Para demonstrar o procedimento sem fabricar dados de catálogo, adota-se **uma geometria hipotética** inspirada apenas nos Ae/Aw da tabela didática: Ae=354 mm², Aw=250 mm². Para o cálculo de relutância somente: le=120 mm e μr=2000 são hipóteses de cálculo, não dados validados de N87/N97. MLT=116 mm é também hipótese simplificada, não comprimento real igual de todas as camadas.

Com Lm=209 µH, Ipk de referência=7,83 A e Blim=0,20 T:

`Np,min=209e−6×7,83/(354e−6×0,20)=23,114`.

Escolha inteira **Np=24 e Ns=16**, razão=0,666667, erro relativo a 0,667 de −0,0500%. Para intercalamento dividir P em 12+12 espiras em série aditiva.

`Bpk=209e−6×7,83/(24×354e−6)=0,192617 T`.

`AL_alvo=209 µH/24²=362,847 nH/espira²`.

`Ls,mag=n²Lm=(16/24)²×209=92,889 µH`.

O arredondamento não determina L sozinho: o entreferro deve ser ajustado para AL=362,847. Depois desse ajuste, L=209 µH e Bpk é o valor acima. Sem ajuste, L=AL_real×576 e deve ser recalculado com AL_real.

ΔB de envelope a 50 kHz: `721,075e−6/(24×354e−6)=0,084872 T`. Na janela, Bmín≈0,1077 T e Bmáx≈0,1925 T; o centro da excursão entre extremos não coincide exatamente com o B médio de uma curva que não é perfeitamente simétrica. A componente média de B para Iavg1 é 0,15005 T. Para 100 kHz, sob a hipótese anterior, ΔB≈0,042436 T e Bpk≈0,1713 T, mas para o exemplo de construção mantêm-se 24/16 e envelope inicial de 7,83 A até validar transientes.

Com 10 A, o mesmo componente chegaria a B≈0,245998 T. A corrente correspondente a 0,20 T é apenas `0,20×24×354e−6/209e−6=8,130 A`: a margem em relação ao limite de projeto é aproximadamente 3,8%. Esse limite NÃO é Bsat; sem curva quente não há margem de saturação comprovada. Para envelope de 10 A sob Blim=0,20 T seriam necessários Np≥29,52, arredondando para 30/20 e redimensionando cobre/gap. Não fixar 10 A como requisito real sem especificação.

Tolerâncias devem ser aplicadas no pior sentido: Lmáx, Ipkmáx, Aemín e Bsat mínimo a quente. Um acréscimo de 5% em L já ultrapassa a meta de 0,20 T no exemplo a 7,83 A. Portanto 24/16 é apenas estudo, não projeto robusto liberado.

## 8. Entreferro e montagem

`Rtotal=Np²/Lm`; `Rcore=le/(μ0 μr Ae)`; `Rgap=g_eq/(μ0 Ae)`.

Logo, sem espraiamento: `g_eq=μ0 Ae Np²/Lm−le/μr`.

Substituindo as hipóteses da seção 7:

`g_ideal=4π×10⁻⁷×354×10⁻⁶×576/(209×10⁻⁶)=1,225997 mm`.

`le/μr=120/2000=0,060000 mm`.

`g_eq≈1,165997 mm`.

É **comprimento magnético equivalente**, não instrução para inserir uma lâmina de 1,166 mm em qualquer junta. Para um E com gap apenas na coluna central e faces externas encostadas, o gap central equivale aproximadamente a g_eq. Em um espaçamento uniforme entre as duas metades, o fluxo cruza a junta central e uma das juntas externas; quando a soma das áreas externas equivale à central, g_eq≈2t. Então t≈0,583 mm seria o começo do estudo. Não dobrar novamente esse valor. Se cada coluna central for retificada em g/2, a separação somada é g.

Com espraiamento, Agap_eff>Ageom. Modelo: `Rtotal=le/(μ0 μr Ae)+Σ gj/(μ0 Agap_eff,j)`. O comprimento físico requerido para a mesma relutância geralmente aumenta. Não se atribui fator numérico sem geometria; a discussão de McLyman explica justamente a dependência da posição do gap e das dimensões. Um único gap de milímetros perto do cobre pode criar perdas localizadas importantes. Considerar gap central usinado pelo fabricante, afastamento das primeiras camadas e/ou gap distribuído suportado pelo conjunto. Não lixar ferrite às cegas nem gerar pó de ferrite no laboratório sem processo apropriado.

Ajuste: montar com espaçadores não magnéticos, medir P com S aberto, manter pressão/fixação repetíveis. Se L alta, aumentar a relutância/gap; se baixa, reduzir gap ou rever espiras. Passos pequenos e medidos; fixar só depois de convergir. Valor final de gap é medido e registrado, não apenas calculado.

**LCR em pequeno sinal mede indutância incremental em torno de i≈0.** A curva real λ(i) pode ser não linear; Lsec=λ/i e Linc=dλ/di diferem. Para o ripple importa Linc na faixa de corrente de operação. Uma medição de 209 µH sem CC não confirma 209 µH entre 4 e 8 A. A interface de polarização CC deve ser apropriada ao LCR; nunca injetar CC em sua porta sem autorização do fabricante.

## 9. Condutores: seleção paramétrica e exemplo

Para cada enrolamento, `Acu≥Irms/J`; `m=ceil(Acu/Área_fio)`. Fio com diâmetro externo máximo determina janela. `d_AWG=0,127×92^((36−AWG)/39) mm`; `A=πd²/4`.

`δ=√[ρ/(π f μ0)]`: a 20 °C, com ρ=1,724×10⁻⁸ Ωm, δ50=0,2955 mm e δ100=0,2090 mm. A 100 °C, ρ aumenta por `1+0,00393×80=1,3144` e δ aumenta por √1,3144. Temperatura maior não compensa o aumento de resistência.

| Fio | d cobre aproximado (mm) | Área (mm²) | Fios para 8 A, J≤3 | Fios para 6 A, J≤3 |
|---|---:|---:|---:|---:|
| AWG26 | 0,405 | 0,1288 | 21 | 16 |
| AWG28 | 0,321 | 0,0810 | 33 | 25 |
| AWG30 | 0,255 | 0,05093 | 53 | 40 |
| AWG32 | 0,202 | 0,03203 | 84 | 63 |

Correntes de 8/6 A são **apenas exemplo de cálculo**, não extraídas da simulação. Muitos fios reduzem efeito pelicular individual, mas multiplicam esmalte, trabalho e risco de divisão desigual; podem aumentar perdas de proximidade. AWG30 é uma alternativa inicial razoável para comparar em ambas as frequências, sem prova de menor perda total.

Fios paralelos comuns não são automaticamente Litz. Cada filamento deve ter comprimento semelhante, mesmo percurso elétrico e ambas as pontas conectadas. Fazer transposição regular de posições, evitando um fio sempre junto ao gap/camada de maior campo. Torcer em conjunto sem transposição de todas as posições não garante correntes iguais. Litz comercial requer construção e terminação verificadas, com possibilidade de pior ocupação e maior custo.

Exemplo 24/16, 53×AWG30 em P e 40×AWG30 em S:

- AcuP=53×0,050926=2,69908 mm²; Jp=8/2,69908=2,96397 A/mm².
- AcuS=2,03704 mm²; Js=6/2,03704=2,94545 A/mm².
- Comprimentos por filamento, assumindo MLT de 116 mm e 0,20 m de terminais: ℓP=24×0,116+0,20=2,984 m; ℓS=16×0,116+0,20=2,056 m.
- ρ100=0,01724×1,3144=0,0226603 Ω·mm²/m.
- RP100=ρ100 ℓP/AcuP=0,0250523 Ω; RS100=0,0228712 Ω.
- Pcu,DC=8²×0,0250523+6²×0,0228712=2,42671 W por componente.

Isso não calcula perdas AC reais. Método apropriado: decompor i(t)=Idc+Σharmônicos e aplicar `Pcu=Idc²Rdc+Σ Ih,rms² Rac(hf,T)`, somando P e S e incluindo campos de proximidade e gap. Estimar Rac por Dowell/solução de campo quando a geometria permitir, ou medir impedância/perdas em bancada. O LCR em circuito aberto inclui perda de núcleo e não mede sozinho Rac do cobre.

Sensibilidade bruta (mesmo fator aplicado ao espectro completo, sem pretensão física de exatidão): se perda efetiva de cobre for 1,5 / 2 / 3 vezes a referência DC, dá 3,640 / 4,853 / 7,280 W. Não atribuir esses fatores a 50 ou 100 kHz sem cálculo/ensaio. Resistência de terminação e perdas de circulação entre filamentos também precisam ser incluídas.

## 10. Arranjo físico, janela e fator de execução

Comparação:

| Arranjo | Dispersão relativa esperada | Compromissos |
|---|---|---|
| P e S em setores separados | Maior | Fácil isolamento, pior para meta de Lk baixa |
| P inteiro e S concêntrico sobreposto | Intermediária | Construção simples; camadas externas mais longas |
| P/2–S–P/2 | Geralmente menor | Mais interfaces/capacitância, terminações e isolamento |
| Intercalamento mais subdividido | Pode reduzir mais | Complexidade e capacitância maiores; não garantia de menor perda total |

Recomendação para protótipo geométrico: P1=12, S=16, P2=12, P1 e P2 em série **aditiva**. O primário total continua 24 espiras; não ligar metades em paralelo. Marcar P1 início pontuado; P1 fim ligado a P2 início conforme teste aditivo. Marcar o S pelo teste elétrico, depois mapear às polaridades específicas de cada ramo do circuito.

Esquema radial, sem escala:

```
coluna central / carretel
│ isolamento inicial e margens
│ P1: 12 espiras, feixe de mP fios
│ barreira entre enrolamentos
│ S : 16 espiras, feixe de mS fios
│ barreira entre enrolamentos
│ P2: 12 espiras, feixe de mP fios
│ isolamento externo / fixação
└ folga até a ferrite; manter cobre afastado do gap
```

Enrolar todas as seções com convenção de início/fim registrada. Mesmo giro visto do mesmo lado pode facilitar a identificação, mas não substitui teste de polaridade. A disposição não assegura isolação galvânica do conversor: isso depende do circuito completo.

A aula p.39 define `FE=Aw_min/Aw`, com `Aw_min=Np mP Aexterna_fioP+Ns mS Aexterna_fioS`; p.11/p.38 indica rever se FE>0,9. Esse FE usa área circular com esmalte e não descreve sozinho vazios, fitas, margens ou cantos do carretel.

Para o exemplo, diâmetro externo HIPOTÉTICO de AWG30 de 0,30 mm:

`Aw_min=(24×53+16×40)×π×0,30²/4=135,151 mm²`.

`FE_anexo=135,151/250=0,54061`.

Se empacotamento dos círculos no feixe=0,785 e reserva equivalente para fitas/margens=20 mm²:

`Aw_ocupada≈135,151/0,785+20=192,167 mm²`, `FE_geom≈0,76867`.

A fração de cobre nu deste exemplo é `(24×2,69908+16×2,03704)/250=0,38948`. Por isso ele pode caber em uma avaliação detalhada apesar da triagem AeAw com ku=0,25 ter reprovado: são critérios de utilização diferentes. A ocupação de 0,3895 precisa ser demonstrada com carretel real e feixe amostral; não está comprovada pelo cálculo escalar.

**Número de camadas:** medir largura axial útil bu e espessura radial disponível hr. Medir o feixe montado, não usar apenas diâmetro equivalente. Se feixe retangular mede w×h, espiras/camada=floor(bu/w); camadas=ceil(N/espiras_por_camada). Somar h×camadas de cada seção, fitas e margens. Deve ser ≤hr sem esmagar esmalte.

Demonstração geométrica, sem atribuir dimensões ao carretel disponível: bu=20 mm, hr=12,5 mm; feixe P organizado em até 11×5 posições de fios externos de 0,30 mm ocupa aproximadamente 3,3×1,5 mm, feixe S 10×4 ocupa 3,0×1,2 mm. P1: 6 espiras/camada, 2 camadas; S: 6 espiras/camada, 3 camadas (6+6+4); P2: 2 camadas. Altura de fios=3+3,6+3=9,6 mm. Reservar, por exemplo, até 1,2 mm adicionais para todas as barreiras/fitas e folgas dá 10,8 mm <12,5 mm. Arranjo ordenado de 53 filamentos é trabalhoso e pode não manter esse retângulo; medir feixe real e testar. Esses números são um **gabarito hipotético**, não dimensões confirmadas nem autorização de montagem nominal.

A espessura das barreiras e as distâncias de escoamento/isolação devem ser definidas pela tensão repetitiva máxima, sobretensões, classe de isolação, poluição, altitude e norma aplicável. Não considerar duas camadas arbitrárias de fita como isolação certificada. Em até 340 Vcc e picos de chaveamento, esmalte comum isoladamente não demonstra segurança.

## 11. Dispersão e referência

Metas na referência P: Lk_obj≤10,45 µH; máximo≤20,9 µH. Referidas ao S: n²×10,45=4,644 µH e n²×20,9=9,289 µH.

Intercalamento é uma estratégia para alcançar a meta, não uma previsão numérica de Lk. Estimativa analítica de dispersão exige altura axial, larguras radiais das camadas, distâncias, MLT e distribuição de ampère-espiras; esses dados faltam. Capacitância cresce aproximadamente com εA/d de cada interface; não se pode minimizar indefinidamente a distância por causa da isolação e das correntes de modo comum.

Na representação de dois indutores acoplados, Lp e Ls são indutâncias próprias medidas com o outro aberto; M é mútua e k=M/√(LpLs). Com o secundário em curto ideal:

`Lsc,P=Lp−M²/Ls=Lp(1−k²)`.

Essa é dispersão equivalente de entrada sob as condições do ensaio. No modelo com transformador ideal + Lm, LσP e LσS, ela aproxima LσP+LσS/n² somente se Lm for muito maior que as dispersões e nas frequências adequadas. Não confundir Lm com Lp nem Lk de um bloco PSIM com Lsc automaticamente.

Apenas se Lp≈Lm, Lsc/Lm≤0,05 implicaria k≥√0,95=0,97468; limite 10% daria k≥0,94868. O valor exato depende do modelo. Se o circuito usar toda a dispersão num único lado, mapear esse modelo antes de fixar o alvo de medição de 209 µH em aberto. Uma LσP em série faz Lp,aberto=Lm+LσP; ajustar cegamente Lp a 209 µH reduziria Lm.

## 12. Perdas de ferrite e temperatura

`Ptotal=Pcu+Pcore`, acrescido de outras perdas locais relevantes que não estiverem contidas no modelo, como aquecimento por campo do gap. `Pcore=Pv(f,forma de B,ΔB,Bdc,T)×Ve`.

Para o exemplo de 50 kHz, ΔB≈84,87 mT, e a amplitude AC em torno do centro da excursão é aproximadamente 42,44 mT; **não usar Bpk total de 0,193 T como amplitude senoidal AC da curva de perdas**. A forma é aproximadamente triangular assimétrica com polarização CC. A 100 kHz condicional, ΔB≈42,44 mT e amplitude≈21,22 mT. Dados senoidais do fabricante são apenas ponto de partida; usar iGSE com parâmetros válidos para o material e faixa, ou medição. Incluir efeito de polarização se suportado; não extrapolar curvas indiscriminadamente.

Para Steinmetz idealizada `Pv∝f^α B_ac^β`, sob f dobrada e B_ac dividida por 2, razão Pcore100/Pcore50=2^(α−β), com mesmo volume e parâmetros. Sem α, β oficiais e validação da forma de onda não há valor numérico. A perda pode cair mesmo com f maior nesse cenário, enquanto cobre AC e perdas nos semicondutores podem aumentar.

Não há valor oficial de Pv ou Ve validado para as peças: **Pcore, Ptotal real e temperatura final ficam indeterminados**. Fornecer um número fechado seria inventar resultados.

Modelo térmico inicial: `Tquente≈Tamb+Ptotal Rθ`, com Rθ dependente da montagem. Para ilustrar a exigência térmica, se uma montagem admitisse no máximo 80 °C a 25 °C e Ptotal fosse 6 W, seria necessário Rθ≤(80−25)/6=9,17 K/W. Isso não é previsão da temperatura do componente. Modelo de dois nós cobre/núcleo ou ensaio de equilíbrio é preferível; termopares externos podem subestimar o ponto quente interno.

## 13. Comparação solicitada

A tabela diferencia o que foi calculado do que ainda exige dados. “Ex.” é a geometria hipotética da seção 7, não núcleo comercial validado.

| Parâmetro | Projeto A — 50 kHz | Projeto B — 100 kHz |
|---|---|---|
| Núcleo selecionado | Pendente; investigar E55 primeiro | Pendente; comparar E55/PQ40 e curvas reais |
| Material | Pendente de código/datasheet | Pendente de código/datasheet |
| Np/Ns | Ex. 24/16; não liberado | Ex. 24/16 mantido; não liberado |
| Lm | 209 µH referido a P, hipótese a confirmar | 209 µH referido a P, hipótese a confirmar |
| Lk | Meta P≤10,45 µH; sem estimativa geométrica confiável | Mesma meta; medir na frequência aplicável |
| Entreferro | Ex. 1,166 mm equivalente sem fringing | Mesmo exemplo, pois L/N/A iguais |
| AWG P e S | Ex. AWG30, 53/40 fios para 8/6 A hipotéticos | Mesma alternativa inicial; RMS real ausente |
| Correntes magnetizantes RMS | 6,1808 / 6,0495 A verificadas | Não simuladas; não usar extrapolação como dado |
| Bmáx | Ex. 0,1926 T a 7,83 A | Envelope inicial mantido; 0,1713 T só sob extrapolação |
| ΔB | Ex. 84,87 mT | Ex. condicional 42,44 mT |
| FE anexo / geométrico | Ex. 0,5406 / 0,7687 | Ex. igual se mesma construção |
| Perda de cobre DC | Ex. 2,427 W, 8/6 A e cobre a 100 °C | Não demonstrada; depende de correntes reais |
| Perda de cobre AC | Pendente de espectro/geometria/ensaio | Pendente; maior exigência de proximidade |
| Perda de núcleo | Pendente de dados oficiais e forma de onda | Pendente dos mesmos dados e nova simulação |
| Perdas totais / temperatura | Indeterminadas | Indeterminadas |
| Ondulação magnetizante | 56,56 / 57,88% verificadas | 28,28 / 28,94% apenas condicionais |

**Decisão técnica neste estágio:** usar 50 kHz como referência experimental inicial porque há dados numéricos verificáveis e a construção com fios paralelos tende a ser menos exigente em AC. Não é uma conclusão de superioridade de eficiência. Não reduzir o núcleo a 100 kHz enquanto permanecerem Lm, polarização CC e energia. A melhor frequência só será escolhida após comparar perdas totais medidas/calculadas, estoque real e ensaios térmicos nas mesmas cargas e limites.

## 14. Manual de construção — procedimento condicionado à liberação

O procedimento serve a ambos os projetos. Não iniciar fabricação nominal a partir do exemplo 24/16 antes de confirmar núcleo, correntes, margem quente e isolação. Pode-se fazer uma bobina de prova desenergizada para medir ocupação e acoplamento. Manter uma folha de fabricação por peça.

1. **Fechar a ficha de engenharia.** Registrar identificação do componente, f, desenho e revisão; núcleo/material/código; Ae mínimo, AL alvo, Np/Ns; correntes RMS/pico; condutor/esmalte; gap; plano de isolação; limites elétricos/térmicos. Confirmar que os dois componentes terão a mesma especificação, dimensionada pelo ramo mais severo.
2. **Conferir estoque.** Separar dois pares completos de ferrite e dois carretéis compatíveis. Inspecionar trincas, lascas nas faces, planicidade, rebarbas, pinos e classe térmica. Não usar metades de materiais ou geometrias diferentes.
3. **Conferir encaixe.** Montar seco, sem cobre. Medir largura axial, altura radial e passagem dos terminais, folga das faces e fixação. Comparar ao desenho do fabricante. Não forçar o carretel.
4. **Preparar ferramentas.** Contador de espiras, guia de tensão moderada, micrômetro, lâminas espaçadoras calibradas, fitas apropriadas, mangas, etiquetas, soldagem com exaustão e LCR compensado. Núcleo não deve depender de uma abraçadeira condutiva fechando uma espira ao redor do fluxo.
5. **Fazer feixe de prova.** Confirmar bitola medindo cobre e externo; contar filamentos. Medir retângulo real do feixe sob tensão leve. Verificar que a soma de camadas e barreiras cabe com margem. Se não couber, interromper e reprojetar, sem esmagar esmalte.
6. **Cortar filamentos.** Para o exemplo apenas, P soma cerca de 2,984 m por fio e S 2,056 m; adicionar margem de manuseio e separar P1/P2 conforme terminações. Usar MLT por camada no projeto final. Não cortar todo o estoque com base no MLT ilustrativo.
7. **Preparar paralelos.** Distribuir filamentos em suporte, igualar comprimentos, transpor posições regularmente sem esforço que rompa o esmalte. Etiquetar P1i/P1f, P2i/P2f e Si/Sf. Reservar comprimento suficiente para soldar todos os fios; não unir somente parte do feixe.
8. **Isolamento inicial.** Remover rebarbas; aplicar isolamento aprovado sobre o carretel e margens. Registrar espessuras. Prever afastamento do gap e escoamento na saída dos terminais. Não aumentar isolação de maneira que elimine a folga previamente calculada.
9. **Enrolar P1.** No exemplo, 12 espiras do feixe de 53 fios AWG30. Cada passagem completa ao redor da coluna conta uma espira; os filamentos paralelos não multiplicam N. No gabarito hipotético da seção 10 são 6+6 espiras em duas camadas. Em carretel real calcular novamente. Distribuir sem cruzamentos, com tensão uniforme e proteção de canto.
10. **Isolar camadas/terminais.** Quando previsto, colocar fita entre camadas e manga nos terminais. Manter terminais fora da zona do gap e sem pressionar o feixe seguinte. Registrar contagem e sentido com foto.
11. **Barreira P1/S.** Aplicar o sistema de isolação definido; manter sobreposição e margens especificadas. A espessura final tem de corresponder à análise de janela. Testar continuidade antes de encobrir.
12. **Enrolar S.** Exemplo: 16 espiras de 40 fios AWG30. No gabarito hipotético: 6+6+4 em três camadas. Marcar início/fim, não confundir o enrolamento S com o segundo componente Lm2.
13. **Barreira S/P2.** Repetir o sistema aprovado; organizar saídas para não criar áreas de contato sem barreira. Um intercalamento aumenta o número de interfaces a isolar.
14. **Enrolar P2.** Exemplo: 12 espiras, mesmo feixe de P1, duas camadas 6+6 apenas no gabarito. Preparar conexão em série aditiva; não fechar uma ligação permanente sem confirmar o sinal da mútua.
15. **Terminar todos os filamentos.** Remover esmalte com processo adequado à classe do fio, sem entalhar cobre. Inspecionar cada filamento, estanhar e unir de modo simétrico. Manga de isolamento e alívio mecânico. Fazer teste de continuidade e resistência; fio não conectado pode continuar ocupando janela sem conduzir corrente.
16. **Montagem inicial do núcleo.** Usar gap de fábrica ou espaçadores não magnéticos calibrados. Para o exemplo sem fringing, gap central equivalente≈1,166 mm ou espaçador uniforme inicial≈0,583 mm, SOMENTE se a geometria suportar a equivalência descrita. Não tratar esses números como gap final.
17. **Fixar provisoriamente.** Empregar pressão uniforme, sem trincar ferrite. Garantir que grampos/chapas não criem espira em curto. Não colar antes do ajuste elétrico.
18. **Medir e ajustar.** Fazer os ensaios da seção 15. Primeiro confirmar espiras/polaridade; depois ajustar gap e AL, distinguindo Lm de indutância própria. Medir P/S abertos e curtos, várias frequências. Registrar todas as condições.
19. **Avaliar dispersão.** Se acima de 5%, revisar sobreposição, altura axial comum, terminações e distância entre camadas sem comprometer isolação. Entre 5 e 10% exige avaliação do circuito, picos e perdas; acima de 10% não atende a especificação. Não reduzir dispersão simplesmente diminuindo o gap, pois isso muda Lm/fluxo.
20. **Fixação definitiva e reinspeção.** Após aprovação de pequeno sinal e polaridade, aplicar fixação compatível com temperatura e isolação. Repetir L/R/Lsc após cura: pressão e cola podem alterar gap. Identificar pontos e terminais de forma durável.
21. **Ensaios sob corrente, térmicos e isolação.** Executar antes de operação nominal; pequeno sinal não é liberação de potência. Se houver perda de indutância excessiva, ponto quente ou falha de isolação, reprojetar.
22. **Construir a segunda unidade.** Repetir com a mesma ficha, não apenas por aparência. Comparar as medições e tolerâncias definidas pelo circuito; uma meta inicial de pareamento de 2% pode ser estudada, mas não substitui a análise de equilíbrio dos barramentos. Conectar as polaridades corretas de cada ramo conforme o esquema final.

Para B, usar esse mesmo roteiro apenas após atualizar a ficha com resultados de 100 kHz. Manter AWG30 e 24/16 como ponto de comparação experimental é permitido como hipótese, não como projeto B validado.

## 15. Ensaios LCR e complementares

### 15.1 Preparação

Desconectar completamente o componente do conversor, descarregar capacitores e confirmar ausência de tensão. Nunca medir LCR no circuito energizado. Compensar aberto/curto com os mesmos cabos e frequência; preferir quatro terminais/Kelvin. Registrar frequência, amplitude de excitação, modo série/paralelo, temperatura e fixação. Começar em baixa amplitude e verificar se o fluxo de ensaio é pequeno. Para seno, Bpk=Vrms/(4,442 f N Ae); evitar frequência muito baixa com tensão alta.

Medir, por exemplo, 1, 10, 50 e 100 kHz somente se disponíveis no instrumento e abaixo da ressonância própria. A frequência de 50/100 kHz só é válida se o componente ainda puder ser representado indutivamente; capacitação parasita pode invalidar a leitura. Se o LCR só mede 1 kHz, esse ensaio é referência de pequeno sinal e os dados em alta frequência continuam pendentes.

### 15.2 Indutâncias próprias e razão

S aberto, medir Lp; P aberto, medir Ls. A razão `sqrt(Ls/Lp)` aproxima Ns/Np quando dispersão é pequena e o modelo é adequado. Para 24/16, esperar perto de 0,6667, não exatamente se as dispersões diferirem. Medir relação de tensões com gerador de baixa tensão e osciloscópio é confirmação melhor. Com P/S conhecidos, separar Lm de Lσ usando o modelo do circuito; não assumir Lp=209 µH sem essa etapa.

### 15.3 Mútua e polaridade por associação

Ligar P e S em série uma vez com ligação A e medir La; inverter somente S e medir Lb, demais pontas livres. A maior leitura é L+=Lp+Ls+2M; a menor L−=Lp+Ls−2M. Assim `M=(L+−L−)/4`, `k=M/√(LpLs)`. Se k>1, rever compensação, modelo, conexões e frequência; não truncar para 1 e ignorar o problema. Na associação aditiva usual conecta-se um terminal pontuado ao não pontuado do outro; confirmar com o teste.

No ideal Lp=209 µH e Ls=92,889 µH, M≈139,333 µH; L+≈580,556 µH e L−≈23,222 µH. Esses valores são referência ideal sem dispersão, não leituras obrigatórias. A relação `(sqrt(L+)−sqrt(L−))/(sqrt(L+)+sqrt(L−))` não deve ser usada cegamente como k.

Gerador isolado de baixa tensão e osciloscópio diferencial podem confirmar polaridade: tensões com mesma fase medidas de ponto para não ponto identificam a convenção. Uma bateria sem limitação pode saturar e danificar; não é método recomendado.

### 15.4 Dispersão

Curto-circuitar S com ligação de baixa impedância, curta e robusta; medir no P: Lsc,P. A resistência do curto e sua indutância parasita precisam ser pequenas e compensadas. Repetir invertendo os lados e expressar tudo na mesma referência: `Lsc,P_equiv≈Lsc,S/n²`. Reportar diferença entre métodos e frequências. Obter k também por `sqrt(1−Lsc,P/Lp)` apenas no modelo e faixa em que a equação vale.

Verificar meta 10,45 µH e limite 20,9 µH somente depois de mapear a grandeza Lk do PSIM à medição. Não somar dispersões referidas a lados diferentes.

### 15.5 Resistência

Medir DCR a temperatura conhecida com quatro fios e corrente pequena para não aquecer. Se o LCR não oferece DCR, o parâmetro Rs de alta frequência NÃO é resistência CC; usar micro-ohmímetro ou fonte limitada + voltímetro Kelvin. Subtrair contatos/cabos. Medir P1 e P2 individualmente antes de fechar série quando possível. Desvio excessivo entre feixes pode indicar filamento não conectado.

### 15.6 Entreferro e repetibilidade

Medir L com uma sequência documentada de espaçadores, mesma força de fixação. Representar 1/L em função do gap equivalente; tendência aproximadamente linear antes das correções de fringing. Repetir desmontagem/montagem para estimar tolerância mecânica. Registrar temperatura e AL medido. Não medir faces de ferrite com pressão que as lasque.

### 15.7 Polarização e saturação — instrumentação adicional obrigatória

Necessários fonte CC limitada, chave/controlador de pulsos, caminho seguro de desmagnetização/clamp, shunt calibrado ou sonda de corrente, osciloscópio e medição diferencial isolada de tensão. LCR sozinho não verifica saturação a 7,83 A.

Fora do conversor, aplicar pulsos inicialmente curtos e de baixa energia a um enrolamento, com o outro na condição definida e protegida contra sobretensão induzida. Medir v(t) e i(t); descontar Ri quando relevante; calcular Linc≈(v−Ri)/(di/dt) e λ=∫(v−Ri)dt. Aceleração abrupta de di/dt indica queda de indutância. Garantir reset entre pulsos e limite independente de corrente. Elevar corrente progressivamente até o envelope definido, repetir a quente e nas tolerâncias. Um ensaio pulsado curto não substitui ensaio térmico contínuo.

O ensaio precisa de projeto próprio de comutação, supressão e intertravamento. Não ligar fonte CC diretamente ao enrolamento e esperar regime permanente seguro. Não aterrar a garra do osciloscópio em nó chaveado/flutuante.

### 15.8 Isolação

Inspeção visual, continuidade indevida entre enrolamentos/núcleo e resistência de isolação com equipamento próprio. Hipot e sua tensão/tempo só após definir norma, tipo de isolação e tensões reais; não inventar uma tensão de ensaio a partir apenas de 340 V. Instrumentos sensíveis e eletrônica devem estar desconectados. Operador treinado, barreira e descarga após ensaio.

### 15.9 Aquecimento e potência

Necessários termopares isolados adequados, carga controlada, monitoramento das correntes e tensões dos barramentos e proteção. Ensaiar inicialmente em tensão/potência reduzidas com limitação; verificar polaridades, reset de fluxo, overshoot e equilíbrio. Subir por patamares, por exemplo 10/25/50/75/100% SOMENTE se o comportamento e os limites do estágio anterior forem aprovados. Esses percentuais são roteiro, não garantia de operação estável do controle.

Esperar estabilização térmica em cada condição crítica (critério prático de estudo: variação menor que 1 °C em 10 min, confirmando que a constante térmica foi coberta). Medir cobre, núcleo, terminais, ambiente e ventilação. Estimar temperatura média do cobre pela resistência: `T=20+[(Rquente/R20)−1]/0,00393`. Essa média não captura o ponto quente. Interromper ao alcançar o limite previamente definido ou crescimento anormal de temperatura/corrente.

Os 340 Vcc e a energia dos capacitores exigem barreiras, fusível, desligamento, descarga controlada, confirmação de ausência de tensão e supervisão de laboratório. Ensaios de defeito/desequilíbrio em potência plena somente com proteção verificada. Repetir em 50 e 100 kHz com mesma carga, condições térmicas e método de medição; não atribuir toda diferença de eficiência aos magnéticos, pois os semicondutores também mudam.

## 16. Lista de materiais para duas unidades

Lista final depende da aprovação elétrica e mecânica. Quantidades do exemplo são indicadas separadamente.

| Item | Quantidade/critério |
|---|---|
| Conjunto de ferrite compatível | 2 pares completos = 4 metades, material e código pendentes |
| Carretel correspondente | 2, não confirmados pelos nomes abreviados |
| Fixação não curto-circuitante | 2 conjuntos |
| Espaçadores calibrados não magnéticos | Jogo para ambos; espessura final obtida em ensaio |
| Fio P e S | Bitola, esmalte e estoque a confirmar |
| Exemplo AWG30 para P | 2×53×2,984=316,304 m de filamento, antes de reservas extras de construção |
| Exemplo AWG30 para S | 2×40×2,056=164,480 m de filamento |
| Exemplo total AWG30 | 480,784 m; com 15% de reserva, aproximadamente 553 m |
| Fitas, barreiras, mangas e margens | Sistema de isolação a dimensionar; metragem pelo desenho final |
| Terminais e emendas | 8 terminais externos para 4 enrolamentos, mais 2 emendas internas P1/P2 se intercalados |
| Etiquetas, alívio mecânico e fixador | Para 2 unidades; classe térmica compatível |
| Instrumentação | LCR existente; adicionais conforme seção 15, não presumidos disponíveis |

O exemplo usa aproximadamente 0,2194 kg de cobre nu no total antes de reservas (densidade 8,96 g/cm³), sem incluir solda/terminais. Comprar somente após confirmar MLT real, número de seções, esmalte, manuseio e estoque. Uma reserva de 15% não cobre automaticamente grandes aumentos de MLT.

## 17. Reprodução computacional e próximos passos

`calculo.py` usa Python e NumPy; foi executado com NumPy 2.3.5. Saídas: JSON completo, CSV de conferência e gráfico SVG. Não altera o repositório, fonte de simulação nem anexos. Valores de exemplo estão agrupados no dicionário de parâmetros e identificados no JSON.

Executar de qualquer diretório, fornecendo caminhos:

```sh
python /workspace/estudo_indutores/calculo.py \
  --correntes /workspace/attachments/ff867785-6410-4f08-81e3-a20a9aacb73e/CorrenteIndutor.txt \
  --saida /workspace/estudo_indutores/resultados
```

Para variar hipóteses criar JSON externo e usar `--config arquivo.json`. Não mudar `f_Hz` para 100 kHz usando o CSV de 50 kHz: esse campo também define a janela de análise. A extrapolação de 100 kHz já é relatada separadamente como condicional. Usar arquivo próprio e janela de cinco períodos em regime para análise real de 100 kHz.

Conclusões confirmadas: tabela de correntes reproduzida; 209 µH não atende 20% no ponto simulado de 50 kHz; duplicar f não bastaria sob a extrapolação simples; dois magnéticos devem ser tratados separadamente dos quatro enrolamentos; correntes magnetizantes não dimensionam os fios por si sós.

Para fechar o projeto: obter arquivos/modelo e estoque; liberar/fornecer datasheets; simular correntes e tensões físicas em ambas as frequências e transientes; inserir geometria oficial; recalcular AeAw, margem quente e camada por camada; estimar perdas com dados válidos; construir bobina de prova; medir L/k/R; ensaiar polarização e calor. Só então liberar os números de fabricação e escolher a frequência por resultados comparáveis.

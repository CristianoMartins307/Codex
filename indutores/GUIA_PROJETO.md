# Guia passo a passo para projetar indutores acoplados

## Conversor CC-CC de 2 kW — projetos a 50 kHz e 100 kHz

Este guia explica como transformar o esquema, os resultados de simulação, os dados do núcleo e as condições do laboratório em uma especificação verificável de dois indutores acoplados. O objetivo é permitir que o estudante refaça as contas, escolha os materiais e entenda o que deve medir antes de aplicar a potência nominal.

A especificação inicial é de dois componentes idênticos, cada um com indutância magnetizante de 209 µH e relação Ns/Np próxima de 2/3. Os nomes Lm1 e Lm2 identificam os ramos magnetizantes dos dois componentes. Eles não representam o primário e o secundário de um único componente.

A apresentação segue a metodologia AeAw do `PROJETO_INDUTOR.pdf`, adaptada a dois enrolamentos a partir de fluxo e ocupação de cobre. O arquivo McLyman é uma referência complementar para circuito magnético, entreferro, espraiamento, perdas e utilização da janela.

**Escopo desta edição:** as correntes magnetizantes de 50 kHz foram recalculadas do arquivo recebido. O projeto PSIM completo não pôde ser transferido por exceder 32 MiB. A planilha de estoque, o segundo PDF metodológico e os datasheets dos materiais não foram recebidos ou validados. Portanto, este é um método de projeto com cálculos verificáveis e hipóteses explícitas, e não uma liberação dos componentes para operação nominal.

## 1. Organizar os dados antes de escolher o núcleo

Comece por uma ficha com quatro categorias. Isso evita que um valor usado para ensinar uma conta seja confundido com um resultado da simulação ou uma propriedade de catálogo.

| Categoria | Exemplos deste trabalho | Como usar |
|---|---|---|
| Especificação fornecida | 2 kW, 56 V de entrada, 209 µH, n≈0,667 | Requisito inicial, sujeito à confirmação de referência e condições |
| Resultado verificado | Média e RMS de I(Lm1)/I(Lm2) a 50 kHz | Evidência do ponto simulado, sem representar todo o envelope |
| Hipótese de estudo | Densidade de corrente de 3 A/mm²; geometria didática | Permite calcular alternativas, sem assegurar aprovação |
| Informação pendente | Correntes físicas dos fios, dados oficiais, operação a 100 kHz | Deve ser obtida antes da especificação definitiva |

Registre a origem de cada valor, as unidades e a temperatura associada. Por exemplo, uma resistência a 20 °C não pode ser usada como resistência de operação a 100 °C sem correção.

### 1.1 O que extrair da simulação

Para cada componente, exporte na mesma base de tempo:

1. Corrente no ramo magnetizante iM(t).
2. Correntes físicas iP(t) e iS(t), com sentido das sondas e dos pontos indicado.
3. Tensões vP(t), vS(t) e, quando acessível, a tensão vM(t) do ramo magnetizante ideal.
4. Comandos das chaves, razão cíclica, defasagem e corrente dos diodos relevantes.
5. Tensões de cada capacitor e correntes de cada carga.
6. Partida, degraus de carga, máxima/mínima entrada e desequilíbrio do barramento bipolar.
7. Limites de proteção, incluindo a corrente máxima antes do desligamento.

Repita esse conjunto a 50 kHz e a 100 kHz. Uma simulação de 100 kHz não consiste somente em reduzir pela metade o eixo do tempo de uma curva de 50 kHz: o controle, as perdas e o modo de condução podem mudar.

### 1.2 O que obter do estoque

Para cada núcleo, registrar fabricante, código completo, material, quantidade de metades ou pares, dimensões, presença de gap de fábrica e carretel correspondente. Para cada fio, registrar AWG ou diâmetro de cobre, diâmetro externo máximo com esmalte, classe de isolação e metragem.

A identificação “E55/26” de um carretel não confirma seu encaixe em um núcleo “E55/28/25”. É necessário o desenho mecânico. O mesmo cuidado vale para PQ32/20, PQ40/40 e códigos incompletos como B65884E.

## 2. Entender o componente no circuito

O recorte do esquema mostra dois símbolos magnéticos separados, cada qual associado a uma Lm e uma Lk. A interpretação preliminar é de dois conjuntos de ferrite independentes, cada um com dois enrolamentos. Isso resulta em dois núcleos completos e quatro enrolamentos. Não há indicação visível de compartilhamento de uma única estrutura magnética, mas o modelo completo precisa confirmar a interpretação.

Desenhe um símbolo simplificado para cada unidade. Dê aos terminais os nomes P1/P2 e S1/S2 e marque os pontos. A posição à esquerda ou à direita no esquema não determina, por si só, qual lado é o primário de referência.

### 2.1 Referência e polaridades

Adote tensões medidas do terminal pontuado para o não pontuado. Se ambas as correntes forem definidas entrando nos pontos, no modelo ideal:

`n = Ns/Np`

`vS = n vP`

`iM = iP + n iS`

A contribuição secundária pode compensar parte da força magnetomotriz primária. Se o sentido de uma sonda for invertido, o sinal da expressão muda. Não mude fisicamente o enrolamento para corrigir uma convenção de sonda sem antes conferir o esquema.

A força magnetomotriz resultante e o fluxo são:

`F = Np iP + Ns iS = Np iM`

`Φ = F/Rtotal`

`B = Φ/Ae`

Essas relações explicam por que uma corrente magnetizante de cerca de 6 A pode coexistir com correntes físicas maiores nos fios.

### 2.2 Equivalente elétrico e magnético

Use no equivalente elétrico um transformador ideal, Lm em paralelo no lado de referência, resistências RP/RS e dispersões LσP/LσS em série. As perdas do ferrite exigem um modelo dependente de forma de onda, frequência, fluxo e temperatura; uma resistência paralela constante serve apenas a uma aproximação local.

No circuito magnético:

`Rtotal = Rcore + Rgap`

`Rcore ≈ le/(μ0 μr Ae)`

`Rgap = Σ gj/(μ0 Agap,efetiva,j)`

A dispersão representa fluxo que não acopla integralmente ambos os enrolamentos. Ela afeta picos de tensão, comutação e circulação de energia; sua energia usa a corrente do enrolamento correspondente.

Para o modo magnetizante linear, a energia é `Wm = 0,5 Lm iM²`. Não some outra vez essa mesma energia como se cada enrolamento tivesse um armazenamento magnetizante independente. Num modelo geral de dois indutores acoplados, a energia é `W = 0,5 Lp iP² + 0,5 Ls iS² ± M iP iS`, com sinais coerentes com os sentidos escolhidos.

## 3. Conferir potência e barramento

Os 340 V podem ser a diferença entre +170 V e −170 V de um mesmo barramento. Isso não produz três saídas independentes de 2 kW.

Se existirem três cargas, uma entre os extremos e duas entre cada extremo e o ponto médio, a potência total fornecida às cargas é:

`Ptotal = 340 I(+−) + 170 I(+0) + 170 I(0−)`

As correntes da expressão são as correntes individuais das cargas, com sinal de consumo. Uma medição que já totalize a potência não deve ser somada novamente.

Como conferência de ordem de grandeza:

`Ientrada,ideal = 2000/56 = 35,714 A`

`Ientrada,real = 2000/(56 η)`

Esse valor não deve ser imposto a iM ou dividido arbitrariamente por dois. A distribuição entre os ramos depende da topologia. Confirmar quais cargas existem, suas potências e o pior desequilíbrio permitido é parte do projeto dos magnéticos.

## 4. Recalcular as correntes do arquivo

Uma curva deve ser analisada em um número inteiro de períodos e, preferencialmente, depois de estabilizar. Para 50 kHz:

`T = 1/f = 20 µs`

O arquivo possui 1.504 amostras, de 34,9178 a 35,0681 ms. Sua duração total é 150,3 µs, equivalente a 7,515 períodos. Usar todo o trecho como se tivesse ciclos completos introduz erro de fase na média e no RMS.

A janela adotada neste estudo é de 34,940 a 35,040 ms, totalizando cinco períodos nominais. As extremidades foram interpoladas e a integração considerou o tempo real.

`Iavg = (1/Δt) integral[i(t) dt]`

`Irms = raiz{(1/Δt) integral[i(t)² dt]}`

`ΔIpp = Imax − Imin`

`ripple(%) = 100 ΔIpp/Iavg`

| Grandeza na janela | Lm1 | Lm2 |
|---|---:|---:|
| Média | 6,099703 A | 5,966345 A |
| RMS magnetizante | 6,180803 A | 6,049461 A |
| Mínimo | 4,373278 A | 4,237980 A |
| Máximo | 7,823397 A | 7,691064 A |
| Pico a pico | 3,450119 A | 3,453084 A |
| Ondulação | 56,5621% | 57,8760% |

O maior pico em todo o arquivo é 7,827687 A no ramo 1. Arredondar para 7,83 A é adequado como referência inicial do ponto observado. Não garante a corrente máxima de partida ou antes da proteção.

Há pequena evolução entre janelas. Antes de usar a simulação como regime permanente definitivo, estender o tempo e conferir se as médias de vários ciclos deixaram de variar.

### 4.1 Por que essas curvas não dimensionam os fios

Partindo de `iP = iM − n iS`:

`Ip,rms² = Im,rms² + n² Is,rms² − 2n média(iM iS)`

O termo de correlação depende da simultaneidade das curvas. Portanto, nem iM RMS sozinha nem o par de valores RMS de iM e iS determina a corrente primária. Exporte as curvas físicas e calcule diretamente o RMS de cada uma.

## 5. Verificar a ondulação antes de mudar a indutância

Para um modelo magnetizante linear:

`vM = Lm diM/dt`

`ΔiM = integral[vM dt]/Lm`

Pelos dados do ramo 1, um envelope de volt-segundos é:

`Lm ΔIpp = 209 µH × 3,450119 A = 721,075 µV·s`

Os extremos foram obtidos ao longo de cinco períodos; para um cálculo final, integrar cada rampa entre seus próprios extremos e conferir diretamente vM(t).

A derivada numérica sugere patamares de aproximadamente +54,3 V e −108,1 V. Isso é coerente com subida de aproximadamente 13,3 µs e descida de 6,7 µs. Não confirma a razão cíclica de uma chave nem demonstra que a tensão do primário é sempre 56 V.

### 5.1 Proposta separada para 20%

Se os volt-segundos e as médias permanecessem iguais:

`Lnovo = Latual × ΔIpp,atual/(0,20 Iavg)`

Para o ramo 1:

`Lnovo = 209 × 3,450119/(0,20 × 6,099703) = 591,074 µH`

Para o ramo 2, o resultado é 604,805 µH. Um alvo inicial comum de aproximadamente 605 µH seria uma proposta a simular, não uma alteração automática dos 209 µH.

Uma indutância maior também altera energia armazenada, número de espiras, cobre, resposta do controle e dinâmica de partida. A conta de ripple não fecha o novo projeto sozinha.

### 5.2 Estudo inicial a 100 kHz

Somente se tensões por estado, frações de período e médias não mudarem:

`ΔIpp,100 = ΔIpp,50/2`

A ondulação seria aproximadamente 28,28% e 28,94%, ainda superior a 20%. Isso é uma extrapolação, não uma simulação de 100 kHz.

Para comparar frequências, mantenha primeiro o requisito original de 209 µH e registre o que muda nas curvas reais. Se decidir avaliar uma segunda indutância, trate-a como variante adicional, com nova memória de cálculo.

## 6. Calcular fluxo, energia e a condição mais severa

A tensão controla a variação de fluxo:

`vM = Np Ae dB/dt`

`ΔB = integral[vM dt]/(Np Ae)`

No modelo linear, sem remanência inicial relevante:

`B ≈ Lm iM/(Np Ae)`

Assim, há duas verificações complementares: os volt-segundos definem a excursão; a corrente magnetizante e a indutância definem o nível de fluxo, incluindo a componente CC.

A frequência maior pode reduzir a excursão AC, mas não elimina o fluxo causado pela polarização CC:

`Bdc ≈ Lm Idc/(Np Ae)`

Não reduza Np pela metade apenas porque f dobrou. Com Lm e Idc mantidos, isso dobraria Bdc.

A energia de referência inicial é:

`Wm = 0,5 × 209 × 10^−6 × 7,83² = 6,40678 mJ`

O gap deve permitir armazenar essa energia com o fluxo escolhido. Aproximadamente, quando o gap domina a relutância, sua energia é `Wgap ≈ B² Agap g/(2 μ0)`. O resultado deve ser coerente com a energia calculada por L e corrente.

### 6.1 Definir limite de fluxo

Escolha Blim usando simultaneamente:

- Saturação mínima do material na temperatura máxima prevista.
- Perdas de núcleo na frequência e na excursão de operação.
- Fluxo adicional de partida, desequilíbrio e tolerâncias.
- Margem contra variações de montagem e área mínima da seção.

Uma meta didática de 0,20 T pode iniciar uma comparação. Ela não é o Bsat validado de N87 ou N97. As sugestões de 0,3–0,35 T da aula também não são autorização para trabalhar nesse nível em qualquer frequência e temperatura.

Use Ae efetivo para a transformação média entre fluxo e densidade; quando houver uma seção mínima menor que Ae, confira o fluxo local também com Amin. Bsat deve ser comparado à condição local e quente, e não somente à média nominal do caminho.

## 7. Aplicar AeAw a dois enrolamentos

O método faz duas exigências caberem no mesmo componente: área de núcleo suficiente para o fluxo e área de janela suficiente para o cobre.

Defina:

- Ae: seção magnética efetiva, m².
- Aw: janela de enrolamento conforme a convenção do núcleo/carretel, m².
- Lm: indutância magnetizante referida ao primário, H.
- IMpk: pico magnetizante de projeto, A.
- Ip,rms e Is,rms: correntes físicas dos dois enrolamentos, A.
- J: densidade de corrente no cobre, A/m².
- ku: fração total de cobre nu utilizável na janela, sem unidade.
- n: Ns/Np, sem unidade.

Evite um erro de fator dois: confira se Aw do catálogo é a área de uma janela lateral ou outra convenção geométrica. Uma volta ocupa os dois lados do carretel; usar a soma das duas janelas com uma fórmula definida para uma janela conta espaço duas vezes.

### 7.1 Derivação

A exigência de fluxo fornece:

`Np >= Lm IMpk/(Ae Blim)`

A exigência de cobre fornece:

`Aw ku >= Np AcuP + Ns AcuS`

Com `AcuP >= Ip,rms/J`, `AcuS >= Is,rms/J` e `Ns = n Np`:

`Aw ku >= Np (Ip,rms + n Is,rms)/J`

Substituindo o limite de Np:

`Ae Aw >= Lm IMpk (Ip,rms + n Is,rms)/(Blim J ku)`

Essa derivação usa a função física do indutor acoplado; não depende das relações de ganho ou potência de um Flyback.

Se as densidades de corrente forem diferentes, use:

`Ae Aw >= (Lm IMpk/Blim) × [Ip,rms/(Jp ku) + n Is,rms/(Js ku)]`

O ku continua representando a fração total de cobre utilizável; não aplique uma segunda penalização idêntica pelo número de enrolamentos.

### 7.2 Unidades e substituição

Em SI, o resultado é m^4. Para converter para cm^4, multiplicar por 10^8.

Com Lm=209 µH, IMpk=7,83 A, Blim=0,20 T, J=3 A/mm²=3×10^6 A/m² e ku=0,25:

`AeAw_req = 1,09098 × (Ip,rms + 0,666667 Is,rms) cm^4`

O valor final depende dos RMS físicos. Se apenas para ilustrar a substituição forem usados 8 A e 6 A:

`AeAw_req = 1,09098 × (8 + 0,666667 × 6) = 13,0918 cm^4`

Esses 8/6 A não são valores extraídos do PSIM.

## 8. Escolher núcleo e carretel

Construa uma tabela de candidatos com Ae, Amin, Aw útil, le, Ve, AL, material, gap, perdas e estoque. Os candidatos informados pelo usuário são PQ40/40 N97, E42/21/20 N87OL, E55/28/25 N87OL e PQ32/20 N87. Confirmar a grafia e o código comercial completo do material é obrigatório.

O núcleo deve atender a cinco verificações:

1. Ae e espiras limitam o fluxo na condição severa.
2. O gap é realizável e armazena a energia necessária.
3. Os dois enrolamentos e o isolamento cabem de verdade.
4. As perdas e a temperatura são aceitáveis.
5. Existem dois conjuntos completos com carretéis compatíveis.

Um núcleo de menor volume pode exigir mais espiras e mais camadas, aumentando resistência, proximidade e tempo de fabricação. Um núcleo maior pode facilitar o uso de feixes finos e reduzir cobre/temperatura. Compare o componente construído, não apenas Ve.

A tabela genérica da aula é útil para ensinar o método, mas não substitui a especificação de uma variante comercial. Não transfira Ae/Aw de “E55” para qualquer E55/28/25 sem verificar o desenho. O acesso aos PDFs oficiais da TDK foi bloqueado nesta execução; por isso nenhum desses candidatos foi homologado por dados de catálogo neste trabalho.

## 9. Escolher espiras inteiras e verificar tolerâncias

Calcule Np mínimo por fluxo e arredonde para cima. Para respeitar exatamente 3:2:

`Np = 3q` e `Ns = 2q`, para q inteiro positivo.

Se a construção intercalada P/2–S–P/2 exigir duas metades primárias iguais, prefira Np múltiplo de 6. Isso não é uma condição elétrica universal; é uma conveniência de montagem.

Depois de arredondar:

`nreal = Ns/Np`

`AL_alvo = Lm/Np²`

`Bpk = Lm IMpk/(Np Ae)`

`Ls,mag = nreal² Lm`

A indutância final depende de AL após montar o gap. O arredondamento de espiras não mantém L automaticamente.

Como microexemplo, apenas para Ae hipotético=354 mm², Lm=209 µH e IMpk=7,83 A, Np mínimo para 0,20 T é aproximadamente 23,115. A escolha 24/16 resulta em AL≈362,847 nH/espira² e Bpk≈0,192617 T. Ela deixa pouca margem à meta de 0,20 T: L+5% já a ultrapassa. Isso demonstra por que uma conta nominal não é um projeto robusto liberado.

Faça a análise de pior caso com Lmáx, IMpkmáx, Aemín e Bsat quente mínimo. Se a corrente limite ainda não existe, mantenha o número de espiras pendente ou estude mais de uma margem, sem inventar que o pico observado é o pior transiente.

## 10. Calcular e ajustar o entreferro

Pela relutância:

`Lm = Np²/Rtotal`

Sem espraiamento e usando a mesma seção efetiva:

`g_eq = μ0 Ae Np²/Lm − le/μr`

Se o resultado fosse negativo, haveria inconsistência entre as hipóteses ou o AL escolhido; um gap físico negativo não é solução. Para gap dominante, o termo do núcleo é pequeno, mas deve ser avaliado antes de desprezá-lo.

### 10.1 Gap equivalente e gap físico

O cálculo fornece uma relutância, expressa por um comprimento equivalente. Sua distribuição depende da geometria.

- Gap somente na coluna central de um E: as faces externas encostam e, aproximadamente, gcentral=g_eq.
- Espaçador uniforme entre todas as faces: o fluxo cruza a separação central e uma externa; quando as áreas externas totais equivalem à central, g_eq≈2t, em que t é a espessura do espaçador.
- Duas metades retificadas na coluna central: as remoções somam o gap final; não dobrar o comprimento novamente.

No exemplo hipotético de 24 espiras, Ae=354 mm², le=120 mm e μr=2000, resulta g_eq≈1,166 mm sem fringing. Isso não significa inserir uma lâmina de 1,166 mm em uma junta uniforme. As propriedades le/μr usadas nesse exemplo são hipóteses, não dados oficiais do ferrite.

### 10.2 Espraiamento e ajuste

O campo se expande nas bordas do gap, aumentando a área efetiva e reduzindo sua relutância em relação à estimativa sem fringing. Para recuperar a mesma relutância, o comprimento físico pode precisar aumentar. O campo espalhado também pode aquecer fios próximos, especialmente em um gap concentrado.

Não atribua um fator arbitrário de espraiamento sem geometria. Use modelo validado, simulação de campo ou ajuste experimental com medição. Mantenha os primeiros condutores afastados da região de campo intenso quando o projeto mecânico permitir.

Monte provisoriamente com espaçadores calibrados e mesma pressão de fixação. Se L estiver alta, aumentar gap reduz L; se L estiver baixa, reduzir gap aumenta L. Ajuste em passos pequenos e registre o resultado. Nunca compense uma contagem de espiras errada apenas mexendo no gap.

Preferir gap de fábrica ou processo de usinagem adequado. Não lixar ferrite no laboratório sem controle de pó, planicidade e acabamento. Fissuras e faces tortas comprometem repetibilidade e confiabilidade.

## 11. Dimensionar fios finos em paralelo

Para cada enrolamento:

`Acu_necessaria = Irms/J`

`m = teto(Acu_necessaria/Área_fio)`

A corrente usada aqui é a corrente física RMS daquele enrolamento. O número m representa filamentos paralelos em cada espira; não multiplica o número de espiras magnéticas.

Para AWG:

`d(mm) = 0,127 × 92^[(36−AWG)/39]`

`Área_fio(mm²) = π d²/4`

| AWG | Diâmetro de cobre aproximado | Área aproximada |
|---|---:|---:|
| 26 | 0,405 mm | 0,1288 mm² |
| 28 | 0,321 mm | 0,0810 mm² |
| 30 | 0,255 mm | 0,05093 mm² |
| 32 | 0,202 mm | 0,03203 mm² |

As áreas de cobre não incluem esmalte. Para janela e camadas, usar o diâmetro externo máximo garantido do fio real.

### 11.1 Efeito pelicular

`δ = raiz[ρ/(π f μ0)]`

Com cobre a 20 °C, δ≈0,296 mm a 50 kHz e ≈0,209 mm a 100 kHz. Diâmetro pequeno em comparação com δ ajuda a reduzir a não uniformidade dentro de cada filamento, mas não elimina proximidade, campo do gap ou divisão desigual de corrente.

Os harmônicos estão em frequências maiores que a fundamental de chaveamento e têm profundidades menores. Uma corrente com pulsos estreitos pode exigir avaliação de espectro mesmo que o fio pareça fino em relação a δ(fchaveamento).

### 11.2 Fios paralelos e Litz

Filamentos devem ter comprimentos, terminações e trajetórias comparáveis. Transpor as posições evita que um fio fique sempre no lado de campo mais intenso. Uma torção simples sem troca adequada das posições não garante comportamento de Litz.

Quanto mais filamentos, maior o volume relativo de esmalte, o trabalho de preparação e o risco de fios desconectados. Compare ao menos duas bitolas antes de escolher. Um feixe de AWG30 pode ser interessante para comparar 50/100 kHz, mas não é automaticamente a opção de menor perda total.

Litz comercial merece avaliação se a redução de perda compensar custo e ocupação. Verificar arquitetura do feixe e técnica de remoção do esmalte e terminação. Não presumir que o interior do feixe foi conectado porque a parte externa aceitou solda.

### 11.3 Resistência CC e perdas

`Rdc(T) = ρ20 [1 + α(T−20)] ℓ/Acu`

Para cobre, ρ20≈0,01724 Ω·mm²/m e α≈0,00393/°C. O comprimento ℓ inclui todas as espiras, terminais e acréscimos de torção. Use MLT por camada, pois as externas são mais longas.

`Pcu,DC = Ip,rms² RPdc + Is,rms² RSdc`

Para perdas AC, decompor as curvas:

`Pcu = Idc² Rdc + soma[IH,rms² Rac(Hf)]`

Somar ambos os enrolamentos e incluir proximidade e campo do gap. Um multiplicador Rac/Rdc usado para estudar sensibilidade deve ser identificado como hipótese, não resultado de medição.

## 12. Desenhar as camadas e conferir a janela

Escolha a disposição antes de fechar os fios. Para baixa dispersão, uma alternativa é P/2–S–P/2. Há mais interfaces e capacitância parasita, e o isolamento fica mais trabalhoso. P e S separados em setores facilitam algumas barreiras, porém tendem a elevar a dispersão.

O desenho deve identificar, em sequência radial:

1. Carretel e isolamento inicial.
2. Primeira seção de P, com Np/2 espiras.
3. Barreira P/S.
4. Enrolamento S completo.
5. Barreira S/P.
6. Segunda seção de P, com Np/2 espiras.
7. Isolamento externo e fixação.

As duas seções de P são ligadas em série aditiva. Não ligá-las em paralelo mantendo a conta original de Np.

### 12.1 Espiras por camada

Meça o feixe real sob tensão leve. Para feixe aproximadamente retangular de largura axial w e altura radial h, e largura útil bu:

`Espiras_por_camada = piso(bu/w)`

`Camadas = teto(N/Espiras_por_camada)`

Some alturas de todas as seções, fitas, barreiras e folgas. A soma deve ser menor que a altura radial disponível. Também confira espaço para cruzamentos e saídas, que não aparecem na conta simples de área.

A largura útil exclui margens de isolação e limites do flange. Não force cobre dentro da janela e não esmague esmalte para recuperar uma conta apertada.

### 12.2 Fator de execução da aula

O material metodológico define:

`Aw_min = Np mP Aexterna_fioP + Ns mS Aexterna_fioS`

`FE = Aw_min/Aw`

O critério didático recomenda revisar quando FE>0,9. Mesmo um valor menor não comprova que o conjunto cabe, pois a soma de áreas circulares não inclui todos os vazios e obstáculos.

Faça também uma análise geométrica:

`Aw_ocupada ≈ Aw_min/fator_empacotamento + Aw_isolamentos_e_margens`

Não confundir FE, que usa área externa de fio, com ku, que expressa fração de cobre nu. Um ku conservador pode reprovar a triagem AeAw; só substituí-lo por um maior depois de comprovar o arranjo real, e não para fazer a conta passar.

## 13. Especificar dispersão, capacitância e isolamento

A meta na referência P é:

`Lk_objetivo <= 0,05 × 209 = 10,45 µH`

`Lk_maximo <= 0,10 × 209 = 20,9 µH`

Para n=2/3, referidas ao secundário:

`LkS = n² LkP`

Logo, os mesmos limites equivalem aproximadamente a 4,644 µH e 9,289 µH no S. Não comparar uma medição de S com 10,45 µH sem converter.

Sobreposição axial e intercalamento tendem a reduzir dispersão. Barreiras mais espessas e seções afastadas tendem a aumentá-la. Interfaces muito próximas aumentam capacitância e correntes de modo comum. O isolamento necessário nunca deve ser removido apenas para reduzir Lk.

A tensão entre enrolamentos pode ter componente de modo comum e picos de chaveamento superiores à simples relação de espiras. Defina o sistema de isolação com as tensões reais, categoria de uso, poluição, altitude e norma aplicável. Duas voltas arbitrárias de fita ou o esmalte dos filamentos não demonstram, sozinhos, isolação apropriada para um conversor com barramento de 340 Vcc.

Uma estimativa numérica de Lk requer dimensões e distribuição das camadas. Sem elas, registrar “meta a medir”, não um número supostamente calculado.

## 14. Calcular perdas de núcleo e temperatura

`Ptotal = Pcu + Pcore`

`Pcore = Pv × Ve`

Pv deve ser obtido de dados ou modelo válidos para material, forma de B, frequência, temperatura e polarização. Curvas senoidais são ponto de partida; o fluxo do conversor pode ser triangular e assimétrico com componente CC.

Não confundir Bpk total com a amplitude AC usada numa curva senoidal. Por exemplo, ΔB de 84,9 mT corresponde a uma amplitude em torno do centro da excursão de cerca de 42,4 mT, embora o fluxo total possa atingir aproximadamente 0,19 T devido à polarização.

Com parâmetros válidos de Steinmetz/iGSE e a forma de B(t), calcular as perdas respeitando a faixa de validade. Se não houver dados suficientes, a perda de ferrite fica pendente. Não inventar um valor de W/cm³ apenas para completar uma tabela.

A estimativa térmica inicial pode usar:

`Tquente ≈ Tamb + Ptotal Rθ`

Rθ depende de geometria, fixação, circulação de ar e gabinete. Sem Rθ medido/justificado não há temperatura final confiável. Para melhorar a análise, separar cobre e núcleo em dois nós térmicos e confirmar os pontos quentes por ensaio.

A temperatura da resistência do cobre pode ser estimada por:

`T ≈ 20 + [(Rquente/R20)−1]/0,00393`

Essa é uma temperatura média do enrolamento. Termopares externos e resistência média podem não revelar o ponto quente interno.

## 15. Comparar 50 kHz e 100 kHz de maneira justa

A comparação deve usar a mesma potência, tensões, carregamento dos polos, ambiente, ventilação e limites de temperatura. Se uma opção muda núcleo, fios ou Lm, registrar essas mudanças em vez de atribuir todo o resultado à frequência.

| Aspecto | O que verificar ao passar de 50 para 100 kHz |
|---|---|
| Ondulação | Pode diminuir se os volt-segundos por ciclo diminuírem, mas precisa de simulação |
| Energia e Bdc | Não desaparecem com a frequência; dependem de Lm e corrente |
| Núcleo | Perda depende de f e da excursão, sem regra universal de dobrar |
| Cobre | Proximidade e harmônicos podem aumentar a exigência de filamentos/transposição |
| Dispersão e capacitância | A construção e os transitórios precisam ser medidos |
| Semicondutores | Perdas de comutação também mudam e afetam eficiência total |
| Construção | Feixes mais finos podem exigir mais trabalho e esmalte |
| Volume | Redução só é real se fluxo, energia, janela e calor continuarem aprovados |

Se, em um estudo estritamente condicional, f dobra e a amplitude AC de B cai pela metade, uma lei de Steinmetz `Pv proporcional a f^α Bac^β` daria razão de perda `2^(α−β)`. Sem parâmetros reais não existe resultado quantitativo. A expressão explica por que maior frequência não significa automaticamente maior ou menor perda de ferrite.

A 50 kHz há dados numéricos verificáveis neste trabalho. Isso justifica começar a validação experimental por esse ponto. Não demonstra que seja a solução de maior eficiência depois de fechar o projeto B.

## 16. Construir os dois componentes: sequência de laboratório

A fabricação nominal começa depois que a ficha estiver completa e as margens aprovadas. Antes disso, uma bobina de prova desenergizada pode validar o espaço e o acoplamento.

1. Separar dois conjuntos completos de ferrite e dois carretéis. Inspecionar trincas, faces, flanges e pinos; rejeitar peças danificadas.
2. Montar a seco, medir a janela e conferir folgas. Garantir que carretel e fixação correspondem ao código real do núcleo.
3. Preparar contador de espiras, guia, micrômetro, espaçadores, fitas, mangas e etiquetas. Definir um lado fixo de observação para registrar o sentido de giro.
4. Fazer um feixe amostral com a bitola e quantidade calculadas. Medir largura/altura e revisar camadas antes de cortar todo o material.
5. Calcular comprimento de cada seção com seu MLT e terminais. Acrescentar margem documentada de manuseio e transposição.
6. Cortar filamentos com comprimentos semelhantes. Identificar P1, S e P2, e seus inícios/fins. Não misturar diâmetros ou classes de esmalte.
7. Organizar e transpor os filamentos. Usar tensão moderada para não esticar o cobre nem romper o esmalte.
8. Aplicar isolamento inicial e margens previstos no desenho. Inspecionar cantos e rebarbas do carretel.
9. Enrolar a primeira seção P com a contagem aprovada. Contar voltas completas ao redor da coluna, não filamentos. Fotografar e registrar a contagem.
10. Organizar terminais sem cruzar a zona de gap ou reduzir as distâncias de isolação. Aplicar isolamento entre camadas quando previsto.
11. Aplicar a barreira entre P e S, com espessuras e margens definidas. Confirmar a altura radial disponível.
12. Enrolar S com número de espiras e camadas da ficha. Marcar início/fim imediatamente.
13. Aplicar a segunda barreira e enrolar P2. Preparar a ligação em série aditiva sem fechar permanentemente antes do teste.
14. Remover esmalte com processo adequado ao fio. Inspecionar e conectar todos os filamentos; um fio não ligado continua ocupando espaço sem conduzir corrente útil.
15. Fazer continuidade e resistência preliminares. Conferir que não há ligação indevida entre enrolamentos ou núcleo.
16. Montar ferrite com gap provisório calculado e pressão repetível. Preferir montagem reversível durante o ajuste.
17. Verificar polaridade, indutâncias próprias, mútua, dispersão e relação de espiras com os ensaios a seguir.
18. Ajustar gap em passos pequenos, registrando AL e as condições de medição. Separar Lm de dispersão antes de ajustar o alvo de 209 µH.
19. Corrigir problemas de dispersão pela geometria aprovada; não remover isolamento necessário. Se não couber ou aquecer, reprojetar.
20. Aplicar fixação final sem criar espira condutora fechada ao redor do fluxo. Repetir medições depois de apertar ou curar o fixador.
21. Fazer ensaios de isolação, polarização e temperatura antes de aplicar potência nominal.
22. Repetir integralmente para a segunda unidade e comparar as medições. As especificações são iguais; as conexões no conversor devem seguir os pontos específicos de cada ramo.

## 17. Medir com o LCR

### 17.1 Preparação e condições

O componente deve estar desconectado e sem tensão. Capacitores do conversor devem estar descarregados e a ausência de tensão confirmada. Não conectar LCR a circuito energizado.

Compensar aberto e curto com os próprios cabos de medição. Preferir conexão de quatro terminais. Registrar frequência, amplitude de excitação, modo série/paralelo e temperatura. Repetir em frequências disponíveis e abaixo da ressonância própria.

Uma excitação de baixa frequência e alta tensão pode saturar até durante um ensaio de bancada. Para seno, conferir `Bpk ≈ Vrms/(4,442 f N Ae)`. Começar com amplitude pequena.

### 17.2 Indutâncias próprias e magnetizante

Com S aberto, medir Lp; com P aberto, medir Ls. Esses valores são indutâncias próprias. No modelo com dispersão primária em série, `Lp,aberto = Lm + LσP`. Portanto, ajustar cegamente a leitura aberta para 209 µH pode deixar Lm abaixo do alvo.

O LCR mede pequeno sinal em torno da corrente de polarização do ensaio, geralmente perto de zero. A indutância incremental no ponto de operação é `Linc=dλ/di`; a secante é `Lsec=λ/i`. Elas diferem num material não linear. A leitura de 209 µH a vazio não comprova 209 µH entre 4 e 8 A.

### 17.3 Mútua e coeficiente de acoplamento

Ligar P e S em série e medir uma associação; inverter S e medir a outra. A maior leitura é L+ e a menor é L−:

`L+ = Lp + Ls + 2M`

`L− = Lp + Ls − 2M`

`M = (L+ − L−)/4`

`k = M/raiz(Lp Ls)`

O teste também identifica ligação aditiva e polaridades. Se k resultar maior que 1, investigar compensação, frequência, contatos e modelo; não simplesmente limitar o número a 1.

### 17.4 Dispersão

Curto-circuitar S com uma ligação curta e de impedância baixa; medir no P. No modelo de dois indutores acoplados e curto ideal:

`Lsc,P = Lp − M²/Ls = Lp(1−k²)`

A medida é uma dispersão equivalente vista da entrada. Sua relação com os blocos Lk e Lm do PSIM depende de como o modelo os distribui. Repetir trocando os lados e converter para uma referência comum.

A aproximação `Lsc,P ≈ LσP + LσS/n²` é útil quando Lm é muito maior que as dispersões e as parasitas não dominam. A resistência/indutância do fio de curto pode distorcer a leitura; compensar e documentar.

### 17.5 Relação de espiras e resistência

`raiz(Ls/Lp)` aproxima Ns/Np quando a dispersão é pequena. Uma verificação com gerador isolado de baixa tensão e medição da relação de tensões fornece confirmação adicional.

Para DCR, usar a função apropriada do instrumento ou método Kelvin com fonte limitada e voltímetro. O parâmetro Rs em alta frequência inclui perdas e não é automaticamente a resistência CC. Usar corrente pequena para evitar aquecimento durante a medição.

## 18. Ensaios que exigem instrumentação complementar

### 18.1 Polarização e saturação

Um LCR comum sozinho não verifica saturação sob corrente nominal. São necessários fonte limitada, circuito de pulsos, chave, caminho seguro de desmagnetização, medição de corrente e tensão e proteção independente.

Com o componente fora do conversor, iniciar com pulsos curtos e baixa energia. Medir v(t) e i(t); descontar a queda Ri e calcular `Linc≈(v−Ri)/(di/dt)`. Aceleração acentuada de di/dt indica redução da indutância. Garantir reset entre pulsos e aumentar a corrente progressivamente até o envelope especificado. Repetir na temperatura relevante.

Não ligar uma fonte CC diretamente ao enrolamento sem limitação e proteção. Não aplicar polarização CC à porta do LCR sem uma interface expressamente compatível. O circuito de ensaio requer projeto de comutação e supressão próprio.

### 18.2 Isolação

Verificar visualmente o sistema de barreiras, continuidade indevida e resistência de isolação com equipamento adequado. Hipot, tensão e tempo devem seguir a norma e o tipo de isolamento definidos; os 340 Vcc não bastam para escolher um valor de ensaio.

Desconectar eletrônica sensível, usar barreiras, descarga controlada e operador habilitado. Nunca assumir que uma peça passou em isolação somente porque o multímetro indicou circuito aberto.

### 18.3 Temperatura e potência

Monitorar núcleo, cobre, terminais, ambiente e ventilação. Iniciar com tensão/potência reduzidas e limitação de corrente; verificar polaridade, equilíbrio e sobretensões antes de aumentar a carga.

Um roteiro de patamares pode usar 10%, 25%, 50%, 75% e 100%, desde que cada estágio seja estável e aprovado. Esperar equilíbrio térmico ou caracterizar a constante térmica. Um critério de estudo é variação inferior a 1 °C em 10 minutos, confirmando que o tempo de ensaio cobriu a dinâmica relevante.

Os limites de temperatura e interrupção devem estar definidos antes do ensaio. Um teste pulsado de saturação não demonstra capacidade térmica contínua; um teste térmico em corrente pequena não demonstra margem de saturação.

O barramento de 340 Vcc e a energia dos capacitores exigem fusível, desligamento, descarga, confirmação de ausência de tensão, barreiras e supervisão de laboratório. Use medição diferencial/isolada apropriada; não aterre a garra de um osciloscópio comum em um nó flutuante de chaveamento.

## 19. Documentar a liberação e a lista de materiais

A ficha final deve conter o desenho com terminais/pontos, núcleo e material completos, Np/Ns, bitolas e número de filamentos, camadas, sistema de isolação, gap medido, método de fixação e tolerâncias. Anexe as curvas de corrente/tensão que justificam o projeto.

Para duas unidades, a lista começa com quatro metades de ferrite compatíveis, dois carretéis, duas fixações, dois jogos de espaçadores e quatro enrolamentos. Intercalamento acrescenta seções e emendas, não aumenta a quantidade de componentes magnéticos.

A metragem de fio é calculada por filamento, não apenas pelo comprimento de uma bobina:

`Metros_totais = 2 × [mP ℓP + mS ℓS]`

Acrescentar a reserva de manuseio indicada no desenho. Os materiais de isolamento devem ter códigos e classes adequados, não apenas a descrição genérica “fita”.

Antes da liberação nominal, confirmar que:

- Todos os valores usados têm origem rastreável e as pendências críticas foram resolvidas.
- O fluxo no pior caso atende o limite quente e as tolerâncias.
- O cobre físico foi dimensionado pelos RMS reais e a janela foi comprovada.
- Lm, dispersão, polaridade e resistência foram medidos no modelo correto.
- O componente passou nos ensaios de polarização, isolação e temperatura aplicáveis.
- As duas unidades foram verificadas individualmente e atendem ao pareamento definido pelo circuito.

## 20. Como usar o exemplo e os arquivos de cálculo

O projeto de exemplo que acompanha este guia demonstra a sequência com números e hipóteses declaradas. Ele não substitui dados ausentes de estoque ou simulação. Ao adaptar o exemplo, altere os parâmetros e refaça todas as verificações, especialmente as que dependem de correntes e geometria.

O código `calculo.py` reproduz a análise de correntes de 50 kHz e o exemplo paramétrico. O arquivo JSON expõe os parâmetros, e as saídas incluem resumo CSV e gráfico SVG. O campo de frequência usado para selecionar a janela de análise não transforma o arquivo de 50 kHz em uma simulação de 100 kHz.

Referências utilizadas: `PROJETO_INDUTOR.pdf`, particularmente a formulação AeAw, espiras e fator de execução; `McLyman.pdf`, como referência de fundamentos; e `CorrenteIndutor.txt`, para resultados numéricos. O segundo PDF e a planilha não estavam disponíveis nesta edição, e os datasheets oficiais permanecem pendentes de acesso ou envio.

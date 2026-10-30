# 📊 Analytics de Cobrança: Teste A/B de Recuperação de Crédito

Projeto de análise de dados em **Python e SQL** que simula o ciclo completo de uma análise de *collections* em uma fintech: extração de dados, cálculo de KPIs, validação estatística de um experimento e geração de relatório executivo com recomendações para produto e liderança.

**Pergunta de negócio:** uma abordagem de cobrança via **WhatsApp com 10% de desconto** recupera mais crédito do que o **SMS padrão**, mesmo abrindo mão de parte do valor da dívida?

> ℹ️ Os dados são **simulados** (1.000 clientes inadimplentes, com `seed` fixa para os resultados serem reproduzíveis). O foco do projeto é o método de análise, não os números em si.

---

## 🎯 Principais resultados

| Indicador | Controle (SMS) | Teste (WhatsApp + desconto) |
|---|---|---|
| Clientes | 490 | 510 |
| Clientes que pagaram | 89 | 121 |
| **Taxa de recuperação** | **18,16%** | **23,73%** |
| Valor recuperado | R$ 259.421,77 | R$ 272.402,40 |
| Eficiência financeira (recuperado / dívida) | 19,47% | 21,28% |

- O grupo teste teve **+5,56 pontos percentuais** na taxa de recuperação.
- Teste qui-quadrado: **χ² = 4,33** e **p-valor = 0,037**. Como p < 0,05, a diferença é estatisticamente significativa ao nível de 5%.
- Mesmo concedendo 10% de desconto, o grupo teste recuperou **mais dinheiro em valor absoluto** e teve **eficiência financeira maior** (21,28% contra 19,47%). Ou seja, o ganho em conversão compensou o desconto.

**Recomendação:** ampliar a estratégia de WhatsApp com desconto de forma gradual, mantendo um grupo controle e monitorando os KPIs no painel.

---

## 🔄 Etapas da análise

1. **Extração de dados (SQL):** criação da base de clientes inadimplentes no SQLite e consulta agregada por grupo do experimento.
2. **KPIs:** cálculo de taxa de recuperação, eficiência financeira e ticket médio da dívida, geral e por grupo, com exportação para uma planilha Excel pronta para o Google Sheets.
3. **Teste A/B:** tabela de contingência (grupo x pagou) e teste qui-quadrado de independência com SciPy, usando nível de significância de 5%.
4. **Relatório executivo:** geração automática de um relatório em Markdown com resultados, validação estatística e recomendações para o roadmap.

---

## 📂 Estrutura do projeto

```text
analyst-data/
├── extracao_sqlite.py         # 1. Cria a base simulada e extrai dados via SQL
├── kpis.py                    # 2. Calcula os KPIs e exporta a planilha
├── teste.py                   # 3. Teste A/B com qui-quadrado e p-valor
├── relatorio.py               # 4. Gera o relatório executivo em Markdown
├── dados_cobranca.db          # Banco de dados SQLite
└── relatorios/
    ├── dashboard_cobranca.xlsx    # KPIs por grupo + amostra dos dados
    └── relatorio_executivo.md     # Relatório para a liderança
```

---

## 🛠️ Tecnologias

- **Python 3**
- **SQL / SQLite3:** armazenamento e consultas agregadas
- **Pandas e NumPy:** manipulação de dados e simulação
- **SciPy:** teste estatístico (`chi2_contingency`)
- **OpenPyXL:** exportação para Excel

---

## ▶️ Como executar

```bash
pip install pandas numpy scipy openpyxl

python extracao_sqlite.py
python kpis.py
python teste.py
python relatorio.py
```

Os arquivos de saída ficam na pasta `relatorios/`.

---

## 🚀 Próximos passos

- Segmentar os resultados por **faixa de dias de atraso** (30-60 e 60-90 dias) para entender em qual perfil o desconto funciona melhor.
- Testar **diferentes níveis de desconto** para encontrar o ponto que maximiza o valor recuperado.
- Calcular o **tamanho de amostra** necessário antes de rodar o experimento.
- Levar os KPIs para um **dashboard no Power BI ou Looker Studio** com atualização automática.

---

👩‍💻 Desenvolvido por **Elizandra Krier** · [LinkedIn](https://www.linkedin.com/in/elizandra-reis-pereira-krier-467854131/) · [GitHub](https://github.com/Elizandrakrier)
# 📊 Analyst Data: Estratégia de Cobrança & Teste A/B

Pipeline analítico desenvolvido em Python e SQL para simular e avaliar o impacto de novas estratégias de recuperação de crédito (*collections*) em uma fintech. O projeto cobre o ciclo completo de análise: extração de dados, cálculo de KPIs operacionais, validação estatística de experimentos e geração de relatórios executivos para tomada de decisão.

---

## 📂 Estrutura do Projeto

```text
analyst data/
│
├── relatorios/
│   ├── dashboard_cobranca.xlsx    # Relatório de KPIs (pronto para o Google Sheets)
│   └── relatorio_executivo.md     # Relatório executivo estruturado para liderança
│
├── dados_cobranca.db              # Banco de dados SQLite local
├── etapa1_extracao.py             # Criação da base e extração via SQL
├── etapa2_kpis.py                 # Cálculo de indicadores e exportação de planilha
├── etapa3_teste_ab.py             # Teste A/B e estatística aplicada (Qui-Quadrado / p-value)
└── etapa4_relatorio.py            # Automação do relatório executivo em Markdown

Tecnologias Utilizadas
Linguagem: Python 3

Manipulação & Análise: Pandas, NumPy

Banco de Dados / SQL: SQLite3

Estatística: SciPy (chi2_contingency)

Exportação: OpenPyXL

Como Executar o Projeto
Certifique-se de ter as bibliotecas instaladas no seu ambiente:

pip install pandas scipy openpyxl numpy

esumo das Etapas
Extração de Dados (SQL): Criação de tabela simulada de inadimplentes e consultas agregadas direto no banco SQLite.

Dashboards & KPIs: Mensuração de indicadores críticos como Taxa de Recuperação, Eficiência Financeira e Ticket Médio, com exportação automatizada para .xlsx.

Testes A/B & Estatística: Aplicação de teste de hipóteses para comparar o grupo controle (SMS) com o grupo teste (WhatsApp + Desconto), garantindo significância estatística (p-value).

Visão de Negócio: Tradução dos dados em recomendações estratégicas e acionáveis para o roadmap de produto e liderança.


---

### 💡 Como salvar:
1. No VS Code, crie um novo arquivo na raiz da pasta `analyst data` chamado exatamente **`README.md`**.
2. Cole o texto acima nele e salve (`Ctrl + S` ou `Cmd + S`). 
3. Se quiser visualizar como ficou, clique no ícone de preview no canto superior direito do VS Code!
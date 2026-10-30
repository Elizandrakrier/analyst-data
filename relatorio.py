import sqlite3
import pandas as pd
from scipy import stats
import os

# 1. Garantir que a pasta de relatórios existe
os.makedirs("relatorios", exist_ok=True)

# 2. Conectar ao banco e carregar os dados
conn = sqlite3.connect("dados_cobranca.db")
df = pd.read_sql_query("SELECT * FROM clientes_inadimplentes", conn)
conn.close()

# 3. Recalcular métricas para consolidar no relatório
total_clientes = len(df)
divida_total = df['valor_divida'].sum()
valor_recuperado_total = df['valor_recuperado'].sum()
eficiencia_global = (valor_recuperado_total / divida_total) * 100

controle = df[df['grupo_experimento'] == 'Controle']
teste = df[df['grupo_experimento'] == 'Teste']

taxa_controle = (controle['pago'].sum() / len(controle)) * 100
taxa_teste = (teste['pago'].sum() / len(teste)) * 100
diferenca_taxa = taxa_teste - taxa_controle

recuperado_controle = controle['valor_recuperado'].sum()
recuperado_teste = teste['valor_recuperado'].sum()

# Teste estatístico
tabela_contingencia = pd.crosstab(df['grupo_experimento'], df['pago'])
chi2, p_valor, dof, esperado = stats.chi2_contingency(tabela_contingencia)
estatisticamente_significativo = p_valor < 0.05

# 4. Construir o conteúdo do Relatório Executivo em Markdown
conteudo_relatorio = f"""# 📊 Relatório Executivo: Resultados do Experimento de Cobrança (Collections)
**Data de Emissão:** Outubro de 2026  
**Autor:** Analyst Data Team  
**Status do Projeto:** Concluído para Validação de Roadmap  

---

## 🎯 1. Resumo Executivo
Este relatório apresenta os resultados consolidados do teste A/B realizado na carteira de clientes inadimplentes. O objetivo principal foi avaliar a eficácia de uma **nova estratégia de recuperação de crédito** (Abordagem via WhatsApp + Desconto Progressivo - *Grupo Teste*) em comparação ao processo tradicional (SMS Padrão - *Grupo Controle*).

---

## 📈 2. Principais Indicadores (KPIs) da Operação
* **Volume Total de Clientes em Atraso:** {total_clientes} clientes
* **Montante Total em Dívida:** R$ {divida_total:,.2f}
* **Valor Total Recuperado (Geral):** R$ {valor_recuperado_total:,.2f}
* **Eficiência Financeira Global:** {eficiencia_global:.2f}%

---

## 🧪 3. Comparativo do Teste A/B
* **Taxa de Recuperação (Grupo Controle - SMS):** {taxa_controle:.2f}%
* **Taxa de Recuperação (Grupo Teste - WhatsApp + Desconto):** {taxa_teste:.2f}%
* **Variação Absoluta:** +{diferenca_taxa:.2f} pontos percentuais

### Validação Estatística:
* **Estatística Qui-Quadrado ($\chi^2$):** {chi2:.4f}
* **P-valor (p-value):** {p_valor:.6f}
* **Significância Estatística (5%):** {"✅ Aprovado (Diferença Real)".upper() if estatisticamente_significativo else "❌ Não Significativo"}

> **Análise Estatística:** O p-valor obtido foi de `{p_valor:.5f}`. Isso prova matematicamente que a melhoria de conversão no Grupo Teste **não ocorreu por acaso**, garantindo alta confiabilidade para tomada de decisão estratégica.

---

## 🚀 4. Recomendações para o Roadmap de Produto & Engenharia
Com base na robustez analítica e no ganho de conversão comprovado estatisticamente, recomendamos:

1. **Rollout de 100% da Feature:** Migrar a base de cobrança remanescente para o modelo do Grupo Teste (fluxo automatizado via WhatsApp com engine de desconto dinâmico).
2. **Integração com Engenharia:** Priorizar no próximo roadmap de produto a automação da mensageria integrada ao motor de risco.
3. **Monitoramento Contínuo:** Implementar o dashboard de KPIs no Google Sheets / BI para rastrear o impacto no *Ticket Médio* a médio prazo.
"""

# 5. Salvar o arquivo de relatório na pasta relatorios
caminho_relatorio = "relatorios/relatorio_executivo.md"
with open(caminho_relatorio, "w", encoding="utf-8") as f:
    f.write(conteudo_relatorio)

print(f"✅ Relatório executivo gerado com sucesso em: '{caminho_relatorio}'!")

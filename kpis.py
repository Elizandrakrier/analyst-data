import sqlite3
import pandas as pd
import os

# 1. Garantir que a pasta de relatórios existe
os.makedirs("relatorios", exist_ok=True)

# 2. Conectar ao banco de dados criado na Etapa 1
conn = sqlite3.connect("dados_cobranca.db")

# 3. Carregar todos os dados da tabela para um DataFrame do pandas
df = pd.read_sql_query("SELECT * FROM clientes_inadimplentes", conn)
conn.close()

print("--- 📈 CALCULANDO KPIs DE COBRANÇA ---")

# 4. Cálculo de Indicadores Globais (KPIs)
total_clientes = len(df)
clientes_pagadores = df['pago'].sum()
taxa_recuperacao_geral = (clientes_pagadores / total_clientes) * 100

divida_total = df['valor_divida'].sum()
valor_recuperado_total = df['valor_recuperado'].sum()
eficiencia_financeira = (valor_recuperado_total / divida_total) * 100

ticket_medio_divida = df['valor_divida'].mean()

print(f"Total de Clientes em Atraso: {total_clientes}")
print(
    f"Taxa de Recuperação Geral (Volume de Clientes): {taxa_recuperacao_geral:.2f}%")
print(
    f"Eficiência Financeira (Valor Recuperado / Dívida Total): {eficiencia_financeira:.2f}%")
print(f"Ticket Médio da Dívida: R$ {ticket_medio_divida:.2f}\n")

# 5. Cálculo de KPIs por Grupo de Experimento (Controle vs Teste)
df_kpis_grupo = df.groupby('grupo_experimento').agg(
    total_clientes=('pago', 'count'),
    clientes_pagadores=('pago', 'sum'),
    divida_total=('valor_divida', 'sum'),
    valor_recuperado=('valor_recuperado', 'sum')
).reset_index()

# Calculando taxas derivadas por grupo
df_kpis_grupo['taxa_conversao_%'] = (
    df_kpis_grupo['clientes_pagadores'] / df_kpis_grupo['total_clientes']) * 100
df_kpis_grupo['eficiencia_recuperacao_%'] = (
    df_kpis_grupo['valor_recuperado'] / df_kpis_grupo['divida_total']) * 100

print("--- 📊 KPIs POR GRUPO DE COBRANÇA ---")
print(df_kpis_grupo.to_string(index=False))

# 6. Exportando para Excel (Simulando o Dashboard que iria para o Google Sheets)
caminho_excel = "relatorios/dashboard_cobranca.xlsx"

# Salvando múltiplas abas na planilha
with pd.ExcelWriter(caminho_excel, engine='openpyxl') as writer:
    df_kpis_grupo.to_excel(writer, sheet_name='KPIs por Grupo', index=False)
    df.head(100).to_excel(
        writer, sheet_name='Amostra de Dados Brutos', index=False)

print(f"\n✅ Relatório de KPIs exportado com sucesso para: '{caminho_excel}'!")

import sqlite3
import pandas as pd
import numpy as np

# Conectar/Criar SQLite local
conn = sqlite3.connect("dados_cobranca.db")
cursor = conn.cursor()

# Tabela de clientes inadimplentes
cursor.execute('''
CREATE TABLE IF NOT EXISTS clientes_inadimplentes (
    id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
    dias_atraso INTEGER,
    valor_divida REAL,
    grupo_experimento TEXT, -- 'Controle' (SMS) ou 'Teste' (WhatsApp + Desconto)
    pago INTEGER,          -- 1 se pagou, 0 se não pagou
    valor_recuperado REAL
)
''')

# Dados simulados
np.random.seed(42)  # Para manter consistência nos resultados
total_clientes = 1000

# Metade para Grupo Controle (SMS) e metade para Grupo Teste (WhatsApp + Desconto)
grupos = np.random.choice(['Controle', 'Teste'], size=total_clientes)
dias_atraso = np.random.randint(30, 90, size=total_clientes)
valores_divida = np.round(np.random.uniform(
    200.0, 5000.0, size=total_clientes), 2)

# Simulação das respostas (Grupo Teste terá uma taxa de recuperação levemente maior)
pagos = []
valores_recuperados = []

for i in range(total_clientes):
    # Probabilidade base de pagamento
    prob_pagamento = 0.18 if grupos[i] == 'Controle' else 0.26

    # Simula se o cliente pagou
    pagou = np.random.choice([1, 0], p=[prob_pagamento, 1 - prob_pagamento])
    pagos.append(pagou)

    # Se pagou, calcula o valor recuperado
    if pagou == 1:
        # Se for teste, considerou um pequeno desconto de 10%
        fator_recuperacao = 0.90 if grupos[i] == 'Teste' else 1.0
        valores_recuperados.append(
            round(valores_divida[i] * fator_recuperacao, 2))
    else:
        valores_recuperados.append(0.0)

# Montar DataFrame inicial
df_simulado = pd.DataFrame({
    'dias_atraso': dias_atraso,
    'valor_divida': valores_divida,
    'grupo_experimento': grupos,
    'pago': pagos,
    'valor_recuperado': valores_recuperados
})

# Salvar na tabela do SQLite
df_simulado.to_sql('clientes_inadimplentes', conn,
                   if_exists='replace', index=False)
conn.commit()

print("✅ Banco de dados 'dados_cobranca.db' criado e populado com sucesso com 1.000 registros!\n")

# -------------------------------------------------------------------
# 4. PRÁTICA SQL: Extrair os dados utilizando Query SQL pura
# -------------------------------------------------------------------
query_sql = """
SELECT 
    grupo_experimento,
    COUNT(id_cliente) AS total_clientes,
    SUM(pago) AS total_pagadores,
    ROUND(SUM(valor_divida), 2) AS divida_total,
    ROUND(SUM(valor_recuperado), 2) AS total_recuperado
FROM clientes_inadimplentes
GROUP BY grupo_experimento;
"""

# Executando a consulta e carregando direto em um DataFrame
df_resumo_sql = pd.read_sql_query(query_sql, conn)

print("📊 RESUMO EXTRAÍDO VIA QUERY SQL:")
print(df_resumo_sql)

# Fechar conexão
conn.close()

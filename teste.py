import sqlite3
import pandas as pd
from scipy import stats

# 1. Conectar ao banco de dados e carregar os dados
conn = sqlite3.connect("dados_cobranca.db")
df = pd.read_sql_query("SELECT * FROM clientes_inadimplentes", conn)
conn.close()

print("--- 🧪 ANÁLISE DE EXPERIMENTO: TESTE A/B ---")

# 2. Separar os dados por grupo de experimento
controle = df[df['grupo_experimento'] == 'Controle']
teste = df[df['grupo_experimento'] == 'Teste']

# 3. Calcular métricas básicas de conversão
taxa_controle = (controle['pago'].sum() / len(controle)) * 100
taxa_teste = (teste['pago'].sum() / len(teste)) * 100

print(f"Taxa de Recuperação - Grupo Controle (SMS): {taxa_controle:.2f}%")
print(
    f"Taxa de Recuperação - Grupo Teste (WhatsApp + Desconto): {taxa_teste:.2f}%")
diferenca = taxa_teste - taxa_controle
print(
    f"Diferença absoluta de conversão: +{diferenca:.2f} pontos percentuais\n")

# 4. Estatística Aplicada: Teste Qui-Quadrado de Independência
# Montamos uma tabela cruzada (contingência) entre o grupo e se o cliente pagou ou não
tabela_contingencia = pd.crosstab(df['grupo_experimento'], df['pago'])

print("Tabela de Contingência (Cruzada):")
print(tabela_contingencia)
print("-" * 40)

# Aplicando o teste estatístico via SciPy
chi2, p_valor, dof, esperado = stats.chi2_contingency(tabela_contingencia)

print(f"Estatística Chi2: {chi2:.4f}")
print(f"P-valor (p-value): {p_valor:.6f}\n")

# 5. Avaliação do Teste (Nível de significância alpha de 5% ou 0.05)
nivel_significancia = 0.05

print("--- 📋 CONCLUSÃO DO TESTE A/B ---")
if p_valor < nivel_significancia:
    print("✅ RESULTADO ESTATISTICAMENTE SIGNIFICATIVO!")
    print(
        f"   Como o p-valor ({p_valor:.6f}) é menor que 0.05, rejeitamos a hipótese nula.")
    print("   Isso significa que a nova estratégia do Grupo Teste teve um desempenho real superior,")
    print("   e a chance de isso ter ocorrido por acaso é menor que 5%.")
else:
    print("❌ RESULTADO NÃO SIGNIFICATIVO.")
    print(f"   O p-valor ({p_valor:.6f}) é maior ou igual a 0.05.")
    print("   Não temos evidências estatísticas suficientes para afirmar que o Grupo Teste é melhor.")

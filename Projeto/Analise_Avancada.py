from Criar_Metricas import criar_metricas_google_ads
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def mostrar_metricas_detalhadas(df):
    """Mostra métricas detalhadas no terminal"""
    print("📊 MÉTRICAS DETALHADAS - GOOGLE ADS")
    print("=" * 60)
    
    # Métricas Gerais
    print("\n🎯 MÉTRICAS GERAIS:")
    print(f"   • Período analisado: {df['date'].min().date()} a {df['date'].max().date()}")
    print(f"   • Total de dias: {len(df)}")
    print(f"   • Total de campanhas: {df['campaign_name'].nunique()}")
    
    print(f"\n💰 INVESTIMENTO E RETORNO:")
    print(f"   • Total investido: R$ {df['cost'].sum():,.2f}")
    print(f"   • Valor total de conversões: R$ {df['conversion_value'].sum():,.2f}")
    print(f"   • ROAS médio: {df['roas'].mean():.2f}")
    print(f"   • ROI: {(df['conversion_value'].sum() - df['cost'].sum()) / df['cost'].sum() * 100:.1f}%")
    
    print(f"\n📈 PERFORMANCE DE TRÁFEGO:")
    print(f"   • Impressões totais: {df['impressions'].sum():,}")
    print(f"   • Cliques totais: {df['clicks'].sum():,}")
    print(f"   • CTR médio: {df['ctr'].mean():.2%}")
    print(f"   • CPC médio: R$ {df['avg_cpc'].mean():.2f}")
    
    print(f"\n🔄 CONVERSÕES:")
    print(f"   • Conversões totais: {df['conversions'].sum()}")
    print(f"   • Taxa de conversão média: {df['conversion_rate'].mean():.2%}")
    print(f"   • Custo por conversão (CPA): R$ {df['cpa'].mean():.2f}")
    print(f"   • Valor médio por conversão: R$ {df['conversion_value'].sum() / df['conversions'].sum():.2f}")

def metricas_por_campanha(df):
    """Métricas detalhadas por campanha"""
    print(f"\n🎪 PERFORMANCE POR CAMPANHA:")
    print("-" * 50)
    
    campanhas = df.groupby('campaign_name').agg({
        'cost': ['sum', 'mean'],
        'conversions': ['sum', 'mean'],
        'conversion_value': 'sum',
        'roas': 'mean',
        'ctr': 'mean',
        'conversion_rate': 'mean',
        'cpa': 'mean'
    }).round(3)
    
    # Formatar para melhor visualização
    for campanha in campanhas.index:
        dados = campanhas.loc[campanha]
        print(f"\n📋 {campanha}:")
        print(f"   • Investimento total: R$ {dados[('cost', 'sum')]:.2f}")
        print(f"   • Conversões: {dados[('conversions', 'sum')]:.0f}")
        print(f"   • ROAS: {dados[('roas', 'mean')]:.2f}")
        print(f"   • CTR: {dados[('ctr', 'mean')]:.2%}")
        print(f"   • Taxa de conversão: {dados[('conversion_rate', 'mean')]:.2%}")
        print(f"   • CPA: R$ {dados[('cpa', 'mean')]:.2f}")

def metricas_por_dispositivo(df):
    """Métricas por dispositivo"""
    print(f"\n📱 PERFORMANCE POR DISPOSITIVO:")
    print("-" * 40)
    
    dispositivos = df.groupby('device').agg({
        'impressions': 'sum',
        'clicks': 'sum',
        'cost': 'sum',
        'conversions': 'sum',
        'ctr': 'mean',
        'conversion_rate': 'mean',
        'roas': 'mean'
    }).round(3)
    
    for dispositivo in dispositivos.index:
        dados = dispositivos.loc[dispositivo]
        print(f"\n{dispositivo}:")
        print(f"   • Impressões: {dados['impressions']:,}")
        print(f"   • Cliques: {dados['clicks']:,}")
        print(f"   • CTR: {dados['ctr']:.2%}")
        print(f"   • Conversões: {dados['conversions']:.0f}")
        print(f"   • Taxa de conversão: {dados['conversion_rate']:.2%}")
        print(f"   • ROAS: {dados['roas']:.2f}")

def metricas_por_rede(df):
    """Métricas por rede de anúncios"""
    print(f"\n📡 PERFORMANCE POR REDE:")
    print("-" * 35)
    
    redes = df.groupby('network').agg({
        'impressions': 'sum',
        'clicks': 'sum',
        'cost': 'sum',
        'conversions': 'sum',
        'ctr': 'mean',
        'conversion_rate': 'mean'
    }).round(3)
    
    for rede in redes.index:
        dados = redes.loc[rede]
        print(f"\n{rede}:")
        print(f"   • Impressões: {dados['impressions']:,}")
        print(f"   • Cliques: {dados['clicks']:,}")
        print(f"   • CTR: {dados['ctr']:.2%}")
        print(f"   • Conversões: {dados['conversions']:.0f}")
        print(f"   • Taxa de conversão: {dados['conversion_rate']:.2%}")

def analise_sazonalidade(df):
    """Análise de performance por dia da semana"""
    print(f"\n📅 ANÁLISE DE SAZONALIDADE:")
    print("-" * 35)
    
    df['dia_semana'] = df['date'].dt.day_name()
    dias_ordenados = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    sazonalidade = df.groupby('dia_semana').agg({
        'conversions': 'mean',
        'ctr': 'mean',
        'roas': 'mean',
        'cost': 'mean'
    }).reindex(dias_ordenados).round(3)
    
    for dia in sazonalidade.index:
        dados = sazonalidade.loc[dia]
        print(f"\n{dia}:")
        print(f"   • Conversões médias: {dados['conversions']:.1f}")
        print(f"   • CTR: {dados['ctr']:.2%}")
        print(f"   • ROAS: {dados['roas']:.2f}")
        print(f"   • Custo médio: R$ {dados['cost']:.2f}")

def top_insights(df):
    """Principais insights e recomendações"""
    print(f"\n💡 INSIGHTS E RECOMENDAÇÕES:")
    print("-" * 40)
    
    # Melhor campanha por ROAS
    melhor_campanha = df.groupby('campaign_name')['roas'].mean().idxmax()
    pior_campanha = df.groupby('campaign_name')['roas'].mean().idxmin()
    
    # Melhor dispositivo
    melhor_dispositivo = df.groupby('device')['conversion_rate'].mean().idxmax()
    
    # Melhor rede
    melhor_rede = df.groupby('network')['roas'].mean().idxmax()
    
    # Melhor dia da semana
    df['dia_semana'] = df['date'].dt.day_name()
    melhor_dia = df.groupby('dia_semana')['conversions'].mean().idxmax()
    
    print(f"1. 🏆 MELHOR CAMPANHA: '{melhor_campanha}' (maior ROAS)")
    print(f"2. ⚠️  CAMPANHA A REVISAR: '{pior_campanha}' (menor ROAS)")
    print(f"3. 📱 DISPOSITIVO MAIS EFICIENTE: '{melhor_dispositivo}'")
    print(f"4. 📡 REDE MAIS LUCRATIVA: '{melhor_rede}'")
    print(f"5. 📅 DIA DE MAIOR PERFORMANCE: '{melhor_dia}'")
    print(f"6. 💰 EFICIÊNCIA: {df['conversions'].sum() / df['cost'].sum():.2f} conversões por R$1 investido")

def criar_dashboard_visual(df):
    """Cria visualizações dos dados"""
    print(f"\n📈 GERANDO VISUALIZAÇÕES...")
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # 1. ROAS por campanha
    df.groupby('campaign_name')['roas'].mean().sort_values().plot(
        kind='barh', ax=axes[0,0], color='skyblue'
    )
    axes[0,0].set_title('ROAS Médio por Campanha')
    axes[0,0].set_xlabel('ROAS')
    
    # 2. Conversões por dispositivo
    df.groupby('device')['conversions'].sum().plot(
        kind='pie', ax=axes[0,1], autopct='%1.1f%%', colors=['#ff9999','#66b3ff','#99ff99']
    )
    axes[0,1].set_title('Distribuição de Conversões por Dispositivo')
    
    # 3. Evolução temporal de conversões
    df.groupby('date')['conversions'].sum().plot(ax=axes[1,0], color='green')
    axes[1,0].set_title('Conversões Diárias')
    axes[1,0].set_ylabel('Conversões')
    
    # 4. Correlação entre custo e conversões
    axes[1,1].scatter(df['cost'], df['conversions'], alpha=0.6, color='purple')
    axes[1,1].set_xlabel('Custo (R$)')
    axes[1,1].set_ylabel('Conversões')
    axes[1,1].set_title('Relação: Custo vs Conversões')
    
    plt.tight_layout()
    plt.savefig('dashboard_avancado.png', dpi=300, bbox_inches='tight')
    plt.show()

def main():
    """Função principal"""
    print("🚀 ANÁLISE AVANÇADA - MÉTRICAS GOOGLE ADS")
    print("=" * 50)
    
    # Carregar dados
    df = criar_metricas_google_ads(n_dias=90, data_inicio='2024-01-01')
    
    # Executar análises
    mostrar_metricas_detalhadas(df)
    metricas_por_campanha(df)
    metricas_por_dispositivo(df)
    metricas_por_rede(df)
    analise_sazonalidade(df)
    top_insights(df)
    criar_dashboard_visual(df)
    
    print(f"\n✅ ANÁLISE CONCLUÍDA!")
    print(f"📊 Métricas detalhadas mostradas acima")
    print(f"📁 Dashboard salvo como 'dashboard_avancado.png'")

if __name__ == "__main__":
    main()
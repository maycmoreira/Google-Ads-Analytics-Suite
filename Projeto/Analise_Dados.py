# Análises essenciais e exploratórias
from Criar_Metricas import criar_metricas_google_ads
import pandas as pd

def analise_basica():
    df = criar_metricas_google_ads()
    
    # Estatísticas básicas
    print("📊 Estatísticas Básicas")
    print(f"Total de conversões: {df['conversions'].sum()}")
    
    # Performance por campanha
    performance = df.groupby('campaign_name').agg({
        'cost': 'sum',
        'conversions': 'sum',
        'roas': 'mean'
    })
    
    return df, performance

if __name__ == "__main__":
    df, performance = analise_basica()
    print(performance)
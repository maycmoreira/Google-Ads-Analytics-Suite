from Criar_Metricas import criar_metricas_google_ads
import pandas as pd
import os
from datetime import datetime

def criar_datasets_power_bi():
    """Cria datasets completos otimizados para Power BI"""
    print("🚀 CRIANDO DATASETS PARA POWER BI...")
    
    # Gerar dados
    df = criar_metricas_google_ads(n_dias=180, data_inicio='2024-01-01')
    
    # 🔧 PREPARAR DADOS PARA POWER BI (Modelo Estrela)
    
    # 1. TABELA FATO (Transações diárias)
    print("1. 📈 Criando tabela FATO...")
    fato = df[[
        'date', 'campaign_id', 'ad_group_id', 'device', 'network',
        'impressions', 'clicks', 'cost', 'conversions', 'conversion_value',
        'ctr', 'avg_cpc', 'conversion_rate', 'cpa', 'roas'
    ]].copy()
    
    # Adicionar colunas de tempo para hierarquias no Power BI
    fato['ano'] = fato['date'].dt.year
    fato['mes'] = fato['date'].dt.month
    fato['mes_nome'] = fato['date'].dt.month_name()
    fato['semana'] = fato['date'].dt.isocalendar().week
    fato['dia_semana'] = fato['date'].dt.day_name()
    fato['trimestre'] = fato['date'].dt.quarter
    fato['dia_do_mes'] = fato['date'].dt.day
    
    # Métricas calculadas avançadas
    fato['lucro'] = fato['conversion_value'] - fato['cost']
    fato['margem_lucro'] = (fato['lucro'] / fato['cost']).replace([float('inf'), -float('inf')], 0).fillna(0)
    fato['conversoes_por_1000_impressoes'] = (fato['conversions'] / fato['impressions']) * 1000
    fato['custo_por_1000_impressoes'] = (fato['cost'] / fato['impressions']) * 1000
    fato['valor_por_clique'] = fato['conversion_value'] / fato['clicks']
    
    # 2. TABELA DIMENSÃO CAMPANHAS (CORRIGIDA)
    print("2. 🎯 Criando tabela DIMENSÃO CAMPANHAS...")
    dimensao_campanhas = df[['campaign_id', 'campaign_name']].drop_duplicates().reset_index(drop=True)
    
    # Classificar campanhas por tipo
    def classificar_campanha(nome):
        nome = nome.lower()
        if 'brand' in nome:
            return 'Marca'
        elif 'competitor' in nome:
            return 'Concorrência'
        elif 'product' in nome:
            return 'Produto'
        elif 'retargeting' in nome:
            return 'Remarketing'
        else:
            return 'Outros'
    
    dimensao_campanhas['tipo_campanha'] = dimensao_campanhas['campaign_name'].apply(classificar_campanha)
    dimensao_campanhas['status_campanha'] = 'Ativa'
    
    # 3. TABELA DIMENSÃO TEMPO
    print("3. 📅 Criando tabela DIMENSÃO TEMPO...")
    datas_unicas = pd.DataFrame({'date': pd.date_range(start=df['date'].min(), end=df['date'].max())})
    dimensao_tempo = datas_unicas.copy()
    
    dimensao_tempo['ano'] = dimensao_tempo['date'].dt.year
    dimensao_tempo['mes'] = dimensao_tempo['date'].dt.month
    dimensao_tempo['mes_nome'] = dimensao_tempo['date'].dt.month_name()
    dimensao_tempo['semana'] = dimensao_tempo['date'].dt.isocalendar().week
    dimensao_tempo['dia_semana'] = dimensao_tempo['date'].dt.day_name()
    dimensao_tempo['trimestre'] = dimensao_tempo['date'].dt.quarter
    dimensao_tempo['dia_do_mes'] = dimensao_tempo['date'].dt.day
    dimensao_tempo['e_fim_de_semana'] = dimensao_tempo['dia_semana'].isin(['Saturday', 'Sunday'])
    dimensao_tempo['trimestre_nome'] = 'T' + dimensao_tempo['trimestre'].astype(str)
    
    # Ordem dos meses e dias
    ordem_meses = ['January', 'February', 'March', 'April', 'May', 'June', 
                  'July', 'August', 'September', 'October', 'November', 'December']
    ordem_dias = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    dimensao_tempo['mes_ordem'] = dimensao_tempo['mes_nome'].apply(lambda x: ordem_meses.index(x) + 1)
    dimensao_tempo['dia_semana_ordem'] = dimensao_tempo['dia_semana'].apply(lambda x: ordem_dias.index(x) + 1)
    
    # 4. TABELA DIMENSÃO DISPOSITIVOS
    print("4. 📱 Criando tabela DIMENSÃO DISPOSITIVOS...")
    dispositivos_unicos = df[['device']].drop_duplicates().reset_index(drop=True)
    dimensao_dispositivos = dispositivos_unicos.copy()
    
    # Classificar dispositivos
    mapeamento_dispositivos = {
        'MOBILE': 'Mobile',
        'DESKTOP': 'Desktop', 
        'TABLET': 'Tablet'
    }
    dimensao_dispositivos['device_nome'] = dimensao_dispositivos['device'].map(mapeamento_dispositivos)
    dimensao_dispositivos['device_categoria'] = 'Dispositivo Digital'
    
    # 5. TABELA DIMENSÃO REDES
    print("5. 📡 Criando tabela DIMENSÃO REDES...")
    redes_unicas = df[['network']].drop_duplicates().reset_index(drop=True)
    dimensao_redes = redes_unicas.copy()
    
    mapeamento_redes = {
        'SEARCH': 'Busca',
        'DISPLAY': 'Display',
        'VIDEO': 'Vídeo'
    }
    dimensao_redes['network_nome'] = dimensao_redes['network'].map(mapeamento_redes)
    dimensao_redes['network_tipo'] = dimensao_redes['network'].apply(
        lambda x: 'Search' if x == 'SEARCH' else 'Display'
    )
    
    # 📁 SALVAR ARQUIVOS CSV (CORRIGIDO)
    print("\n💾 SALVANDO ARQUIVOS CSV...")
    
    # Criar pasta se não existir
    pasta_bi = "Power_BI_Datasets_Corrigido"
    if not os.path.exists(pasta_bi):
        os.makedirs(pasta_bi)
    
    # Salvar como CSV garantindo os nomes das colunas
    fato.to_csv(f"{pasta_bi}/fato_google_ads.csv", index=False, encoding='utf-8-sig')
    dimensao_campanhas.to_csv(f"{pasta_bi}/dimensao_campanhas.csv", index=False, encoding='utf-8-sig')
    dimensao_tempo.to_csv(f"{pasta_bi}/dimensao_tempo.csv", index=False, encoding='utf-8-sig')
    dimensao_dispositivos.to_csv(f"{pasta_bi}/dimensao_dispositivos.csv", index=False, encoding='utf-8-sig')
    dimensao_redes.to_csv(f"{pasta_bi}/dimensao_redes.csv", index=False, encoding='utf-8-sig')
    
    # 📋 VERIFICAR COLUNAS
    print(f"\n🔍 VERIFICANDO COLUNAS DAS TABELAS:")
    print(f"   • FATO: {list(fato.columns)}")
    print(f"   • CAMPANHAS: {list(dimensao_campanhas.columns)}")
    print(f"   • TEMPO: {list(dimensao_tempo.columns)}")
    print(f"   • DISPOSITIVOS: {list(dimensao_dispositivos.columns)}")
    print(f"   • REDES: {list(dimensao_redes.columns)}")
    
    caminho_base = os.path.abspath(pasta_bi)
    
    print(f"\n✅ DATASETS CRIADOS COM SUCESSO!")
    print(f"📁 Pasta: {caminho_base}")
    
    return {
        'fato': fato,
        'campanhas': dimensao_campanhas,
        'tempo': dimensao_tempo,
        'dispositivos': dimensao_dispositivos,
        'redes': dimensao_redes
    }

def criar_arquivo_instrucoes_corrigido():
    """Cria instruções atualizadas"""
    instrucoes = """
📋 INSTRUÇÕES CORRIGIDAS - POWER BI

🎯 RELACIONAMENTOS CORRETOS:

FATO_GOOGLE_ADS[date] → DIMENSAO_TEMPO[date]
FATO_GOOGLE_ADS[campaign_id] → DIMENSAO_CAMPANHAS[campaign_id]  
FATO_GOOGLE_ADS[device] → DIMENSAO_DISPOSITIVOS[device]
FATO_GOOGLE_ADS[network] → DIMENSAO_REDES[network]

📊 COLUNAS EM CADA TABELA:

• FATO_GOOGLE_ADS: date, campaign_id, device, network, impressions, clicks, cost, conversions, etc.
• DIMENSAO_CAMPANHAS: campaign_id, campaign_name, tipo_campanha, status_campanha
• DIMENSAO_TEMPO: date, ano, mes, mes_nome, dia_semana, etc.
• DIMENSAO_DISPOSITIVOS: device, device_nome, device_categoria  
• DIMENSAO_REDES: network, network_nome, network_tipo

🚀 COMO CRIAR AS RELAÇÕES:

1. Importe todos os arquivos CSV
2. Vá para "Visão de Modelo" 
3. ARRASTE E SOLTE:
   - FATO[campaign_id] → CAMPANHAS[campaign_id]
   - FATO[date] → TEMPO[date]
   - FATO[device] → DISPOSITIVOS[device]
   - FATO[network] → REDES[network]

✅ VERIFIQUE SE:
- As colunas campaign_id existem em ambas as tabelas
- Os nomes estão exatamente iguais
- As tabelas estão conectadas por linhas
"""
    
    with open("Power_BI_Datasets_Corrigido/INSTRUCOES_CORRIGIDAS.txt", "w", encoding='utf-8') as f:
        f.write(instrucoes)
    
    print(f"📖 Instruções corrigidas criadas!")

if __name__ == "__main__":
    print("=" * 60)
    print("           POWER BI - VERSÃO CORRIGIDA")
    print("=" * 60)
    
    datasets = criar_datasets_power_bi()
    criar_arquivo_instrucoes_corrigido()
    
    # Abrir a pasta automaticamente
    os.startfile("Power_BI_Datasets_Corrigido")
    
    print(f"\n🎉 ARQUIVOS CORRIGIDOS CRIADOS!")
    print(f"📁 Pasta: Power_BI_Datasets_Corrigido")
    print(f"🔍 Verifique se a tabela DIMENSAO_CAMPANHAS tem a coluna 'campaign_id'")
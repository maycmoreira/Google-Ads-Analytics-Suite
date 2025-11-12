import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def criar_metricas_google_ads(n_dias=90, data_inicio='2024-01-01', seed=42):
    np.random.seed(seed)
    start_date = datetime.strptime(data_inicio, '%Y-%m-%d')
    
    dates = [start_date + timedelta(days=x) for x in range(n_dias)]
    
    data = {
        'date': dates,
        'campaign_id': np.random.choice(['CAMP_001', 'CAMP_002', 'CAMP_003', 'CAMP_004'], n_dias),
        'campaign_name': np.random.choice(['Brand_Search', 'Competitor_Keywords', 'Product_Launch', 'Retargeting'], n_dias),
        'ad_group_id': np.random.choice(['AG_001', 'AG_002', 'AG_003', 'AG_004', 'AG_005'], n_dias),
        'device': np.random.choice(['MOBILE', 'DESKTOP', 'TABLET'], n_dias, p=[0.6, 0.3, 0.1]),
        'network': np.random.choice(['SEARCH', 'DISPLAY', 'VIDEO'], n_dias, p=[0.7, 0.2, 0.1]),
        'impressions': (np.random.poisson(5000, n_dias) + np.random.randint(-1000, 1000, n_dias)).astype(float),
        'clicks': (np.random.poisson(150, n_dias) + np.random.randint(-30, 30, n_dias)).astype(float),
        'cost': np.round(np.random.uniform(50, 500, n_dias), 2),
        'conversions': (np.random.poisson(8, n_dias)).astype(float),
        'conversion_value': np.round(np.random.uniform(10, 200, n_dias), 2),
        'ctr': np.round(np.random.uniform(0.01, 0.08, n_dias), 4),
        'avg_cpc': np.round(np.random.uniform(0.5, 3.5, n_dias), 2),
        'conversion_rate': np.round(np.random.uniform(0.02, 0.15, n_dias), 4),
        'cpa': np.round(np.random.uniform(5, 50, n_dias), 2),
        'roas': np.round(np.random.uniform(1, 8, n_dias), 2),
        'avg_position': np.round(np.random.uniform(1, 4, n_dias), 2),
        'search_impression_share': np.round(np.random.uniform(0.1, 0.9, n_dias), 4),
        'search_absolute_top_impression_share': np.round(np.random.uniform(0.05, 0.6, n_dias), 4),
        'video_views': (np.random.poisson(200, n_dias)).astype(float),
        'view_rate': np.round(np.random.uniform(0.1, 0.4, n_dias), 4),
    }
    
    df_ads = pd.DataFrame(data)
    
    df_ads['clicks'] = (df_ads['impressions'] * df_ads['ctr']).astype(int)
    df_ads['cost'] = df_ads['clicks'] * df_ads['avg_cpc']
    df_ads['conversions'] = (df_ads['clicks'] * df_ads['conversion_rate']).astype(int)
    df_ads['conversion_value'] = df_ads['conversions'] * np.random.uniform(15, 25, n_dias)
    df_ads['roas'] = df_ads['conversion_value'] / df_ads['cost']
    
    df_ads['day_of_week'] = df_ads['date'].dt.dayofweek
    df_ads['is_weekend'] = df_ads['day_of_week'].isin([5, 6]).astype(int)
    
    weekend_multiplier = 1.3
    weekend_mask = df_ads['is_weekend'] == 1
    
    df_ads.loc[weekend_mask, 'impressions'] = (df_ads.loc[weekend_mask, 'impressions'] * weekend_multiplier).astype(int)
    df_ads.loc[weekend_mask, 'clicks'] = (df_ads.loc[weekend_mask, 'clicks'] * weekend_multiplier).astype(int)
    
    return df_ads

if __name__ == "__main__":
    df = criar_metricas_google_ads()
    print("Dataset criado com sucesso!")
    print(f"Dimensões: {df.shape}")
    print("\nPrimeiras 5 linhas:")
    print(df.head())
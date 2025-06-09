import pandas as pd
import numpy as np
import datetime as dt

def data_load():
    """
    Loads the main dataset (or a sample of it for testing).
    
    This main dataset shall be sliced by other methods that will call on this one.
    
    Some of its columns are exemplified on the table below. 

    Returns:
        Dataframe.

    | Regiao | Estado | Municipio | Revenda | CNPJ | Produto | Data da Coleta | Valor de Venda
    |---|---|---|---|---|---|---|---
    | NE | BA | Salvador | Posto BR | 01.xxx.xxx/0001-90 | DIESEL | 01-01-2025 | 3.567
    | NE | BA | Feira de Santana | Posto Shell | 02.xxx.xxx/0001-90 | ETANOL | 01-01-2025 | 2.908
    """ 
    # Reduced dataset made of Northeast (NE) retailers only
    anp_data_NE = pd.read_csv("./data/northeast.csv",
                              parse_dates=["Data da Coleta"],
                              nrows=100000
                  )
    anp_data_NE.loc[:, "Municipio"] = anp_data_NE.loc[:, "Municipio"].str.title()
    anp_data_NE.loc[:, "Ano"] = anp_data_NE["Data da Coleta"].dt.year
    # Reduction to Bahia state only AND not cooking gas
    is_Bahia = anp_data_NE["Estado"]=="BA"
    isnt_GLP = anp_data_NE["Produto"]!="GLP"
    return anp_data_NE[is_Bahia & isnt_GLP]

def city_overall():
    """
    Summarizes by year the minimum and maximum fuel prices for all cities. Scope is all retailers ("Revenda").

    Dataframe columns:

    | Municipio | Ano | Produto | Numero de Revendas | Valor de Venda (min) | Valor de Venda (max)
    |---|---|---|---|---|---
    ALAGOINHAS | 2004 | DIESEL | 9 | 1.220| 1.490
    Returns:
        Dataframe.
    """
    # City overall info - for table
    city_overall = data_load()
    # city_overall.loc[:, "Ano"] = city_overall["Data da Coleta"].dt.year
    city_overall = city_overall.groupby(["Municipio","Ano","Produto"]).agg({"Revenda":"nunique", "Valor de Venda":["min","max"]}).reset_index()

    new_column_names = []

    # Fixes the multilevel column generated when "Valor de Venda" was aggregated by "min" and "max" at the same time.
    for cols in city_overall.columns:
        # This only works for the top and adjacent level right below it.
        new_col_name = f'{cols[0]}_{cols[1]}'
        new_column_names.append(new_col_name)
    city_overall.columns = new_column_names
    city_overall.columns = ['Municipio', 'Ano', 'Produto', 'Numero de Revendas', 'Valor de Venda (min)', 'Valor de Venda (max)']
    return city_overall

def daily_average_price():
    """
    Generates a time series with average pricing of each fuel type considering all retailers in all cities.

    Granularity in days.

    Produto | Data da Coleta | Valor de Venda medio | Ano
    |---|---|---|---
    DIESEL  |  2004-05-10    |         1.315086     | 2004
    """
    # Daily average for all gas stations, by fuel type
    daily_fuel_avg = data_load().groupby(["Produto","Data da Coleta","Ano"])["Valor de Venda"].agg(["mean"]).reset_index()
    daily_fuel_avg.columns = ["Produto", "Data da Coleta", "Ano", "Valor de Venda medio"]
    # daily_fuel_avg.loc[:, "Ano"] = daily_fuel_avg["Data da Coleta"].dt.year
    return daily_fuel_avg

def all_time_avg():

    # Calculates average for every fuel sold in every city
    city_alltime_avg = data_load().groupby(["Municipio","Produto"])["Valor de Venda"].agg("mean")
    city_alltime_avg = city_alltime_avg.reset_index()

    # Calculates maximum of the sum of the average fuel prices for each city.
    # Then normalizes all averages calculated on "city_alltime_avg" by this maximum value.
    city_alltime_avg_sum = city_alltime_avg.groupby("Municipio")["Valor de Venda"].agg("sum").reset_index()
    divisor = city_alltime_avg_sum["Valor de Venda"].max()
    city_alltime_avg["Normalized"] = city_alltime_avg["Valor de Venda"].apply(lambda x:x/divisor)

    # Ordering by the city with the highest overall means
    city_order = city_alltime_avg_sum.sort_values("Valor de Venda", ascending=False)
    city_ordered_list = city_order.set_index("Municipio").index

    city_alltime_avg["Municipio"]= pd.Categorical(city_alltime_avg["Municipio"], categories=city_ordered_list)
    return city_alltime_avg
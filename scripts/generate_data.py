import pandas as pd
from geopy.distance import geodesic as GD


if __name__ == '__main__':
    # gera um dataframe com os voos agrupados em intervalos de 1h
    flights = pd.read_csv('data/flights.csv', sep=';')
    airports = pd.read_csv('data/airports.csv')

    flights = flights.merge(airports[['Código OACI', 'LATGEOPOINT', 'LONGEOPOINT']], left_on='ICAO Aerodromo Origem', right_on='Código OACI').rename(columns={'LATGEOPOINT': 'lat_origem', 'LONGEOPOINT': 'lon_origem'})
    flights = flights.merge(airports[['Código OACI', 'LATGEOPOINT', 'LONGEOPOINT']], left_on='ICAO Aerodromo Destino', right_on='Código OACI').rename(columns={'LATGEOPOINT': 'lat_destino', 'LONGEOPOINT': 'lon_destino'})
    flights = flights.loc[flights['Situacao Voo'] == 'REALIZADO']
    flights = flights.sort_values(by='Partida Real')
    flights = flights.reset_index().rename(columns={'index': 'flight_index'})
    flights['Partida Real'] = pd.to_datetime(flights['Partida Real'])
    flights['origem'] = flights.apply(lambda row: [row['lat_origem'], row['lon_origem']], axis=1)
    flights['destino'] = flights.apply(lambda row: [row['lat_destino'], row['lon_destino']], axis=1)
    flights['dist'] = flights.apply(lambda row: GD(row['origem'], row['destino']).meters, axis=1)

    hourly_flights = flights.set_index('Partida Real').resample('60t').apply(list).reset_index()
    hourly_flights['numero_de_voos'] = hourly_flights['flight_index'].apply(len)
    hourly_flights['data_partida'] = hourly_flights['Partida Real'].apply(lambda x: x.date()) 
    hourly_flights = hourly_flights.loc[hourly_flights['numero_de_voos'] > 0]
    hourly_flights['tot_dist'] = hourly_flights['dist'].apply(sum)

    hourly_flights.to_csv('data/hourly_flights.csv')
import pandas as pd
import matplotlib.pyplot as plt

#wczytujemy dane
df_polisy = pd.read_csv("polisy.csv")
df_szkody = pd.read_csv("szkody.csv")

#czyszczenie danych
df_polisy['region'] = df_polisy['region'].str.capitalize()
df_polisy['region'] = df_polisy['region'].fillna('brak danych')
df_szkody['kwota_wyplacona_pln']= df_szkody['kwota_wyplacona_pln'].fillna(0)

szkody_zsumowane = df_szkody.groupby('id_klienta')['kwota_wyplacona_pln'].sum().reset_index() #agregujemy szkody tak aby każdy klient pojawiał się w tabeli tylko 1 raz

df_master = pd.merge(df_polisy, szkody_zsumowane, on='id_klienta', how='left') # łączymy tabele

df_master['kwota_wyplacona_pln'] = df_master['kwota_wyplacona_pln'].fillna(0)

print(df_master)

raport_regiony = df_master.groupby('region').agg({
    'skladka_pln': 'sum',
    'kwota_wyplacona_pln': 'sum'
}).reset_index()

raport_regiony['szkodowosc_%'] = ((raport_regiony['kwota_wyplacona_pln'] / raport_regiony['skladka_pln']) * 100).round(2)

raport_regiony = raport_regiony.sort_values(by='szkodowosc_%', ascending=False)

print("raport:")
print(raport_regiony)

raport_regiony.to_excel('raport.xlsx', index=False)

plt.figure(figsize=(10,6))

plt.bar(raport_regiony['region'], raport_regiony['szkodowosc_%'], color='skyblue', edgecolor='black')
plt.axhline(y=100, color='red', linestyle='--', label='Próg straty')

plt.title('wskaźnik straty dla każdego regionu')
plt.xlabel('region')
plt.ylabel('szkodowosc %')
plt.legend()

plt.show()
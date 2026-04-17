import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def wczytanie_danych(sciezka):
    print(f"Wczytywanie danych z {sciezka}")
    try:
        df = pd.read_csv(sciezka)
        print(f"wczytano {len(df)} wierszy")
        return df
    except FileNotFoundError:
        print("nie udało się wczytać pliku")
        return None
    
def podzial_wiek(df):
    przedzialy=[18,25,35,50,65,100]
    etykiety=['18-25','26-35','36-50','51-65','66-100']
    df['grupa_wiekowa'] = pd.cut(df['age'], przedzialy, etykiety)
    return df

def tabela_szkodowosc(df):
    pivot = df.pivot_table(
        values = 'total_claim_amount',
        index = 'auto_make',
        columns=['grupa_wiekowa','insured_sex'],
        aggfunc='mean'
    )
    return pivot

def heatmap(tabela):
    plt.figure(figsize=(14,8))

    sns.heatmap(tabela, fmt=".0f", annot=True)
    plt.title("Średnia kwota wypłaconej szkodu (USD) wiek, marka")
    plt.ylabel("Marka pojazdu")
    plt.xlabel("Grupa wiekowa i płeć")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    sciezka = "insurance_claims.csv"
    dane = wczytanie_danych(sciezka)
    dane = podzial_wiek(dane)
    tabela = tabela_szkodowosc(dane)
    heatmap(tabela)
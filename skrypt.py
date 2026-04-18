import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
import statsmodels.api as sm

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
    przedzialy=[17,25,35,50,65,100]
    etykiety=['18-25','26-35','36-50','51-65','66-100']
    df['grupa_wiekowa'] = pd.cut(df['age'], przedzialy, etykiety)
    return df

def tabela_szkodowosc(df):
    pivot = df.pivot_table(
        values = 'total_claim_amount',
        index = 'auto_make',
        columns=['grupa_wiekowa','insured_sex'],
        aggfunc='median'
    )
    return pivot

def heatmap(tabela):
    plt.figure(figsize=(14,8))

    sns.heatmap(tabela, cmap="flare", fmt=".0f", annot=True)
    plt.title("Mediana wypłaconych kwot dla wieku, marki samochodu i płci")
    plt.ylabel("Marka pojazdu")
    plt.xlabel("Grupa wiekowa i płeć")
    plt.tight_layout()
    plt.show()

def sprawdz_rozklad_zmiennej(df):
    plt.figure(figsize=(10, 6))
    
    sns.histplot(df['total_claim_amount'], bins=100, kde=True, color='purple')
    
    plt.title("Rozkład wypłaconych odszkodowań (Total Claim Amount)")
    plt.xlabel("Kwota wypłaty ($)")
    plt.ylabel("Liczba wypadków")
    plt.show()

def filtruj_duze_szkody(df):
    duze_szkody = df[df['total_claim_amount']>25000].copy()
    duze_szkody['nadwyzka'] = duze_szkody['total_claim_amount'] - 25000

    return duze_szkody
# Widoczne na wykresie są dwa szczyty z czego drugi przypomina rozkład normalny lub prawoskośny

# Przeprowadzamy analize TYLKO dla szkód większych niż 25 000 USD
def model_duze_szkody(df):
    formula = "nadwyzka ~ C(collision_type) + bodily_injuries + number_of_vehicles_involved + age + I(age**2) + C(insured_sex) + C(auto_make)"

    model_duze = smf.glm(formula=formula, 
                         data=df, 
                         family=sm.families.Gamma(link=sm.families.links.Log()))
    
    wynik_duze = model_duze.fit()
    print(wynik_duze.summary())
    return wynik_duze

def wykres_wynikow(wynik_duze):
    wspolczynniki = wynik_duze.params.drop("Intercept")
    
    wspolczynniki.sort_values().plot(kind='barh', figsize=(8, 5))
    
    plt.axvline(x=0, color='red', linestyle='--')
    plt.title("Wpływ cech na wielkość szkody (Współczynniki)")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    sciezka = "insurance_claims.csv"

    dane = wczytanie_danych(sciezka) # Wczytujemy dane
    dane = podzial_wiek(dane) # Tworzymy dodatkową kolumne (podział na wiek)
    tabela = tabela_szkodowosc(dane) # Tworzymy tabele przestawną obliczającą mediane wypłaconych szkód z podziałem na wiek oraz płeć i marke samochodu
    heatmap(tabela) # Szkicujemy heatmape

    sprawdz_rozklad_zmiennej(dane) # Szkicujemy rozkład wypłaconych ubezpieczeń
    dane_duze_szkody = filtruj_duze_szkody(dane) # usuwamy wszystkie wiersze gdzie wyplacona kwota jest mniejsza niz 25 000 USD
    sprawdz_rozklad_zmiennej(dane_duze_szkody)
    print(f"Współczynnik skośności: {dane_duze_szkody['total_claim_amount'].skew()}") # współczynnik ~= 0.27 zatem dane są lekko prawo skośne wybieramy rozkład gamma

    model_prawy_pik = model_duze_szkody(dane_duze_szkody)
    wykres_wynikow(model_prawy_pik)
# Automatyzacja raportu szkodowości w Pythonie

## O projekcie
Prosty skrypt w Pythonie automatyzujący proces wyliczania wskaźnika szkodowości na podstawie dwóch plików `polisy.csv` i `szkody.csv`. Zastępuje on manualną pracę np w MS Excel (używanie funkcji VLOOKUP i Tabel przestawnych).

## Rozwiązanie
Skrypt wykonuje następujące kroki:
1. Wczytanie oraz czyszczenie plików `.csv`
2. Agregacja danych w celu uniknięcia podwójnego liczenia składek przy wielu szkodach jednego klienta.
3. Połączenie tabel.
4. Obliczenie wskaźnika szkodowości.
5. Eksport raportu do pliku `.xslx`.
6. Wygenerowanie wykresu słupkowego na podstawie raportu.

## Stack
* **Python 3**
* **Pandas, Matplotlib, Openpyxl**
   

import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv('fatal-police-shootings-data.csv')
df_copy = df.copy()

result = df_copy.groupby(['race', 'signs_of_mental_illness']).size().reset_index(name='count')

print(result)

race_counts = df_copy['race'].value_counts()
mental_illness_counts = df_copy[df_copy['signs_of_mental_illness'] == True]['race'].value_counts()

result['percent_mental_illness'] = result.apply(lambda row: (mental_illness_counts[row['race']] / race_counts[row['race']]) * 100, axis=1)

max_percent_race = result.loc[result['percent_mental_illness'].idxmax()]['race']

print(f"Rasa, która charakteryzuje się największym odsetkiem znamion choroby psychicznej: {max_percent_race}")

# Konwersja kolumny 'date' na format daty
df_copy['date'] = pd.to_datetime(df['date'])

# Dodanie kolumny 'day_of_week' oznaczającej dzień tygodnia (0 - poniedziałek, 6 - niedziela)
df_copy['day_of_week'] = df_copy['date'].dt.dayofweek

# Zamiana numerów dnia tygodnia na nazwy
day_names = ['poniedziałek', 'wtorek', 'środa', 'czwartek', 'piątek', 'sobota', 'niedziela']
df_copy['day_of_week'] = df_copy['day_of_week'].map(lambda x: day_names[x])

# Zliczenie interwencji według odpowiedniego dnia tygodnia
interventions_by_day = df_copy['day_of_week'].value_counts()

# Sortowanie dni tygodnia
interventions_by_day = interventions_by_day.reindex(day_names)

# Tworzenie wykresu kolumnowego
plt.bar(interventions_by_day.index, interventions_by_day.values)
plt.xlabel('Dzień tygodnia')
plt.ylabel('Liczba interwencji')
plt.title('Liczba interwencji według dnia tygodnia')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# Wczytanie danych populacji
population_url = "https://simple.wikipedia.org/wiki/List_of_U.S._states_by_population"
population_data = pd.read_html(population_url, header=0)[0]

#wczytanie stanów
state_url = "https://en.wikipedia.org/wiki/List_of_U.S._state_and_territory_abbreviations"
state_data = pd.read_html(state_url, header=0)[0]

test = "test.csv"
state_data.to_csv(test)

# Wybór odpowiednich kolumn
population_data = population_data[["State", "Census population, April 1, 2020 [1][2]", "Census population, April 1, 2010 [1][2]"]]

# Grupowanie incydentów według stanu i liczenie ich liczności
incidents_per_state = df_copy.groupby('state').size().reset_index(name='Incident Count')

# Połączenie danych z obu tabel
merged_data = pd.merge(population_data, incidents_per_state, left_on='State', right_on='State', how='left')

# Obliczanie ilości incydentów na 1000 mieszkańców
merged_data['Incidents per 1000 Residents'] = (merged_data['Incident Count'] / merged_data['Census population, April 1, 2020 [1][2]']) * 1000

# Wyświetlanie wyniku
print(merged_data[['State', 'Incidents per 1000 Residents']])
import pandas as pd
import matplotlib.pyplot as plt
from countryinfo import CountryInfo
import time

print("Скрипт запущен")
start_time = time.time()

# Загрузка данных
try:
    df = pd.read_excel('gtd.xlsx')
    print(f"Данные загружены за {time.time() - start_time:.2f} секунд")
except FileNotFoundError:
    print("Файл gtd.xlsx не найден.")
    exit()

# Удаление строк с отсутствующими значениями в столбце 'country_txt'
df.dropna(subset=['country_txt'], inplace=True)
print("Строки без названия страны удалены")

# Получение данных о населении
unique_countries = df['country_txt'].unique()
print(f"Найдено {len(unique_countries)} уникальных стран")
population_data = {}
countries_processed = 0
for country in unique_countries:
    try:
        population_data[country] = CountryInfo(country).population()
    except (KeyError, ValueError):
        population_data[country] = None
    countries_processed += 1
    if countries_processed % 20 == 0:
        print(f"Обработано {countries_processed}/{len(unique_countries)} стран...")

print(f"Данные о населении собраны за {time.time() - start_time:.2f} секунд")

df['population'] = df['country_txt'].map(population_data)

# Удаление строк, где не удалось получить данные о населении
df.dropna(subset=['population'], inplace=True)
print("Строки без данных о населении удалены")

# Расчет количества атак на 1 миллион человек
# Группируем по странам и считаем количество атак
attacks_by_country = df.groupby('country_txt').size()
# Получаем население для каждой страны
population_by_country = df.groupby('country_txt')['population'].first()
# Рассчитываем атаки на миллион
attacks_per_million = (attacks_by_country / population_by_country) * 1_000_000
attacks_per_million = attacks_per_million.sort_values(ascending=False)

print(f"Расчеты завершены за {time.time() - start_time:.2f} секунд")

# Визуализация
plt.figure(figsize=(12, 8))
attacks_per_million.head(20).plot(kind='bar')
plt.title('Топ-20 стран по количеству атак на 1 миллион человек')
plt.xlabel('Страна')
plt.ylabel('Атаки на 1 миллион человек')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('attacks_per_capita.png')
plt.show()

print("График 'attacks_per_capita.png' успешно сохранен.")

# Анализ для Центральной Азии
central_asia_countries = df[df['region_txt'] == 'Central Asia']['country_txt'].unique()
central_asia_attacks = attacks_per_million.loc[attacks_per_million.index.isin(central_asia_countries)]

print("\nАтаки на 1 миллион человек в Центральной Азии:")
print(central_asia_attacks)

if 'Kazakhstan' in attacks_per_million.index:
    print(f"\nАтаки на 1 миллион человек в Казахстане: {attacks_per_million['Kazakhstan']:.2f}")

# Визуализация для Центральной Азии
plt.figure(figsize=(10, 6))
central_asia_attacks.sort_values(ascending=False).plot(kind='bar')
plt.title('Атаки на 1 миллион человек в Центральной Азии')
plt.xlabel('Страна')
plt.ylabel('Атаки на 1 миллион человек')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('attacks_per_capita_central_asia.png')
plt.show()
print("График 'attacks_per_capita_central_asia.png' успешно сохранен.")

print(f"Скрипт завершен за {time.time() - start_time:.2f} секунд")

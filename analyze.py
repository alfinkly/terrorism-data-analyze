import pandas as pd

# --- КОНФИГУРАЦИЯ ---
# Установите True для использования полного набора данных, False для использования мини-набора данных для разработки
USE_FULL_DATASET = False
# -------------------

# Определяем, какой файл загружать
if USE_FULL_DATASET:
    file_to_load = 'gtd.xlsx'
    print("Попытка загрузить полный набор данных...")
else:
    file_to_load = 'gtd-mini.xlsx'
    print("Попытка загрузить мини-набор данных для разработки...")


# Загрузка набора данных
try:
    df = pd.read_excel(file_to_load)
    print(f"Набор данных успешно загружен из {file_to_load}.")
except FileNotFoundError:
    print(f"Ошибка: {file_to_load} не найден. Убедитесь, что файл находится в правильном каталоге.")
    if not USE_FULL_DATASET:
        print("Возможно, вам сначала нужно запустить скрипт create_mini_dataset.py.")
    exit()

# Display basic information about the dataset
print("Shape of the dataset:", df.shape)
print("Columns of the dataset:", df.columns.tolist())

# Analyze data by region
region_attacks = df['region_txt'].value_counts()
print("\nNumber of attacks by region:")
print(region_attacks)

# Analyze data for Central Asia
central_asia_attacks = df[df['region_txt'] == 'Central Asia']
print("\nNumber of attacks in Central Asia:", len(central_asia_attacks))

# Analyze data for Kazakhstan
kazakhstan_attacks = df[df['country_txt'] == 'Kazakhstan']
print("Number of attacks in Kazakhstan:", len(kazakhstan_attacks))

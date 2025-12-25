import pandas as pd
import matplotlib.pyplot as plt

def run_analysis():
    # --- КОНФИГУРАЦИЯ ---
    # Установите True для использования полного набора данных, False для использования мини-набора данных для разработки
    USE_FULL_DATASET = False
    # -------------------

    # Определяем, какой файл загружать
    if USE_FULL_DATASET:
        file_to_load = "gtd.xlsx"
        print("Попытка загрузить полный набор данных...")
    else:
        file_to_load = "gtd-mini.xlsx"
        print("Попытка загрузить мини-набор данных для разработки...")


    # Загрузка набора данных
    try:
        df = pd.read_excel(file_to_load)
        print(f"Набор данных успешно загружен из {file_to_load}.")
    except FileNotFoundError:
        print(f"Ошибка: Файл '{file_to_load}' не найден. Убедитесь, что он находится в правильном каталоге.")
        return

    # --- АНАЛИЗ ДАННЫХ ---

    # 1. Обзор данных
    print("\n--- 1. Обзор данных ---")
    print("Первые 5 строк:")
    print(df.head())
    print("\nИнформация о наборе данных:")
    df.info()
    print("\nОсновные статистические данные:")
    print(df.describe())

    # 2. Анализ атак по времени
    print("\n--- 2. Анализ атак по времени ---")
    plt.figure(figsize=(15, 7))
    df['iyear'].value_counts().sort_index().plot(kind='line')
    plt.title('Количество терактов по годам (в мире)')
    plt.xlabel('Год')
    plt.ylabel('Количество атак')
    plt.grid(True)
    plt.savefig('attachments/attacks_over_time_world.png')
    # plt.show()
    plt.close()
    print("График 'Количество терактов по годам' сохранен в attachments/attacks_over_time_world.png")

    # 3. Анализ по регионам
    print("\n--- 3. Анализ по регионам ---")
    plt.figure(figsize=(12, 8))
    df['region_txt'].value_counts().plot(kind='barh')
    plt.title('Количество терактов по регионам')
    plt.xlabel('Количество атак')
    plt.ylabel('Регион')
    plt.tight_layout()
    plt.savefig('attachments/attacks_by_region.png')
    # plt.show()
    plt.close()
    print("График 'Количество терактов по регионам' сохранен в attachments/attacks_by_region.png")

    # 4. Анализ типов атак
    print("\n--- 4. Анализ типов атак ---")
    plt.figure(figsize=(12, 6))
    df['attacktype1_txt'].value_counts().plot(kind='bar')
    plt.title('Самые распространенные типы атак')
    plt.xlabel('Тип атаки')
    plt.ylabel('Количество')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('attachments/attacks_by_type.png')
    # plt.show()
    plt.close()
    print("График 'Самые распространенные типы атак' сохранен в attachments/attacks_by_type.png")

    # 5. Анализ целей атак
    print("\n--- 5. Анализ целей атак ---")
    plt.figure(figsize=(12, 8))
    df['targtype1_txt'].value_counts().plot(kind='barh')
    plt.title('Самые частые цели атак')
    plt.xlabel('Количество атак')
    plt.ylabel('Тип цели')
    plt.tight_layout()
    plt.savefig('attachments/attacks_by_target.png')
    # plt.show()
    plt.close()
    print("График 'Самые частые цели атак' сохранен в attachments/attacks_by_target.png")

    print("\n--- Анализ завершен ---")

if __name__ == '__main__':
    run_analysis()

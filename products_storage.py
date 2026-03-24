#Импорт, глобальные переменные
from datetime import datetime, date, timedelta
from decimal import Decimal

DATE_FORMAT = '%Y-%m-%d'

goods = {}

#Добавляет продукт в словарь goods
def add(items, title, amount, expiration_date=None):
    if title not in items:
        items[title] = []
    if expiration_date is not None:
        expiration_date = datetime.strptime(expiration_date, DATE_FORMAT).date()
    items[title].append({'amount': amount, 'expiration_date': expiration_date})

#Добавляет продукт в словарь goods, преобразуя текстовое описание продукта в структурированные данные
def add_by_note(items, note):
    parts = note.split(' ')
    if len(parts[-1].split('-')) == 3:
        expiration_date = parts[-1]
        amount = Decimal(parts[-2])
        title = ' '.join(parts[:-2])
    else:
        expiration_date = None
        amount = Decimal(parts[-1])
        title = ' '.join(parts[:-1])

    add(items, title, amount, expiration_date)

#Ищет в словаре goods заданное слово или строку и возвращает список продуктов, в названии которых есть это слово
def find(items, needle):
    result = []
    needle = needle.lower()
    for item in items:
        if needle in item.lower():
            result.append(item)
    return result

#Возвращает количество запрошенного продукта
def get_amount(items, needle):
    product_amount = Decimal(0)
    needle = needle.lower()
    fnd_titles = find(items, needle)
    for title in fnd_titles:
        for part in items[title]:
            product_amount += Decimal(part['amount'])
    return product_amount

#Возвращает список просроченных продуктов
def get_expired(items, in_advance_days=0):
    result = []
    date_t = date.today()
    days_left = date_t + timedelta(days=in_advance_days)
    for title, parts in items.items():
        amount = Decimal(0)
        for part in parts:
            if 'expiration_date' in part:
                expiration_date = part['expiration_date']
                if expiration_date is not None and expiration_date <= days_left:
                    amount += Decimal(part['amount'])
        if amount > 0:
            result.append((title, amount))
    return result

#Интерфейс
def interface():
    for _ in range(2):
        print()
    print('= Управление складом =')
    print()

    while True:
        print('Выберите действие:')
        print('1. Добавить товар')
        print('2. Добавить товар по заметке')
        print('3. Найти сумму товаров по подстроке')
        print('4. Найти просроченные товары')
        print('5. Показать все товары')
        print('6. Выход')

        #Ввод данных + избавление от грязи
        choice = input('Ваш выбор: ').strip()

        if choice == '1':
            title = input('Введите название товара: ').strip()
            amount = Decimal(input('Введите количество: ').strip())
            exp_date = input('Введите дату истечения срока (ГГГГ-ММ-ДД) или оставьте пустым: ').strip()
            if exp_date:
                add(goods, title, amount, exp_date)
            else:
                add(goods, title, amount)
            print(f'Товар "{title}" добавлен!')

        elif choice == '2':
            note = input("Введите заметку (например: 'Молоко 1.5 2025-12-31'): ").strip()
            add_by_note(goods, note)
            print('Товар добавлен по заметке!')

        elif choice == '3':
            needle = input('Введите подстроку для поиска: ').strip()
            total = get_amount(goods, needle)
            print(f'Общая сумма товаров, содержащих "{needle}": {total}')

        elif choice == '4':
            days = input('Введите количество дней для учета просрочки (по умолчанию 0): ').strip()
            if days:
                expired = get_expired(goods, int(days))
            else:
                expired = get_expired(goods)

            if expired:
                print()
                print('Товары с истекающим сроком годности:')
                for title, amount in expired:
                    print(f'  {title}: {amount}')
            else:
                print('Просроченных или истекающих товаров не найдено.')

        elif choice == '5':
            if not goods:
                print('Склад пуст.')
            else:
                print()
                print('Все товары на складе:')
                for title, parts in goods.items():
                    total_amount = sum(part['amount'] for part in parts)
                    print()
                    print(f'{title}: всего {total_amount}')
                    for i, part in enumerate(parts, 1):
                        exp = part['expiration_date'] if part['expiration_date'] else 'без срока'
                        print(f'  Часть {i}: количество={part['amount']}, срок={exp}')

        elif choice == '6':
            print('До свидания!')
            break

        else:
            print('Неверный выбор. Попробуйте снова.')
#Вызываем интерфейс
interface()

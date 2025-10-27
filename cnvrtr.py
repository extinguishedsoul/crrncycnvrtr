import sys
import requests
import pyperclip
from decimal import Decimal, ROUND_HALF_UP
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QLineEdit, QPushButton, QLabel, 
                               QDialog, QListWidget, QListWidgetItem, QFrame)
from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QFont, QIcon, QPixmap, QPainter, QColor


class CurrencySelector(QDialog):
    """Модальное окно для выбора валюты"""
    currency_selected = Signal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Выбор валюты")
        self.setModal(True)
        self.setFixedSize(300, 400)
        self.setWindowFlags(Qt.Dialog)
        
        # Список доступных валют (уникальные валюты)
        self.currencies = {
            'USD': 'Доллар США',
            'EUR': 'Евро',
            'RUB': 'Российский рубль',
            'GBP': 'Британский фунт',
            'JPY': 'Японская иена',
            'CNY': 'Китайский юань',
            'CHF': 'Швейцарский франк',
            'CAD': 'Канадский доллар',
            'AUD': 'Австралийский доллар',
            'NZD': 'Новозеландский доллар',
            'SEK': 'Шведская крона',
            'NOK': 'Норвежская крона',
            'DKK': 'Датская крона',
            'PLN': 'Польский злотый',
            'CZK': 'Чешская крона',
            'HUF': 'Венгерский форинт',
            'RON': 'Румынский лей',
            'BGN': 'Болгарский лев',
            'HRK': 'Хорватская куна',
            'RSD': 'Сербский динар',
            'UAH': 'Украинская гривна',
            'BYN': 'Белорусский рубль',
            'KZT': 'Казахстанский тенге',
            'TRY': 'Турецкая лира',
            'ILS': 'Израильский шекель',
            'AED': 'Дирхам ОАЭ',
            'SAR': 'Саудовский риял',
            'QAR': 'Катарский риал',
            'KWD': 'Кувейтский динар',
            'BHD': 'Бахрейнский динар',
            'OMR': 'Оманский риал',
            'JOD': 'Иорданский динар',
            'LBP': 'Ливанский фунт',
            'EGP': 'Египетский фунт',
            'ZAR': 'Южноафриканский рэнд',
            'NGN': 'Нигерийская найра',
            'KES': 'Кенийский шиллинг',
            'GHS': 'Ганский седи',
            'MAD': 'Марокканский дирхам',
            'TND': 'Тунисский динар',
            'DZD': 'Алжирский динар',
            'ETB': 'Эфиопский быр',
            'UGX': 'Угандийский шиллинг',
            'TZS': 'Танзанийский шиллинг',
            'RWF': 'Руандский франк',
            'BWP': 'Ботсванская пула',
            'SZL': 'Свазилендский лилангени',
            'LSL': 'Лесотский лоти',
            'NAD': 'Намибийский доллар',
            'ZMW': 'Замбийская квача',
            'MWK': 'Малавийская квача',
            'BIF': 'Бурундийский франк',
            'DJF': 'Джибутийский франк',
            'KMF': 'Коморский франк',
            'MGA': 'Малагасийский ариари',
            'MUR': 'Маврикийская рупия',
            'SCR': 'Сейшельская рупия',
            'MVR': 'Мальдивская руфия',
            'LKR': 'Шри-ланкийская рупия',
            'BDT': 'Бангладешская така',
            'NPR': 'Непальская рупия',
            'PKR': 'Пакистанская рупия',
            'INR': 'Индийская рупия',
            'BTN': 'Бутанский нгултрум',
            'MMK': 'Мьянманский кьят',
            'THB': 'Тайский бат',
            'LAK': 'Лаосский кип',
            'VND': 'Вьетнамский донг',
            'KHR': 'Камбоджийский риель',
            'MYR': 'Малайзийский ринггит',
            'SGD': 'Сингапурский доллар',
            'IDR': 'Индонезийская рупия',
            'PHP': 'Филиппинское песо',
            'BND': 'Брунейский доллар',
            'KRW': 'Южнокорейская вона',
            'MOP': 'Патака Макао',
            'HKD': 'Гонконгский доллар',
            'TWD': 'Тайваньский доллар',
            'MNT': 'Монгольский тугрик',
            'UZS': 'Узбекский сум',
            'KGS': 'Киргизский сом',
            'TJS': 'Таджикский сомони',
            'AFN': 'Афганский афгани',
            'IRR': 'Иранский риал',
            'IQD': 'Иракский динар',
            'SYP': 'Сирийский фунт',
            'YER': 'Йеменский риал',
            'AMD': 'Армянский драм',
            'GEL': 'Грузинский лари',
            'AZN': 'Азербайджанский манат',
            'MDL': 'Молдавский лей',
            'BAM': 'Боснийская марка',
            'MKD': 'Македонский денар',
            'ALL': 'Албанский лек',
            'ISK': 'Исландская крона',
            'FJD': 'Доллар Фиджи',
            'PGK': 'Кина Папуа-Новой Гвинеи',
            'SBD': 'Доллар Соломоновых островов',
            'VUV': 'Вату Вануату',
            'WST': 'Тала Самоа',
            'TOP': 'Паанга Тонга',
            'XPF': 'Французский тихоокеанский франк',
            'XCD': 'Восточно-карибский доллар',
            'BBD': 'Барбадосский доллар',
            'BZD': 'Белизский доллар',
            'GTQ': 'Гватемальский кетсаль',
            'HNL': 'Гондурасская лемпира',
            'NIO': 'Никарагуанская кордоба',
            'CRC': 'Коста-риканский колон',
            'PAB': 'Панамский бальбоа',
            'DOP': 'Доминиканское песо',
            'HTG': 'Гаитянский гурд',
            'JMD': 'Ямайский доллар',
            'TTD': 'Доллар Тринидада и Тобаго',
            'BMD': 'Бермудский доллар',
            'KYD': 'Доллар Каймановых островов',
            'AWG': 'Арубанский флорин',
            'ANG': 'Нидерландский антильский гульден',
            'SRD': 'Суринамский доллар',
            'GYD': 'Гайанский доллар',
            'VES': 'Венесуэльский боливар',
            'COP': 'Колумбийское песо',
            'PEN': 'Перуанский соль',
            'BOB': 'Боливийский боливиано',
            'CLP': 'Чилийское песо',
            'ARS': 'Аргентинское песо',
            'UYU': 'Уругвайское песо',
            'PYG': 'Парагвайский гуарани',
            'BRL': 'Бразильский реал',
            'FKP': 'Фунт Фолклендских островов',
            'GIP': 'Гибралтарский фунт',
            'SHP': 'Фунт Святой Елены',
            'CUP': 'Кубинское песо',
            'MXN': 'Мексиканское песо'
        }
        
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Заголовок
        title = QLabel("Выбор валюты")
        title.setFont(QFont("Arial", 12, QFont.Bold))
        layout.addWidget(title)
        
        # Строка поиска
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Искомая валюта")
        self.search_input.textChanged.connect(self.filter_currencies)
        layout.addWidget(self.search_input)
        
        # Список валют
        self.currency_list = QListWidget()
        self.populate_currency_list()
        self.currency_list.itemDoubleClicked.connect(self.select_currency)
        layout.addWidget(self.currency_list)
        
        
    def populate_currency_list(self):
        self.currency_list.clear()
        for code, name in self.currencies.items():
            item = QListWidgetItem(f"{code} - {name}")
            item.setData(Qt.UserRole, code)
            self.currency_list.addItem(item)
            
    def filter_currencies(self, text):
        self.currency_list.clear()
        for code, name in self.currencies.items():
            if text.lower() in code.lower() or text.lower() in name.lower():
                item = QListWidgetItem(f"{code} - {name}")
                item.setData(Qt.UserRole, code)
                self.currency_list.addItem(item)
                
    def select_currency(self, item):
        currency_code = item.data(Qt.UserRole)
        self.currency_selected.emit(currency_code)
        self.close()
        
    def keyPressEvent(self, event):
        """Обработка нажатий клавиш"""
        if event.key() == Qt.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(event)


class CurrencyConverter(QMainWindow):
    """Главное окно приложения конвертера валют"""
    
    def __init__(self):
        super().__init__()
        self.from_currency = "USD"
        self.to_currency = "RUB"
        self.exchange_rates = {}
        self.conversion_timer = QTimer()
        self.conversion_timer.setSingleShot(True)
        self.conversion_timer.timeout.connect(self.convert_currency)
        
        # Таймер для проверки интернет-соединения
        self.internet_check_timer = QTimer()
        self.internet_check_timer.timeout.connect(self.check_internet_connection)
        self.internet_check_timer.start(10000)  # Проверяем каждые 10 секунд
        
        # Флаг для отслеживания состояния соединения
        self.is_connected = True
        
        self.setup_ui()
        self.load_exchange_rates()
        
    def setup_ui(self):
        self.setWindowTitle("Конвертер валют")
        self.setFixedSize(600, 300)
        
        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Основной layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Верхняя часть - выбор валют
        currency_layout = QHBoxLayout()
        
        # Левая валюта
        left_currency_layout = QVBoxLayout()
        self.from_currency_btn = QPushButton("Валюта1")
        self.from_currency_btn.clicked.connect(lambda: self.show_currency_selector("from"))
        self.from_currency_btn.setStyleSheet(self.get_currency_button_style())
        left_currency_layout.addWidget(self.from_currency_btn)
        
        # Кнопка обмена валют
        swap_btn = QPushButton("⇄")
        swap_btn.setFixedSize(40, 40)
        swap_btn.clicked.connect(self.swap_currencies)
        swap_btn.setStyleSheet("""
            QPushButton {
                background-color: #404040;
                color: white;
                border: 1px solid #666666;
                border-radius: 20px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #555555;
                border-color: #888888;
            }
        """)
        
        # Правая валюта
        right_currency_layout = QVBoxLayout()
        self.to_currency_btn = QPushButton("валюта2")
        self.to_currency_btn.clicked.connect(lambda: self.show_currency_selector("to"))
        self.to_currency_btn.setStyleSheet(self.get_currency_button_style())
        right_currency_layout.addWidget(self.to_currency_btn)
        
        currency_layout.addLayout(left_currency_layout)
        currency_layout.addWidget(swap_btn)
        currency_layout.addLayout(right_currency_layout)
        
        main_layout.addLayout(currency_layout)
        
        # Средняя часть - поля ввода и вывода
        fields_layout = QHBoxLayout()
        
        # Левое поле ввода
        left_field_layout = QVBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Введите число")
        self.input_field.textChanged.connect(self.on_input_changed)
        self.input_field.setStyleSheet(self.get_field_style())
        left_field_layout.addWidget(self.input_field)
        
        # Правое поле вывода
        right_field_layout = QVBoxLayout()
        self.output_field = QLineEdit()
        self.output_field.setPlaceholderText("Результат")
        self.output_field.setReadOnly(True)
        self.output_field.setStyleSheet(self.get_field_style())
        right_field_layout.addWidget(self.output_field)
        
        fields_layout.addLayout(left_field_layout)
        fields_layout.addLayout(right_field_layout)
        
        main_layout.addLayout(fields_layout)
        
        # Нижняя часть - кнопки действий
        actions_layout = QHBoxLayout()
        
        # Кнопки для левого поля
        left_actions = QHBoxLayout()
        copy_input_btn = QPushButton("📋")
        copy_input_btn.setFixedSize(40, 40)
        copy_input_btn.clicked.connect(self.copy_input)
        copy_input_btn.setStyleSheet(self.get_action_button_style())
        
        clear_input_btn = QPushButton("🗑")
        clear_input_btn.setFixedSize(40, 40)
        clear_input_btn.clicked.connect(self.clear_input)
        clear_input_btn.setStyleSheet(self.get_action_button_style())
        
        left_actions.addWidget(copy_input_btn)
        left_actions.addWidget(clear_input_btn)
        left_actions.addStretch()
        
        # Кнопки для правого поля
        right_actions = QHBoxLayout()
        right_actions.addStretch()
        copy_output_btn = QPushButton("📋")
        copy_output_btn.setFixedSize(40, 40)
        copy_output_btn.clicked.connect(self.copy_output)
        copy_output_btn.setStyleSheet(self.get_action_button_style())
        right_actions.addWidget(copy_output_btn)
        
        actions_layout.addLayout(left_actions)
        actions_layout.addLayout(right_actions)
        
        main_layout.addLayout(actions_layout)
        
        
    def get_currency_button_style(self):
        return """
            QPushButton {
                background-color: #2c2c2c;
                color: white;
                border: 1px solid #555555;
                border-radius: 5px;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #404040;
                border-color: #777777;
            }
        """
        
    def get_field_style(self):
        return """
            QLineEdit {
                background-color: #f5f5f5;
                border: 2px solid #ddd;
                border-radius: 5px;
                padding: 15px;
                font-size: 16px;
            }
            QLineEdit:focus {
                border-color: #2196F3;
            }
        """
        
    def get_action_button_style(self):
        return """
            QPushButton {
                background-color: #666666;
                color: white;
                border: 1px solid #888888;
                border-radius: 20px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #777777;
                border-color: #aaaaaa;
            }
        """
        
    def show_currency_selector(self, field_type):
        selector = CurrencySelector(self)
        selector.currency_selected.connect(
            lambda currency: self.set_currency(currency, field_type)
        )
        selector.exec()
        
    def set_currency(self, currency, field_type):
        if field_type == "from":
            self.from_currency = currency
            self.from_currency_btn.setText(currency)
        else:
            self.to_currency = currency
            self.to_currency_btn.setText(currency)
        self.convert_currency()
        
    def swap_currencies(self):
        self.from_currency, self.to_currency = self.to_currency, self.from_currency
        self.from_currency_btn.setText(self.from_currency)
        self.to_currency_btn.setText(self.to_currency)
        
        # Меняем местами значения полей
        input_text = self.input_field.text()
        output_text = self.output_field.text()
        self.input_field.setText(output_text)
        self.output_field.setText(input_text)
        
    def on_input_changed(self):
        # Запускаем таймер для автоматической конвертации через 300мс после окончания ввода
        self.conversion_timer.stop()
        self.conversion_timer.start(300)
        
    def convert_currency(self):
        try:
            input_text = self.input_field.text().strip()
            if not input_text:
                self.output_field.clear()
                return
                
            amount = Decimal(input_text)
            
            if self.from_currency == self.to_currency:
                result = amount
            else:
                # Получаем курс валют
                if self.from_currency in self.exchange_rates and self.to_currency in self.exchange_rates:
                    from_rate = self.exchange_rates[self.from_currency]
                    to_rate = self.exchange_rates[self.to_currency]
                    
                    # Конвертируем через USD как базовую валюту
                    # from_rate - это курс валюты к USD (например, EUR = 0.85, RUB = 75.0)
                    # to_rate - это курс валюты к USD (например, EUR = 0.85, RUB = 75.0)
                    
                    # Сначала конвертируем в USD
                    usd_amount = amount / from_rate
                    # Затем конвертируем из USD в целевую валюту
                    result = usd_amount * to_rate
                else:
                    # Если курсы недоступны, делаем быструю проверку соединения
                    if not self.is_connected:
                        self.output_field.setText("Нет подключения к интернету")
                    else:
                        self.output_field.setText("Курс валют недоступен")
                    return
                    
            # Округляем до 2 знаков после запятой
            result = result.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            self.output_field.setText(str(result))
            
        except Exception as e:
            print(f"Ошибка конвертации: {e}")  # Для отладки
            self.output_field.setText("Ошибка конвертации")
            
    def load_exchange_rates(self):
        """Загружает курсы валют с API"""
        try:
            # Используем бесплатный API для получения курсов валют
            url = "https://api.exchangerate-api.com/v4/latest/USD"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            # Преобразуем все курсы валют в Decimal для совместимости
            self.exchange_rates = {currency: Decimal(str(rate)) for currency, rate in data['rates'].items()}
            
            # Обновляем кнопки валют
            self.from_currency_btn.setText(self.from_currency)
            self.to_currency_btn.setText(self.to_currency)
            
            print(f"Курсы валют загружены успешно. Доступно валют: {len(self.exchange_rates)}")
            
        except Exception as e:
            print(f"Ошибка загрузки курсов валют: {e}")
            print("Приложение требует подключения к интернету для работы")
            # Оставляем пустой словарь курсов - приложение не будет работать без интернета
            self.exchange_rates = {}
            
    def check_internet_connection(self):
        """Проверяет интернет-соединение с оптимизацией"""
        try:
            # Быстрая проверка с коротким таймаутом
            response = requests.get("https://www.google.com", timeout=2)
            if response.status_code == 200:
                if not self.is_connected:
                    # Соединение восстановлено
                    self.is_connected = True
                    print("Интернет-соединение восстановлено")
                    if not self.exchange_rates:
                        self.load_exchange_rates()
            else:
                if self.is_connected:
                    # Соединение потеряно
                    self.is_connected = False
                    self.exchange_rates = {}
                    print("Интернет-соединение потеряно")
        except Exception:
            if self.is_connected:
                # Соединение потеряно
                self.is_connected = False
                self.exchange_rates = {}
                print("Интернет-соединение потеряно")
            
    def copy_input(self):
        pyperclip.copy(self.input_field.text())
        
    def copy_output(self):
        pyperclip.copy(self.output_field.text())
        
    def clear_input(self):
        self.input_field.clear()
        self.output_field.clear()
        


def main():
    app = QApplication(sys.argv)
    
    # Устанавливаем стиль приложения
    app.setStyle('Fusion')
    
    converter = CurrencyConverter()
    converter.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

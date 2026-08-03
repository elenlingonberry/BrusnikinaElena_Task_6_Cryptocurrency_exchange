# Application Cryptocurrency exchange rates
# Ver 1.0.1
# Application for getting TOP-10 popular cryptocurrency exchange rates (with timeout)


from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb
import requests
from pathlib import Path

from requests import Timeout


def update_b_label(event):
    # Получаем полное название криптовалюты из словаря и обновляем метку
    code = base_combobox.get()
    name = currencies[code]
    b_label.config(text=name)


def exchange():
    base_code = base_combobox.get()

    if base_code:
        try:
            response = requests.get(f'https://api.coingecko.com/api/v3/simple/price?ids='
                                     f'bitcoin,ethereum,tether,binancecoin,ripple,usd-coin,'
                                     f'solana,cardano,dogecoin,tron&vs_currencies=usd', timeout=10)
            response.raise_for_status()

            data = response.json()
            result = {key: value['usd'] for key, value in data.items()}
            new_keys = list(currencies.keys())[:len(result)]
            new_result = dict(zip(new_keys, result.values()))

            if base_code in new_keys:
                response = new_result[base_code]
                base = currencies[base_code]
                res = (f" {response:.2f} USD\nза 1 {base}")
                int_part['text'] = res
            else:
                mb.showerror("Ошибка", f'Валюта "{base_code}" не найдена')
        except Timeout:
            mb.showerror("Ошибка",f"Сервер не отвечает.\n"
                                  f"Повторите попытку позже.")
        except requests.exceptions.RequestException as e:
            mb.showerror("Ошибка сети", f"О ш и б к а   с е т и: {str(e)}\n"
                                        f"\n П р о в е р ь т е   и н т е р н е т   с о е д и н е н и е")
        except Exception as e:
            mb.showerror("Ошибка", f"О ш и б к а: {e}")
    else:
        mb.showwarning("Внимание", "Выберите код валюты")


# Словарь тикеров и наименований криптовалют
currencies = {
    "BTC": "Bitcoin",
    "ETH": "Ethereum",
    "USDT": "Tether",
    "BNB": "BNB",
    "XRP": "XRP",
    "USDC": "USD Coin",
    "SOL": "Solana",
    "ADA": "Cardano",
    "DOGE": "Dogecoin",
    "TRX": "TRON"
}

# Создание графического интерфейса
window = Tk()
window.title("Курсы криптовалют")
window.geometry("360x320+1000+50")
icon_path = Path('icon.png')
if icon_path.exists():
    img = PhotoImage(file=icon_path)
    window.iconphoto(False, img)
else:
    print('Иконка не найдена, используется стандартная')

Label(text="Криптовалюта:", font='Comfortaa 15').pack(padx=10, pady=15)
base_combobox = ttk.Combobox(values=list(currencies.keys()))
base_combobox.config(font='Comfortaa 15')
base_combobox.pack(padx=10, pady=1)
base_combobox.set("BTC")
base_combobox.bind("<<ComboboxSelected>>", update_b_label)

b_label = ttk.Label(text=currencies[base_combobox.get()], font='Comfortaa 15')
b_label.pack(padx=10, pady=5)

Label(text="Текущий курс:", font='Comfortaa 15').pack(padx=10, pady=10)

int_part = Label(window, text='   ')
int_part.config(font='Comfortaa 15', justify='center', bg='lightgray', width=20)
int_part.pack(pady=5)

Button(text="Получить текущий курс", command=exchange, font='Comfortaa 15').pack(padx=10, pady=25)

window.mainloop()
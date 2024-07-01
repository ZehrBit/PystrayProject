# python 3.12.3
import PIL.Image
import pyautogui
import pystray
import winsound
import threading

# Флаг для остановки потока
stop_event = threading.Event()
search_thread = None


def on_click(icon, item):
    """Функция включает или выключает поиск кнопки на экране.
    Функция меняет значок в трее и меняет меню.
    Значок зелёный - поиск кнопки на экране активен
    Значок красный - поиск остановлен"""
    global name_item, menu_items, search_thread
    if str(item) == "Включить":
        icon.icon = PIL.Image.open('turbo_on.png')
        name_item = 'Выключить'
        menu_items[0] = pystray.MenuItem(text=name_item, action=on_click)
        icon.update_menu()
        stop_event.clear()  # Сбрасываем флаг остановки
        search_thread = threading.Thread(target=search_button_and_click)
        search_thread.start()
    elif str(item) == "Выключить":
        icon.icon = PIL.Image.open('turbo_off.png')
        name_item = 'Включить'
        menu_items[0] = pystray.MenuItem(text=name_item, action=on_click)
        icon.update_menu()
        stop_event.set()  # Устанавливаем флаг остановки
        if search_thread and search_thread.is_alive():
            try:
                search_thread.join()  # Ожидаем завершения потока
            except:
                pass
    elif str(item) == "Выход":
        stop_event.set()  # Устанавливаем флаг остановки при выходе
        if search_thread and search_thread.is_alive():
            search_thread.join()  # Ожидаем завершения потока
        icon.stop()


def search_button_and_click():
    """Ожидает пока на экране появятся 4 пикселя определённого цвета в определённых координатах.
    Функция рассчитана на экран 3840 x 2160
    Когда пиксели совпадают с условиями, то происходит клик со звуковым сигналом
    и программа останавливает поиск и переключает значок на красный"""
    button_coordinates = [1818, 1174]
    while not stop_event.is_set():
        try:
            if (pyautogui.pixelMatchesColor(1790, 1176, (66, 224, 66)) and
                    pyautogui.pixelMatchesColor(1809, 1166, (255, 255, 255)) and
                    pyautogui.pixelMatchesColor(1844, 1170, (66, 224, 66)) and
                    pyautogui.pixelMatchesColor(1815, 1200, (0, 121, 219))):
                pyautogui.click(button_coordinates[0], button_coordinates[1])
                break
        except:
            pass
    if not stop_event.is_set():  # Проверяем, был ли флаг остановки установлен
        winsound.Beep(1976, 50)
        winsound.Beep(1568, 50)
        winsound.Beep(1976, 50)
        winsound.Beep(1568, 50)
        on_click(icon, item='Выключить')


image = PIL.Image.open('turbo_off.png')
name_item = 'Включить'
menu_items = [pystray.MenuItem(text=name_item, action=on_click),
              pystray.MenuItem(text='Выход', action=on_click)]
icon = pystray.Icon(name='Turbo', icon=image, menu=pystray.Menu(lambda: menu_items))

icon.run()

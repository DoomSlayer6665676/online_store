import sqlite3
COMMANDS = "/clear - очистка терминала\n/del output -" \
           " очистка файла output\n/del input - очистка файла input\n/list - " \
           "список вещей на складе\n/??? - яйцо\n/database - связь со складом"
TABLE_NAME = "Список_продуктов"
TABLE_COLUMNS = ["id", "Предмет", "Количество", "Стоимость"]
IMAGE_NAME = './txt_and_jpg/High_resolution_wallpaper_background_ID_77700322238-1024x576.jpg'
CON = sqlite3.connect("Склад.db")
CUR = CON.cursor()
MISSING_ELEMENT = 'Нет такого предмета\n\n\nЧтобы добавить перейдите в терминал связи со складом'
LACK_OF_QUANTITY = 'Нет такого количества\n\n\nЧтобы заказать больше перейдите в терминал связи со складом'
LOCATION_OF_MP3_DOOM = './MP3/DOOM.mp3'
LOCATION_OF_MP3_box_office = './MP3/box_office.mp3'

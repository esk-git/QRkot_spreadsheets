LIFETIME_SECONDS_JWTSTRATEGY = int(3600)
MAX_LENGHT = int(100)
MIN_LENGHT = int(1)
MIN_LENGHT_PASSWORD = int(3)
LIST_TITLE = 'Лист1'
ROWS = int(100)
COLUMNS = int(11)
SPREADSHEET_BODY = {
    'properties': {'title': 'Отчёт',
                   'locale': 'ru_RU'},
    'sheets': [{'properties': {'sheetType': 'GRID',
                               'sheetId': 0,
                               'title': LIST_TITLE,
                               'gridProperties': {'rowCount': ROWS,
                                                  'columnCount': COLUMNS}}}]
}
SHEETS_NAME = 'sheets'
SHEETS_VER = 'v4'

DRIVE_VER = 'v3'
TABLE_VALUES = [
    ['Отчёт от', ],
    ['Топ проектов по скорости закрытие'],
    ['Название проекта', 'Время сбора', 'Описание']
]
FORMAT_TIME = "%Y/%m/%d %H:%M:%S"
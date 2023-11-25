from datetime import datetime
from copy import deepcopy

from aiogoogle import Aiogoogle
from app.core.config import settings
from app.core.constants import (DRIVE_VER,
                                FORMAT_TIME,
                                SHEETS_NAME,
                                SHEETS_VER,
                                SPREADSHEET_BODY,
                                TABLE_VALUES)


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    spreadsheet_body_copy = deepcopy(SPREADSHEET_BODY)
    now_date_time = datetime.now().strftime(FORMAT_TIME)
    service = await wrapper_services.discover(SHEETS_NAME, SHEETS_VER)
    spreadsheet_body_copy['properties']['title'] = f'Отчёт на {now_date_time}'
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body_copy)
    )
    spreadsheetid = response['spreadsheetId']
    return spreadsheetid


async def set_user_permissions(
        spreadsheetid: str,
        wrapper_services: Aiogoogle
) -> None:
    permissions_body = {'type': 'user',
                        'role': 'writer',
                        'emailAddress': settings.email}
    service = await wrapper_services.discover('drive', DRIVE_VER)
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheetid,
            json=permissions_body,
            fields="id"
        ))


async def spreadsheets_update_value(
        spreadsheetid: str,
        charity_projects: list,
        wrapper_services: Aiogoogle
) -> None:
    now_date_time = datetime.now().strftime(FORMAT_TIME)
    service = await wrapper_services.discover(SHEETS_NAME, SHEETS_VER)

    table_values = deepcopy(TABLE_VALUES)
    table_values[0].append(now_date_time)
    for project in charity_projects:
        new_row = [
            project.name,
            str(project.close_date - project.create_date),
            project.description
        ]
        table_values.append(new_row)

    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range='A1:E30',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )

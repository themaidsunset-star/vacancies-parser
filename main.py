import sqlite3
import httpx
import asyncio
connection = sqlite3.connect('vacancies.db')

cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS vacancies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    company TEXT NOT NULL,
    salary_from INTEGER NOT NULL,
    salary_to INTEGER,
    url TEXT NOT NULL UNIQUE,
    description TEXT,
    parsed_at TEXT NOT NULL,
    date INTEGER NOT NULL
)
''')

connection.commit()

connection.close()

async def fetch_vacancies():
    headers = {
        'User-Agent': 'MyJobParser/1.0 (my_email@example.com)'
    }
    params = {
        'text': 'Python Junior',
        'area': 1,
        'per_page': 100,
        'page': 0
    }
    url = 'https://api.hh.ru/vacancies'

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, params=params)

            if response.status_code == 200:
                data = response.json()
                print(f"Найдено: {data['found']}")

                for vacancy in data['items']:
                    print(f"[{vacancy['id']}] {vacancy['name']}")

            elif response.status_code == 403:
                print("403 Forbidden")

        except httpx.RequestError as e:
            print(f"Ошибка сети: {e}")

if __name__ == "__main__":
    asyncio.run(fetch_vacancies())
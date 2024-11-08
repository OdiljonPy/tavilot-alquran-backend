import gspread
from google.oauth2.service_account import Credentials
from collections import Counter
import json

SCOPE = ["https://www.googleapis.com/auth/spreadsheets"]

# JSON faylingiz yo'lini kiriting
creds = Credentials.from_service_account_file("oceanic-catcher-441013-i5-81e6f9afdfa2.json", scopes=SCOPE)

# Google Sheets API bilan bog'laning
client = gspread.authorize(creds)

# Google Sheets ID sini kiriting
sheet_id = '1YR6zo3dMgh0tO2pHBlogpJDgLK24MjdBY8y6OTSudAU'
sheet = client.open_by_key(sheet_id)

# Ma'lumotlarni olish
worksheet = sheet.sheet1
rows = worksheet.get_all_values()

# JSON formatida statistikani hisoblash
if rows:
    # Bosh satrni kalit sifatida olish
    headers = rows[0]
    data = rows[1:]

    # Statistikani saqlash uchun lug'at yaratish
    statistics = {}

    for i, question in enumerate(headers):
        # Har bir ustun (savol) bo'yicha javoblarni to'plash
        answers = [row[i] for row in data if row[i]]  # Har bir ustundan barcha javoblar
        answer_count = dict(Counter(answers))  # Javoblarni hisoblash
        statistics[question] = answer_count  # Statistikani lug'atga qo'shish

    # Statistikani JSON formatida chop etish
    print(json.dumps(statistics, indent=4, ensure_ascii=False))
else:
    print("Sheetda ma'lumot yo'q")

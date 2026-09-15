import os
import asyncio
from threading import Thread
from flask import Flask

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, FSInputFile, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# --- 1. RENDER PORT BINDING UCHUN FLASK SERVER ---
app = Flask('')

@app.route('/')
def home():
    return "Rezyume Bot muvaffaqiyatli ishlamoqda!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run_flask)
    t.daemon = True
    t.start()

# --- 2. TELEGRAM BOT BOT_TOKEN SOZLAMASI ---
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8895389668:AAHKkjNuIlpjylzQPVBQgCmqegHQCA2hbxU")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# FSM holatlari
class ResumeForm(StatesGroup):
    first_name = State()
    last_name = State()
    birth_date = State()
    photo = State()
    email = State()
    phone = State()
    city = State()
    summary = State()
    experience = State()
    education = State()
    skills = State()
    languages = State()
    certificates = State()
    bad_habits = State()
    driving_license = State()
    expected_salary = State()

# Tugmalar
def skip_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="O'tkazib yuborish ➡️")]],
        resize_keyboard=True,
        one_time_keyboard=True
    )

def habits_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Yo'q (Zararli odatlarim yo'q)")],
            [KeyboardButton(text="Chekish"), KeyboardButton(text="Alkogol")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

def license_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Yo'q"), KeyboardButton(text="B toifa")],
            [KeyboardButton(text="B, C toifa"), KeyboardButton(text="A, B, C, D toifa")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

# /start komandasi
@dp.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "👋 Assalomu alaykum!\n\n"
        "Professional rezyume tayyorlash botiga xush kelibsiz.\n"
        "Ish beruvchi uchun to'liq va sifatli rezyume yaratamiz.\n\n"
        "Boshlash uchun **Ismingizni** kiriting:"
    )
    await state.set_state(ResumeForm.first_name)

# 1. Ism
@dp.message(ResumeForm.first_name)
async def process_first_name(message: Message, state: FSMContext):
    await state.update_data(first_name=message.text)
    await message.answer("Familiyangizni kiriting:")
    await state.set_state(ResumeForm.last_name)

# 2. Familiya
@dp.message(ResumeForm.last_name)
async def process_last_name(message: Message, state: FSMContext):
    await state.update_data(last_name=message.text)
    await message.answer("Tug'ilgan sanangiz va yilingizni kiriting (Masalan: 15.05.1998):")
    await state.set_state(ResumeForm.birth_date)

# 3. Tug'ilgan sana
@dp.message(ResumeForm.birth_date)
async def process_birth_date(message: Message, state: FSMContext):
    await state.update_data(birth_date=message.text)
    await message.answer(
        "📷 Rezyume uchun rasmingizni yuboring:\n"
        "(Galereyadan rasmingizni yoki hozir kameraga tushib yuborishingiz mumkin)",
        reply_markup=skip_keyboard()
    )
    await state.set_state(ResumeForm.photo)

# 4. Rasm
@dp.message(ResumeForm.photo)
async def process_photo(message: Message, state: FSMContext):
    os.makedirs("downloads", exist_ok=True)
    
    if message.photo:
        photo = message.photo[-1]
        file_path = f"downloads/{message.from_user.id}.jpg"
        await bot.download(photo, destination=file_path)
        await state.update_data(photo=file_path)
    else:
        await state.update_data(photo=None)

    await message.answer(
        "Email manzilingizni kiriting:",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(ResumeForm.email)

# 5. Email
@dp.message(ResumeForm.email)
async def process_email(message: Message, state: FSMContext):
    await state.update_data(email=message.text)
    await message.answer("Telefon raqamingizni kiriting (Masalan: +998901234567):")
    await state.set_state(ResumeForm.phone)

# 6. Telefon
@dp.message(ResumeForm.phone)
async def process_phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await message.answer("Hozirda qaysi shahar/tumanda yashaysiz?")
    await state.set_state(ResumeForm.city)

# 7. Shahar
@dp.message(ResumeForm.city)
async def process_city(message: Message, state: FSMContext):
    await state.update_data(city=message.text)
    await message.answer(
        "O'zingiz haqingizda qisqacha xulosa (Professional summary) yozing:\n"
        "*(Maqsadingiz, kuchli tomonlaringiz va qaysi sohada mutaxassisligingiz haqida)*"
    )
    await state.set_state(ResumeForm.summary)

# 8. Summary
@dp.message(ResumeForm.summary)
async def process_summary(message: Message, state: FSMContext):
    await state.update_data(summary=message.text)
    await message.answer(
        "💼 **Ish tajribangiz (Oldingi ishlagan joylaringiz):**\n\n"
        "Qaysi kompaniyalarda, qaysi lavozimda va qaysi yillarda ishlaganingizni batafsil yozing.\n"
        "*(Masalan: 2021-2023: 'Texno-Market' MCHJ - Sotuvchi maslahatchi)*",
        reply_markup=skip_keyboard()
    )
    await state.set_state(ResumeForm.experience)

# 9. Ish tajribasi
@dp.message(ResumeForm.experience)
async def process_experience(message: Message, state: FSMContext):
    exp = message.text if message.text != "O'tkazib yuborish ➡️" else "Ko'rsatilmagan"
    await state.update_data(experience=exp)
    await message.answer(
        "🎓 **Ta'lim va O'qigan joylaringiz:**\n\n"
        "Qaysi universitet, litsey, kollej yoki maktabni bitirgansiz va mutaxassisligingiz nima?\n"
        "*(Masalan: 2019-2023: Farg'ona Davlat Universiteti - Kompyuter injiniringi)*",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(ResumeForm.education)

# 10. Ta'lim
@dp.message(ResumeForm.education)
async def process_education(message: Message, state: FSMContext):
    await state.update_data(education=message.text)
    await message.answer(
        "🛠 **Ko'nikma va vositalaringiz (Skills):**\n"
        "Qanday kompyuter dasturlari, texnik bilimlar va qobiliyatlarga egasiz?\n"
        "*(Masalan: Python, HTML/CSS, MS Office, 1S Buxgalteriya, Muloqotga kirishuvchanlik)*"
    )
    await state.set_state(ResumeForm.skills)

# 11. Ko'nikmalar
@dp.message(ResumeForm.skills)
async def process_skills(message: Message, state: FSMContext):
    await state.update_data(skills=message.text)
    await message.answer(
        "🌐 **Qaysi tillarni bilasiz?**\n"
        "*(Masalan: O'zbek tili (Ona tili), Rus tili (A'lo), Ingliz tili (B2))* "
    )
    await state.set_state(ResumeForm.languages)

# 12. Tillar
@dp.message(ResumeForm.languages)
async def process_languages(message: Message, state: FSMContext):
    await state.update_data(languages=message.text)
    await message.answer(
        "📜 **Sertifikatlar va o'quv kurslari:**\n"
        "Qanday o'quv kurslarini bitirgansiz yoki sertifikatlaringiz bor?\n"
        "*(Masalan: IT-Park Python kurs sertifikati, IELTS 6.5)*",
        reply_markup=skip_keyboard()
    )
    await state.set_state(ResumeForm.certificates)

# 13. Sertifikatlar
@dp.message(ResumeForm.certificates)
async def process_certificates(message: Message, state: FSMContext):
    cert = message.text if message.text != "O'tkazib yuborish ➡️" else "Mavjud emas"
    await state.update_data(certificates=cert)
    await message.answer(
        "🚬 **Zararli odatlaringiz bormi?**",
        reply_markup=habits_keyboard()
    )
    await state.set_state(ResumeForm.bad_habits)

# 14. Zararli odatlar
@dp.message(ResumeForm.bad_habits)
async def process_bad_habits(message: Message, state: FSMContext):
    await state.update_data(bad_habits=message.text)
    await message.answer(
        "🚗 **Haydovchilik guvohnomangiz (Prava) bormi?**",
        reply_markup=license_keyboard()
    )
    await state.set_state(ResumeForm.driving_license)

# 15. Haydovchilik guvohnomasi
@dp.message(ResumeForm.driving_license)
async def process_license(message: Message, state: FSMContext):
    await state.update_data(driving_license=message.text)
    await message.answer(
        "💰 **Kutilayotgan maosh miqdori:**\n"
        "*(Masalan: 5,000,000 so'm yoki Kelishilgan holda)*",
        reply_markup=skip_keyboard()
    )
    await state.set_state(ResumeForm.expected_salary)

# 16. Maosh va PDF Yaratish
@dp.message(ResumeForm.expected_salary)
async def process_salary(message: Message, state: FSMContext):
    sal = message.text if message.text != "O'tkazib yuborish ➡️" else "Kelishiladi"
    await state.update_data(expected_salary=sal)
    
    data = await state.get_data()
    
    await message.answer("⏳ Rezyumeingiz shakllantirilmoqda, iltimos kuting...", reply_markup=ReplyKeyboardRemove())

    pdf_filename = f"downloads/resume_{message.from_user.id}.pdf"
    
    # PDF Yaratish
    generate_pdf(data, pdf_filename)
    
    # PDF yuborish
    doc = FSInputFile(pdf_filename)
    await message.answer_document(doc, caption="✅ Rezyumeingiz muvaffaqiyatli tayyorlandi!")
    
    # Vaqtincha fayllarni tozalash
    if os.path.exists(pdf_filename):
        os.remove(pdf_filename)
    if data.get("photo") and os.path.exists(data["photo"]):
        os.remove(data["photo"])

    await state.clear()

# PDF Generator Funksiyasi
def generate_pdf(data, filename):
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )
    story = []
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=18, textColor=colors.HexColor('#1a3a52'))
    heading_style = ParagraphStyle('HeadingStyle', parent=styles['Heading2'], fontSize=12, textColor=colors.HexColor('#1a3a52'), spaceBefore=10, spaceAfter=4)
    body_style = ParagraphStyle('BodyStyle', parent=styles['Normal'], fontSize=10, leading=14)

    birth_date_text = data.get('birth_date', 'Ko\'rsatilmagan')
    expected_salary_text = data.get('expected_salary', 'Kelishiladi')

    header_data = []
    text_info = f"<b><font size=15>{data.get('first_name', '')} {data.get('last_name', '')}</font></b><br/><br/>" \
                f"<b>Tug'ilgan sana:</b> {birth_date_text}<br/>" \
                f"<b>Manzil:</b> {data.get('city', '')}<br/>" \
                f"<b>Tel:</b> {data.get('phone', '')}<br/>" \
                f"<b>Email:</b> {data.get('email', '')}<br/>" \
                f"<b>Kutilayotgan maosh:</b> {expected_salary_text}"
    
    p_info = Paragraph(text_info, body_style)

    if data.get("photo") and os.path.exists(data["photo"]):
        img = RLImage(data["photo"], width=105, height=130)
        header_data.append([img, p_info])
        col_widths = [115, 395]
    else:
        header_data.append([p_info])
        col_widths = [510]

    header_table = Table(header_data, colWidths=col_widths)
    header_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10)
    ]))
    story.append(header_table)
    story.append(Spacer(1, 10))

    def add_section(title, content):
        if content:
            story.append(Paragraph(title.upper(), heading_style))
            formatted_content = str(content).replace('\n', '<br/>')
            story.append(Paragraph(formatted_content, body_style))
            story.append(Spacer(1, 8))

    add_section("Professional Xulosa", data.get("summary"))
    add_section("Ish Tajribasi", data.get("experience"))
    add_section("Ta'lim va Ma'lumoti", data.get("education"))
    add_section("Ko'nikmalar va Dasturlar", data.get("skills"))
    add_section("Chet tillari", data.get("languages"))
    add_section("Sertifikatlar va Kurslar", data.get("certificates"))

    bad_habits_text = data.get('bad_habits', 'Yo\'q')
    driving_license_text = data.get('driving_license', 'Yo\'q')
    
    extra_info = f"<b>Zararli odatlar:</b> {bad_habits_text}<br/>" \
                 f"<b>Haydovchilik guvohnomasi:</b> {driving_license_text}"
    add_section("Qo'shimcha Ma'lumotlar", extra_info)

    doc.build(story)

# --- 4. ISHGA TUSHIRISH ---
async def main():
    print("Bot muvaffaqiyatli ishga tushdi...")
    keep_alive()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

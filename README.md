# 🧹 Hite Discord Cleaner (v1.0)

<p align="center">
  <b>A blazing-fast, safe, and modern CLI utility to clean, sanitize, and wipe your Discord account.</b><br>
  ابزار خط فرمان پیشرفته، پرسرعت و امن برای پاکسازی، خروج از سرورها، حذف دوستان و دایرکت‌های اکانت دیسکورد.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.10+" />
  <img src="https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge" alt="License: MIT" />
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-0284c7?style=for-the-badge" alt="Platform" />
  <img src="https://img.shields.io/badge/Developer-HikaruIR-8b5cf6?style=for-the-badge" alt="Developer" />
</p>

---

## 📑 Table of Contents | فهرست مطالب

1. [Features | ویژگی‌ها](#-features--ویژگی‌ها)
2. [Prerequisites | پیش‌نیازها](#-prerequisites--پیش‌نیازها)
3. [How to Download | راهنمای دانلود](#-how-to-download--راهنمای-دانلود)
4. [How to get Discord User Token | آموزش دریافت توکن](#-how-to-get-discord-user-token--آموزش-دریافت-توکن)
5. [Installation & Running | نحوه نصب و اجرا](#-installation--running--نحوه-نصب-و-اجرا)
6. [Build Standalone EXE | ساخت فایل اجرایی](#-build-standalone-exe--ساخت-فایل-اجرایی-exe)
7. [Troubleshooting | رفع مشکلات احتمالی](#-troubleshooting--رفع-مشکلات-احتمالی)
8. [License & Disclaimer | لایسنس و سلب مسئولیت](#-license--disclaimer--لایسنس-و-سلب-مسئولیت)

---

## ✨ Features | ویژگی‌ها

- 📩 **Close Direct Messages (DMs & Group DMs):** بستن و مخفی‌سازی تمام دایرکت‌ها و گروه‌های چت خصوصی.
- 🗑️ **Sweep Sent Messages:** جستجو و حذف کامل پیام‌های ارسالی توسط اکانت در چت‌ها و چنل‌ها.
- 👥 **Remove Friends & Pending Requests:** آنفرند کردن تمام ادلیست و لغو درخواست‌های دوستی معلق (ارسال شده یا دریافتی).
- 🚪 **Leave Joined Guilds:** لفت دادن خودکار از تمام سرورهایی که در آنها عضو هستید.
- 💥 **Delete Owned Guilds:** حذف کامل سرورهایی که مالکیت (Owner) آنها با اکانت شماست.
- ☢️ **Full Purge (Nuke Mode):** اجرای تمام گزینه‌های بالا به‌صورت متوالی و خودکار در یک عملیات جامع.
- 🛡️ **Two-Factor Safety Confirmation:** الزام به تایپ کلمه `CONFIRM` برای جلوگیری از دستکاری‌های اشتباهی و تصادفی.
- ⏳ **Smart Rate-Limit Backoff:** هندل خودکار محدودیت‌های شبکه دیسکورد (HTTP 429) همراه با مکث هوشمند جهت حفظ امنیت اکانت.
- 🎨 **Modern Dark Minimalist UI:** محیط ترمینالی شیک، مدرن با پشتیبانی کامل از UTF-8 و فونت‌های مدرن.

---

## 📋 Prerequisites | پیش‌نیازها

قبل از شروع، مطمئن شوید موارد زیر را آماده دارید:

1. **پایتون نسخه 3.10 یا بالاتر (Python 3.10+):**
   - دانلود از سایت رسمی: [python.org/downloads](https://www.python.org/downloads/)
   - ⚠️ **نکته بسیار مهم هنگام نصب:** حتماً در صفحه اول نصب، تیک گزینه **`Add python.exe to PATH`** را بزنید!
2. **توکن کاربری دیسکورد (Discord User Token):**
   - جهت دسترسی و اجرای فرامین در دیسکورد (راهنمای استخراج در پایین توضیح داده شده است).
3. **سیستم‌عامل:** ویندوز ۱۰/۱۱، لینوکس یا macOS.

---

## 📥 How to Download | راهنمای دانلود

### روش اول: دانلود مستقیم فایل فشرده ZIP (ساده‌ترین روش)
1. در بالای همین صفحه گیت‌هاب، روی دکمه سبز رنگ **Code** کلیک کنید.
2. گزینه **Download ZIP** را بزنید.
3. فایل دانلود شده را با راست‌کلیک و انتخاب `Extract All...` از حالت فشرده خارج کنید.

### روش دوم: با استفاده از Git (برای برنامه‌نویسان)
ترمینال را باز کرده و دستور زیر را اجرا کنید:
```bash
git clone https://github.com/HikaruIR/HiteDiscordCleaner.git
cd HiteDiscordCleaner
```

---

## 🔑 How to get Discord User Token | آموزش دریافت توکن

1. مرورگر خود (Chrome / Firefox / Brave / Edge) را باز کنید و وارد اکانت [Discord Web](https://discord.com/app) شوید.
2. کلیدهای ترکیبی `Ctrl + Shift + I` (یا کلید `F12`) را فشار دهید تا پنل **Developer Tools** باز شود.
3. از تب‌های بالای پنل، وارد تب **Network** شوید.
4. در کادر جستجو/فیلتر، عبارت `/api` را تایپ کنید.
5. در صفحه دیسکورد یک چت، چنل یا پروفایل را باز کنید تا تب تبادلات شبکه فعال شود.
6. روی یکی از درخواست‌ها (مانند `messages` یا `users/@me`) کلیک کنید.
7. در پنجره سمت راست زیر بخش **Headers**، به قسمت **Request Headers** بروید.
8. مقدار موجود در مقابل عبارت **`Authorization`** را کپی کنید. این عبارت همان **User Token** شماست.

> 🔒 **نکته امنیتی:** توکن دیسکورد شما مانند رمز عبور دوم اکانت شماست. هرگز آن را برای افراد دیگر ارسال نکنید!

---

## 🚀 Installation & Running | نحوه نصب و اجرا

### ⚡ روش اول: اجرای تک‌کلیک و خودکار با `run.bat` (پیشنهادی برای ویندوز)

فقط کافیست روی فایل **`run.bat`** دابل کلیک کنید! این اسکریپت:
- نسخه مناسب پایتون (`py` یا `python`) را شناسایی می‌کند.
- محیط مجازی ایزوله (`.venv`) می‌سازد.
- تمام وابستگی‌ها (`rich` و `requests`) را خودکار نصب می‌کند.
- کدپیج ترمینال را روی UTF-8 تنظیم کرده و برنامه را بدون کرش اجرا می‌کند.

---

### 💻 روش دوم: اجرای دستی از طریق ترمینال (ویندوز / لینوکس / مک)

```bash
# ۱. رفتن به پوشه پروژه
cd HiteDiscordCleaner

# ۲. ایجاد محیط مجازی ایزوله
python -m venv .venv

# ۳. فعال‌سازی محیط مجازی
# در ویندوز (PowerShell یا CMD):
.venv\Scripts\activate
# در لینوکس یا مک:
source .venv/bin/activate

# ۴. نصب کتابخانه‌های مورد نیاز
pip install -r requirements.txt

# ۵. اجرای برنامه
python main.py
```

---

## 📦 Build Standalone EXE | ساخت فایل اجرایی EXE

اگر می‌خواهید این برنامه را بدون نیاز به پایتون، روی هر سیستمی به عنوان یک فایل `.exe` مستقل اجرا کنید:

کافیست فایل **`build_exe.bat`** را اجرا کنید.
اسکریپت به صورت خودکار `PyInstaller` را تنظیم کرده و فایل خروجی را در پوشه زیر تحویل می‌دهد:
```
dist/HiteDiscordCleaner.exe
```

---

## 🛠️ Troubleshooting | رفع مشکلات احتمالی

#### ۱. ارور `Python was not found...` یا هدایت به مایکروسافت استور
- **دلیل:** مسیر پایتون در PATH تنظیم نشده یا میانبر App Execution Aliases ویندوز فعال است.
- **راه‌حل:** منوی Start را باز کرده و سرچ کنید `Manage app execution aliases`، سپس گزینه‌های `App Installer (python.exe)` و `python3.exe` را خاموش (OFF) کنید. همچنین می‌توانید دستور را با `py main.py` اجرا کنید.

#### ۲. ارور `ModuleNotFoundError: No module named 'rich'`
- **راه‌حل:** کتابخانه‌ها در محیط جاری نصب نشده‌اند. کافیست اسکریپت `run.bat` را اجرا کنید تا خودکار نصب شوند، یا دستور `pip install -r requirements.txt` را داخل ترمینال بزنید.

#### ۳. بسته شدن ناگهانی ترمینال
- **راه‌حل:** در آخرین آپدیت، تمام باگ‌های کدپیج ویندوز و پرانتزهای بچ‌فایل رفع شده است. مطمئن شوید آخرین نسخه مخزن را دریافت کرده‌اید و فایل `run.bat` را اجرا می‌کنید.

---

## 📜 License & Disclaimer | لایسنس و سلب مسئولیت

### License
این پروژه تحت پروانه متن‌باز **[MIT License](LICENSE)** منتشر شده است. استفاده، ویرایش و توسعه آن با حفظ نام صاحب اثر آزاد است:
```text
Copyright (c) 2026 HikaruIR
```

### Disclaimer
این ابزار صرفاً جهت مدیریت و پاکسازی امن اکانت‌های شخصی توسعه داده شده است. مسئولیت استفاده نادرست، اسپم یا نقض قوانین سرویس‌دهی دیسکورد (ToS) تماماً بر عهده کاربر استفاده‌کننده می‌باشد.
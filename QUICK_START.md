# ⚡ התחלה מהירה - 5 דקות

מדריך קצר וממוקד להתחלה מהירה.

## 🎯 שלבים מהירים

### 1️⃣ בדיקת דרישות (30 שניות)

```bash
# בדוק Python
python3 --version
# צריך: Python 3.10 או גבוה יותר

# בדוק FFmpeg (אופציונלי - רק להורדת אודיו)
ffmpeg -version
```

### 2️⃣ שכפול הפרויקט (1 דקה)

```bash
git clone https://github.com/ZyrticX/YTDLPFIXED1.git
cd YTDLPFIXED1
```

### 3️⃣ התקנת תלויות (2 דקות)

```bash
# Windows
pip install -r requirements_api.txt

# Linux/macOS
pip3 install -r requirements_api.txt
```

### 4️⃣ הגדרת Supabase (3 דקות)

1. **צור חשבון**: [supabase.com](https://supabase.com) → Start your project
2. **צור פרויקט**: New Project → בחר שם ואזור
3. **קבל פרטים**: Settings → API → העתק:
   - Project URL
   - anon public key
4. **צור Bucket**: Storage → New bucket → שם: `videos` → Public ✅

### 5️⃣ הגדרת .env (1 דקה)

```bash
# העתק תבנית
cp config.env.example .env

# ערוך את הקובץ
# Windows: notepad .env
# Linux/macOS: nano .env
```

עדכן את הערכים:
```env
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
SUPABASE_BUCKET=videos
```

### 6️⃣ הפעלה (10 שניות)

```bash
python3 api_server.py
```

✅ **השרת פועל על `http://localhost:5000`**

## 🧪 בדיקה מהירה

פתח בדפדפן:
```
http://localhost:5000/health
```

או פתח את `test_api.html` בדפדפן.

## 📖 מה הלאה?

- **מדריך מפורט**: [START_HERE.md](START_HERE.md)
- **מדריך API**: [API_GUIDE_HE.md](API_GUIDE_HE.md)
- **התקנה על שרת**: [DEPLOYMENT_GUIDE_HE.md](DEPLOYMENT_GUIDE_HE.md)

## 🆘 בעיות?

ראה [פתרון בעיות ב-START_HERE.md](START_HERE.md#פתרון-בעיות)


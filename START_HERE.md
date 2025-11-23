# 🚀 מדריך התחלה מלא - yt-dlp API עם Supabase

מדריך שלב-אחר-שלב להתקנה והפעלה מלאה של הפרויקט.

---

## 📋 תוכן עניינים

1. [דרישות מערכת](#דרישות-מערכת)
2. [שלב 1: התקנת Python](#שלב-1-התקנת-python)
3. [שלב 2: התקנת FFmpeg](#שלב-2-התקנת-ffmpeg)
4. [שלב 3: שכפול הפרויקט](#שלב-3-שכפול-הפרויקט)
5. [שלב 4: התקנת תלויות Python](#שלב-4-התקנת-תלויות-python)
6. [שלב 5: הגדרת Supabase](#שלב-5-הגדרת-supabase)
7. [שלב 6: הגדרת קובץ .env](#שלב-6-הגדרת-קובץ-env)
8. [שלב 7: הפעלת השרת](#שלב-7-הפעלת-השרת)
9. [שלב 8: בדיקת השרת](#שלב-8-בדיקת-השרת)
10. [שלב 9: שימוש ב-API](#שלב-9-שימוש-ב-api)

---

## דרישות מערכת

### Windows:
- Windows 10/11
- Python 3.10 או גבוה יותר
- FFmpeg

### Linux/Ubuntu:
- Ubuntu 18.04 או גבוה יותר
- Python 3.10 או גבוה יותר
- FFmpeg

### macOS:
- macOS 10.15 או גבוה יותר
- Python 3.10 או גבוה יותר
- FFmpeg

---

## שלב 1: התקנת Python

### Windows:

1. הורד Python מ-[python.org](https://www.python.org/downloads/)
2. התקן Python (ודא שסימנת "Add Python to PATH")
3. פתח Command Prompt או PowerShell
4. בדוק שההתקנה הצליחה:

```cmd
python --version
```

אמור להציג: `Python 3.10.x` או גבוה יותר

### Linux/Ubuntu:

```bash
# עדכון רשימת חבילות
sudo apt update

# התקנת Python 3
sudo apt install python3 python3-pip

# בדיקה
python3 --version
```

### macOS:

```bash
# עם Homebrew
brew install python3

# או הורד מ-python.org
# בדיקה
python3 --version
```

---

## שלב 2: התקנת FFmpeg

FFmpeg נדרש להורדת אודיו (MP3).

### Windows:

1. הורד FFmpeg מ-[ffmpeg.org](https://ffmpeg.org/download.html)
2. חלץ את הקובץ לתיקייה (למשל `C:\ffmpeg`)
3. הוסף את התיקייה ל-PATH:
   - לחץ ימני על "This PC" → Properties
   - Advanced system settings → Environment Variables
   - הוסף `C:\ffmpeg\bin` ל-Path
4. פתח Command Prompt חדש ובדוק:

```cmd
ffmpeg -version
```

### Linux/Ubuntu:

```bash
sudo apt update
sudo apt install ffmpeg

# בדיקה
ffmpeg -version
```

### macOS:

```bash
brew install ffmpeg

# בדיקה
ffmpeg -version
```

---

## שלב 3: שכפול הפרויקט

### אפשרות 1: עם Git

```bash
# שכפול מה-GitHub
git clone https://github.com/ZyrticX/YTDLPFIXED1.git
cd YTDLPFIXED1
```

### אפשרות 2: הורדה כ-ZIP

1. לך ל-[GitHub Repository](https://github.com/ZyrticX/YTDLPFIXED1)
2. לחץ על "Code" → "Download ZIP"
3. חלץ את הקובץ
4. פתח Terminal/Command Prompt בתיקייה

---

## שלב 4: התקנת תלויות Python

### Windows:

```cmd
cd YTDLPFIXED1
pip install -r requirements_api.txt
```

אם יש שגיאה, נסה:

```cmd
python -m pip install --upgrade pip
python -m pip install -r requirements_api.txt
```

### Linux/macOS:

```bash
cd YTDLPFIXED1
pip3 install -r requirements_api.txt
```

אם יש שגיאה, נסה:

```bash
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements_api.txt
```

### בדיקה שהכל הותקן:

```bash
# Windows
python -c "import flask, yt_dlp, supabase; print('✅ כל התלויות מותקנות!')"

# Linux/macOS
python3 -c "import flask, yt_dlp, supabase; print('✅ כל התלויות מותקנות!')"
```

אם אין שגיאה - הכל תקין! ✅

---

## שלב 5: הגדרת Supabase

### 5.1 יצירת חשבון Supabase

1. לך ל-[supabase.com](https://supabase.com)
2. לחץ על "Start your project"
3. היכנס עם GitHub/Google או צור חשבון חדש

### 5.2 יצירת פרויקט חדש

1. לחץ על "New Project"
2. מלא את הפרטים:
   - **Name**: שם הפרויקט (למשל: `yt-dlp-api`)
   - **Database Password**: בחר סיסמה חזקה (שמור אותה!)
   - **Region**: בחר אזור קרוב אליך
3. לחץ "Create new project"
4. המתן 2-3 דקות עד שהפרויקט מוכן

### 5.3 קבלת פרטי API

1. בפרויקט שלך, לך ל-**Settings** (⚙️) בתפריט השמאלי
2. לחץ על **API**
3. תמצא שני ערכים חשובים:
   - **Project URL** - נראה כך: `https://xxxxx.supabase.co`
   - **anon public** key - מפתח ארוך שמתחיל ב-`eyJ...`

📝 **שמור את שני הערכים האלה - נצטרך אותם בהמשך!**

### 5.4 יצירת Storage Bucket

1. בתפריט השמאלי, לחץ על **Storage**
2. לחץ על **New bucket**
3. מלא את הפרטים:
   - **Name**: `videos` (או כל שם אחר שתרצה)
   - **Public bucket**: ✅ סמן את זה אם אתה רוצה גישה ציבורית לקבצים
4. לחץ **Create bucket**

### 5.5 הגדרת Policies (הרשאות)

1. ב-Storage, לחץ על ה-bucket שיצרת (`videos`)
2. לחץ על **Policies** (בתפריט העליון)
3. לחץ על **New Policy**

**Policy 1 - הוספת קבצים (INSERT):**

- **Policy name**: `Allow authenticated uploads`
- **Allowed operation**: `INSERT`
- **Target roles**: `authenticated` (או `anon` אם אתה רוצה גישה ציבורית)
- **USING expression**: השאר ריק או `true`
- **WITH CHECK expression**: `bucket_id = 'videos'`

לחץ **Review** ואז **Save policy**

**Policy 2 - קריאת קבצים (SELECT):**

- **Policy name**: `Allow public read access`
- **Allowed operation**: `SELECT`
- **Target roles**: `public`
- **USING expression**: `bucket_id = 'videos'`

לחץ **Review** ואז **Save policy**

✅ **Supabase מוכן!**

---

## שלב 6: הגדרת קובץ .env

### 6.1 יצירת הקובץ

**Windows:**

```cmd
copy config.env.example .env
notepad .env
```

**Linux/macOS:**

```bash
cp config.env.example .env
nano .env
```

### 6.2 עדכון הערכים

פתח את הקובץ `.env` ועדכן את הערכים הבאים:

```env
# העתק את ה-Project URL מ-Supabase
SUPABASE_URL=https://xxxxx.supabase.co

# העתק את ה-anon public key מ-Supabase
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# שם ה-bucket שיצרת (ברירת מחדל: videos)
SUPABASE_BUCKET=videos

# פורט השרת (ברירת מחדל: 5000)
PORT=5000

# מצב debug (false לייצור, true לפיתוח)
DEBUG=False
```

**דוגמה לקובץ .env מלא:**

```env
SUPABASE_URL=https://abcdefghijklmnop.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFiY2RlZmdoaWprbG1ub3AiLCJyb2xlIjoiYW5vbiIsImlhdCI6MTYzODk2NzI5MCwiZXhwIjoxOTU0NTQzMjkwfQ.abcdefghijklmnopqrstuvwxyz1234567890
SUPABASE_BUCKET=videos
PORT=5000
DEBUG=False
```

💾 **שמור את הקובץ**

---

## שלב 7: הפעלת השרת

### Windows:

```cmd
python api_server.py
```

### Linux/macOS:

```bash
python3 api_server.py
```

### מה אמור לקרות:

```
INFO - Starting API server on port 5000
INFO - Debug mode: False
 * Running on http://0.0.0.0:5000
INFO - ✅ Supabase client initialized successfully
```

✅ **השרת פועל!**

אם אתה רואה שגיאה, עיין ב[פתרון בעיות](#פתרון-בעיות) למטה.

---

## שלב 8: בדיקת השרת

### בדיקה 1: Health Check

פתח דפדפן או Terminal ונסה:

**דפדפן:**
```
http://localhost:5000/health
```

**Terminal (curl):**
```bash
curl http://localhost:5000/health
```

**תגובה צפויה:**
```json
{
  "status": "ok",
  "supabase_configured": true,
  "temp_dir": "/tmp/yt-dlp-downloads"
}
```

### בדיקה 2: עם דף HTML

1. פתח את הקובץ `test_api.html` בדפדפן
2. ודא שה-API URL הוא: `http://localhost:5000`
3. הכנס כתובת YouTube
4. לחץ "הורד והעלה"

---

## שלב 9: שימוש ב-API

### דוגמה 1: הורדת וידאו

**JavaScript:**

```javascript
const response = await fetch('http://localhost:5000/download', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    url: 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
    format: 'video',
    upload_to_supabase: true
  })
});

const data = await response.json();
console.log('Video URL:', data.upload.public_url);
```

**cURL:**

```bash
curl -X POST http://localhost:5000/download \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "format": "video",
    "upload_to_supabase": true
  }'
```

### דוגמה 2: הורדת אודיו (MP3)

```javascript
const response = await fetch('http://localhost:5000/download', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    url: 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
    format: 'audio',
    upload_to_supabase: true
  })
});

const data = await response.json();
console.log('Audio URL:', data.upload.public_url);
```

### דוגמה 3: קבלת מידע על סרטון (ללא הורדה)

```javascript
const response = await fetch('http://localhost:5000/info', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    url: 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
  })
});

const data = await response.json();
console.log('Title:', data.info.title);
console.log('Duration:', data.info.duration);
```

---

## 🎉 סיכום - מה יש לך עכשיו?

✅ שרת API פועל על `http://localhost:5000`  
✅ יכולת להוריד סרטונים מ-YouTube ואתרים אחרים  
✅ העלאה אוטומטית ל-Supabase Storage  
✅ תמיכה בוידאו ואודיו  
✅ API מוכן לשימוש באתר שלך  

---

## 🛠️ פתרון בעיות

### שגיאה: "ModuleNotFoundError: No module named 'flask'"

**פתרון:**
```bash
pip3 install -r requirements_api.txt
```

### שגיאה: "Supabase client not initialized"

**פתרון:**
1. ודא שקובץ `.env` קיים
2. ודא שהערכים `SUPABASE_URL` ו-`SUPABASE_KEY` נכונים
3. ודא שאין רווחים מיותרים בערכים

### שגיאה: "ffmpeg not found"

**פתרון:**
- Windows: ודא ש-FFmpeg ב-PATH
- Linux: `sudo apt install ffmpeg`
- macOS: `brew install ffmpeg`

### שגיאה: "Permission denied" ב-Supabase

**פתרון:**
1. ודא שיצרת bucket ב-Storage
2. בדוק את ה-Policies ב-Storage → Policies
3. ודא שה-bucket הוא public או שיש לך הרשאות

### השרת לא עולה

**פתרון:**
1. בדוק שהפורט 5000 לא תפוס:
   ```bash
   # Windows
   netstat -ano | findstr :5000
   
   # Linux/macOS
   lsof -i :5000
   ```
2. נסה לשנות את הפורט ב-`.env`:
   ```env
   PORT=5001
   ```

---

## 📚 משאבים נוספים

- [API_GUIDE_HE.md](API_GUIDE_HE.md) - מדריך API מלא
- [DEPLOYMENT_GUIDE_HE.md](DEPLOYMENT_GUIDE_HE.md) - התקנה על שרת
- [README_API_HE.md](README_API_HE.md) - התחלה מהירה

---

## 💬 תמיכה

אם נתקלת בבעיה:

1. בדוק את [פתרון בעיות](#פתרון-בעיות) למעלה
2. פתח Issue ב-[GitHub](https://github.com/ZyrticX/YTDLPFIXED1/issues)
3. עיין ב-[תיעוד yt-dlp](https://github.com/yt-dlp/yt-dlp#readme)

---

**בהצלחה! 🚀**


# 🚀 התחלה מההתחלה - מדריך מלא

מדריך שלב-אחר-שלב להתקנה והפעלה של yt-dlp API Server עם Supabase.

---

## 📋 תוכן עניינים

1. [דרישות מוקדמות](#דרישות-מוקדמות)
2. [שלב 1: התקנת Python](#שלב-1-התקנת-python)
3. [שלב 2: התקנת FFmpeg](#שלב-2-התקנת-ffmpeg)
4. [שלב 3: שכפול הפרויקט](#שלב-3-שכפול-הפרויקט)
5. [שלב 4: התקנת תלויות](#שלב-4-התקנת-תלויות)
6. [שלב 5: הגדרת Supabase](#שלב-5-הגדרת-supabase)
7. [שלב 6: הגדרת .env](#שלב-6-הגדרת-env)
8. [שלב 7: הפעלת השרת](#שלב-7-הפעלת-השרת)
9. [שלב 8: בדיקה](#שלב-8-בדיקה)
10. [שלב 9: שימוש](#שלב-9-שימוש)

---

## דרישות מוקדמות

- מחשב עם Windows/Linux/macOS
- חיבור לאינטרנט
- חשבון GitHub (לשכפול)
- חשבון Supabase (ניצור בהמשך)

---

## שלב 1: התקנת Python

### Windows:

1. הורד Python מ-[python.org/downloads](https://www.python.org/downloads/)
2. בזמן ההתקנה, **חשוב**: סמן ✅ "Add Python to PATH"
3. לחץ "Install Now"
4. פתח Command Prompt חדש ובדוק:

```cmd
python --version
```

אמור להציג: `Python 3.10.x` או גבוה יותר ✅

### Linux (Ubuntu/Debian):

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv

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

FFmpeg נדרש להורדת אודיו (MP3). אם אתה רק מוריד וידאו, אפשר לדלג.

### Windows:

1. הורד מ-[ffmpeg.org/download.html](https://ffmpeg.org/download.html)
2. בחר "Windows builds" → "Windows builds from gyan.dev"
3. הורד את הגרסה המלאה (full)
4. חלץ לתיקייה (למשל `C:\ffmpeg`)
5. הוסף ל-PATH:
   - לחץ ימני על "This PC" → Properties
   - Advanced system settings → Environment Variables
   - ב-System variables, מצא "Path" → Edit
   - New → הוסף `C:\ffmpeg\bin`
   - OK בכל החלונות
6. פתח Command Prompt חדש:

```cmd
ffmpeg -version
```

### Linux:

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

### אפשרות 1: עם Git (מומלץ)

```bash
git clone https://github.com/ZyrticX/YTDLPFIXED1.git
cd YTDLPFIXED1
```

### אפשרות 2: הורדה כ-ZIP

1. לך ל-[github.com/ZyrticX/YTDLPFIXED1](https://github.com/ZyrticX/YTDLPFIXED1)
2. לחץ על "Code" → "Download ZIP"
3. חלץ את הקובץ
4. פתח Terminal/Command Prompt בתיקייה

---

## שלב 4: התקנת תלויות

### שיטה 1: סקריפט אוטומטי (מומלץ)

```bash
# Windows
python setup.py

# Linux/macOS
python3 setup.py
```

הסקריפט יבצע:
- ✅ בדיקת Python
- ✅ התקנת כל התלויות
- ✅ בדיקת FFmpeg
- ✅ יצירת קובץ .env

### שיטה 2: ידנית

```bash
# Windows
pip install -r requirements_api.txt

# Linux/macOS
pip3 install -r requirements_api.txt
```

אם יש שגיאה:

```bash
# עדכן pip קודם
python -m pip install --upgrade pip
python -m pip install -r requirements_api.txt
```

### בדיקה שהכל הותקן:

```bash
# Windows
python -c "import flask, yt_dlp, supabase; print('✅ הכל מותקן!')"

# Linux/macOS
python3 -c "import flask, yt_dlp, supabase; print('✅ הכל מותקן!')"
```

---

## שלב 5: הגדרת Supabase

### 5.1 יצירת חשבון

1. לך ל-[supabase.com](https://supabase.com)
2. לחץ "Start your project"
3. היכנס עם GitHub/Google או צור חשבון

### 5.2 יצירת פרויקט

1. לחץ "New Project"
2. מלא:
   - **Name**: `yt-dlp-api` (או כל שם)
   - **Database Password**: בחר סיסמה חזקה (שמור אותה!)
   - **Region**: בחר אזור קרוב
3. לחץ "Create new project"
4. המתן 2-3 דקות

### 5.3 קבלת פרטי API

1. בתפריט השמאלי → **Settings** (⚙️)
2. לחץ **API**
3. העתק שני ערכים:
   - **Project URL**: `https://xxxxx.supabase.co`
   - **anon public** key: מפתח ארוך שמתחיל ב-`eyJ...`

📝 **שמור את שני הערכים האלה!**

### 5.4 יצירת Storage Bucket

1. בתפריט השמאלי → **Storage**
2. לחץ **New bucket**
3. מלא:
   - **Name**: `videos`
   - **Public bucket**: ✅ סמן
4. לחץ **Create bucket**

### 5.5 הגדרת Policies (הרשאות)

1. ב-Storage → לחץ על ה-bucket `videos`
2. לחץ **Policies** (בתפריט העליון)
3. לחץ **New Policy**

**Policy 1 - הוספת קבצים:**

- **Policy name**: `Allow uploads`
- **Allowed operation**: `INSERT`
- **Target roles**: `anon` (או `authenticated`)
- **WITH CHECK expression**: `bucket_id = 'videos'`
- לחץ **Review** → **Save policy**

**Policy 2 - קריאת קבצים:**

- **Policy name**: `Allow public read`
- **Allowed operation**: `SELECT`
- **Target roles**: `public`
- **USING expression**: `bucket_id = 'videos'`
- לחץ **Review** → **Save policy**

✅ **Supabase מוכן!**

---

## שלב 6: הגדרת .env

### יצירת הקובץ

```bash
# Windows
copy config.env.example .env
notepad .env

# Linux/macOS
cp config.env.example .env
nano .env
```

### עדכון הערכים

פתח את `.env` ועדכן:

```env
# העתק מ-Supabase → Settings → API
SUPABASE_URL=https://xxxxx.supabase.co

# העתק את ה-anon public key
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# שם ה-bucket שיצרת
SUPABASE_BUCKET=videos

# פורט השרת
PORT=5000

# מצב debug
DEBUG=False
```

💾 **שמור את הקובץ**

---

## שלב 7: הפעלת השרת

```bash
# Windows
python api_server.py

# Linux/macOS
python3 api_server.py
```

### מה אמור להופיע:

```
INFO - Starting API server on port 5000
INFO - Debug mode: False
 * Running on http://0.0.0.0:5000
INFO - ✅ Supabase client initialized successfully
```

✅ **השרת פועל!**

---

## שלב 8: בדיקה

### בדיקה 1: Health Check

פתח בדפדפן:
```
http://localhost:5000/health
```

אמור להציג:
```json
{
  "status": "ok",
  "supabase_configured": true,
  "temp_dir": "/tmp/yt-dlp-downloads"
}
```

### בדיקה 2: עם דף HTML

1. פתח את `test_api.html` בדפדפן
2. ודא שה-API URL הוא: `http://localhost:5000`
3. הכנס כתובת YouTube
4. לחץ "הורד והעלה"

### בדיקה 3: עם cURL

```bash
curl -X POST http://localhost:5000/info \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}'
```

---

## שלב 9: שימוש

### דוגמה 1: הורדת וידאו

```javascript
const response = await fetch('http://localhost:5000/download', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    url: 'https://www.youtube.com/watch?v=VIDEO_ID',
    format: 'video',
    upload_to_supabase: true
  })
});

const data = await response.json();
console.log('Video URL:', data.upload.public_url);
```

### דוגמה 2: הורדת אודיו

```javascript
const response = await fetch('http://localhost:5000/download', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    url: 'https://www.youtube.com/watch?v=VIDEO_ID',
    format: 'audio',
    upload_to_supabase: true
  })
});

const data = await response.json();
console.log('Audio URL:', data.upload.public_url);
```

---

## 🎉 סיכום

עכשיו יש לך:

✅ שרת API פועל על `http://localhost:5000`  
✅ יכולת להוריד סרטונים  
✅ העלאה אוטומטית ל-Supabase  
✅ תמיכה בוידאו ואודיו  
✅ API מוכן לשימוש באתר שלך  

---

## 🛠️ פתרון בעיות

### "ModuleNotFoundError: No module named 'flask'"

```bash
pip3 install -r requirements_api.txt
```

### "Supabase client not initialized"

1. ודא שקובץ `.env` קיים
2. ודא שהערכים נכונים (ללא רווחים מיותרים)
3. ודא שהפרויקט ב-Supabase פעיל

### "ffmpeg not found"

- Windows: ודא ש-FFmpeg ב-PATH
- Linux: `sudo apt install ffmpeg`
- macOS: `brew install ffmpeg`

### "Permission denied" ב-Supabase

1. ודא שיצרת bucket
2. בדוק Policies ב-Storage → Policies
3. ודא שה-bucket הוא public

### הפורט תפוס

שנה את הפורט ב-`.env`:
```env
PORT=5001
```

---

## 📚 משאבים נוספים

- **[QUICK_START.md](QUICK_START.md)** - התחלה מהירה (5 דקות)
- **[START_HERE.md](START_HERE.md)** - מדריך מפורט מאוד
- **[API_GUIDE_HE.md](API_GUIDE_HE.md)** - מדריך API מלא
- **[DEPLOYMENT_GUIDE_HE.md](DEPLOYMENT_GUIDE_HE.md)** - התקנה על שרת

---

**בהצלחה! 🚀**


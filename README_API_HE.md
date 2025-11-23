# 🚀 yt-dlp API עם Supabase - התחלה מהירה

API server להפעלת yt-dlp על השרת שלך עם העלאה אוטומטית ל-Supabase Storage.

## ⚡ התקנה מהירה

### 1. התקנת תלויות

```bash
pip3 install -r requirements_api.txt
```

### 2. הגדרת Supabase

1. צור פרויקט ב-[Supabase](https://supabase.com)
2. לך ל-**Settings** → **API** והעתק:
   - Project URL
   - anon public key
3. צור Storage Bucket בשם `videos`
4. צור קובץ `.env`:

```bash
cp config.env.example .env
nano .env
```

עדכן את הערכים:
```env
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=your-key-here
SUPABASE_BUCKET=videos
```

### 3. הפעלה

```bash
python3 api_server.py
```

השרת יעלה על `http://0.0.0.0:5000`

## 📡 שימוש ב-API

### הורדת סרטון

```bash
curl -X POST http://localhost:5000/download \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.youtube.com/watch?v=VIDEO_ID",
    "format": "video",
    "upload_to_supabase": true
  }'
```

### הורדת אודיו

```bash
curl -X POST http://localhost:5000/download \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.youtube.com/watch?v=VIDEO_ID",
    "format": "audio",
    "upload_to_supabase": true
  }'
```

## 📚 תיעוד מלא

לקריאת המדריך המלא, ראה: [API_GUIDE_HE.md](API_GUIDE_HE.md)

## 🔧 Endpoints זמינים

- `GET /health` - בדיקת תקינות
- `POST /download` - הורדת סרטון והעלאה ל-Supabase
- `POST /info` - קבלת מידע על סרטון (ללא הורדה)
- `POST /formats` - רשימת פורמטים זמינים

## 💡 דוגמה מ-JavaScript

```javascript
const response = await fetch('http://your-server:5000/download', {
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

## 🛠️ פתרון בעיות

**Supabase לא מוגדר?**
- ודא שקובץ `.env` קיים ומוגדר נכון

**FFmpeg לא נמצא?**
```bash
sudo apt install ffmpeg  # Ubuntu/Debian
```

**שגיאת הרשאות Supabase?**
- ודא שיצרת bucket ב-Storage
- בדוק Policies ב-Storage → Policies

לקריאת פתרונות נוספים, ראה [API_GUIDE_HE.md](API_GUIDE_HE.md#פתרון-בעיות)


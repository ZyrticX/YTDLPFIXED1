# yt-dlp API Server with Supabase Integration

🚀 API server להפעלת yt-dlp על השרת עם העלאה אוטומטית ל-Supabase Storage.

## ✨ תכונות

- ✅ הורדת סרטונים מ-yt-dlp דרך API
- ✅ העלאה אוטומטית ל-Supabase Storage
- ✅ תמיכה בוידאו ואודיו (MP3)
- ✅ Docker support
- ✅ תיעוד מלא בעברית

## 📦 התקנה מהירה

```bash
# התקנת תלויות
pip3 install -r requirements_api.txt

# הגדרת Supabase (ראה config.env.example)
cp config.env.example .env
# ערוך את .env והוסף את פרטי Supabase שלך

# הפעלה
python3 api_server.py
```

## 🐳 עם Docker

```bash
# העתק את config.env.example ל-.env ועדכן את הערכים
cp config.env.example .env

# הפעלה
docker-compose up -d
```

## 📚 תיעוד

- **[README_API_HE.md](README_API_HE.md)** - התחלה מהירה בעברית
- **[API_GUIDE_HE.md](API_GUIDE_HE.md)** - מדריך מלא בעברית
- **[DEPLOYMENT_GUIDE_HE.md](DEPLOYMENT_GUIDE_HE.md)** - מדריך התקנה על שרת

## 🔌 API Endpoints

- `GET /health` - בדיקת תקינות
- `POST /download` - הורדת סרטון והעלאה ל-Supabase
- `POST /info` - קבלת מידע על סרטון (ללא הורדה)
- `POST /formats` - רשימת פורמטים זמינים

## 💻 דוגמת שימוש

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

## 📁 קבצים

- `api_server.py` - שרת API הראשי
- `requirements_api.txt` - תלויות Python
- `config.env.example` - תבנית להגדרות Supabase
- `Dockerfile` - Docker image
- `docker-compose.yml` - Docker Compose configuration
- `test_api.html` - דף HTML לבדיקת ה-API

## 🔧 דרישות

- Python 3.10+
- FFmpeg (להורדת אודיו)
- Supabase account
- Storage bucket ב-Supabase

## 📝 רישיון

פרויקט זה מבוסס על [yt-dlp](https://github.com/yt-dlp/yt-dlp) (Unlicense).

## 🤝 תרומה

תרומות מתקבלות בברכה! פתח issue או pull request.

---

Made with ❤️ for easy video downloading and storage

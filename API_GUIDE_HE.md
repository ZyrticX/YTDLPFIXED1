# מדריך API - yt-dlp עם Supabase

## תוכן עניינים
1. [התקנה](#התקנה)
2. [הגדרת Supabase](#הגדרת-supabase)
3. [הפעלת השרת](#הפעלת-השרת)
4. [שימוש ב-API](#שימוש-ב-api)
5. [דוגמאות קוד](#דוגמאות-קוד)
6. [פתרון בעיות](#פתרון-בעיות)

---

## התקנה

### 1. התקנת תלויות

```bash
# התקנת Python packages
pip3 install -r requirements_api.txt

# או התקנה ידנית
pip3 install flask flask-cors yt-dlp supabase python-dotenv
```

### 2. התקנת FFmpeg (נדרש להורדת אודיו)

```bash
# Ubuntu/Debian
sudo apt install ffmpeg

# CentOS/RHEL
sudo yum install ffmpeg
```

---

## הגדרת Supabase

### 1. יצירת פרויקט ב-Supabase

1. היכנס ל-[Supabase](https://supabase.com)
2. צור פרויקט חדש או השתמש בפרויקט קיים
3. לך ל-**Settings** → **API**
4. העתק את:
   - **Project URL** (SUPABASE_URL)
   - **anon public key** (SUPABASE_KEY)

### 2. יצירת Storage Bucket

1. לך ל-**Storage** ב-Supabase Dashboard
2. לחץ על **New bucket**
3. שם ה-bucket: `videos` (או כל שם אחר)
4. בחר **Public bucket** אם אתה רוצה גישה ציבורית לקבצים
5. לחץ **Create bucket**

### 3. הגדרת הרשאות (Policies)

לך ל-**Storage** → **Policies** → ה-bucket שלך

**Policy להוספת קבצים (INSERT):**
```sql
CREATE POLICY "Allow authenticated uploads"
ON storage.objects FOR INSERT
TO authenticated
WITH CHECK (bucket_id = 'videos');
```

**Policy לקריאת קבצים (SELECT):**
```sql
CREATE POLICY "Allow public read access"
ON storage.objects FOR SELECT
TO public
USING (bucket_id = 'videos');
```

### 4. הגדרת משתני סביבה

צור קובץ `.env` בתיקיית הפרויקט:

```bash
cp .env.example .env
nano .env
```

עדכן את הערכים:

```env
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
SUPABASE_BUCKET=videos
PORT=5000
DEBUG=False
```

---

## הפעלת השרת

### הפעלה ישירה:

```bash
python3 api_server.py
```

השרת יעלה על `http://0.0.0.0:5000`

### הפעלה עם systemd (כשירות):

צור קובץ `/etc/systemd/system/yt-dlp-api.service`:

```ini
[Unit]
Description=yt-dlp API Server with Supabase
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/yt-dlp
Environment="PATH=/usr/bin:/usr/local/bin"
ExecStart=/usr/bin/python3 /path/to/yt-dlp/api_server.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

הפעלה:

```bash
sudo systemctl daemon-reload
sudo systemctl start yt-dlp-api
sudo systemctl enable yt-dlp-api
sudo systemctl status yt-dlp-api
```

### הפעלה עם Docker:

צור `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# התקנת FFmpeg
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

# העתקת קבצים
COPY requirements_api.txt .
RUN pip install --no-cache-dir -r requirements_api.txt

COPY api_server.py .
COPY .env .

EXPOSE 5000

CMD ["python", "api_server.py"]
```

צור `docker-compose.yml`:

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "5000:5000"
    environment:
      - SUPABASE_URL=${SUPABASE_URL}
      - SUPABASE_KEY=${SUPABASE_KEY}
      - SUPABASE_BUCKET=${SUPABASE_BUCKET}
    volumes:
      - ./downloads:/tmp/yt-dlp-downloads
    restart: unless-stopped
```

הפעלה:

```bash
docker-compose up -d
```

---

## שימוש ב-API

### Base URL

```
http://your-server-ip:5000
```

### Endpoints

#### 1. Health Check

```http
GET /health
```

**תגובה:**
```json
{
  "status": "ok",
  "supabase_configured": true,
  "temp_dir": "/tmp/yt-dlp-downloads"
}
```

#### 2. הורדת סרטון

```http
POST /download
Content-Type: application/json

{
  "url": "https://www.youtube.com/watch?v=VIDEO_ID",
  "format": "video",
  "quality": "best",
  "upload_to_supabase": true,
  "remote_filename": "my-video.mp4"
}
```

**פרמטרים:**
- `url` (חובה) - כתובת הסרטון
- `format` (אופציונלי) - `"video"` או `"audio"` (ברירת מחדל: `"video"`)
- `quality` (אופציונלי) - `"best"`, `"worst"`, או format selector (ברירת מחדל: `"best"`)
- `upload_to_supabase` (אופציונלי) - `true` או `false` (ברירת מחדל: `true`)
- `remote_filename` (אופציונלי) - שם מותאם לקובץ ב-Supabase

**תגובה מוצלחת:**
```json
{
  "download": {
    "success": true,
    "file_path": "/tmp/yt-dlp-downloads/video.mp4",
    "filename": "video.mp4",
    "title": "Video Title",
    "duration": 120,
    "uploader": "Channel Name",
    "view_count": 1000,
    "file_size": 10485760
  },
  "upload": {
    "success": true,
    "filename": "video.mp4",
    "public_url": "https://xxxxx.supabase.co/storage/v1/object/public/videos/video.mp4",
    "file_size": 10485760
  }
}
```

#### 3. קבלת מידע על סרטון (ללא הורדה)

```http
POST /info
Content-Type: application/json

{
  "url": "https://www.youtube.com/watch?v=VIDEO_ID"
}
```

**תגובה:**
```json
{
  "success": true,
  "info": {
    "id": "VIDEO_ID",
    "title": "Video Title",
    "duration": 120,
    "uploader": "Channel Name",
    "view_count": 1000,
    "description": "Video description...",
    ...
  }
}
```

#### 4. קבלת רשימת פורמטים זמינים

```http
POST /formats
Content-Type: application/json

{
  "url": "https://www.youtube.com/watch?v=VIDEO_ID"
}
```

---

## דוגמאות קוד

### JavaScript/TypeScript (Frontend)

```javascript
// הורדת סרטון והעלאה ל-Supabase
async function downloadVideo(url, format = 'video') {
  try {
    const response = await fetch('http://your-server:5000/download', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        url: url,
        format: format,
        upload_to_supabase: true
      })
    });
    
    const data = await response.json();
    
    if (data.download.success && data.upload.success) {
      console.log('Video uploaded to:', data.upload.public_url);
      return data.upload.public_url;
    } else {
      throw new Error(data.error || 'Download failed');
    }
  } catch (error) {
    console.error('Error:', error);
    throw error;
  }
}

// שימוש
downloadVideo('https://www.youtube.com/watch?v=VIDEO_ID', 'video')
  .then(url => console.log('Success:', url))
  .catch(err => console.error('Failed:', err));
```

### Python

```python
import requests

def download_video(url, format_type='video'):
    response = requests.post(
        'http://your-server:5000/download',
        json={
            'url': url,
            'format': format_type,
            'upload_to_supabase': True
        }
    )
    return response.json()

# שימוש
result = download_video('https://www.youtube.com/watch?v=VIDEO_ID')
if result.get('upload', {}).get('success'):
    print(f"Video URL: {result['upload']['public_url']}")
```

### cURL

```bash
# הורדת וידאו
curl -X POST http://your-server:5000/download \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.youtube.com/watch?v=VIDEO_ID",
    "format": "video",
    "upload_to_supabase": true
  }'

# הורדת אודיו
curl -X POST http://your-server:5000/download \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.youtube.com/watch?v=VIDEO_ID",
    "format": "audio",
    "upload_to_supabase": true
  }'

# קבלת מידע
curl -X POST http://your-server:5000/info \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.youtube.com/watch?v=VIDEO_ID"}'
```

---

## אינטגרציה עם אתר

### דוגמה עם React

```jsx
import React, { useState } from 'react';

function VideoDownloader() {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleDownload = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://your-server:5000/download', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          url: url,
          format: 'video',
          upload_to_supabase: true
        })
      });

      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <input
        type="text"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
        placeholder="Enter YouTube URL"
      />
      <button onClick={handleDownload} disabled={loading}>
        {loading ? 'Downloading...' : 'Download'}
      </button>
      
      {result?.upload?.public_url && (
        <div>
          <p>Video uploaded!</p>
          <a href={result.upload.public_url} target="_blank" rel="noopener noreferrer">
            View Video
          </a>
        </div>
      )}
    </div>
  );
}
```

---

## פתרון בעיות

### שגיאת Supabase לא מוגדר

**בעיה:** `Supabase client not initialized`

**פתרון:**
1. ודא שקובץ `.env` קיים ומוגדר נכון
2. בדוק שהערכים `SUPABASE_URL` ו-`SUPABASE_KEY` נכונים
3. ודא שהקובץ `.env` נמצא באותה תיקייה כמו `api_server.py`

### שגיאת FFmpeg

**בעיה:** `ERROR: ffmpeg not found`

**פתרון:**
```bash
# התקן FFmpeg
sudo apt install ffmpeg  # Ubuntu/Debian
sudo yum install ffmpeg  # CentOS/RHEL
```

### שגיאת הרשאות Supabase

**בעיה:** `Permission denied` בעת העלאה

**פתרון:**
1. ודא שיצרת bucket ב-Supabase Storage
2. בדוק את ה-Policies ב-Storage → Policies
3. ודא שה-bucket הוא public או שיש לך הרשאות מתאימות

### שגיאת CORS

**בעיה:** `CORS policy blocked`

**פתרון:**
הקוד כבר כולל `flask-cors`. אם יש בעיות, הוסף:

```python
from flask_cors import CORS
CORS(app, resources={r"/*": {"origins": "*"}})
```

### שגיאת שטח דיסק

**בעיה:** `No space left on device`

**פתרון:**
1. בדוק שטח דיסק זמין: `df -h`
2. נקה קבצים זמניים: `rm -rf /tmp/yt-dlp-downloads/*`
3. הגדר תיקייה אחרת ב-`TEMP_DOWNLOAD_DIR`

---

## אבטחה

### 1. הגבלת גישה

הוסף authentication ל-API:

```python
from functools import wraps
from flask import request, jsonify

API_KEY = os.getenv('API_KEY')

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if api_key != API_KEY:
            return jsonify({'error': 'Invalid API key'}), 401
        return f(*args, **kwargs)
    return decorated_function

@app.route('/download', methods=['POST'])
@require_api_key
def download_endpoint():
    # ...
```

### 2. Rate Limiting

התקן `flask-limiter`:

```bash
pip install flask-limiter
```

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["100 per hour"]
)

@app.route('/download', methods=['POST'])
@limiter.limit("10 per minute")
def download_endpoint():
    # ...
```

### 3. HTTPS

השתמש ב-Nginx כ-reverse proxy עם SSL:

```nginx
server {
    listen 443 ssl;
    server_name your-domain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## סיכום

עכשיו יש לך API מלא שמאפשר:
- ✅ הורדת סרטונים מ-yt-dlp
- ✅ העלאה אוטומטית ל-Supabase Storage
- ✅ תמיכה בוידאו ואודיו
- ✅ API נקי ונוח לשימוש
- ✅ אינטגרציה קלה עם אתרים

לשאלות נוספות, עיין ב-[תיעוד yt-dlp](https://github.com/yt-dlp/yt-dlp#readme) ו-[תיעוד Supabase](https://supabase.com/docs).


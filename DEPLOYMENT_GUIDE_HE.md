# מדריך התקנה והפעלה של yt-dlp על השרת

## תוכן עניינים
1. [דרישות מערכת](#דרישות-מערכת)
2. [התקנה](#התקנה)
3. [שימוש בסיסי](#שימוש-בסיסי)
4. [הפעלה כשירות](#הפעלה-כשירות)
5. [הפעלה עם Docker](#הפעלה-עם-docker)
6. [יצירת API/Web Interface](#יצירת-apiveb-interface)
7. [טיפים ופתרון בעיות](#טיפים-ופתרון-בעיות)

---

## דרישות מערכת

### דרישות מינימליות:
- **מערכת הפעלה**: Linux/Unix (Ubuntu, Debian, CentOS, וכו')
- **Python**: גרסה 3.10 ומעלה
- **זיכרון**: לפחות 512MB RAM
- **שטח דיסק**: תלוי בכמות התוכן שתוריד

### בדיקת גרסת Python:
```bash
python3 --version
# או
python --version
```

אם Python לא מותקן, התקן אותו:
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip

# CentOS/RHEL
sudo yum install python3 python3-pip
```

---

## התקנה

### שיטה 1: התקנה עם pip (מומלץ)

```bash
# התקנת yt-dlp
pip3 install yt-dlp

# או עם sudo אם צריך
sudo pip3 install yt-dlp

# עדכון yt-dlp
pip3 install --upgrade yt-dlp
```

### שיטה 2: התקנה מהבינארי (ללא Python)

```bash
# הורדת הבינארי
sudo wget https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -O /usr/local/bin/yt-dlp

# מתן הרשאות הרצה
sudo chmod a+rx /usr/local/bin/yt-dlp

# בדיקה שההתקנה הצליחה
yt-dlp --version
```

### שיטה 3: התקנה מהקוד המקור

```bash
# שכפול המאגר
git clone https://github.com/yt-dlp/yt-dlp.git
cd yt-dlp

# התקנה
pip3 install -e .

# או התקנה ישירה
python3 -m pip install -e .
```

---

## שימוש בסיסי

### הורדת וידאו פשוט:
```bash
yt-dlp "https://www.youtube.com/watch?v=VIDEO_ID"
```

### הורדת אודיו בלבד (MP3):
```bash
yt-dlp -x --audio-format mp3 "https://www.youtube.com/watch?v=VIDEO_ID"
```

### הורדה באיכות מסוימת:
```bash
# איכות טובה ביותר
yt-dlp -f "bestvideo+bestaudio/best" "URL"

# רק וידאו 1080p
yt-dlp -f "bestvideo[height<=1080]+bestaudio/best[height<=1080]" "URL"
```

### הורדה לתיקייה מסוימת:
```bash
yt-dlp -o "/path/to/downloads/%(title)s.%(ext)s" "URL"
```

### הורדת פלייליסט:
```bash
yt-dlp "https://www.youtube.com/playlist?list=PLAYLIST_ID"
```

---

## הפעלה כשירות

### יצירת שירות systemd

צור קובץ שירות:
```bash
sudo nano /etc/systemd/system/yt-dlp-api.service
```

תוכן הקובץ:
```ini
[Unit]
Description=yt-dlp API Service
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/home/your_username/yt-dlp
ExecStart=/usr/bin/python3 /path/to/your/api_server.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

החלף:
- `your_username` - שם המשתמש שלך
- `/path/to/your/api_server.py` - נתיב לקובץ השרת שלך

הפעלת השירות:
```bash
# טעינת השירות
sudo systemctl daemon-reload

# הפעלת השירות
sudo systemctl start yt-dlp-api

# הפעלה אוטומטית בעת אתחול
sudo systemctl enable yt-dlp-api

# בדיקת סטטוס
sudo systemctl status yt-dlp-api
```

---

## הפעלה עם Docker

### שימוש ב-Docker Compose

צור קובץ `docker-compose.yml`:
```yaml
version: '3.8'

services:
  yt-dlp:
    image: ghcr.io/yt-dlp/yt-dlp:latest
    container_name: yt-dlp
    volumes:
      - ./downloads:/downloads
      - ./config:/config
    environment:
      - DOWNLOAD_PATH=/downloads
    command: tail -f /dev/null  # שומר על הקונטיינר פעיל
    restart: unless-stopped
```

הפעלה:
```bash
docker-compose up -d
```

### הרצת פקודות דרך Docker:
```bash
docker exec -it yt-dlp yt-dlp "URL"
```

---

## יצירת API/Web Interface

### אפשרות 1: שימוש ב-yt-dlp-webui

```bash
# התקנת yt-dlp-webui
pip3 install yt-dlp-webui

# הפעלה
yt-dlp-webui --host 0.0.0.0 --port 8080
```

גישה דרך הדפדפן: `http://77.42.29.11:8080`

### אפשרות 2: יצירת API פשוט עם Flask

צור קובץ `api_server.py`:
```python
#!/usr/bin/env python3
from flask import Flask, request, jsonify, send_file
import yt_dlp
import os
import tempfile
from pathlib import Path

app = Flask(__name__)
DOWNLOAD_DIR = Path('/var/www/downloads')
DOWNLOAD_DIR.mkdir(exist_ok=True)

@app.route('/download', methods=['POST'])
def download():
    url = request.json.get('url')
    format_type = request.json.get('format', 'video')  # 'video' or 'audio'
    
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    
    try:
        ydl_opts = {
            'outtmpl': str(DOWNLOAD_DIR / '%(title)s.%(ext)s'),
        }
        
        if format_type == 'audio':
            ydl_opts.update({
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            })
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
            if format_type == 'audio':
                filename = filename.rsplit('.', 1)[0] + '.mp3'
            
            return jsonify({
                'status': 'success',
                'filename': os.path.basename(filename),
                'title': info.get('title'),
                'url': f'/files/{os.path.basename(filename)}'
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/files/<filename>')
def download_file(filename):
    file_path = DOWNLOAD_DIR / filename
    if file_path.exists():
        return send_file(str(file_path), as_attachment=True)
    return jsonify({'error': 'File not found'}), 404

@app.route('/health')
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
```

התקנת Flask:
```bash
pip3 install flask
```

הפעלה:
```bash
python3 api_server.py
```

### אפשרות 3: שימוש ב-yt-dlp-server

```bash
# התקנה
pip3 install yt-dlp-server

# הפעלה
yt-dlp-server --host 0.0.0.0 --port 8080
```

---

## הגדרת Firewall

אם אתה משתמש ב-API או Web Interface, פתח את הפורטים:

```bash
# Ubuntu/Debian (UFW)
sudo ufw allow 5000/tcp  # Flask API
sudo ufw allow 8080/tcp  # WebUI
sudo ufw reload

# CentOS/RHEL (firewalld)
sudo firewall-cmd --permanent --add-port=5000/tcp
sudo firewall-cmd --permanent --add-port=8080/tcp
sudo firewall-cmd --reload
```

---

## טיפים ופתרון בעיות

### עדכון yt-dlp:
```bash
pip3 install --upgrade yt-dlp
# או
yt-dlp -U
```

### בדיקת גרסה:
```bash
yt-dlp --version
```

### הורדה עם פרוקסי:
```bash
yt-dlp --proxy "http://proxy:port" "URL"
```

### הורדה עם cookies (לאתרים שדורשים התחברות):
```bash
yt-dlp --cookies cookies.txt "URL"
```

### הגדרת קובץ config:
צור קובץ `~/.config/yt-dlp/config`:
```
-o /var/www/downloads/%(title)s.%(ext)s
-f bestvideo+bestaudio/best
--no-mtime
```

### בעיות נפוצות:

**בעיה**: `command not found: yt-dlp`
**פתרון**: ודא שההתקנה הצליחה והנתיב נכון:
```bash
which yt-dlp
```

**בעיה**: שגיאת הרשאות
**פתרון**: בדוק הרשאות על תיקיית ההורדה:
```bash
sudo chmod 755 /var/www/downloads
sudo chown your_user:your_user /var/www/downloads
```

**בעיה**: שגיאת FFmpeg (להורדת אודיו)
**פתרון**: התקן FFmpeg:
```bash
# Ubuntu/Debian
sudo apt install ffmpeg

# CentOS/RHEL
sudo yum install ffmpeg
```

---

## דוגמאות שימוש מתקדמות

### הורדת תת-כותרות:
```bash
yt-dlp --write-subs --write-auto-subs --sub-lang en "URL"
```

### הורדת תמונות ממוזערות:
```bash
yt-dlp --write-thumbnail "URL"
```

### הורדה עם שם מותאם:
```bash
yt-dlp -o "%(uploader)s - %(title)s.%(ext)s" "URL"
```

### הורדת פלייליסט עם הגבלה:
```bash
yt-dlp --playlist-end 10 "PLAYLIST_URL"  # רק 10 סרטונים ראשונים
```

---

## אבטחה

1. **אל תפעיל את השרת כ-root** - השתמש במשתמש רגיל
2. **הגבל גישה** - השתמש ב-firewall או reverse proxy (nginx)
3. **השתמש ב-HTTPS** - הגדר SSL/TLS עם Let's Encrypt
4. **הגבל גודל קבצים** - הוסף הגבלות על גודל ההורדות

### הגדרת Nginx כ-Reverse Proxy:

```nginx
server {
    listen 80;
    server_name 77.42.29.11;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## סיכום

לאחר ההתקנה, תוכל להשתמש ב-yt-dlp בשרת שלך (77.42.29.11) בדרכים הבאות:

1. **שימוש ישיר**: `yt-dlp "URL"`
2. **כשירות**: דרך systemd
3. **עם Docker**: קונטיינר מוכן
4. **דרך API**: Flask או yt-dlp-webui

לשאלות נוספות, עיין ב-[תיעוד הרשמי](https://github.com/yt-dlp/yt-dlp#readme).



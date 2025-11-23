FROM python:3.11-slim

# הגדרת תיקיית עבודה
WORKDIR /app

# התקנת FFmpeg (נדרש להורדת אודיו)
RUN apt-get update && \
    apt-get install -y ffmpeg curl && \
    rm -rf /var/lib/apt/lists/*

# העתקת requirements והתקנת תלויות
COPY requirements_api.txt .
RUN pip install --no-cache-dir -r requirements_api.txt

# העתקת קבצי האפליקציה
COPY api_server.py .

# יצירת תיקיית הורדות זמנית
RUN mkdir -p /tmp/yt-dlp-downloads

# חשיפת פורט
EXPOSE 5000

# הפעלת השרת
CMD ["python", "api_server.py"]


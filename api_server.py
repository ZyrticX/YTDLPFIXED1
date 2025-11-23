#!/usr/bin/env python3
"""
API Server for yt-dlp with Supabase Storage Integration
מאפשר הורדת סרטונים והעלאתם ל-Supabase
"""

import os
import tempfile
import logging
import traceback
from pathlib import Path
from typing import Optional, Dict, Any
from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp
from supabase import create_client, Client
from dotenv import load_dotenv

# טעינת משתני סביבה
load_dotenv()

app = Flask(__name__)
CORS(app)  # מאפשר גישה מ-CORS

# הגדרת לוגים
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# משתני סביבה - Supabase
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
SUPABASE_BUCKET = os.getenv('SUPABASE_BUCKET', 'videos')  # שם ה-bucket ב-Supabase

# תיקיית הורדה זמנית
TEMP_DOWNLOAD_DIR = Path(tempfile.gettempdir()) / 'yt-dlp-downloads'
TEMP_DOWNLOAD_DIR.mkdir(exist_ok=True)

# אתחול Supabase Client
supabase: Optional[Client] = None
if SUPABASE_URL and SUPABASE_KEY:
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        logger.info("✅ Supabase client initialized successfully")
    except Exception as e:
        logger.error(f"❌ Failed to initialize Supabase client: {e}")
else:
    logger.warning("⚠️ Supabase credentials not found. Upload to Supabase will be disabled.")


class DownloadProgressHook:
    """מחלקה לטיפול בהתקדמות ההורדה"""
    def __init__(self):
        self.progress_data = {
            'status': 'downloading',
            'percent': 0,
            'speed': None,
            'eta': None,
            'filename': None
        }
    
    def hook(self, d):
        """Callback function להתקדמות ההורדה"""
        if d['status'] == 'downloading':
            self.progress_data['status'] = 'downloading'
            if 'total_bytes' in d:
                percent = (d['downloaded_bytes'] / d['total_bytes']) * 100
                self.progress_data['percent'] = round(percent, 2)
            elif '_percent_str' in d:
                percent_str = d['_percent_str'].replace('%', '')
                try:
                    self.progress_data['percent'] = float(percent_str)
                except:
                    pass
            
            self.progress_data['speed'] = d.get('speed')
            self.progress_data['eta'] = d.get('eta')
            self.progress_data['filename'] = d.get('filename')
            
        elif d['status'] == 'finished':
            self.progress_data['status'] = 'finished'
            self.progress_data['percent'] = 100
            self.progress_data['filename'] = d.get('filename')


def download_video(url: str, format_type: str = 'video', quality: str = 'best') -> Dict[str, Any]:
    """
    מוריד סרטון באמצעות yt-dlp
    
    Args:
        url: כתובת ה-URL של הסרטון
        format_type: 'video' או 'audio'
        quality: איכות הורדה ('best', 'worst', או format selector)
    
    Returns:
        dict עם מידע על הקובץ שהורד
    """
    progress_hook = DownloadProgressHook()
    
    # הגדרות yt-dlp
    ydl_opts = {
        'outtmpl': str(TEMP_DOWNLOAD_DIR / '%(title)s.%(ext)s'),
        'progress_hooks': [progress_hook.hook],
        'quiet': False,
        'no_warnings': False,
    }
    
    # הגדרות לפי סוג ההורדה
    if format_type == 'audio':
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        })
    else:
        # הורדת וידאו
        if quality == 'best':
            ydl_opts['format'] = 'bestvideo+bestaudio/best'
        elif quality == 'worst':
            ydl_opts['format'] = 'worst'
        else:
            ydl_opts['format'] = quality
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # חילוץ מידע על הסרטון
            info = ydl.extract_info(url, download=True)
            info_dict = ydl.sanitize_info(info)
            
            # מציאת שם הקובץ שהורד
            filename = ydl.prepare_filename(info)
            if format_type == 'audio':
                # אם הורדנו אודיו, הקובץ יהיה mp3
                filename = filename.rsplit('.', 1)[0] + '.mp3'
            
            file_path = Path(filename)
            
            if not file_path.exists():
                raise FileNotFoundError(f"Downloaded file not found: {filename}")
            
            return {
                'success': True,
                'file_path': str(file_path),
                'filename': file_path.name,
                'title': info_dict.get('title'),
                'duration': info_dict.get('duration'),
                'uploader': info_dict.get('uploader'),
                'view_count': info_dict.get('view_count'),
                'file_size': file_path.stat().st_size,
                'info': info_dict
            }
            
    except Exception as e:
        logger.error(f"Error downloading video: {e}")
        logger.error(traceback.format_exc())
        raise


def upload_to_supabase(file_path: str, remote_filename: Optional[str] = None) -> Dict[str, Any]:
    """
    מעלה קובץ ל-Supabase Storage
    
    Args:
        file_path: נתיב לקובץ המקומי
        remote_filename: שם הקובץ ב-Supabase (אופציונלי)
    
    Returns:
        dict עם מידע על הקובץ שהועלה
    """
    if not supabase:
        raise ValueError("Supabase client not initialized. Check your SUPABASE_URL and SUPABASE_KEY.")
    
    file_path_obj = Path(file_path)
    if not file_path_obj.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    # שם הקובץ ב-Supabase
    if not remote_filename:
        remote_filename = file_path_obj.name
    
    try:
        # קריאת הקובץ
        with open(file_path_obj, 'rb') as f:
            file_data = f.read()
        
        # העלאה ל-Supabase
        response = supabase.storage.from_(SUPABASE_BUCKET).upload(
            remote_filename,
            file_data,
            file_options={"content-type": "application/octet-stream"}
        )
        
        # קבלת URL ציבורי
        public_url = supabase.storage.from_(SUPABASE_BUCKET).get_public_url(remote_filename)
        
        return {
            'success': True,
            'filename': remote_filename,
            'public_url': public_url,
            'file_size': file_path_obj.stat().st_size
        }
        
    except Exception as e:
        logger.error(f"Error uploading to Supabase: {e}")
        logger.error(traceback.format_exc())
        raise


@app.route('/health', methods=['GET'])
def health_check():
    """בדיקת תקינות השרת"""
    return jsonify({
        'status': 'ok',
        'supabase_configured': supabase is not None,
        'temp_dir': str(TEMP_DOWNLOAD_DIR)
    })


@app.route('/download', methods=['POST'])
def download_endpoint():
    """
    נקודת קצה להורדת סרטון
    
    Body JSON:
    {
        "url": "https://youtube.com/watch?v=...",
        "format": "video" | "audio",
        "quality": "best" | "worst" | format selector,
        "upload_to_supabase": true | false,
        "remote_filename": "optional_custom_name.mp4"
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        url = data.get('url')
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        format_type = data.get('format', 'video')
        quality = data.get('quality', 'best')
        upload_to_supabase_flag = data.get('upload_to_supabase', True)
        remote_filename = data.get('remote_filename')
        
        logger.info(f"Downloading: {url} (format: {format_type}, quality: {quality})")
        
        # הורדת הסרטון
        download_result = download_video(url, format_type, quality)
        
        result = {
            'download': download_result,
            'upload': None
        }
        
        # העלאה ל-Supabase אם נדרש
        if upload_to_supabase_flag:
            if not supabase:
                logger.warning("Supabase not configured, skipping upload")
                result['upload'] = {
                    'success': False,
                    'error': 'Supabase not configured'
                }
            else:
                try:
                    upload_result = upload_to_supabase(
                        download_result['file_path'],
                        remote_filename or download_result['filename']
                    )
                    result['upload'] = upload_result
                    
                    # מחיקת הקובץ המקומי לאחר העלאה מוצלחת
                    try:
                        Path(download_result['file_path']).unlink()
                        logger.info(f"Deleted local file: {download_result['file_path']}")
                    except Exception as e:
                        logger.warning(f"Failed to delete local file: {e}")
                        
                except Exception as e:
                    result['upload'] = {
                        'success': False,
                        'error': str(e)
                    }
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Error in download endpoint: {e}")
        logger.error(traceback.format_exc())
        return jsonify({
            'error': str(e),
            'traceback': traceback.format_exc() if app.debug else None
        }), 500


@app.route('/info', methods=['POST'])
def info_endpoint():
    """
    חילוץ מידע על סרטון ללא הורדה
    
    Body JSON:
    {
        "url": "https://youtube.com/watch?v=..."
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        url = data.get('url')
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            info_dict = ydl.sanitize_info(info)
        
        return jsonify({
            'success': True,
            'info': info_dict
        }), 200
        
    except Exception as e:
        logger.error(f"Error in info endpoint: {e}")
        return jsonify({
            'error': str(e)
        }), 500


@app.route('/formats', methods=['POST'])
def formats_endpoint():
    """
    קבלת רשימת פורמטים זמינים לסרטון
    
    Body JSON:
    {
        "url": "https://youtube.com/watch?v=..."
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        url = data.get('url')
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        ydl_opts = {
            'listformats': True,
            'quiet': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = info.get('formats', [])
        
        return jsonify({
            'success': True,
            'formats': formats
        }), 200
        
    except Exception as e:
        logger.error(f"Error in formats endpoint: {e}")
        return jsonify({
            'error': str(e)
        }), 500


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    
    logger.info(f"Starting API server on port {port}")
    logger.info(f"Debug mode: {debug}")
    
    app.run(host='0.0.0.0', port=port, debug=debug)


#!/usr/bin/env python3
"""
סקריפט התקנה אוטומטי ל-yt-dlp API Server
מבצע בדיקות והתקנות אוטומטיות
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def print_step(step_num, description):
    """הדפסת שלב"""
    print(f"\n{'='*60}")
    print(f"שלב {step_num}: {description}")
    print(f"{'='*60}\n")

def check_command(cmd, name):
    """בדיקה אם פקודה קיימת"""
    try:
        result = subprocess.run(
            [cmd, '--version'] if cmd != 'python' else [cmd, '--version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            version = result.stdout.strip().split('\n')[0]
            print(f"✅ {name} מותקן: {version}")
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    print(f"❌ {name} לא נמצא")
    return False

def install_python_packages():
    """התקנת חבילות Python"""
    print_step(1, "בדיקת Python")
    
    python_cmd = 'python3' if platform.system() != 'Windows' else 'python'
    
    if not check_command(python_cmd, 'Python'):
        print("\n❌ Python לא מותקן!")
        print("הורד והתקן מ: https://www.python.org/downloads/")
        return False
    
    # בדיקת גרסה
    try:
        result = subprocess.run(
            [python_cmd, '--version'],
            capture_output=True,
            text=True
        )
        version_str = result.stdout.strip()
        version_num = version_str.split()[1]
        major, minor = map(int, version_num.split('.')[:2])
        
        if major < 3 or (major == 3 and minor < 10):
            print(f"❌ Python {version_num} - צריך Python 3.10 או גבוה יותר!")
            return False
    except Exception as e:
        print(f"⚠️ לא ניתן לבדוק גרסה: {e}")
    
    print_step(2, "התקנת תלויות Python")
    
    requirements_file = Path('requirements_api.txt')
    if not requirements_file.exists():
        print("❌ קובץ requirements_api.txt לא נמצא!")
        return False
    
    try:
        print(f"מריץ: {python_cmd} -m pip install -r requirements_api.txt")
        result = subprocess.run(
            [python_cmd, '-m', 'pip', 'install', '-r', 'requirements_api.txt'],
            check=True
        )
        print("✅ כל התלויות הותקנו בהצלחה!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ שגיאה בהתקנה: {e}")
        print("\nנסה ידנית:")
        print(f"  {python_cmd} -m pip install --upgrade pip")
        print(f"  {python_cmd} -m pip install -r requirements_api.txt")
        return False

def check_ffmpeg():
    """בדיקת FFmpeg"""
    print_step(3, "בדיקת FFmpeg (אופציונלי)")
    
    if check_command('ffmpeg', 'FFmpeg'):
        return True
    
    print("\n⚠️ FFmpeg לא מותקן - נדרש להורדת אודיו")
    print("\nהתקנה:")
    system = platform.system()
    if system == 'Linux':
        print("  sudo apt update && sudo apt install ffmpeg")
    elif system == 'Darwin':  # macOS
        print("  brew install ffmpeg")
    elif system == 'Windows':
        print("  הורד מ: https://ffmpeg.org/download.html")
        print("  הוסף ל-PATH")
    
    return False

def setup_env_file():
    """הגדרת קובץ .env"""
    print_step(4, "הגדרת קובץ .env")
    
    env_example = Path('config.env.example')
    env_file = Path('.env')
    
    if not env_example.exists():
        print("❌ קובץ config.env.example לא נמצא!")
        return False
    
    if env_file.exists():
        response = input("קובץ .env כבר קיים. האם להחליף? (y/n): ")
        if response.lower() != 'y':
            print("⏭️ דילוג על יצירת .env")
            return True
    
    # העתקת הקובץ
    try:
        import shutil
        shutil.copy(env_example, env_file)
        print("✅ קובץ .env נוצר מ-config.env.example")
        print("\n⚠️ חשוב: ערוך את .env והוסף את פרטי Supabase שלך!")
        print("   - SUPABASE_URL")
        print("   - SUPABASE_KEY")
        print("   - SUPABASE_BUCKET")
        return True
    except Exception as e:
        print(f"❌ שגיאה ביצירת .env: {e}")
        return False

def verify_installation():
    """אימות התקנה"""
    print_step(5, "אימות התקנה")
    
    python_cmd = 'python3' if platform.system() != 'Windows' else 'python'
    
    # בדיקת יבוא חבילות
    packages = ['flask', 'yt_dlp', 'supabase']
    missing = []
    
    for package in packages:
        try:
            if package == 'yt_dlp':
                __import__('yt_dlp')
            elif package == 'supabase':
                __import__('supabase')
            else:
                __import__(package)
            print(f"✅ {package} מותקן")
        except ImportError:
            print(f"❌ {package} לא מותקן")
            missing.append(package)
    
    if missing:
        print(f"\n❌ חבילות חסרות: {', '.join(missing)}")
        print("הרץ: pip install -r requirements_api.txt")
        return False
    
    print("\n✅ כל החבילות מותקנות!")
    return True

def main():
    """פונקציה ראשית"""
    print("""
    ╔══════════════════════════════════════════════════════╗
    ║   yt-dlp API Server - סקריפט התקנה אוטומטי        ║
    ╚══════════════════════════════════════════════════════╝
    """)
    
    # בדיקת Python
    if not install_python_packages():
        sys.exit(1)
    
    # בדיקת FFmpeg (אופציונלי)
    check_ffmpeg()
    
    # הגדרת .env
    setup_env_file()
    
    # אימות
    if not verify_installation():
        sys.exit(1)
    
    print("\n" + "="*60)
    print("✅ ההתקנה הושלמה!")
    print("="*60)
    print("\nהשלבים הבאים:")
    print("1. ערוך את קובץ .env והוסף את פרטי Supabase")
    print("2. הפעל את השרת: python3 api_server.py")
    print("3. בדוק: http://localhost:5000/health")
    print("\nלקריאת המדריך המלא: START_HERE.md")
    print("="*60 + "\n")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ ההתקנה בוטלה על ידי המשתמש")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ שגיאה: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


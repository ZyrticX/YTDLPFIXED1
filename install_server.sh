#!/bin/bash

# סקריפט התקנה מהירה של yt-dlp על השרת
# שימוש: bash install_server.sh

set -e

echo "=========================================="
echo "מדריך התקנת yt-dlp על השרת"
echo "=========================================="
echo ""

# בדיקת הרשאות
if [ "$EUID" -eq 0 ]; then 
   echo "⚠️  אזהרה: לא מומלץ להריץ כשורש. המשך בכל זאת? (y/n)"
   read -r response
   if [ "$response" != "y" ]; then
       exit 1
   fi
fi

# זיהוי מערכת הפעלה
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$ID
    VER=$VERSION_ID
else
    echo "❌ לא ניתן לזהות את מערכת ההפעלה"
    exit 1
fi

echo "📦 מערכת הפעלה מזוהה: $OS $VER"
echo ""

# עדכון רשימת חבילות
echo "🔄 מעדכן רשימת חבילות..."
if [ "$OS" = "ubuntu" ] || [ "$OS" = "debian" ]; then
    sudo apt update
elif [ "$OS" = "centos" ] || [ "$OS" = "rhel" ]; then
    sudo yum check-update || true
fi

# בדיקת Python
echo "🐍 בודק Python..."
if ! command -v python3 &> /dev/null; then
    echo "📥 מתקין Python3..."
    if [ "$OS" = "ubuntu" ] || [ "$OS" = "debian" ]; then
        sudo apt install -y python3 python3-pip
    elif [ "$OS" = "centos" ] || [ "$OS" = "rhel" ]; then
        sudo yum install -y python3 python3-pip
    fi
else
    echo "✅ Python3 כבר מותקן: $(python3 --version)"
fi

# בדיקת pip
if ! command -v pip3 &> /dev/null; then
    echo "📥 מתקין pip3..."
    if [ "$OS" = "ubuntu" ] || [ "$OS" = "debian" ]; then
        sudo apt install -y python3-pip
    elif [ "$OS" = "centos" ] || [ "$OS" = "rhel" ]; then
        sudo yum install -y python3-pip
    fi
fi

# התקנת yt-dlp
echo ""
echo "📥 מתקין yt-dlp..."
pip3 install --upgrade yt-dlp

# בדיקת ההתקנה
if command -v yt-dlp &> /dev/null; then
    echo "✅ yt-dlp הותקן בהצלחה!"
    yt-dlp --version
else
    echo "❌ שגיאה בהתקנת yt-dlp"
    exit 1
fi

# התקנת FFmpeg (אופציונלי)
echo ""
echo "🎵 האם להתקין FFmpeg? (נדרש להורדת אודיו) (y/n)"
read -r install_ffmpeg
if [ "$install_ffmpeg" = "y" ]; then
    if ! command -v ffmpeg &> /dev/null; then
        echo "📥 מתקין FFmpeg..."
        if [ "$OS" = "ubuntu" ] || [ "$OS" = "debian" ]; then
            sudo apt install -y ffmpeg
        elif [ "$OS" = "centos" ] || [ "$OS" = "rhel" ]; then
            sudo yum install -y ffmpeg
        fi
        echo "✅ FFmpeg הותקן בהצלחה!"
    else
        echo "✅ FFmpeg כבר מותקן"
    fi
fi

# יצירת תיקיית הורדות
echo ""
echo "📁 האם ליצור תיקיית הורדות? (y/n)"
read -r create_downloads
if [ "$create_downloads" = "y" ]; then
    DOWNLOAD_DIR="$HOME/downloads"
    mkdir -p "$DOWNLOAD_DIR"
    echo "✅ תיקיית הורדות נוצרה: $DOWNLOAD_DIR"
    
    # יצירת קובץ config
    CONFIG_DIR="$HOME/.config/yt-dlp"
    mkdir -p "$CONFIG_DIR"
    CONFIG_FILE="$CONFIG_DIR/config"
    
    cat > "$CONFIG_FILE" << EOF
# קובץ הגדרות yt-dlp
-o $DOWNLOAD_DIR/%(title)s.%(ext)s
-f bestvideo+bestaudio/best
--no-mtime
EOF
    echo "✅ קובץ הגדרות נוצר: $CONFIG_FILE"
fi

# התקנת WebUI (אופציונלי)
echo ""
echo "🌐 האם להתקין yt-dlp-webui? (y/n)"
read -r install_webui
if [ "$install_webui" = "y" ]; then
    echo "📥 מתקין yt-dlp-webui..."
    pip3 install yt-dlp-webui
    echo "✅ yt-dlp-webui הותקן!"
    echo ""
    echo "להפעלה, הרץ:"
    echo "  yt-dlp-webui --host 0.0.0.0 --port 8080"
fi

# התקנת Flask API (אופציונלי)
echo ""
echo "🔌 האם להתקין Flask API? (y/n)"
read -r install_flask
if [ "$install_flask" = "y" ]; then
    echo "📥 מתקין Flask..."
    pip3 install flask
    echo "✅ Flask הותקן!"
    echo ""
    echo "צור קובץ api_server.py (ראה DEPLOYMENT_GUIDE_HE.md)"
fi

echo ""
echo "=========================================="
echo "✅ ההתקנה הושלמה בהצלחה!"
echo "=========================================="
echo ""
echo "דוגמאות שימוש:"
echo "  yt-dlp 'URL'                    # הורדת וידאו"
echo "  yt-dlp -x --audio-format mp3 'URL'  # הורדת אודיו"
echo "  yt-dlp --version                # בדיקת גרסה"
echo ""
echo "לקריאת המדריך המלא, ראה: DEPLOYMENT_GUIDE_HE.md"



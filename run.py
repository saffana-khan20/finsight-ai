import warnings
warnings.filterwarnings('ignore', category=DeprecationWarning)
from app import app, socketio
from db import init_db
from services.reminders import start_reminder_scheduler

if __name__ == '__main__':
    print("🔧 Initializing database...")
    init_db()
    start_reminder_scheduler()
    print("🚀 Starting FinSight AI on http://localhost:5000")
    # ⭐ Debug mode off
    socketio.run(app, host='0.0.0.0', port=5000, debug=False)
from flask import Flask, request, jsonify
from flask_cors import CORS
import secrets
from datetime import datetime
import mysql.connector

app = Flask(__name__)
# 2. Use this EXACT line to allow the dashboard to talk to the brain
CORS(app, resources={r"/api/*": {"origins": "*"}})
# --- Database Config ---
db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '',
    'database': 'attendance_system'
}

@app.route('/api/start_session', methods=['POST'])
def start_session():
    print("--- Start Session Request Received ---")
    data = request.get_json()
    course_code = data.get("course_code", "Unknown")
    
    generated_secret = secrets.token_urlsafe(16)
    token = f"http://192.168.43.12:5000/api/mark_attendance?token={generated_secret}"
    now = datetime.now()
    
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        sql = "INSERT INTO Class_Sessions (CourseCode, SessionDate, StartTime, ActiveToken) VALUES (%s, %s, %s, %s)"
        val = (course_code, now.date(), now.time(), token)
        
        cursor.execute(sql, val)
        conn.commit()
        session_id = cursor.lastrowid
        
        print(f"✅ Success! Session {session_id} created.")
        return jsonify({
            "status": "success",
            "session_id": session_id,
            "current_token": token
        }), 201

    except Exception as e:
        print(f"❌ DATABASE ERROR: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/')
def home():
    return "<h1>Attendance Server is Running!</h1>"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
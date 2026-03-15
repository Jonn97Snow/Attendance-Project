import qrcode
import secrets
import time
import os

def generate_session_token():
    """
    Generates a secure, 32-character random token for the database.
    """
    # Generate a URL-safe text string
    token = secrets.token_urlsafe(32)
    return token

def create_qr_code(token, session_id):
    """
    Converts the token into a QR code image and saves it.
    In a live web app, you would pass this directly to the frontend 
    instead of saving it as a file, but this is great for testing.
    """
    # The data the phone will read when it scans the code
    # We include the session_id so the server knows which class this is for
    qr_data = f"session:{session_id}|token:{token}"

    # Configure the QR code appearance and error correction
    qr = qrcode.QRCode(
        version=1, # Size of the QR code (1 is smallest)
        error_correction=qrcode.constants.ERROR_CORRECT_H, # High error correction
        box_size=10, # Size of each 'pixel' in the QR code
        border=4,
    )
    
    qr.add_data(qr_data)
    qr.make(fit=True)

    # Create the image
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Save it locally to test
    filename = f"live_qr_session_{session_id}.png"
    img.save(filename)
    
    print(f"QR Code generated and saved as {filename}")
    print(f"Contained Data: {qr_data}")
    
    return qr_data

# --- Testing the Logic ---
if __name__ == '__main__':
    print("Starting Live Attendance Session...")
    
    # Simulating a specific class session (e.g., SessionID = 101 from your database)
    current_session_id = 101 
    
    # Generate the secure token
    active_token = generate_session_token()
    
    # Create the QR code containing that token
    qr_content = create_qr_code(active_token, current_session_id)
    
    # In your final app, this is where you would call an UPDATE SQL query 
    # to save 'active_token' to the 'Class_Sessions' table for this SessionID.
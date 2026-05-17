from flask import Flask, request, redirect, session
import psycopg2
import time

app = Flask(__name__)
app.secret_key = "ctf_secret_key"

# ---------------- DB CONNECTION ----------------
while True:
    try:
        conn = psycopg2.connect(
            host="postgres-sqli",
            database="blindsqli",
            user="postgres",
            password="postgres"
        )
        print("Connected to DB")
        break
    except Exception as e:
        print("Waiting for DB...")
        time.sleep(2)

# ---------------- HOME PAGE ----------------
@app.route("/")
def home():
    return """
    <html>
    <head>
        <title>Secure Portal</title>
        <style>
            body {
                margin: 0;
                height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                background: radial-gradient(circle, #1e293b, #0f172a);
                font-family: Arial;
                color: white;
            }
            .card {
                width: 360px;
                padding: 30px;
                background: rgba(30, 41, 59, 0.95);
                border-radius: 15px;
                text-align: center;
                box-shadow: 0 0 20px rgba(0,0,0,0.6);
            }
            input {
                width: 100%;
                padding: 10px;
                margin: 8px 0;
                border-radius: 8px;
                border: none;
                background: #0f172a;
                color: white;
            }
            button {
                width: 100%;
                padding: 10px;
                border-radius: 8px;
                border: none;
                background: #38bdf8;
                font-weight: bold;
                cursor: pointer;
            }
            button:hover {
                background: #0ea5e9;
            }
            h2 { color: #38bdf8; }
        </style>
    </head>
    <body>
        <div class="card">
            <h2>Secure Login</h2>
            <form action="/login" method="POST">
                <input name="username" placeholder="Username">
                <input name="password" type="password" placeholder="Password">
                <button type="submit">Login</button>
            </form>
        </div>
    </body>
    </html>
    """

# ---------------- TIME-BASED BLIND SQLi LOGIN ----------------
@app.route("/login", methods=["POST"])
def login():

    username = request.form.get("username")
    password = request.form.get("password")

    cur = conn.cursor()

    query = f"SELECT password FROM users WHERE username = '{username}'"

    print("QUERY:", query)

   
    cur.execute(query)
    result = cur.fetchone()

    if result and password == result[0]:
        session["user"] = username
        return redirect("/dashboard")

    # NO sleep here. NO message. NOTHING.
    # The sleep comes ONLY from your injected payload
    return ""

# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")
    
    user = session["user"]
    cur = conn.cursor()
    
    if user == "admin":
        # Get users
        cur.execute("SELECT id, username, password FROM users")
        users = cur.fetchall()
        
        # Get credit cards
        cur.execute("""
            SELECT u.username, c.card_number, c.expiry 
            FROM credit_cards c 
            JOIN users u ON c.user_id = u.id
        """)
        cards = cur.fetchall()
        
        # Get flag
        cur.execute("SELECT flag FROM flags LIMIT 1")
        flag = cur.fetchone()[0]
        
        # Build users table rows
        users_rows = ""
        for u in users:
            users_rows += f"""
            <tr>
                <td>{u[0]}</td>
                <td>{u[1]}</td>
                <td>{u[2]}</td>
            </tr>
            """
        
        # Build credit cards table rows
        cards_rows = ""
        for c in cards:
            cards_rows += f"""
            <tr>
                <td>{c[0]}</td>
                <td class="credit-card">{c[1]}</td>
                <td>{c[2]}</td>
            </tr>
            """
        
        return f"""
        <html>
        <head>
            <style>
                body {{
                    margin: 0;
                    min-height: 100vh;
                    background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
                    font-family: 'Segoe UI', Arial, sans-serif;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    padding: 20px;
                }}
                .container {{
                    max-width: 900px;
                    width: 100%;
                    background: rgba(30, 41, 59, 0.95);
                    border-radius: 20px;
                    padding: 30px;
                    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
                    backdrop-filter: blur(10px);
                    border: 1px solid rgba(56, 189, 248, 0.3);
                }}
                h1 {{
                    text-align: center;
                    color: #38bdf8;
                    margin-bottom: 30px;
                    font-size: 28px;
                }}
                h2 {{
                    color: #38bdf8;
                    margin-top: 25px;
                    margin-bottom: 15px;
                    font-size: 20px;
                    border-bottom: 1px solid #334155;
                    padding-bottom: 8px;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 10px;
                    margin-bottom: 20px;
                }}
                th {{
                    background: #0f172a;
                    color: #38bdf8;
                    padding: 12px;
                    text-align: left;
                    font-weight: 600;
                }}
                td {{
                    background: #1e293b;
                    color: #cbd5e1;
                    padding: 10px;
                    border-bottom: 1px solid #334155;
                }}
                .flag-box {{
                    text-align: center;
                    background: linear-gradient(135deg, #1e3a5f 0%, #0f172a 100%);
                    border: 2px solid #38bdf8;
                    border-radius: 12px;
                    padding: 20px;
                    margin-top: 25px;
                }}
                .flag-box h2 {{
                    border: none;
                    color: #38bdf8;
                    margin-bottom: 10px;
                }}
                .flag-value {{
                    font-family: monospace;
                    font-size: 20px;
                    font-weight: bold;
                    color: #fbbf24;
                    letter-spacing: 1px;
                }}
                .credit-card {{
                    font-family: monospace;
                    font-weight: bold;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🔐 ADMIN DASHBOARD</h1>
                
                <h2>👥 System Users</h2>
                <table>
                    <tr>
                        <th>ID</th>
                        <th>Username</th>
                        <th>Password</th>
                    </tr>
                    {users_rows}
                </table>
                
                <h2>💳 Credit Cards (Sensitive Data)</h2>
                <table>
                    <tr>
                        <th>User</th>
                        <th>Card Number</th>
                        <th>Expiry</th>
                    </tr>
                    {cards_rows}
                </table>
                
                <div class="flag-box">
                    <h2>🏁 SECRET FLAG</h2>
                    <div class="flag-value">{flag}</div>
                </div>
            </div>
        </body>
        </html>
        """
    
    # Normal user dashboard
    return f"""
    <html>
    <head>
        <style>
            body {{
                margin: 0;
                min-height: 100vh;
                background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
                font-family: 'Segoe UI', Arial, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
            }}
            .container {{
                text-align: center;
                background: rgba(30, 41, 59, 0.95);
                border-radius: 20px;
                padding: 40px;
                box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
            }}
            h1 {{
                color: #38bdf8;
                font-size: 32px;
            }}
            p {{
                color: #cbd5e1;
                font-size: 18px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>👋 Welcome {user}</h1>
            <p>You are logged in as a standard user.</p>
            <p>Administrator privileges required to access sensitive data.</p>
        </div>
    </body>
    </html>
    """

# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
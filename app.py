from flask import Flask, request, redirect, session

app = Flask(__name__)
app.secret_key = "secret123"

users = {}
tickets = {}

def html_page(content):
    return f"<html><body>{content}</body></html>"

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        u = request.form["username"]
        p = request.form["password"]
        if u in users and users[u] == p:
            session["user"] = u
            return redirect("/dashboard")
    return html_page('''
    <h2>Login</h2>
    <form method="POST">
    Username:<input name="username"><br>
    Passwort:<input type="password" name="password"><br>
    <button>Login</button>
    </form>
    <a href="/register">Registrieren</a>
    ''')

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        users[request.form["username"]] = request.form["password"]
        return redirect("/")
    return html_page('''
    <h2>Registrieren</h2>
    <form method="POST">
    Username:<input name="username"><br>
    Passwort:<input type="password" name="password"><br>
    <button>Registrieren</button>
    </form>
    ''')

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "user" not in session:
        return redirect("/")
    
    user = session["user"]
    if user not in tickets:
        tickets[user] = []

    if request.method == "POST":
        start = request.form["start"]
        ziel = request.form["ziel"]
        preis = float(request.form["distanz"]) * 0.5
        tickets[user].append(f"{start} → {ziel} | {preis:.2f}€")

    ticket_list = "<br>".join(tickets[user])

    return html_page(f'''
    <h2>Dashboard ({user})</h2>
    <form method="POST">
    Start:<input name="start"><br>
    Ziel:<input name="ziel"><br>
    Distanz:<input name="distanz"><br>
    <button>Ticket kaufen</button>
    </form>
    <h3>Tickets:</h3>
    {ticket_list}
    <br><br>
    <a href="/logout">Logout</a>
    ''')

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

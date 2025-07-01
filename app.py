from flask import Flask, render_template, request, redirect, url_for, flash
import os, requests

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "change_this_secret")

GITHUB_USERNAME = "Codezxz"  # Nirnay Sheshware

@app.route("/")
def index():
    resp = requests.get(f"https://api.github.com/users/{GITHUB_USERNAME}/repos?sort=updated")
    repos = resp.json() if resp.ok else []
    projects = [
        {"name": r["name"], "url": r["html_url"], "desc": r.get("description") or ""}
        for r in repos if not r.get("private")
    ][:6]
    return render_template("index.html", projects=projects)

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")
        with open("messages.txt", "a", encoding="utf-8") as f:
            f.write(f"{name} <{email}>: {message}\n")
        flash("Thanks for reaching out! I'll get back to you soon.")
        return redirect(url_for("index"))
    return render_template("contact.html")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)

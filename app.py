import os
import pandas as pd
from flask import Flask, render_template, redirect, request, url_for, make_response, flash

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "polls.csv")
COLUMNS = ["question", "option1", "option2", "option3", "votes1", "votes2", "votes3"]

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-only-change-me")


def load_polls():
    if not os.path.exists(DATA_FILE):
        pd.DataFrame(columns=COLUMNS).rename_axis("p_id").to_csv(DATA_FILE)
    try:
        polls = pd.read_csv(DATA_FILE, index_col=0)
    except (pd.errors.EmptyDataError, pd.errors.ParserError):
        polls = pd.DataFrame(columns=COLUMNS)
    for column in COLUMNS:
        if column not in polls.columns:
            polls[column] = 0 if column.startswith("votes") else ""
    return polls[COLUMNS]


def save_polls(polls):
    polls.to_csv(DATA_FILE, index_label="p_id")


@app.route("/")
def index():
    return render_template("index.html", polls=load_polls())


@app.route("/poll/<int:p_id>")
def show_poll(p_id):
    polls = load_polls()
    if p_id not in polls.index:
        flash("That poll does not exist.", "error")
        return redirect(url_for("index"))
    return render_template("show_poll.html", p_id=p_id, poll=polls.loc[p_id].to_dict())


@app.route("/polls", methods=["GET", "POST"])
def create_poll():
    if request.method == "POST":
        question = request.form.get("question", "").strip()
        options = [request.form.get(f"option{i}", "").strip() for i in (1, 2, 3)]
        if not question or any(not option for option in options):
            flash("Enter a question and all three options.", "error")
            return render_template("create_poll.html", question=question, options=options), 400
        polls = load_polls()
        p_id = int(polls.index.max()) + 1 if len(polls.index) else 1
        polls.loc[p_id] = [question, *options, 0, 0, 0]
        save_polls(polls)
        flash("Poll created successfully.", "success")
        return redirect(url_for("index"))
    return render_template("create_poll.html", question="", options=["", "", ""])


@app.route("/vote/<int:p_id>/<int:option_number>", methods=["POST"])
def vote(p_id, option_number):
    polls = load_polls()
    if p_id not in polls.index or option_number not in (1, 2, 3):
        flash("Invalid poll or option.", "error")
        return redirect(url_for("index"))
    cookie_name = f"voted_poll_{p_id}"
    if request.cookies.get(cookie_name):
        flash("You have already voted in this poll on this browser.", "error")
        return redirect(url_for("show_poll", p_id=p_id))
    vote_column = f"votes{option_number}"
    polls.loc[p_id, vote_column] = int(polls.loc[p_id, vote_column]) + 1
    save_polls(polls)
    response = make_response(redirect(url_for("show_poll", p_id=p_id)))
    response.set_cookie(cookie_name, str(option_number), max_age=60 * 60 * 24 * 365,
                        httponly=True, samesite="Lax")
    return response


if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, request, session, redirect, url_for, jsonify
import os, json

app = Flask(__name__)
app.secret_key = "change_this_secret"
RECIPE_DIR = "recipes"
os.makedirs(RECIPE_DIR, exist_ok=True)
@app.route("/")
def index():
    recipes = [f[:-5] for f in os.listdir(RECIPE_DIR) if f.endswith('.json')]
    return render_template('index.html', recipes=recipes)
@app.route("/select/<rid>")
def select(rid):
    session['rid'] = rid; session['idx'] = 0
    return redirect(url_for('view'))
@app.route("/view")
def view():
    rid = session.get('rid');
    if not rid: return redirect(url_for('index'))
    with open(f"{RECIPE_DIR}/{rid}.json") as f: recipe = json.load(f)
    idx = session.get('idx', 0)
    return render_template('recipe.html', title=recipe['title'], ingredients=recipe['ingredients'], step=recipe['steps'][idx], idx=idx+1, total=len(recipe['steps']))
@app.route("/navigate", methods=["POST"])
def navigate():
    data = request.get_json() or request.form; cmd = data.get('command','').lower()
    rid, idx = session.get('rid'), session.get('idx', 0)
    with open(f"{RECIPE_DIR}/{rid}.json") as f: recipe = json.load(f)
    if 'next' in cmd: idx = min(idx+1, len(recipe['steps'])-1)
    elif 'back' in cmd: idx = max(idx-1,0)
    elif 'start' in cmd: idx = 0
    session['idx'] = idx
    return jsonify(step=recipe['steps'][idx], idx=idx+1)
if __name__=='__main__': app.run(host='0.0.0.0', port=5000)
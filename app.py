from flask import Flask, request, redirect, render_template_string, url_for
import string, random, sqlite3, os

app = Flask(__name__)
USE_SQLITE = os.environ.get('USE_SQLITE', 'False').lower() == 'true'  # Switch via env var, default in-memory



# SQLite setup
DB_PATH = 'urls.db'
def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS urls (
            shortcode TEXT PRIMARY KEY,
            url TEXT NOT NULL
        )''')

# Always initialize SQLite table at module import if needed
if USE_SQLITE:
    init_db()

# Ensure SQLite table is initialized on every worker startup (gunicorn spawns multiple workers)

# Ensure SQLite table is initialized on every request (compatible with all Flask versions)
@app.before_request
def setup_db():
    if USE_SQLITE and not os.path.exists(DB_PATH):
        init_db()

# In-memory storage
url_map = {}

def save_url(shortcode, url):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('INSERT INTO urls (shortcode, url) VALUES (?, ?)', (shortcode, url))

def get_url(shortcode):
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute('SELECT url FROM urls WHERE shortcode=?', (shortcode,))
        row = cur.fetchone()
        return row[0] if row else None

def get_all_urls():
    with sqlite3.connect(DB_PATH) as conn:
        return conn.execute('SELECT shortcode, url FROM urls').fetchall()

def generate_shortcode(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@app.route('/', methods=['GET', 'POST'])
def index():
    # Pagination
    page = int(request.args.get('page', 1))
    per_page = 10
    if request.method == 'POST':
        long_url = request.form['url']
        shortcode = generate_shortcode()
        if USE_SQLITE:
            save_url(shortcode, long_url)
        else:
            url_map[shortcode] = long_url
        # After adding, redirect to main page
        return redirect(url_for('index'))
    # Get links
    if USE_SQLITE:
        all_links = get_all_urls()
    else:
        all_links = list(url_map.items())
    total = len(all_links)
    start = (page - 1) * per_page
    end = start + per_page
    links = all_links[start:end]
    next_page = page + 1 if end < total else None
    prev_page = page - 1 if start > 0 else None
    return render_template_string('''
        <h1>URL Shortener</h1>
        <form method="post">
            <input name="url" type="url" required placeholder="Enter long URL">
            <input type="submit" value="Shorten">
        </form>
        <h2>All Stored Links</h2>
        <ul>
        {% for code, url in links %}
            <li><a href="/{{ code }}">{{ request.host_url }}{{ code }}</a> &rarr; {{ url }}</li>
        {% endfor %}
        </ul>
        <div>
            {% if prev_page %}<a href="?page={{ prev_page }}">Previous</a>{% endif %}
            {% if next_page %}<a href="?page={{ next_page }}">Next</a>{% endif %}
        </div>
    ''', links=links, next_page=next_page, prev_page=prev_page)

@app.route('/<shortcode>')
def redirect_short(shortcode):
    if USE_SQLITE:
        url = get_url(shortcode)
    else:
        url = url_map.get(shortcode)
    if url:
        return redirect(url)
    return 'Shortcode not found', 404

@app.route('/list')
def list_links():
    if USE_SQLITE:
        links = get_all_urls()
    else:
        links = url_map.items()
    return render_template_string('''
        <h2>All Stored Links</h2>
        <ul>
        {% for code, url in links %}
            <li><a href="/{{ code }}">{{ request.host_url }}{{ code }}</a> &rarr; {{ url }}</li>
        {% endfor %}
        </ul>
        <a href="/">Back</a>
    ''', links=links)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

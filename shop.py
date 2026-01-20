from flask import Flask, render_template_string, request, session, redirect, url_for
import random
import datetime
import os

app = Flask(__name__)
app.secret_key = 'flipkart_mega_master_v10_final'

# ==========================================
# 1. SETTINGS & CONFIG
# ==========================================
MY_UPI_ID = "9653314458@naviaxis"
MY_NAME = "Apni Dukaan"

products = []
next_id = 1

# ==========================================
# 2. MEGA INVENTORY GENERATOR (STRICT LOGIC)
# ==========================================
def add_item(name, price, mrp, cat, img):
    global next_id
    products.append({
        'id': next_id, 'name': name, 'price': price, 'mrp': mrp,
        'discount': int(((mrp - price) / mrp) * 100),
        'category': cat, 'main_image': img,
        'rating': round(random.uniform(4.1, 4.9), 1),
        'reviews': f"{random.randint(800, 70000)}",
    })
    next_id += 1

def generate_mega_stock():
    # --- 1. ROBOTICS & MODULES (Under Rs 250) --- 120 items
    robotic_images = [
        "https://m.media-amazon.com/images/I/61pInh+6fVL._SX679_.jpg", # Pi Pico
        "https://m.media-amazon.com/images/I/61+A+B+C+DL._SX679_.jpg", # Arduino
        "https://m.media-amazon.com/images/I/51r-J1Y2+ZL._SX679_.jpg", # IR Sensor
        "https://m.media-amazon.com/images/I/61+E+F+G+HL._SX679_.jpg"  # Ultrasonic
    ]
    robotic_names = ["Raspberry Pi Pico W", "Arduino Uno R3", "IR Sensor Pro", "Ultrasonic Distance Sensor", "SG90 Servo Motor", "Relay 5V Module"]
    
    for i in range(120):
        name = f"{random.choice(robotic_names)} v{i}"
        price = random.choice([9, 19, 49, 99, 149, 249])
        img = robotic_images[i % len(robotic_images)]
        add_item(name, price, price+300, "Robotics", img)

    # --- 2. FASHION (Saree, Bra, Coat, Shoes) --- 150 items
    fashion_pool = [
        {"name": "Silk Banarasi Saree", "img": "https://m.media-amazon.com/images/I/91J-Wd8kH+L._UY879_.jpg", "price": 499},
        {"name": "Premium Lace Bra", "img": "https://m.media-amazon.com/images/I/71k+p+q+r+sL._UY879_.jpg", "price": 99},
        {"name": "Woolen Winter Coat", "img": "https://m.media-amazon.com/images/I/61utX8kBDlL._UY879_.jpg", "price": 899},
        {"name": "Nike Sports Shoes", "img": "https://m.media-amazon.com/images/I/61utX8kBDlL._UY695_.jpg", "price": 1299},
        {"name": "Leather Formal Belt", "img": "https://m.media-amazon.com/images/I/71V2pYmB8LL._UY695_.jpg", "price": 199}
    ]
    for i in range(150):
        item = fashion_pool[i % len(fashion_pool)]
        add_item(f"{item['name']} Classic {i}", item['price'], item['price']*4, "Fashion", item['img'])

    # --- 3. SPORTS (Bat, Ball) --- 50 items
    bat_img = "https://rukminim2.flixcart.com/image/416/416/xif0q/bat/q/t/y/1-plastic-cricket-bat-for-kids-plastic-cricket-bat-full-size-original-imagpyz5a5z5z5ze.jpeg"
    ball_img = "https://m.media-amazon.com/images/I/61+w+e+r+tL._UY695_.jpg"
    for i in range(50):
        if i % 2 == 0:
            add_item(f"Heavy Plastic Cricket Bat {i}", 99, 999, "Sports", bat_img)
        else:
            add_item(f"Leather Cricket Stitch Ball {i}", 49, 499, "Sports", ball_img)

    # --- 4. MOBILES (Samsung, iPhone, Vivo, Poco) --- 100 items
    mobile_pool = [
        {"name": "iPhone 15 Pro Max", "img": "https://m.media-amazon.com/images/I/81Sig6biNGL._SX679_.jpg", "price": 148900},
        {"name": "Samsung S24 Ultra", "img": "https://m.media-amazon.com/images/I/81vxWpPpgNL._SX679_.jpg", "price": 129999},
        {"name": "Poco M6 Pro 5G", "img": "https://m.media-amazon.com/images/I/6175SlKKECL._SX679_.jpg", "price": 999}, # Loot
        {"name": "Vivo V29 5G", "img": "https://m.media-amazon.com/images/I/61f4dTush1L._SX679_.jpg", "price": 32999}
    ]
    for i in range(100):
        m = mobile_pool[i % len(mobile_pool)]
        add_item(f"{m['name']} Edition-{i}", m['price'], m['price']+15000, "Mobiles", m['img'])

    # --- 5. LOOT DEALS --- 100 items
    for i in range(100):
        add_item(f"Super Loot Item {i}", random.choice([5, 9, 19, 49]), 499, "Loot", "https://m.media-amazon.com/images/I/51+a+b+c+dL._SX679_.jpg")

generate_mega_stock()

# ==========================================
# 3. HTML UI (Flipkart Real Theme)
# ==========================================
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Flipkart Mega Store</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        :root { --fk-blue: #2874f0; --fk-yellow: #ff9f00; --bg: #f1f3f6; }
        body { background: var(--bg); padding-bottom: 70px; font-family: sans-serif; }
        a { text-decoration: none; color: inherit; }
        .navbar { background: var(--fk-blue); padding: 10px; position: sticky; top: 0; z-index: 1000; }
        .cat-scroll { display: flex; overflow-x: auto; background: white; padding: 10px; gap: 15px; border-bottom: 1px solid #ddd; scrollbar-width: none; }
        .cat-item { text-align: center; min-width: 65px; text-decoration: none; color: #333; font-size: 0.75rem; }
        .cat-icon { width: 45px; height: 45px; background: #eef3ff; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-bottom: 5px; font-size: 1.2rem; }
        .loot-banner { background: linear-gradient(90deg, #ff0000, #ff9f00); color: white; padding: 25px 15px; text-align: center; font-weight: bold; font-size: 1.3rem; margin: 10px; border-radius: 8px; border: 2px solid white; box-shadow: 0 4px 15px rgba(255,0,0,0.3); }
        .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 4px; padding: 4px; }
        .card { background: white; border: 1px solid #ddd; border-radius: 4px; display: flex; flex-direction: column; overflow: hidden; height: 100%; position: relative;}
        .card img { width: 100%; height: 150px; object-fit: contain; padding: 10px; background: white; }
        .tag-loot { position: absolute; top: 0; left: 0; background: #26a541; color: white; font-size: 9px; padding: 2px 5px; }
        .p-price { font-weight: bold; font-size: 1rem; }
    </style>
</head>
<body>
    {% if page == 'register' %}
    <div class="container-fluid bg-white" style="min-height: 100vh; padding-top: 50px;">
        <div class="text-center mb-4"><h1 style="color:var(--fk-blue); font-weight:bold; font-style:italic;">Flipkart</h1><p class="text-muted">Account Setup</p></div>
        <div class="p-4 border rounded mx-2 shadow-sm">
            <form action="/setup_account" method="POST">
                <input name="name" class="form-control mb-3" placeholder="Full Name" required>
                <input name="phone" type="number" class="form-control mb-3" placeholder="Mobile Number" required>
                <textarea name="address" class="form-control mb-3" placeholder="Full Address with Pincode" required></textarea>
                <button class="btn btn-warning w-100 fw-bold py-2 shadow-sm">CREATE ACCOUNT</button>
            </form>
        </div>
    </div>
    {% else %}
    <nav class="navbar text-white">
        <div class="cat-scroll w-100 mb-2">
            <a href="/?cat=all" class="cat-item"><div class="cat-icon">🏠</div>All</a>
            <a href="/?cat=Mobiles" class="cat-item"><div class="cat-icon">📱</div>Mobiles</a>
            <a href="/?cat=Robotics" class="cat-item"><div class="cat-icon">🤖</div>Robotics</a>
            <a href="/?cat=Fashion" class="cat-item"><div class="cat-icon">👕</div>Fashion</a>
            <a href="/?cat=Sports" class="cat-item"><div class="cat-icon">🏏</div>Sports</a>
            <a href="/?cat=Loot" class="cat-item"><div class="cat-icon">🔥</div>Loot</a>
        </div>
        <div class="d-flex w-100 justify-content-between align-items-center mb-2">
            <div class="fw-bold fs-5 italic">Flipkart</div>
            <div class="small"><i class="fas fa-user-circle"></i> {{ session.user.name }}</div>
        </div>
        <form action="/" class="w-100"><input name="q" class="form-control rounded-1" placeholder="Search 500+ Unique Items..."></form>
    </nav>

    {% if page == 'home' %}
        <a href="/?cat=Loot" style="text-decoration:none;"><div class="loot-banner">🔥 HUGE BILLION LOOT: ₹9, ₹19, ₹49 STORE! 🔥</div></a>
        <div class="grid">
            {% for p in items %}<a href="/product/{{ p.id }}" class="card text-dark text-decoration-none">
                <span class="tag-loot">Hot Deal</span>
                <img src="{{ p.main_image }}" loading="lazy" onerror="this.src='https://via.placeholder.com/150?text=Flipkart'">
                <div class="p-2"><div class="small text-truncate" style="height:32px;">{{ p.name }}</div><div class="fw-bold">₹{{ p.price }} <span class="text-muted text-decoration-line-through small" style="font-size:10px;">₹{{ p.mrp }}</span></div></div>
            </a>{% endfor %}
        </div>
    {% elif page == 'detail' %}
        <div class="bg-white p-4 text-center border-bottom"><img src="{{ p.main_image }}" style="max-height: 350px; max-width: 100%;"></div>
        <div class="p-3 bg-white mt-2">
            <h5 class="fw-bold">{{ p.name }}</h5><div class="badge bg-success mb-2">{{ p.rating }} ★</div>
            <h2 class="fw-bold">₹{{ p.price }} <span class="text-muted fs-6 text-decoration-line-through">₹{{ p.mrp }}</span></h2>
            <hr><p class="small text-muted"><i class="fas fa-map-marker-alt"></i> Delivering to: <b>{{ session.user.address }}</b></p>
            <a href="/buy_now/{{ p.id }}" class="btn btn-warning w-100 py-3 fw-bold">BUY NOW</a>
        </div>
    {% elif page == 'payment' %}
        <div class="p-4 bg-white m-3 text-center shadow-sm rounded">
            <h5>Payment Confirmation</h5><div class="alert alert-success mt-3">Amount: ₹{{ session.buy_price }}</div>
            <a href="upi://pay?pa={{ upi_id }}&pn={{ upi_name }}&am={{ session.buy_price }}&cu=INR" class="btn btn-success w-100 py-3 fw-bold" onclick="ok()">PAY VIA UPI</a>
            <form id="f" action="/success" method="POST"></form>
        </div><script>function ok(){setTimeout(()=>document.getElementById('f').submit(),5000);}</script>
    {% elif page == 'success' %}
        <div class="text-center mt-5 p-5"><i class="fas fa-check-circle text-success" style="font-size:80px;"></i><h2 class="mt-4">Order Confirmed!</h2><a href="/" class="btn btn-primary mt-4">Continue Shopping</a></div>
    {% elif page == 'my_orders' %}
        <div class="p-3"><h5>My Orders</h5>
            {% for o in orders %}<div class="card mb-3 p-3 flex-row gap-3 shadow-sm"><img src="{{ o.image }}" style="width:60px; height:60px; object-fit:contain;"><div>{{ o.item }}<br>₹{{ o.amount }}<br><span class="text-success small fw-bold">Shipped</span></div></div>{% endfor %}
        </div>
    {% endif %}

    <div class="fixed-bottom bg-white d-flex border-top py-2 shadow-lg" style="z-index: 1000;">
        <a href="/" class="flex-grow-1 text-center small text-dark"><i class="fas fa-home d-block"></i>Home</a>
        <a href="/my_orders" class="flex-grow-1 text-center small text-dark"><i class="fas fa-box d-block"></i>Orders</a>
        <a href="/cart" class="flex-grow-1 text-center small text-dark"><i class="fas fa-shopping-cart d-block"></i>Cart</a>
        <a href="/" class="flex-grow-1 text-center small text-dark"><i class="fas fa-user d-block"></i>User</a>
    </div>
    {% endif %}
</body>
</html>
"""

# ==========================================
# 4. ROUTES
# ==========================================
@app.before_request
def check_user():
    if 'user' not in session and request.endpoint not in ['setup_account', 'static']:
        return render_template_string(HTML_TEMPLATE, page='register')

@app.route('/setup_account', methods=['POST'])
def setup_account():
    session['user'] = {'name': request.form.get('name'), 'address': request.form.get('address')}
    return redirect('/')

@app.route('/')
def home():
    q, cat = request.args.get('q', '').lower(), request.args.get('cat', 'all')
    items = products
    if q: items = [p for p in products if q in p['name'].lower()]
    elif cat != 'all': items = [p for p in products if p['category'] == cat]
    return render_template_string(HTML_TEMPLATE, page='home', items=items[:300])

@app.route('/product/<int:pid>')
def detail(pid):
    p = next((i for i in products if i['id'] == pid), None)
    return render_template_string(HTML_TEMPLATE, page='detail', p=p)

@app.route('/buy_now/<int:pid>')
def buy_now(pid):
    p = next((i for i in products if i['id'] == pid), None)
    session['buy_price'], session['buy_item'], session['buy_img'] = p['price'], p['name'], p['main_image']
    return redirect('/payment')

@app.route('/payment')
def payment(): return render_template_string(HTML_TEMPLATE, page='payment', upi_id=MY_UPI_ID, upi_name=MY_NAME)

@app.route('/success', methods=['POST'])
def ok():
    orders = session.get('orders', [])
    orders.insert(0, {'item': session.get('buy_item'), 'amount': session.get('buy_price'), 'image': session.get('buy_img')})
    session['orders'] = orders
    return render_template_string(HTML_TEMPLATE, page='success')

@app.route('/my_orders')
def my_orders(): return render_template_string(HTML_TEMPLATE, page='my_orders', orders=session.get('orders', []))

@app.route('/cart')
def cart(): return redirect('/?cat=all')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

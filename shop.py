from flask import Flask, render_template_string, request, session, redirect, url_for
import random
import datetime
import os

app = Flask(__name__)
app.secret_key = 'flipkart_master_v100'

# ==========================================
# 1. SETTINGS & GLOBAL DATA
# ==========================================
MY_UPI_ID = "9653314458@naviaxis"
MY_NAME = "Apni Dukaan"
START_DATE = datetime.date(2024, 1, 1) # Is date se ginti shuru hogi

products = []
next_id = 1

# ==========================================
# 2. DAILY UPDATE POOL (Daily 5 Items)
# ==========================================
DAILY_POOL = [
    ("Realme 12 Pro", 22999, "Mobile", "https://m.media-amazon.com/images/I/81ogvU1sn6L._SX679_.jpg", {"RAM":"8GB", "ROM":"128GB"}),
    ("JBL Flip 6 Speaker", 8999, "Electronics", "https://m.media-amazon.com/images/I/71+y+z+0+1L._SX679_.jpg", {"Type":"Bluetooth", "Battery":"12Hrs"}),
    ("Nike Air Jordan", 4999, "Fashion", "https://m.media-amazon.com/images/I/61utX8kBDlL._UY695_.jpg", {"Size":"UK 9", "Material":"Leather"}),
    ("Digital Watch (Loot)", 49, "Loot", "https://m.media-amazon.com/images/I/61+m+n+o+pL._SX679_.jpg", {"Type":"LED", "Color":"Black"}),
    ("Kitchen Knife Set", 199, "Home", "https://m.media-amazon.com/images/I/61+q+r+s+tL._SX679_.jpg", {"Pieces":"6", "Steel":"Stainless"}),
    ("Lava Agni 2", 19999, "Mobile", "https://m.media-amazon.com/images/I/71W89+8+kHL._SX679_.jpg", {"RAM":"8GB", "ROM":"256GB"}),
    ("Banarasi Silk Saree", 1299, "Fashion", "https://m.media-amazon.com/images/I/91J-Wd8kH+L._UY879_.jpg", {"Fabric":"Silk", "Length":"6.3m"}),
    ("USB OTG (Loot)", 5, "Loot", "https://m.media-amazon.com/images/I/61+m+n+o+pL._SX679_.jpg", {"Type":"Type-C", "Speed":"480Mbps"}),
    ("Gaming Mouse", 499, "Electronics", "https://m.media-amazon.com/images/I/61+u+v+w+xL._SX679_.jpg", {"DPI":"3200", "RGB":"Yes"}),
    ("School Bag Waterproof", 449, "Bags", "https://m.media-amazon.com/images/I/91y+S0r+jXL._UY879_.jpg", {"Capacity":"30L", "Color":"Blue"})
]

# ==========================================
# 3. HELPER FUNCTIONS
# ==========================================
def add_item(name, price, mrp, cat, imgs, specs, desc, is_new=False):
    global next_id
    products.append({
        'id': next_id,
        'name': name, 'price': price, 'mrp': mrp,
        'discount': int(((mrp - price) / mrp) * 100),
        'category': cat, 'images': imgs, 'specs': specs,
        'desc': desc, 'rating': round(random.uniform(4.0, 4.9), 1),
        'reviews': f"{random.randint(1000, 50000)}", 'is_new': is_new
    })
    next_id += 1

def setup_store():
    # --- FIXED ITEMS (Hamesha rahenge) ---
    # Mobiles (iPhone/Samsung)
    add_item("iPhone 15 Pro Max", 148900, 159900, "Mobile", ["https://m.media-amazon.com/images/I/81vxWpPpgNL._SX679_.jpg", "https://m.media-amazon.com/images/I/81Sig6biNGL._SX679_.jpg", "https://m.media-amazon.com/images/I/81CgtwSII3L._SX679_.jpg"], {"RAM":"8GB", "Storage":"256GB", "Processor":"A17 Pro Chip"}, "Titanium flagship.")
    add_item("Samsung S24 Ultra", 129999, 149999, "Mobile", ["https://m.media-amazon.com/images/I/81vxWpPpgNL._SX679_.jpg", "https://m.media-amazon.com/images/I/71lD7eGdW-L._SX679_.jpg", "https://m.media-amazon.com/images/I/71JLhMM6lAL._SX679_.jpg"], {"RAM":"12GB", "Storage":"256GB", "Processor":"Snapdragon 8 Gen 3"}, "Galaxy AI integration.")
    
    # Sports (Bats/Badminton)
    bat_img = "https://rukminim2.flixcart.com/image/416/416/xif0q/bat/q/t/y/1-plastic-cricket-bat-for-kids-plastic-cricket-bat-full-size-original-imagpyz5a5z5z5ze.jpeg"
    add_item("Plastic Cricket Bat", 99, 999, "Sports", [bat_img, bat_img, bat_img], {"Material":"PVC", "Size":"Full"}, "Durable gully cricket bat.")
    
    badminton_img = "https://rukminim2.flixcart.com/image/416/416/l51d30w0/racquet/z/j/w/g-force-3600-super-lite-strung-1-g-force-3600-super-lite-original-imagft56z7sz5hze.jpeg"
    add_item("Badminton Racket Set", 70, 799, "Sports", [badminton_img, badminton_img, badminton_img], {"Weight":"78g", "Strings":"Strung"}, "Super lite performance.")

    # Loot Items ( Lipstick/Bra/Gadgets)
    add_item("Matte Red Lipstick", 29, 399, "Loot", ["https://m.media-amazon.com/images/I/51+Y+Z+0+1L._SX679_.jpg", "https://m.media-amazon.com/images/I/61+2+3+4+5L._SX679_.jpg", "https://m.media-amazon.com/images/I/61+6+7+8+9L._SX679_.jpg"], {"Finish":"Matte", "Shade":"Ruby Red"}, "12 hour long stay.")
    add_item("Lace Push-up Bra", 49, 899, "Loot", ["https://m.media-amazon.com/images/I/71k+p+q+r+sL._UY879_.jpg", "https://m.media-amazon.com/images/I/71+t+u+v+wL._UY879_.jpg", "https://m.media-amazon.com/images/I/71+x+y+z+0L._UY879_.jpg"], {"Material":"Cotton Lace", "Type":"Padded"}, "Comfort and style.")

    # --- DAILY AUTO-ADD LOGIC ---
    days_passed = (datetime.date.today() - START_DATE).days
    total_to_add = min(days_passed * 5, 100) # Max 100 items

    for i in range(total_to_add):
        pool_item = DAILY_POOL[i % len(DAILY_POOL)]
        add_item(pool_item[0], pool_item[1], pool_item[1]*5, pool_item[2], [pool_item[3], pool_item[3], pool_item[3]], pool_item[4], "Premium New Arrival Product.", is_new=True)

setup_store()

# ==========================================
# 4. HTML TEMPLATE (All Features Integrated)
# ==========================================
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Flipkart Master Sale</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        :root { --fk-blue: #2874f0; --fk-yellow: #ff9f00; --bg: #f1f2f4; }
        body { background: var(--bg); padding-bottom: 70px; font-family: sans-serif; }
        a { text-decoration: none; color: inherit; }
        .navbar { background: var(--fk-blue); padding: 10px; position: sticky; top: 0; z-index: 1000; }
        .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 6px; padding: 6px; }
        .card { background: white; border-radius: 4px; overflow: hidden; position: relative; border: 1px solid #ddd; display: flex; flex-direction: column; }
        .card img { width: 100%; height: 160px; object-fit: contain; padding: 10px; }
        .loot-banner { background: linear-gradient(90deg, #ff0000, #ff9f00); color: white; padding: 15px; text-align: center; font-weight: bold; font-size: 1.1rem; border-radius: 4px; margin: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.2); }
        .tag-new { position: absolute; top: 0; right: 0; background: #ff4d4d; color: white; font-size: 10px; padding: 2px 6px; font-weight:bold; }
        .tag-loot { position: absolute; top: 0; left: 0; background: #26a541; color: white; font-size: 10px; padding: 2px 6px; }
        .sticky-footer { position: fixed; bottom: 0; width: 100%; display: flex; z-index: 2000; background: white; }
        .btn-buy { background: var(--fk-yellow); color: white; padding: 15px; font-weight: bold; flex: 1; border: none; text-align: center; }
        .btn-cart { background: white; color: black; padding: 15px; font-weight: bold; flex: 1; border: 1px solid #ddd; text-align: center;}
        .spec-row { display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #eee; font-size: 0.9rem; }
        .track-box { border-left: 3px solid #26a541; padding-left: 15px; margin-top: 10px; position: relative; }
        .track-dot { width: 10px; height: 10px; background: #26a541; border-radius: 50%; position: absolute; left: -6.5px; top: 0; }
    </style>
</head>
<body>

    <nav class="navbar d-flex flex-column align-items-start">
        <div class="d-flex w-100 justify-content-between align-items-center mb-2">
            <div class="text-white fw-bold italic fs-5">Flipkart<span style="color:var(--fk-yellow)">Plus</span></div>
            <a href="/cart" class="text-white position-relative"><i class="fas fa-shopping-cart fa-lg"></i>
                {% if session.get('cart') %}<span class="badge rounded-pill bg-danger position-absolute top-0 start-100 translate-middle">{{ session.get('cart')|length }}</span>{% endif %}
            </a>
        </div>
        <form action="/" class="w-100"><input name="q" class="form-control rounded-1" placeholder="Search for Products..." value="{{ request.args.get('q', '') }}"></form>
    </nav>

    {% if page == 'home' %}
        <a href="/?cat=Loot"><div class="loot-banner">⚡ CLICK HERE: ₹5 TO ₹99 LOOT STORE ⚡</div></a>
        <div class="d-flex gap-2 overflow-auto p-2 bg-white mb-2 shadow-sm">
            <a href="/?cat=all" class="btn btn-sm btn-outline-primary rounded-pill">All</a>
            <a href="/?cat=Loot" class="btn btn-sm btn-outline-danger rounded-pill">Loot Deals</a>
            <a href="/?cat=Mobile" class="btn btn-sm btn-outline-primary rounded-pill">Mobiles</a>
            <a href="/?cat=Sports" class="btn btn-sm btn-outline-primary rounded-pill">Sports</a>
            <a href="/?cat=Fashion" class="btn btn-sm btn-outline-primary rounded-pill">Fashion</a>
        </div>

        <div class="grid">
            {% for p in items %}
            <a href="/product/{{ p.id }}" class="card text-dark">
                {% if p.is_new %}<span class="tag-new">NEW</span>{% endif %}
                {% if p.discount > 80 %}<span class="tag-loot">{{ p.discount }}% OFF</span>{% endif %}
                <img src="{{ p.images[0] }}" onerror="this.src='https://via.placeholder.com/150'">
                <div class="p-2">
                    <div class="small text-truncate">{{ p.name }}</div>
                    <div class="fw-bold">₹{{ p.price }} <span class="text-muted text-decoration-line-through small">₹{{ p.mrp }}</span></div>
                    <div class="text-success small fw-bold">Free Delivery</div>
                </div>
            </a>
            {% endfor %}
        </div>

    {% elif page == 'detail' %}
        <div id="gallery" class="carousel slide bg-white" data-bs-ride="carousel">
            <div class="carousel-inner">
                {% for img in p.images %}<div class="carousel-item {% if loop.first %}active{% endif %}"><img src="{{ img }}" class="d-block w-100" style="height:350px; object-fit:contain;"></div>{% endfor %}
            </div>
            <button class="carousel-control-prev" data-bs-target="#gallery" data-bs-slide="prev"><span class="carousel-control-prev-icon bg-dark rounded"></span></button>
            <button class="carousel-control-next" data-bs-target="#gallery" data-bs-slide="next"><span class="carousel-control-next-icon bg-dark rounded"></span></button>
        </div>
        <div class="p-3 bg-white mt-2">
            <h5>{{ p.name }}</h5>
            <div class="mb-2"><span class="badge bg-success">{{ p.rating }} ★</span> <small>{{ p.reviews }} ratings</small></div>
            <h1 class="fw-bold">₹{{ p.price }} <span class="text-muted fs-5 text-decoration-line-through">₹{{ p.mrp }}</span></h1>
            <div class="mt-4"><h6 class="fw-bold border-bottom pb-2">Specifications</h6>
                {% for label, val in p.specs.items() %}<div class="spec-row"><span class="text-muted">{{ label }}</span><span>{{ val }}</span></div>{% endfor %}
            </div>
            <div class="bg-light p-3 mt-4 rounded small"><b>7 Days Replacement Policy</b><br>Quality assured product.</div>
        </div>
        <div class="sticky-footer">
            <a href="/" class="btn-cart">ADD CART</a>
            <a href="/buy_now/{{ p.id }}" class="btn-buy">BUY NOW</a>
        </div>

    {% elif page == 'address' %}
        <div class="p-4 bg-white m-3 rounded shadow-sm">
            <h5 class="mb-4">Delivery Address</h5>
            <form action="/payment" method="GET">
                <input name="name" class="form-control mb-3" placeholder="Full Name" required>
                <input name="pincode" class="form-control mb-3" placeholder="Pincode" required>
                <textarea name="addr" class="form-control mb-3" placeholder="Full Address" required></textarea>
                <button class="btn btn-warning w-100 fw-bold py-3">CONTINUE</button>
            </form>
        </div>

    {% elif page == 'payment' %}
        <div class="p-4 bg-white m-3 text-center rounded shadow-sm">
            <h5>Payment Method</h5>
            <div class="alert alert-success mt-3">Pay <b>₹{{ session.buy_price }}</b> via UPI</div>
            <a href="upi://pay?pa={{ upi_id }}&pn={{ upi_name }}&am={{ session.buy_price }}&cu=INR" class="btn btn-success w-100 py-3 fw-bold" onclick="ok()">PAY NOW</a>
            <form id="f" action="/success" method="POST"></form>
        </div>
        <script>function ok(){setTimeout(()=>document.getElementById('f').submit(),5000);}</script>

    {% elif page == 'success' %}
        <div class="text-center mt-5 p-5"><i class="fas fa-check-circle text-success" style="font-size:80px;"></i><h2 class="mt-4">Order Placed!</h2><a href="/my_orders" class="btn btn-primary mt-4 w-100">Track Order</a></div>

    {% elif page == 'my_orders' %}
        <div class="p-3"><h5>My Orders</h5>
            {% for o in orders %}
            <div class="card mb-3 p-3 shadow-sm border-0">
                <div class="d-flex gap-3 mb-2"><img src="{{ o.image }}" style="width:60px; height:60px; object-fit:contain; border:1px solid #eee;">
                    <div class="flex-grow-1"><div class="fw-bold small">{{ o.item }}</div><div class="small text-muted">₹{{ o.amount }}</div></div>
                </div>
                <div class="bg-light p-2 rounded small"><div class="fw-bold text-success mb-2">Arriving by {{ o.date }}</div>
                    <div class="track-box"><div class="track-dot"></div><div>{{ o.status }}</div><div class="text-muted" style="font-size:10px;">{{ o.location }}</div></div>
                </div>
            </div>
            {% else %}<div class="text-center mt-5">No Orders Yet</div>{% endfor %}
        </div>
    {% endif %}

    <div class="fixed-bottom bg-white d-flex border-top py-2" style="z-index: 1000;">
        <a href="/" class="flex-grow-1 text-center small text-dark"><i class="fas fa-home d-block"></i>Home</a>
        <a href="/my_orders" class="flex-grow-1 text-center small text-dark"><i class="fas fa-box d-block"></i>Orders</a>
        <a href="/cart" class="flex-grow-1 text-center small text-dark"><i class="fas fa-shopping-cart d-block"></i>Cart</a>
        <a href="/" class="flex-grow-1 text-center small text-dark"><i class="fas fa-user d-block"></i>User</a>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

# ==========================================
# 5. ROUTES
# ==========================================
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
    session['buy_price'] = p['price']
    session['buy_item'] = p['name']
    session['buy_img'] = p['images'][0]
    return render_template_string(HTML_TEMPLATE, page='address')

@app.route('/payment')
def payment(): return render_template_string(HTML_TEMPLATE, page='payment', upi_id=MY_UPI_ID, upi_name=MY_NAME)

@app.route('/success', methods=['POST'])
def success():
    orders = session.get('orders', [])
    del_date = (datetime.datetime.now() + datetime.timedelta(days=7)).strftime("%d %b")
    orders.insert(0, {'item': session.get('buy_item'), 'amount': session.get('buy_price'), 'date': del_date, 'image': session.get('buy_img'), 'status': 'Shipped', 'location': 'Mumbai Hub'})
    session['orders'] = orders
    return render_template_string(HTML_TEMPLATE, page='success')

@app.route('/my_orders')
def my_orders(): return render_template_string(HTML_TEMPLATE, page='my_orders', orders=session.get('orders', []))

@app.route('/cart')
def cart(): return redirect('/?cat=all') # Simplified for this version

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

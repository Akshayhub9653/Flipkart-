from flask import Flask, render_template_string, request, session, redirect, url_for
import random
import datetime
import os

app = Flask(__name__)
app.secret_key = 'flipkart_master_final_v200'

# ==========================================
# 1. SETTINGS & AUTO-UPDATE LOGIC
# ==========================================
MY_UPI_ID = "9653314458@naviaxis"
MY_NAME = "Apni Dukaan"
START_DATE = datetime.date(2025, 1, 1) 

products = []
next_id = 1

# ==========================================
# 2. HELPER TO ADD PRODUCTS (With Specs & Images)
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
    # --- FIXED ITEMS: LOOT & SPORTS (Pura Purana Data) ---
    bat_img = "https://rukminim2.flixcart.com/image/416/416/xif0q/bat/q/t/y/1-plastic-cricket-bat-for-kids-plastic-cricket-bat-full-size-original-imagpyz5a5z5z5ze.jpeg"
    add_item("Plastic Cricket Bat (Kids Special)", 99, 999, "Loot", [bat_img, bat_img], {"Material":"PVC", "Size":"Full"}, "Durable gully cricket bat.")
    
    badminton_img = "https://rukminim2.flixcart.com/image/416/416/l51d30w0/racquet/z/j/w/g-force-3600-super-lite-strung-1-g-force-3600-super-lite-original-imagft56z7sz5hze.jpeg"
    add_item("Badminton Racket Set", 70, 899, "Loot", [badminton_img, badminton_img], {"Weight":"78g", "Strings":"Strung"}, "Super lite performance.")

    add_item("Matte Red Lipstick (Loot)", 29, 399, "Loot", ["https://m.media-amazon.com/images/I/51+Y+Z+0+1L._SX679_.jpg"], {"Shade":"Ruby Red", "Type":"Matte"}, "12 hour long stay.")
    add_item("Premium Lace Bra (Black)", 49, 799, "Loot", ["https://m.media-amazon.com/images/I/71k+p+q+r+sL._UY879_.jpg"], {"Material":"Cotton Lace", "Type":"Padded"}, "Comfort and style.")

    # --- MOBILES (Samsung, Vivo, iPhone, Poco) ---
    add_item("Samsung Galaxy S24 Ultra", 129999, 159999, "Mobile", ["https://m.media-amazon.com/images/I/81vxWpPpgNL._SX679_.jpg"], {"RAM":"12GB", "ROM":"256GB", "Processor":"Snapdragon 8 Gen 3"}, "Best AI Smartphone.")
    add_item("Vivo T2x 5G (Loot Phone)", 999, 15999, "Loot", ["https://m.media-amazon.com/images/I/71W89+8+kHL._SX679_.jpg"], {"RAM":"6GB", "ROM":"128GB"}, "Limited offer loot phone.")
    add_item("iPhone 15 Pro Max", 148900, 159900, "Mobile", ["https://m.media-amazon.com/images/I/81vxWpPpgNL._SX679_.jpg"], {"RAM":"8GB", "Chip":"A17 Pro"}, "Premium titanium build.")

    # --- SHOES (Nike, Adidas, Campus) ---
    add_item("Nike Revolution Running Shoes", 2499, 4999, "Shoes", ["https://m.media-amazon.com/images/I/61utX8kBDlL._UY695_.jpg"], {"Brand":"Nike", "Type":"Sports"}, "Original Nike quality.")
    add_item("Asian Casual Sneakers", 199, 1999, "Loot", ["https://m.media-amazon.com/images/I/61+w+e+r+tL._UY695_.jpg"], {"Brand":"Asian", "Style":"Sneaker"}, "Special loot for shoes.")

    # --- DAILY AUTO-ADD (Daily 5 Items) ---
    days_passed = (datetime.date.today() - START_DATE).days
    total_extra = min(days_passed * 5, 50)
    extra_pool = [
        ("Realme 12 Pro", 25999, "Mobile", "https://m.media-amazon.com/images/I/81ogvU1sn6L._SX679_.jpg"),
        ("Adidas Walking Shoes", 2199, "Shoes", "https://m.media-amazon.com/images/I/71V2pYmB8LL._UY695_.jpg"),
        ("Bluetooth DJ Speaker", 499, "Electronics", "https://m.media-amazon.com/images/I/71+y+z+0+1L._SX679_.jpg"),
        ("Smart Watch Series 9", 899, "Electronics", "https://m.media-amazon.com/images/I/61+m+n+o+pL._SX679_.jpg")
    ]
    for i in range(total_extra):
        item = extra_pool[i % len(extra_pool)]
        add_item(item[0], item[1], item[1]*3, item[2], [item[3]], {"Type":"New Stock"}, "Daily fresh arrival.", is_new=True)

setup_store()

# ==========================================
# 3. HTML TEMPLATE (All Features Together)
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
        .card { background: white; border-radius: 4px; overflow: hidden; position: relative; border: 1px solid #ddd; }
        .card img { width: 100%; height: 160px; object-fit: contain; padding: 10px; }
        .loot-banner { background: linear-gradient(90deg, #ff0000, #ff9f00); color: white; padding: 15px; text-align: center; font-weight: bold; margin: 10px; border-radius: 4px; }
        .tag-new { position: absolute; top: 0; right: 0; background: red; color: white; font-size: 10px; padding: 2px 5px; font-weight: bold; }
        .tag-loot { position: absolute; top: 0; left: 0; background: #26a541; color: white; font-size: 10px; padding: 2px 5px; }
        .sticky-footer { position: fixed; bottom: 0; width: 100%; display: flex; z-index: 2000; background: white; }
        .btn-buy { background: var(--fk-yellow); color: white; padding: 15px; font-weight: bold; flex: 1; border: none; text-align: center; }
        .spec-row { display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #eee; font-size: 0.9rem; }
    </style>
</head>
<body>

    <nav class="navbar d-flex flex-column align-items-start">
        <div class="d-flex w-100 justify-content-between align-items-center mb-2">
            <div class="text-white fw-bold italic fs-5">Flipkart<span style="color:var(--fk-yellow)">Plus</span></div>
            <a href="/cart" class="text-white"><i class="fas fa-shopping-cart fa-lg"></i></a>
        </div>
        <form action="/" class="w-100"><input name="q" class="form-control" placeholder="Search brands, products..." value="{{ request.args.get('q', '') }}"></form>
    </nav>

    {% if page == 'home' %}
        <a href="/?cat=Loot"><div class="loot-banner">🚀 CLICK HERE: ₹5, ₹99, ₹999 LOOT DEALS LIVE! 🚀</div></a>
        <div class="d-flex gap-2 overflow-auto p-2 bg-white mb-2 shadow-sm">
            <a href="/?cat=all" class="btn btn-sm btn-outline-primary rounded-pill">All</a>
            <a href="/?cat=Loot" class="btn btn-sm btn-outline-danger rounded-pill">Loot Store</a>
            <a href="/?cat=Mobile" class="btn btn-sm btn-outline-primary rounded-pill">Mobiles</a>
            <a href="/?cat=Shoes" class="btn btn-sm btn-outline-primary rounded-pill">Shoes</a>
        </div>
        <div class="grid">
            {% for p in items %}
            <a href="/product/{{ p.id }}" class="card text-dark text-decoration-none">
                {% if p.is_new %}<span class="tag-new">NEW</span>{% endif %}
                {% if p.discount > 80 %}<span class="tag-loot">{{ p.discount }}% OFF</span>{% endif %}
                <img src="{{ p.images[0] }}" loading="lazy" onerror="this.src='https://via.placeholder.com/300?text=Flipkart'">
                <div class="p-2">
                    <div class="small text-truncate">{{ p.name }}</div>
                    <div class="fw-bold">₹{{ p.price }} <span class="text-muted text-decoration-line-through small">₹{{ p.mrp }}</span></div>
                </div>
            </a>
            {% endfor %}
        </div>

    {% elif page == 'detail' %}
        <div id="gallery" class="carousel slide bg-white">
            <div class="carousel-inner">
                {% for img in p.images %}<div class="carousel-item {% if loop.first %}active{% endif %}"><img src="{{ img }}" class="d-block w-100" style="height:350px; object-fit:contain;"></div>{% endfor %}
            </div>
            <button class="carousel-control-prev" data-bs-target="#gallery" data-bs-slide="prev"><span class="carousel-control-prev-icon bg-dark rounded"></span></button>
            <button class="carousel-control-next" data-bs-target="#gallery" data-bs-slide="next"><span class="carousel-control-next-icon bg-dark rounded"></span></button>
        </div>
        <div class="p-3 bg-white mt-2">
            <h5>{{ p.name }}</h5>
            <div class="badge bg-success mb-2">{{ p.rating }} ★ <small>{{ p.reviews }} ratings</small></div>
            <h1 class="fw-bold">₹{{ p.price }} <span class="text-muted fs-5 text-decoration-line-through">₹{{ p.mrp }}</span></h1>
            <div class="mt-4"><h6 class="fw-bold border-bottom pb-2">Technical Details</h6>
                {% for label, val in p.specs.items() %}<div class="spec-row"><span class="text-muted">{{ label }}</span><span>{{ val }}</span></div>{% endfor %}
            </div>
            <div class="bg-light p-3 mt-4 rounded small"><b>7 Days Replacement Policy</b><br>Quality assured product.</div>
        </div>
        <div class="sticky-footer">
            <button style="background:white; border:none; flex:1; font-weight:bold;">ADD CART</button>
            <a href="/buy_now/{{ p.id }}" class="btn-buy">BUY NOW</a>
        </div>

    {% elif page == 'address' %}
        <div class="p-4 bg-white m-3 rounded shadow-sm">
            <h5>Delivery Address</h5>
            <form action="/payment" method="GET">
                <input name="name" class="form-control mb-3" placeholder="Full Name" required>
                <input name="pincode" class="form-control mb-3" placeholder="Pincode" required>
                <textarea name="addr" class="form-control mb-3" placeholder="Full Address" required></textarea>
                <button class="btn btn-warning w-100 fw-bold py-3">CONTINUE</button>
            </form>
        </div>

    {% elif page == 'payment' %}
        <div class="p-4 bg-white m-3 text-center rounded shadow-sm">
            <h5>Payable: ₹{{ session.buy_price }}</h5>
            <div class="alert alert-success mt-3">Secured UPI Payment</div>
            <a href="upi://pay?pa={{ upi_id }}&pn={{ upi_name }}&am={{ session.buy_price }}&cu=INR" class="btn btn-success w-100 py-3 fw-bold" onclick="ok()">PAY NOW</a>
            <form id="f" action="/success" method="POST"></form>
        </div>
        <script>function ok(){setTimeout(()=>document.getElementById('f').submit(),5000);}</script>

    {% elif page == 'success' %}
        <div class="text-center mt-5 p-5"><i class="fas fa-check-circle text-success" style="font-size:80px;"></i><h2 class="mt-4">Order Placed!</h2><a href="/my_orders" class="btn btn-primary mt-4">Track Order</a></div>

    {% elif page == 'my_orders' %}
        <div class="p-3"><h5>My Orders</h5>
            {% for o in orders %}<div class="card mb-3 p-3 shadow-sm border-0"><div class="d-flex gap-3"><img src="{{ o.image }}" style="width:60px;"><div><div class="fw-bold small">{{ o.item }}</div><div class="text-muted">₹{{ o.amount }}</div></div></div><div class="bg-light p-2 mt-2 rounded small text-success fw-bold">Arriving in 7 Days • {{ o.status }}</div></div>{% else %}<div class="text-center mt-5">No orders found.</div>{% endfor %}
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
# 4. ROUTES
# ==========================================
@app.route('/')
def home():
    q = request.args.get('q', '').lower()
    cat = request.args.get('cat', 'all')
    items = products
    if q: items = [i for i in products if q in i['name'].lower() or q in i['category'].lower()]
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
    return render_template_string(HTML_TEMPLATE, page='address')

@app.route('/payment')
def payment(): return render_template_string(HTML_TEMPLATE, page='payment', upi_id=MY_UPI_ID, upi_name=MY_NAME)

@app.route('/success', methods=['POST'])
def success():
    orders = session.get('orders', [])
    orders.insert(0, {'item': session.get('buy_item'), 'amount': session.get('buy_price'), 'image': session.get('buy_img'), 'status': 'Shipped'})
    session['orders'] = orders
    return render_template_string(HTML_TEMPLATE, page='success')

@app.route('/my_orders')
def my_orders(): return render_template_string(HTML_TEMPLATE, page='my_orders', orders=session.get('orders', []))

@app.route('/cart')
def cart(): return redirect('/?cat=all')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

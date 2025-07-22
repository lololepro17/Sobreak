from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from models import db, Drink, UserDrink

app = Flask(__name__)
app.config['SECRET_KEY'] = 'change_this_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

# Initialisation de la base de données
# (db vient de models.py)
db.init_app(app)

login_manager = LoginManager(app)

from models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        date_of_birth = request.form.get('date_of_birth')
        weight = request.form.get('weight')
        gender = request.form.get('gender')

        # Conversion de la date de naissance
        date_obj = None
        if date_of_birth:
            try:
                date_obj = datetime.strptime(date_of_birth, "%Y-%m-%d").date()
            except ValueError:
                flash("Date de naissance invalide.", "error")
                return render_template('register.html')

        # Vérifier si l'utilisateur existe déjà
        if User.query.filter((User.username == username) | (User.email == email)).first():
            flash('Nom d\'utilisateur ou email déjà utilisé.', 'error')
            return render_template('register.html')

        hashed_password = generate_password_hash(password)
        user = User(
            username=username,
            email=email,
            password_hash=hashed_password,
            date_of_birth=date_obj,
            weight=float(weight) if weight else None,
            gender=gender
        )
        db.session.add(user)
        db.session.commit()
        flash('Inscription réussie ! Vous pouvez maintenant vous connecter.', 'success')
        return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username_or_email = request.form['username']
        password = request.form['password']
        user = User.query.filter((User.username == username_or_email) | (User.email == username_or_email)).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash('Connexion réussie !', 'success')
            return redirect(url_for('index'))
        else:
            flash('Identifiants invalides.', 'error')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Déconnexion réussie.', 'success')
    return redirect(url_for('index'))

def calculer_bac(user, consommations):
    # Formule de Widmark simplifiée
    if not user.weight or not user.gender:
        return None
    r = 0.7 if user.gender == 'homme' else 0.6
    poids = user.weight
    total_alcool_g = 0
    for c in consommations:
        if c.drink_id:
            drink = Drink.query.get(c.drink_id)
            if drink:
                deg = drink.alcohol_percentage
                vol = drink.volume_ml
            else:
                deg = 0
                vol = 0
        else:
            try:
                deg = float(c.custom_alcohol_percentage) if hasattr(c, 'custom_alcohol_percentage') and c.custom_alcohol_percentage else 0
                vol = float(c.custom_volume_ml) if hasattr(c, 'custom_volume_ml') and c.custom_volume_ml else 0
            except:
                deg = 0
                vol = 0
        quantite = c.quantity or 1
        alcool_pur_ml = vol * (deg / 100.0) * quantite
        alcool_g = alcool_pur_ml * 0.8
        total_alcool_g += alcool_g
    # Temps écoulé depuis la première consommation (en heures)
    if consommations:
        t0 = min([c.consumed_at for c in consommations])
        heures = (datetime.now() - t0).total_seconds() / 3600
    else:
        heures = 0
    # Élimination : 0.15 g/L/h
    bac = (total_alcool_g / (poids * r)) - (0.15 * heures)
    return max(0, round(bac, 3))

@app.route('/dashboard')
@login_required
def dashboard():
    consommations = UserDrink.query.filter_by(user_id=current_user.id).order_by(UserDrink.consumed_at.desc()).all()
    bac = calculer_bac(current_user, consommations)
    return render_template('dashboard.html', user=current_user, consommations=consommations, bac=bac)

@app.route('/add_drink', methods=['GET', 'POST'])
@login_required
def add_drink():
    drinks = Drink.query.all()
    if request.method == 'POST':
        drink_id = request.form.get('drink_id')
        custom_drink_name = request.form.get('custom_drink_name')
        quantity = request.form.get('quantity')
        consumed_at = request.form.get('consumed_at')
        notes = request.form.get('notes')
        # Conversion date/heure
        consumed_dt = None
        if consumed_at:
            try:
                consumed_dt = datetime.strptime(consumed_at, "%Y-%m-%dT%H:%M")
            except ValueError:
                flash("Date/heure invalide.", "error")
                return render_template('add_drink.html', drinks=drinks, now=datetime.now().strftime('%Y-%m-%dT%H:%M'))
        user_drink = UserDrink(
            user_id=current_user.id,
            drink_id=int(drink_id) if drink_id else None,
            custom_drink_name=custom_drink_name if custom_drink_name else None,
            quantity=int(quantity),
            consumed_at=consumed_dt if consumed_dt else datetime.now(),
            notes=notes
        )
        db.session.add(user_drink)
        db.session.commit()
        flash('Consommation ajoutée !', 'success')
        return redirect(url_for('dashboard'))
    now = datetime.now().strftime('%Y-%m-%dT%H:%M')
    return render_template('add_drink.html', drinks=drinks, now=now)

@app.route('/delete_drink/<int:drink_id>', methods=['POST'])
@login_required
def delete_drink(drink_id):
    drink = UserDrink.query.get_or_404(drink_id)
    if drink.user_id != current_user.id:
        flash("Action non autorisée.", "error")
        return redirect(url_for('dashboard'))
    db.session.delete(drink)
    db.session.commit()
    flash("Consommation supprimée.", "success")
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True) 
from flask import Blueprint,render_template,request,redirect,url_for,flash
from app.models import db, Parkinglot, Parkingspot,User,Reservation

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/dashboard')
def dashboard():
    return render_template('admin_dashboard.html')

@admin_bp.route('/create_lot', methods=['GET', 'POST'])
def create_lot():
    if request.method == 'POST':
        location_name = request.form['location_name']
        address = request.form['address']
        pin_code = request.form['pin_code']
        price_per_hour = float(request.form['price_per_hour'])
        max_spots = int(request.form['max_spots'])

        #creating the lot
        lot = Parkinglot(location_name=location_name, address=address, pin_code=pin_code, price_per_hour=price_per_hour, max_spots=max_spots)
        db.session.add(lot)
        db.session.flush()

         #generating the parking spots 
        for _ in range(max_spots):
            spot = Parkingspot(lot_id=lot.id, status='A')  
            db.session.add(spot)
        db.session.commit()

        flash('Parking lot and its parking spot are created')
        return redirect(url_for('admin.view_lots'))

    return render_template('create_lot.html')

@admin_bp.route('/view_lots')
def view_lots():
    lots = Parkinglot.query.all()  
    return render_template('view_lots.html', lots=lots)

@admin_bp.route('/edit_lot/<int:lot_id>', methods=['GET', 'POST'])
def edit_lot(lot_id):
    lot = Parkinglot.query.get_or_404(lot_id)

    if request.method == 'POST':
        lot.location_name = request.form['location_name']
        lot.address = request.form['address']
        lot.pin_code = request.form['pin_code']
        lot.price_per_hour = float(request.form['price_per_hour'])

        if lot.max_spots != int(request.form['max_spots']):

        # To change no of max spota if greater than before than add and if less than befor then delete
            new_max_spots = int(request.form['max_spots'])
            difference = new_max_spots - lot.max_spots

            if difference > 0:
                for _ in range(difference):
                    new_spot = Parkingspot(lot_id=lot.id, status='A')
                    db.session.add(new_spot)

            elif difference < 0:
                available_spots = Parkingspot.query.filter_by(lot_id=lot.id, status='A').limit(abs(difference)).all()
                if len(available_spots) < abs(difference):
                    flash('The spots cannot be reduced as the available spots are not enough.')
                    return redirect(url_for('admin.view_lots'))

                for spot in available_spots:
                    db.session.delete(spot)

            lot.max_spots = new_max_spots
        db.session.commit() 
        flash('The Lot has been updated')
        return redirect(url_for('admin.view_lots'))

    return render_template('edit_lot.html', lot=lot)

@admin_bp.route('/delete_lot/<int:lot_id>', methods=['POST'])
def delete_lot(lot_id):
    lot = Parkinglot.query.get_or_404(lot_id)
#If any spot is occupied then the lot cannot be deleted
    for spot in lot.spots:
        if spot.status == 'O':
            flash("Some spots are still occupied in this lot so it cannot be deleted.")
            return redirect(url_for('admin.view_lots'))
        
        for spot in lot.spots:
            db.session.delete(spot)

    db.session.delete(lot)
    db.session.commit()
    flash("The Parking lot is deleted successfully.")
    return redirect(url_for('admin.view_lots'))

@admin_bp.route('/view_spots/<int:lot_id>')
def view_spots(lot_id):
    lot = Parkinglot.query.get_or_404(lot_id)
    spots = lot.spots  # relationship
    return render_template('view_spots.html', lot=lot, spots=spots)

@admin_bp.route('/view_users')
def view_users():
    users = User.query.filter_by(is_admin=False).all()

    return render_template('view_users.html', users=users)

@admin_bp.route('/admin/view_reservations')
def view_all_reservations():
    reservations = Reservation.query.order_by(Reservation.start_time.desc()).all()
    return render_template('admi_view_reservation.html', reservations=reservations)

@admin_bp.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    filter_by = request.args.get('filter')

    results = []
    if filter_by == 'user':
        results = User.query.filter(User.username.ilike(f"%{query}%")).all()
    elif filter_by == 'spot':
        results = Parkingspot.query.filter(Parkingspot.id.like(f"%{query}%")).all()
    elif filter_by == 'lot':
        results = Parkinglot.query.filter(Parkinglot.location_name.ilike(f"%{query}%")).all()

    return render_template('admin_search.html', results=results, filter_by=filter_by, query=query)

from flask import Blueprint, render_template, session, flash, redirect, url_for
from app.models import Parkinglot, Parkingspot, Reservation, User, db
from datetime import datetime

user_bp = Blueprint('user', __name__)

@user_bp.route('/user/view_lots')
def view_lots():
    lots = Parkinglot.query.all()
    lot_data = []
    for lot in lots:
        total_spots = lot.max_spots
        available_spots = sum(1 for spot in lot.spots if spot.status == 'A')
        lot_data.append({
            'id': lot.id,
            'location_name': lot.location_name,
            'address': lot.address,
            'price_per_hour': lot.price_per_hour,
            'available_spots': available_spots,
            'total_spots': total_spots
        })
    return render_template('user_view_lots.html', lots=lot_data)

@user_bp.route('/user/reserve_spot/<int:lot_id>', methods=['POST'])
def reserve_spot(lot_id):
    user_id = session.get('user_id')
    if not user_id:
        flash("Please log in to reserve a parking spot.",'warning')
        return redirect(url_for('authentication.login'))

    user = User.query.get(user_id)
    if not user:
        flash("Your session expired or account could not be found. Please log in again or create a new account.",'warning')
        return redirect(url_for('authentication.login'))

    active_res = Reservation.query.filter_by(user_id=user.id, status='active').first()
    if active_res:
        flash("You already have an active reservation.",'info')
        return redirect(url_for('user.view_lots'))

    available_spot = Parkingspot.query.filter_by(lot_id=lot_id, status='A').first()
    if not available_spot:
        flash("Sorry, no available spots in this lot right now.",'danger')
        return redirect(url_for('user.view_lots'))

    available_spot.status = 'O'
    db.session.add(available_spot)

    reservation = Reservation(
        user_id=user.id,
        spot_id=available_spot.id,
        status='active'
    )
    db.session.add(reservation)
    db.session.commit()

    flash(f"Spot {available_spot.id} reserved successfully at lot '{available_spot.lot.location_name}'!",'success')
    return redirect(url_for('user.parking_history'))

@user_bp.route('/user/occupy_spot/<int:reservation_id>', methods=['POST'])
def occupy_spot(reservation_id):
    user_id = session.get('user_id')
    if not user_id:
        flash("Please log in.",'warning')
        return redirect(url_for('authentication.login'))

    reservation = Reservation.query.filter_by(id=reservation_id, user_id=user_id).first()
    if not reservation:
        flash("Reservation not found.",'danger')
        return redirect(url_for('user.parking_history'))

    if reservation.status != 'active':
        flash("Cannot occupy a reservation that is not active.",'danger')
        return redirect(url_for('user.parking_history'))
    
    if reservation.start_time:
        flash("This spot is already occupied.",'warning')
        return redirect(url_for('user.parking_history'))

    # Update start_time to now if you want
    reservation.start_time = datetime.utcnow()
    db.session.commit()

    flash("Spot occupied. Happy parking!",'success')
    return redirect(url_for('user.parking_history'))

@user_bp.route('/user/parking_history')
def parking_history():
    user_id = session.get('user_id')
    if not user_id:
        flash("Please log in to view your parking history.",'warning')
        return redirect(url_for('authentication.login'))

    reservations = Reservation.query.filter_by(user_id=user_id).order_by(Reservation.start_time.desc()).all()

    history = []
    for res in reservations:
        if res.start_time and res.end_time:
            duration = round((res.end_time - res.start_time).total_seconds() / 3600, 2)
        else:
            duration = None 

        cost = res.cost if res.cost is not None else 0

        history.append({
            'reservation': res,
            'duration': duration,
            'cost': res.cost
        })

    return render_template('parking_history.html', history=history)

@user_bp.route('/user/release_spot/<int:reservation_id>', methods=['POST'])
def release_spot(reservation_id):
    user_id = session.get('user_id')
    if not user_id:
        flash("Please log in.",'warning')
        return redirect(url_for('authentication.login'))

    reservation = Reservation.query.filter_by(id=reservation_id, user_id=user_id).first()
    if not reservation:
        flash("Reservation not found.",'danger')
        return redirect(url_for('user.parking_history'))

    if reservation.status != 'active':
        flash("This reservation is already completed.",'info')
        return redirect(url_for('user.parking_history'))

    # Set end time to now
    reservation.end_time = datetime.utcnow()

    if reservation.start_time:
        duration_hours = round((reservation.end_time - reservation.start_time).total_seconds() / 3600, 2)
        price_per_hour = reservation.spot.lot.price_per_hour
        cost = round(duration_hours * price_per_hour, 2)
        
    else:
        duration_hours = 0
        cost = 0
        flash("Warning: Spot was never occupied, so cost is ₹0.", "info")
    reservation.cost = cost
    reservation.status = 'completed'

    # Free up the parking spot
    reservation.spot.status = 'A'

    db.session.commit() 

    flash(f"Spot released successfully. Duration: {duration_hours:.2f} hrs | Cost: ₹{cost}",'success')
    return redirect(url_for('user.parking_history'))
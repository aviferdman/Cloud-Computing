from flask import Flask, request, jsonify
from datetime import datetime
import uuid

app = Flask(__name__)
entries = {}

@app.route('/entry', methods=['POST'])
def vehicle_entry():
    plate = request.args.get('plate')
    parking_lot = request.args.get('parkingLot')

    if not plate or not parking_lot:
        return jsonify({'error': 'Missing plate or parkingLot parameter'}), 400

    ticket_id = str(uuid.uuid4())
    entries[ticket_id] = {
        'plate': plate,
        'parking_lot': parking_lot,
        'entry_time': datetime.utcnow()
    }
    return jsonify({'ticketId': ticket_id})

@app.route('/exit', methods=['POST'])
def vehicle_exit():
    ticket_id = request.args.get('ticketId')

    if not ticket_id or ticket_id not in entries:
        return jsonify({'error': 'Invalid or missing ticketId'}), 400

    entry_data = entries.pop(ticket_id)
    exit_time = datetime.utcnow()
    parked_time = exit_time - entry_data['entry_time']
    total_minutes = parked_time.total_seconds() / 60
    charge = round((total_minutes / 60) * 10, 2)

    return jsonify({
        'plate': entry_data['plate'],
        'parkingLot': entry_data['parking_lot'],
        'parkedTimeMinutes': int(total_minutes),
        'charge': charge
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

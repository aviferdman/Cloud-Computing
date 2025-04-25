from flask import Flask, request, jsonify
from datetime import datetime
import uuid
import boto3
from botocore.exceptions import ClientError

app = Flask(__name__)
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('parking-entries')

@app.route('/entry', methods=['POST'])
def vehicle_entry():
    plate = request.args.get('plate')
    parking_lot = request.args.get('parkingLot')

    if not plate or not parking_lot:
        return jsonify({'error': 'Missing plate or parkingLot parameter'}), 400

    ticket_id = str(uuid.uuid4())
    entry_time = datetime.utcnow().isoformat()
    
    try:
        table.put_item(
            Item={
                'ticket_id': ticket_id,
                'plate': plate,
                'parking_lot': parking_lot,
                'entry_time': entry_time
            }
        )
        return jsonify({'ticketId': ticket_id})
    except ClientError as e:
        return jsonify({'error': str(e)}), 500

@app.route('/exit', methods=['POST'])
def vehicle_exit():
    ticket_id = request.args.get('ticketId')

    if not ticket_id:
        return jsonify({'error': 'Missing ticketId'}), 400

    try:
        response = table.get_item(Key={'ticket_id': ticket_id})
    except ClientError as e:
        return jsonify({'error': str(e)}), 500

    if 'Item' not in response:
        return jsonify({'error': 'Invalid ticketId'}), 400

    entry_data = response['Item']
    exit_time = datetime.utcnow()
    entry_time = datetime.fromisoformat(entry_data['entry_time'])
    parked_time = exit_time - entry_time

    try:
        table.delete_item(Key={'ticket_id': ticket_id})
    except ClientError as e:
        return jsonify({'error': str(e)}), 500
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

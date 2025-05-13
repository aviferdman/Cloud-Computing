from flask import Flask, request, Response
import time
from datetime import datetime, timedelta
import uuid
import boto3
from typing import Tuple, Dict, Any
from botocore.exceptions import ClientError
import json

app = Flask(__name__)
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('parking-entries')


class TicketResponse:
    def __init__(self, ticket_id: str):
        self.ticketId = ticket_id

    def to_dict(self) -> Dict[str, Any]:
        return {"ticketId": self.ticketId}


class ErrorResponse:
    def __init__(self, message: str):
        self.error = message

    def to_dict(self) -> Dict[str, Any]:
        return {"error": self.error}


class RequestHandler:
    def __init__(self, request: request):
        self.request = request

    def get_query_param(self, param_name: str) -> str:
        return self.request.args.get(param_name)

    def validate_params(self, required_params: list) -> Tuple[bool, str]:
        for param in required_params:
            if not self.get_query_param(param):
                return False, f"Missing {param} parameter"
        return True, ""


class ResponseHandler:
    @staticmethod
    def success(data: Any, status_code: int = 200) -> Response:
        if hasattr(data, "to_dict"):
            data = data.to_dict()
        return Response(json.dumps(data), status=status_code, mimetype='application/json')

    @staticmethod
    def error(message: str, status_code: int = 400) -> Response:
        error_response = ErrorResponse(message)
        return Response(json.dumps(error_response.to_dict()), status=status_code, mimetype='application/json')


def parked_time_calc(entry_time: str) -> timedelta:
    exit_time: datetime = datetime.fromtimestamp(time.time())
    entry_time_dt: datetime = datetime.fromisoformat(entry_time)
    parked_time: timedelta = exit_time - entry_time_dt
    return parked_time


def calc_price(entry_time: str) -> Tuple[float, float]:
    parked_time: timedelta = parked_time_calc(entry_time)
    total_minutes: float = parked_time.total_seconds() / 60
    charge: float = round((total_minutes / 60) * 10, 2)
    return charge, total_minutes


@app.route('/entry', methods=['POST'])
def vehicle_entry():
    req_handler = RequestHandler(request)
    is_valid, error_message = req_handler.validate_params(['plate', 'parkingLot'])
    if not is_valid:
        return ResponseHandler.error(error_message)

    plate = req_handler.get_query_param('plate')
    parking_lot = req_handler.get_query_param('parkingLot')

    try:
        response = table.scan(
            FilterExpression='plate = :plate',
            ExpressionAttributeValues={':plate': plate}
        )
        if response.get('Items'):
            return ResponseHandler.error('Plate already exists')
    except ClientError as e:
        return ResponseHandler.error(e.response['Error']['Message'], 500)

    ticket_id = str(uuid.uuid4())
    entry_time = datetime.fromtimestamp(time.time()).isoformat()

    try:
        table.put_item(
            Item={
                'ticket_id': ticket_id,
                'plate': plate,
                'parking_lot': parking_lot,
                'entry_time': entry_time
            }
        )
        return ResponseHandler.success(TicketResponse(ticket_id))
    except ClientError as e:
        return ResponseHandler.error(e.response['Error']['Message'], 500)


@app.route('/exit', methods=['POST'])
def vehicle_exit():
    req_handler = RequestHandler(request)
    ticket_id = req_handler.get_query_param('ticketId')

    if not ticket_id:
        return ResponseHandler.error('Missing ticketId')

    try:
        response = table.get_item(Key={'ticket_id': ticket_id})
    except ClientError as e:
        return ResponseHandler.error(e.response['Error']['Message'], 500)

    if 'Item' not in response or not response['Item']:
        return ResponseHandler.error('Invalid ticketId')

    try:
        table.delete_item(Key={'ticket_id': ticket_id})
    except ClientError as e:
        return ResponseHandler.error(e.response['Error']['Message'], 500)

    entry_data = response['Item']
    fee, total_minutes = calc_price(entry_data['entry_time'])
    return ResponseHandler.success({
        'plate': entry_data['plate'],
        'parkingLot': entry_data['parking_lot'],
        'parkedTimeMinutes': int(total_minutes),
        'fee': fee
    })

#for debugging
# @app.route('/entries', methods=['GET'])
# def get_all_entries():
#     try:
#         response = table.scan()
#         items = response.get('Items', [])
#         return ResponseHandler.success(items)
#     except ClientError as e:
#         return ResponseHandler.error(e.response['Error']['Message'], 500)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

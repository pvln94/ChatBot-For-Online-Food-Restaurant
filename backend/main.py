from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import db_helper
import generic_helper

app = FastAPI()

inprogress_orders = {}


@app.post("/")
async def handle_request(request: Request):
    try:
        payload = await request.json()
        query_result = payload.get("queryResult", {})

        intent = query_result.get("intent", {}).get("displayName")
        parameters = query_result.get("parameters", {})
        output_contexts = query_result.get("outputContexts", [])

        if not intent or not output_contexts:
            return JSONResponse(content={"fulfillmentText": "Invalid request format."})

        session_id = generic_helper.extract_session_id(output_contexts[0].get("name", ""))

        intent_handler_dict = {
            'order.add - context: ongoing-order': add_to_order,
            'order.remove - context: ongoing-order': remove_from_order,
            'order.complete - context: ongoing-order': complete_order,
            'track.order - context: ongoing-tracking': track_order
        }

        if intent in intent_handler_dict:
            return intent_handler_dict[intent](parameters, session_id)
        else:
            return JSONResponse(content={"fulfillmentText": "Intent not recognized."})

    except Exception as e:
        return JSONResponse(content={"fulfillmentText": f"Error processing request: {str(e)}"})


def save_to_db(order: dict):
    next_order_id = db_helper.get_next_order_id()

    if next_order_id is None:
        return -1

    for food_item, quantity in order.items():
        rcode = db_helper.insert_order_item(food_item, quantity, next_order_id)
        if rcode == -1:
            return -1

    db_helper.insert_order_tracking(next_order_id, "in progress")
    return next_order_id


def complete_order(parameters: dict, session_id: str):
    if session_id not in inprogress_orders:
        return JSONResponse(
            content={"fulfillmentText": "I'm having trouble finding your order. Can you place a new order, please?"})

    order = inprogress_orders.pop(session_id)
    order_id = save_to_db(order)

    if order_id == -1:
        return JSONResponse(content={
            "fulfillmentText": "Sorry, we couldn't process your order due to a backend error. Please try again."})

    order_total = db_helper.get_total_order_price(order_id)
    fulfillment_text = f"Awesome! Your order has been placed. Order ID: {order_id}. Total: {order_total}. Please pay at the time of delivery."

    return JSONResponse(content={"fulfillmentText": fulfillment_text})


def add_to_order(parameters: dict, session_id: str):
    food_items = parameters.get("food-item", [])
    quantities = parameters.get("number", [])

    if len(food_items) != len(quantities):
        return JSONResponse(content={"fulfillmentText": "Please specify food items and quantities clearly."})

    new_food_dict = dict(zip(food_items, quantities))

    if session_id in inprogress_orders:
        inprogress_orders[session_id].update(new_food_dict)
    else:
        inprogress_orders[session_id] = new_food_dict

    order_str = generic_helper.get_str_from_food_dict(inprogress_orders[session_id])
    return JSONResponse(content={"fulfillmentText": f"So far, you have: {order_str}. Do you need anything else?"})


def remove_from_order(parameters: dict, session_id: str):
    if session_id not in inprogress_orders:
        return JSONResponse(
            content={"fulfillmentText": "I'm having trouble finding your order. Can you place a new order, please?"})

    food_items = parameters.get("food-item", [])
    current_order = inprogress_orders[session_id]

    removed_items = [item for item in food_items if item in current_order]
    no_such_items = [item for item in food_items if item not in current_order]

    for item in removed_items:
        del current_order[item]

    fulfillment_text = ""
    if removed_items:
        fulfillment_text += f"Removed {', '.join(removed_items)} from your order. "
    if no_such_items:
        fulfillment_text += f"Your order does not contain {', '.join(no_such_items)}. "
    if not current_order:
        fulfillment_text += "Your order is now empty!"
    else:
        order_str = generic_helper.get_str_from_food_dict(current_order)
        fulfillment_text += f" Remaining items: {order_str}."

    return JSONResponse(content={"fulfillmentText": fulfillment_text})


def track_order(parameters: dict, session_id: str):
    try:
        order_id = int(parameters.get("number", -1))


        if order_id == -1:
            return JSONResponse(content={"fulfillmentText": "Please provide a valid order ID."})

        order_status = db_helper.get_order_status(order_id)
        if order_status:
            fulfillment_text = f"The status of order {order_id} is: {order_status}."
        else:
            fulfillment_text = f"No order found with order ID: {order_id}."
    except ValueError:
        fulfillment_text = "Invalid order ID format."

    return JSONResponse(content={"fulfillmentText": fulfillment_text})
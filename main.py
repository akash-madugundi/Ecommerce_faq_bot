from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse
import generic_helper

app = FastAPI()

# In-memory storage for orders and sessions
inprogress_orders = {}

@app.post("/")
async def handle_request(request: Request):
    # Retrieve the JSON data from the request
    payload = await request.json()

    # Extract the necessary information from the payload
    intent = payload['queryResult']['intent']['displayName']
    parameters = payload['queryResult']['parameters']
    output_contexts = payload['queryResult']['outputContexts']
    session_id = generic_helper.extract_session_id(output_contexts[0]["name"])

    # Mapping intent to handler function
    intent_handler_dict = {
        'order.related': handle_order_related,
        'payment.related': handle_payment_related,
        'policy.related': handle_policy_related,
        'product.related': handle_product_related,
        'support.related': handle_support_related,
        'warranty.related': handle_warranty_related
    }

    # Handle the intent and return the response
    return intent_handler_dict.get(intent, handle_unknown_intent)(parameters, session_id)

# Handling 'order.related' intent
def handle_order_related(parameters: dict, session_id: str):
    if session_id not in inprogress_orders:
        fulfillment_text = "It seems you haven't placed an order yet. Would you like to place an order?"
    else:
        order = inprogress_orders[session_id]
        order_str = generic_helper.get_str_from_food_dict(order)
        fulfillment_text = f"Your current order is: {order_str}. Can I help you with anything else?"

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })

# Handling 'payment.related' intent
def handle_payment_related(parameters: dict, session_id: str):
    if session_id not in inprogress_orders:
        fulfillment_text = "It seems you haven't placed an order yet. Please place an order first to proceed with payment."
    else:
        order = inprogress_orders[session_id]
        order_total = sum(order.values())  # Calculate a dummy total (you can update this as per your logic)
        fulfillment_text = f"Your current order total is {order_total}. Would you like to proceed with payment?"

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })

# Handling 'policy.related' intent
def handle_policy_related(parameters: dict, session_id: str):
    # Return a predefined policy message
    fulfillment_text = "Our policy includes a 30-day return window, free shipping on orders over $50, and 24/7 customer support. Let me know if you need more details."
    
    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })

# Handling 'product.related' intent
def handle_product_related(parameters: dict, session_id: str):
    # Assuming parameters contain product-related queries
    product_query = parameters.get('product-query', 'No query provided')
    fulfillment_text = f"Here is some information regarding the product: {product_query}. Can I assist you with more product details?"
    
    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })

# Handling 'support.related' intent
def handle_support_related(parameters: dict, session_id: str):
    # Return a predefined support response
    fulfillment_text = "For support, you can contact us via our website or by calling 1-800-123-4567. Let me know if I can assist you with anything else."
    
    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })

# Handling 'warranty.related' intent
def handle_warranty_related(parameters: dict, session_id: str):
    # Return a predefined warranty response
    fulfillment_text = "Our products come with a 1-year warranty. If you need help with a warranty claim, please provide your order ID."
    
    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })

# Handling unknown intents
def handle_unknown_intent(parameters: dict, session_id: str):
    fulfillment_text = "I'm sorry, I didn't understand your request. Could you please clarify?"
    
    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })

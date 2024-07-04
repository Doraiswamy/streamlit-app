import streamlit as st
import asyncio
import websockets
import json
import base64


# Function to prepare and send the query
def prepare_and_send_query(user_query, query_vector_db, assistant_type, model_id):
    # json_string = json.dumps(user_query)
    # base64_encoded_string = base64.b64encode(json_string.encode('utf-8')).decode('utf-8')

    data = {
        "query": user_query,
        "query_vectordb": query_vector_db,
        "behaviour": assistant_type,
        "model_id": model_id,
        "action": "bedrock",
        "emailId": "nachiketh_d@nec.com.sg"
    }

    return json.dumps(data)


# Function to connect to WebSocket
async def connect_to_websocket(user_query, placeholder):
    url = "wss://lhat0mbzql.execute-api.us-east-1.amazonaws.com/dev/?x-api-key=bedrock-access-internal"

    try:
        async with websockets.connect(url) as websocket:
            query_vector_db = "yes"
            assistant_type = "english"
            model_id = "anthropic.claude-3-haiku-20240307-v1:0"

            data = prepare_and_send_query(user_query, query_vector_db, assistant_type, model_id)
            print(user_query)
            await websocket.send(data)

            complete_response = ""
            while True:
                response = await websocket.recv()
                decoded_response = base64.b64decode(response).decode('utf-8')
                response_json = json.loads(decoded_response)
                complete_response += response_json["text"]
                placeholder.text(complete_response)

    except websockets.exceptions.InvalidStatusCode as e:
        placeholder.text(f"Connection failed with status code: {e.status_code}")
    except Exception as e:
        placeholder.text(f"An error occurred: {e}")


# Main function to run in Streamlit
def main():
    st.title("NEC ARC Client with Streamlit")

    user_query = st.text_input("Enter your query:")

    if st.button("Send Query"):
        if user_query:
            placeholder = st.empty()
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(connect_to_websocket(user_query, placeholder))
        else:
            st.warning("Please enter a query.")


if __name__ == "__main__":
    main()

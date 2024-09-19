import streamlit as st
import aiohttp
import asyncio

st.title('LLM Response Generator')

# Text input from the user
user_input = st.text_input('Enter your text here:')

async def fetch_llm_response(payload):
    url = 'https://5n9abgtpde.execute-api.us-east-1.amazonaws.com/generateLLMresponse'
    headers = {'Content-Type': 'application/json'}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers=headers) as response:
            response.raise_for_status()
            return await response.json()

# When the user clicks the button
if st.button('Generate Response'):
    if user_input.strip():
        payload = {
          "inputMode": "Text",
          "sessionId": "5fed3c93-fa7b-413b-941c-88c209129444",
          "requestAttributes": {
            "x-amz-lex:accept-content-types": "PlainText",
            "x-amz-lex:channels:platform": "Connect Chat"
          },
          "inputTranscript": user_input,
          "jwt_token":"",
          "username":"menghai_teh",
          "interpretations": [
            {
              "interpretationSource": "Lex",
              "intent": {
                "confirmationState": "None",
                "name": "FallbackIntent",
                "slots": {},
                "state": "InProgress"
              }
            },
            {
              "interpretationSource": "Lex",
              "nluConfidence": 0.69,
              "intent": {
                "confirmationState": "None",
                "name": "CallBedrock",
                "slots": {},
                "state": "InProgress"
              }
            }
          ],
          "bot": {
            "aliasId": "TSTALIASID",
            "aliasName": "TestBotAlias",
            "name": "InvokeAIAgent",
            "version": "DRAFT",
            "localeId": "en_US",
            "id": "LOXEUYM2T9"
          },
          "responseContentType": "text/plain; charset=utf-8",
          "sessionState": {
            "originatingRequestId": "a2f8eecc-f1ba-4b2d-acf8-e5c45e1865ba",
            "sessionAttributes": {
              "jwt_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiIxNDk2MjA3Zi02MmU4LTQzMWYtODNlZC00OTFiOWQ0YmM4MTQiLCJpYXQiOjE3MjUzMzAwMDksImh0dHA6Ly9zY2hlbWFzLnhtbHNvYXAub3JnL3dzLzIwMDUvMDUvaWRlbnRpdHkvY2xhaW1zL25hbWUiOiIxIiwic3ViIjoiMSIsImFmZmVjdGVkX3NlcnZpY2UiOiJQb3J0YWwiLCJodHRwOi8vc2NoZW1hcy54bWxzb2FwLm9yZy93cy8yMDA1LzA1L2lkZW50aXR5L2NsYWltcy9lbWFpbGFkZHJlc3MiOiJraGFuaG5kK3BvcnRhbGFkbWluLm5lY0BoYmxhYi52biIsImV4cCI6MTcyNTM0ODAwOSwiaXNzIjoiVGVzdC5jb20iLCJhdWQiOiJUZXN0LmNvbSJ9.IuRjd4Rc5fX4k6b2YbPc26Wt4Uh60XWIy52mI5VuY8E",
              "username": "menghai_teh"
            },
            "intent": {
              "confirmationState": "None",
              "name": "FallbackIntent",
              "slots": {},
              "state": "InProgress"
            }
          },
          "messageVersion": "1.0",
          "invocationSource": "DialogCodeHook",
          "transcriptions": [
            {
              "resolvedContext": {
                "intent": "FallbackIntent"
              },
              "resolvedSlots": {},
              "transcriptionConfidence": 1.0,
              "transcription": user_input
            }
          ]
        }

        with st.spinner('Generating response...'):
            try:
                # Use asyncio to run the asynchronous function
                result = asyncio.run(fetch_llm_response(payload))

                content_message = result["messages"][0]["content"]

                # Display the content in Streamlit
                st.title("LLM Response")
                st.write(content_message)

            except aiohttp.ClientResponseError as http_err:
                st.error(f'HTTP error occurred: {http_err}')
            except Exception as err:
                st.error(f'An error occurred: {err}')
    else:
        st.warning('Please enter some text.')
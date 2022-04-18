import os
import dialogflow
from google.api_core.exceptions import InvalidArgument

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'f0974f38084c2710153b01bfce1abcbf1fb2f0d3'
DIALOGFLOW_PROJECT_ID = 'my-project-1470291891373'
DIALOGFLOW_LANGUAGE_CODE = 'en'
SESSION_ID = 'anything'

text_to_be_analyzed = "hi"

session_client = dialogflow.SessionsClient()
session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
text_input = dialogflow.types.TextInput(text=text_to_be_analyzed, language_code=DIALOGFLOW_LANGUAGE_CODE)
query_input = dialogflow.types.QueryInput(text=text_input)
try:
    response = session_client.detect_intent(session=session, query_input=query_input)
except InvalidArgument:
    raise

print("輸入文字:", response.query_result.query_text)
print("得到的 intent:", response.query_result.intent.display_name)
print("偵測到 intent 的 confidence:", response.query_result.intent_detection_confidence)
print("回應的話:", response.query_result.fulfillment_text)

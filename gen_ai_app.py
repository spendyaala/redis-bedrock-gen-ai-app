import streamlit as st

import boto3
import json



# Import any other libraries and the generative AI model here
session = boto3.Session()
credentials = session.get_credentials()
print(credentials.access_key)
bedrock = boto3.client(service_name='bedrock',region_name='us-west-2',endpoint_url='https://bedrock.us-west-2.amazonaws.com')
fms = bedrock.list_foundation_models()
print(" **** AWS Bedrock Foundation Models Available - START ****")
print(fms)
print(" **** AWS Bedrock Foundation Models Available - END   ****")

# Function to generate text using the generative AI model
def generate_text(prompt_data):
    # Here we are going to invoke Amazon Large Titan AI model for our generative ai needs.
    body = json.dumps({"inputText": prompt_data})
    modelId = 'amazon.titan-tg1-large' # change this to use a different version from the model provider
    accept = 'application/json'
    contentType = 'application/json'

    response = bedrock.invoke_model(body=body, modelId=modelId, accept=accept, contentType=contentType)
    response_body = json.loads(response.get('body').read())
    generated_text = response_body.get('results')[0].get('outputText')
    return generated_text

def main():
    st.title("Generative AI Text Generation App with Redis and AWS Bedrock")
    st.write("Enter a text prompt and see the generative AI model's response.")

    # Text input for the user to enter the prompt
    user_input = st.text_area("Enter your text prompt:", height=150)

    # Generate button
    if st.button("Generate"):
        if user_input:
            # Call the function to generate text based on the user's input
            generated_text = generate_text(user_input)
            st.write("Generated Text:")
            st.write(generated_text)
        else:
            st.warning("Please enter a text prompt.")

if __name__ == "__main__":
    main()

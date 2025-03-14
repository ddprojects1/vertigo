import boto3
import json
import random
import string

# Replace these with your actual Agent IDs
AGENT_ID = "7ZH4TX6M6T"
AGENT_ALIAS_ID = "UYY6Z9VGEF"

bedrock_agent_runtime = boto3.client("bedrock-agent-runtime")


def lambda_handler(event, context):
	print(event)

	# Parse the incoming event body

	body = event["body"]
	print(body)

	session_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
	input_text = body['message']
	client_code = body['clientCode']

	# Invoke the Bedrock agent
	response = bedrock_agent_runtime.invoke_agent(
    	enableTrace=True,
    	agentId=AGENT_ID,
    	agentAliasId=AGENT_ALIAS_ID,
    	sessionId=session_id,
    	inputText=input_text,
	)

	print(response)

	# Process the response chunks
	resp_text = ""
	for chunk in response["completion"]:
		print(chunk)
		if "chunk" in chunk:
			decoded_chunk = chunk["chunk"]["bytes"].decode()
			print(decoded_chunk)
			resp_text += decoded_chunk
			file_name = session_id + ".md"
			s3 = boto3.client('s3')
			s3.put_object(Body=resp_text, Bucket="vertigo-lambda-bucket", Key=file_name)

	# Prepare the response
	response = {
    	"statusCode": 200,
    	"headers": {
        	"Content-Type": "application/json",
        	"Access-Control-Allow-Origin": "*",
        	"Access-Control-Allow-Credentials": True,
    	},
    	"body": "File Uploaded Successfully",
	}

	return response
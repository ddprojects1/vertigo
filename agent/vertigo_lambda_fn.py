import boto3
import json
import random
import string
from datetime import datetime
import gzip
import base64
from fpdf import FPDF
import markdown
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from botocore.exceptions import ClientError
import requests 




# SuperVisor Details

AGENT_ID = "7ZH4TX6M6T"
AGENT_ALIAS_ID = "UYY6Z9VGEF"

# Writer Agent Details
# AGENT_ID = "EDPBQCYQTF"
# AGENT_ALIAS_ID = "6G8GGTVXDH"


bedrock_agent_runtime = boto3.client("bedrock-agent-runtime")
bucket_name = "vertigo-lambda-bucket" 
object_key_prefix = "Log_Alerts_"  
writer_instruction = "Write a Run book for the below error message in "
RECIPIENT_EMAIL = ["aswani.karteek@accionlabs.com","sre1.vertigo.demo@gmail.com"]
#RECIPIENT_EMAIL ="sre1.vertigo.demo@gmail.com"
time_stamped =''
def getMarkDownHeader(incidentNo):
	now = datetime.now()
	global time_stamped
	time_stamped = now.strftime("%Y-%m-%d %H:%M:%S")

	headerData = "| ** Incident Number **|" + incidentNo +"\n" +"| ** Date of Incident ** |"+ time_stamped +"\n"
	print(headerData)
	return headerData


def getErrorContextFromLog(event,context):
	global writer_instruction
	if event and 'awslogs' in event and 'data' in event['awslogs']:
		try:
			payload = base64.b64decode(event['awslogs']['data'])
			decompressed_data = gzip.decompress(payload).decode('ascii')
			parsed_result = json.loads(decompressed_data)
			print("Event Data:", json.dumps(parsed_result, indent=2))
			event_context = parsed_result["logGroup"]
			if event_context.find("lambda") != -1:
				event_context = "lambda"
			else:
				event_context = "ecs"
			
			writer_instruction = writer_instruction + " " + event_context
			return parsed_result
		except (json.JSONDecodeError, OSError) as e:
			print("Error processing logs:", e)
			return {
				'statusCode': 500,
				'body': str(e)
			}
	else:
		print("No awslogs data found in event:", event)
		return {
			'statusCode': 400,
			'body': 'No awslogs data found'
		}

def getEmailTemplate():
	global time_stamped
	template = "<html>"
	template = template + "<p>You are receiving this email because your Amazon CloudWatch Alarm 'Vertigo-Lambda-Mem-Spike' in the US East (Ohio) region has entered the ALARM state, because 'Threshold Crossed: 1 out of the last 1 datapoints  "+ time_stamped +"  was greater than or equal to the threshold (1.0) (minimum 1 datapoint for OK -&gt; ALARM transition).' at "+time_stamped+"UTC .<span class='im'><br />"
	template = template + "<br />View this alarm in the AWS Management Console:<br /><a href='https://us-east-2.console.aws.amazon.com/cloudwatch/deeplink.js?region=us-east-2#alarmsV2:alarm/Vertigo-Lambda-Mem-Spike' target='_blank' rel='noreferrer' data-saferedirecturl='https://www.google.com/url?q=https://us-east-2.console.aws.amazon.com/cloudwatch/deeplink.js?region%3Dus-east-2%23alarmsV2:alarm/Vertigo-Lambda-Mem-Spike&amp;source=gmail&amp;ust=1742131723451000&amp;usg=AOvVaw24g4QOITygn-0g2cW6XONu'>https://us-east-2.console.aws.<wbr />amazon.com/cloudwatch/deeplink<wbr />.js?region=us-east-2#alarmsV2:<wbr />alarm/Vertigo-Lambda-Mem-Spike</a><br />"
	template = template + " <br />Alarm Details:<br />- Name:&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;Vertigo-Lambda-Mem-Spike<br />- Description:&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;<br />- State Change:&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;INSUFFICIENT_DATA -&gt; ALARM<br /></span>- Reason for State Change:&nbsp; &nbsp; Threshold Crossed: 1 out of the last 1 datapoints "+time_stamped+" was greater than or equal to the threshold (1.0) (minimum 1 datapoint for OK -&gt; ALARM transition).<br />- Timestamp:&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; "+time_stamped+" UTC</p>"
	template = template+"</html>"
	return template

def sendEmailWithAttachement(s3,ses,object_key,subject):
    
    try:
        response = s3.get_object(Bucket=bucket_name, Key=object_key)
        file_data = response['Body'].read()
        file_name = object_key.split('/')[-1] # Extract filename from key
        # Construct email
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = "super.vertigo.demo@gmail.com"  # Get sender email from environment variable
        msg['To'] =  ', '.join(RECIPIENT_EMAIL)
        #msg['To'] = RECIPIENT_EMAIL
		
        # Add text body
        body = MIMEText(getEmailTemplate(), 'html')
        msg.attach(body)

        # Add attachment
        attachment = MIMEApplication(file_data, content_maintype='application', content_subtype='octet-stream')
        attachment.add_header('Content-Disposition', 'attachment', filename=file_name)
        msg.attach(attachment)

		
        #Send email
        try:
            ses.send_raw_email(
                Source="super.vertigo.demo@gmail.com",
                Destinations=RECIPIENT_EMAIL,
                RawMessage={'Data': msg.as_string()}
            )
            print('Email sent successfully!')
        except ClientError as e:
            print(f'Error sending email: {e}')
            raise
		# try:
		# 	response = requests.post(
		# 	'https://notify.cx/api/send-email',
		# 	headers={
		# 	'x-api-key': "91b7e386-ed14-443c-b0c4-31903c60d14a",
		# 	'Content-Type': 'application/json'
		# 	},
		# 	json={
		# 	'to': 'sre1.vertigo.demo@gmail.com',
		# 	'subject': 'Hello world',
		# 	'name': 'John Doe',
		# 	'message': 'Your email content here'
		# 	}
		# 	)
		# 	response.raise_for_status()
		# 	print('Email sent successfully:', response.json())
		
		# except requests.exceptions.RequestException as error:
		# 	print('Failed to send email:', error)

    except ClientError as e:
        print(f'Error getting object from S3: {e}')
        raise


def lambda_handler(event, context):
	# Parse the incoming event body
	#body = event["body"]
	print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<,")
	#sendEmail()
	event_data = getErrorContextFromLog(event, context)
	print("Event Data:", event_data)
	print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<,")

	#print(event['alarmData']['state']['reason'])
	#print(event['alarmData']['state']['reasonData'])

	for record in event_data["logEvents"]:
		message = record["message"]
		print(message)
		if(message.find("REPORT") != -1):
			break

	session_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
	input_text = writer_instruction +" "+ message
	client_code = "vertigo"

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
			decoded_chunk = chunk["chunk"]["bytes"].decode('utf-8')
			
			resp_text += decoded_chunk
			file_name = session_id + ".pdf"
			s3 = boto3.client('s3')
			ses = boto3.client('ses')			
			resp_text = getMarkDownHeader(session_id)+"\n"+resp_text

			resp_text = ""+resp_text+""
			pdf = FPDF()
			pdf.add_page()
			pdf.set_font("Arial", size=12)
			pdf.multi_cell(0, 10, resp_text)

			# Upload the PDF to S3
			pdf_content = pdf.output(dest='S').encode('latin-1')
			s3.put_object(Body=pdf_content, Bucket="vertigo-lambda-bucket", Key=file_name)
			
			sendEmailWithAttachement(s3,ses,file_name,"ALARM: 'Vertigo-Lambda-Mem-Spike' in US East (Ohio)")
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
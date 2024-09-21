import boto3
import os

client = boto3.client('comprehend', region_name='ap-southeast-1', aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'), aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))

def anonymise(text: str) -> str:
    try: 
      response = client.detect_pii_entities(Text=text, LanguageCode='en')
      entities = sorted(response['Entities'], key=lambda x: x['BeginOffset'], reverse=True)
      for entity in entities:
          start = entity['BeginOffset']
          end = entity['EndOffset']
          entity_type = entity['Type']
          anonymised_text = text[:start] + f"[{entity_type}]" + text[end:]
          text = anonymised_text
      return text
    except Exception as e:
        print(e)
        return text

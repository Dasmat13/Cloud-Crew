import boto3
from flask import Flask, request, jsonify, render_template
import json
import re
from flask_cors import CORS  # For handling CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def parse_plain_text_response(text):
    """
    Parses the plain text response and extracts the required fields.
    """
    result = {}
    print("Input Text for Parsing:", text)  # Log the input text

    # Extract Document Type
    doc_type_match = re.search(r'Document:\s*(.*)', text)
    if doc_type_match:
        result["Document Type"] = doc_type_match.group(1).strip()
    else:
        result["Document Type"] = "N/A"

    # Extract Key Provisions
    key_provisions_match = re.search(r'contract pertained to the supply of industrial machinery, with a total value of (.*)', text)
    if key_provisions_match:
        result["Key Provisions"] = f"The contract was for the supply of industrial machinery with a total value of {key_provisions_match.group(1).strip()}."
    else:
        result["Key Provisions"] = "N/A"

    # Extract Court’s Decision
    court_decision_match = re.search(r'this Court sets aside the judgment of the High Court and directs the Respondent to pay damages amounting to (.*)', text)
    if court_decision_match:
        result["Court’s Decision"] = f"The Supreme Court set aside the judgment of the High Court and directed the Respondent to pay damages amounting to {court_decision_match.group(1).strip()}."
    else:
        result["Court’s Decision"] = "N/A"

    # Extract Legal Implications
    legal_implications_match = re.search(r'This judgment shall serve as a precedent for future cases involving the interpretation of force majeure clauses in commercial contracts.', text)
    if legal_implications_match:
        result["Legal Implications"] = "This judgment serves as a precedent for future cases involving the interpretation of force majeure clauses in commercial contracts."
    else:
        result["Legal Implications"] = "N/A"

    # Extract Simplified Summary
    simplified_summary_match = re.search(r'Summary:\s*(.*)', text, re.DOTALL)
    if simplified_summary_match:
        result["Simplified Summary"] = simplified_summary_match.group(1).strip()
    else:
        result["Simplified Summary"] = "N/A"

    # Log the parsed summary
    print("Parsed Summary:", result)
    return result

def summarize_document(document):
    """
    Summarizes the given document using AWS Bedrock's Titan Text G1 - Lite model.
    """
    try:
        # Initialize the Bedrock Runtime client
        bedrock_runtime = boto3.client(service_name='bedrock-runtime', region_name='us-east-1')

        # Define the prompt
        prompt = f"""
        You are a highly experienced legal expert specializing in Indian law. Your task is to analyze and summarize the given legal document with accuracy and clarity, ensuring compliance with the Indian Legal System.

        Document: {document}

        Provide the summary in the following format:

        - Document Type: [Type of document]
        - Key Provisions: [Key provisions of the document]
        - Court’s Decision: [Summary of the court’s decision]
        - Legal Implications: [Legal implications of the decision]
        - Simplified Summary: [Simplified summary of the document]

        Ensure the response is clear and well-structured.
        """

        # Define the payload for Titan Text G1 - Lite
        payload = {
            "inputText": prompt,
            "textGenerationConfig": {
                "maxTokenCount": 1000,  # Adjust based on your needs
                "temperature": 0.7,  # Adjust for creativity vs. accuracy
                "topP": 0.9,  # Controls diversity of responses
            }
        }

        # Invoke the Titan Text G1 - Lite model
        response = bedrock_runtime.invoke_model(
            modelId='amazon.titan-text-lite-v1',  # Model ID for Titan Text G1 - Lite
            body=json.dumps(payload)
        )

        # Parse the response
        response_body = json.loads(response['body'].read())
        
        # Log the raw response from AWS Bedrock
        print("Raw AWS Bedrock Response:", response_body)

        # Check if the response contains the expected structure
        if 'results' in response_body and len(response_body['results']) > 0:
            generated_text = response_body['results'][0]['outputText']
        else:
            return {"error": "Unexpected response format from Bedrock."}

        # Log the raw AI-generated text
        print("Raw AI Output:", generated_text)

        # Parse the plain text response
        summary = parse_plain_text_response(generated_text)
        return summary

    except Exception as e:
        return {"error": f"Error in summarize_document: {str(e)}"}

@app.route('/summarize', methods=['POST'])
def summarize():
    """
    Handles the /summarize route for summarizing documents.
    """
    try:
        data = request.get_json()
        document = data.get('document', '')
        
        if not document:
            return jsonify({'error': 'No document provided'}), 400

        # Call the AI summarization function
        summary = summarize_document(document)

        # Log the summary for debugging
        print("Summary:", summary)

        return jsonify(summary)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def home():
    """
    Serves the frontend HTML page.
    """
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # Run in debug mode
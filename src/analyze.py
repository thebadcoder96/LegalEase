import json
from groq import Groq

from dotenv import load_dotenv
load_dotenv()


PROMPT="""You are a legal expert in the digital space. You know all the regulations like HIPPA, GDPR, and many more. You will analyze the given document using the following framework and provide output in JSON format.
You will give brief but informative explanations and ensure all text is clear, concise, and free of legal jargon.

<framework> 
1. Readability and Clarity
   * Use of plain language
   * Organized structure
   * Clear definitions of key terms
2. User Rights and Protections
   * Data privacy and protection clauses
   * User content ownership
   * Account termination policies
3. Company Rights and Limitations
   * Scope of service
   * Intellectual property rights
   * Limitation of liability
4. Legal Compliance
   * Adherence to relevant laws (e.g., GDPR, CCPA)
   * Dispute resolution mechanisms
   * Jurisdiction and governing law
5. Fairness and Balance
   * Equitable terms for both parties
   * Reasonable limitations on user actions
   * Fair pricing and refund policies (if applicable)

Grading Process
1. Analyze each section of document based on the framework above.
2. Assign scores for each category (1-10, with 10 being the best).
3. Calculate an overall grade based on the average score.
4.The 'user_friendly_summary' should be a concise paragraph that gives users a quick understanding of the document with any significant concerns.
5. Highlight key takeaways and unusual or potentially concerning clauses).
</framework>

You will follow the following JSON structure:

{{
    "document_type": "string",
    "company": "string",
    "last_updated": "string (YYYY-MM-DD or 'Not specified')",
    "analysis": {{
        "readability_and_clarity": {{
            "score": "integer (1-10)",
            "key_points": [
                "string"
            ]
        }},
        "user_rights_and_protections": {{
            "score": "integer (1-10)",
            "key_points": [
                "string"
            ]
        }},
        "company_rights_and_limitations": {{
            "score": "integer (1-10)",
            "key_points": [
                "string"
            ]
        }},
        "legal_compliance": {{
            "score": "integer (1-10)",
            "key_points": [
                "string"
            ]
        }},
        "fairness_and_balance": {{
            "score": "integer (1-10)",
            "key_points": [
                "string"
            ]
        }}
    }},
    "overall_grade": "float (average of all scores out of 10)",
    "summary": {{
        "key_takeaways": [
            "string",
        ],
        "unusual_clauses": [
            "string",
        ],
        "user_friendly_summary": "string"
    }},
}}

Additional Context:
Take into account that some clauses maybe related to the laws in that are particular to a certain country or region.

Here is the document: 
<document>{doc_text}</document>
"""

def analyze_document(doc_text):
    client = Groq()
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": PROMPT.format(doc_text=doc_text)},
        ],
        temperature=0.1,
        response_format={"type": "json_object"},
    )
    analysis = json.loads(response.choices[0].message.content)
    return analysis
import json
from groq import Groq

from dotenv import load_dotenv
load_dotenv()


PROMPT = """You are a legal expert tasked with analyzing a legal document for the average user who doesn't have time to read the entire document. Your goal is to provide a detailed, specific points or sections that users should be aware of and what actions they should take.
Carefully analyze the following document and extract the most important information:

<document>
{doc_text}
</document>

Provide your analysis in the following JSON format:

{{
    "document_type": "string",
    "company": "string",
    "last_updated": "string (YYYY-MM-DD or 'Not specified')",
    "key_points": [
        {{
            "category": "string (e.g., 'Copyrights', 'Data Privacy', 'User Rights', 'Company Limitations', etc.)",
            "point": "string (brief description)",
            "relevant_text": "string (exact quote from the document)",
            "explanation": "string (explain in simple terms what this means for the user)",
            "user_action": "string (what the user should do or be aware of regarding this point)"
        }}
    ],
    "concerning_clauses": [
        {{
            "clause": "string (exact quote of the concerning clause)",
            "explanation": "string (explain why this clause is concerning)",
            "user_action": "string (what the user should do or be aware of regarding this clause)"
        }}
    ],
    "unusual_elements": [
        {{
            "element": "string (description of the unusual element)",
            "relevant_text": "string (exact quote from the document)",
            "explanation": "string (explain why this is unusual and what it means for the user)"
        }}
    ],
    "user_friendly_summary": "string (a brief, easy-to-understand summary of the most important points)"
}}

Important guidelines:
1. Be specific and detailed. Always quote relevant passages from the document.
2. Focus on extracting and explaining information that is directly relevant and important for users. Avoid generalizations or broad statements.
3. Ensure all explanations are in clear, simple language without legal jargon.
4. For each point, clause, or element, provide concrete explanations of real-world implications for users.
5. Always specify actions users should take or be aware of for each point.
6. Pay special attention to anything unusual or potentially concerning for users. Do not include obvious basic rules like drinking age or avoid harm.
7. Make sure to accurately capture the document type, company name, and last updated date from the document.

Your analysis should enable users to understand the most important aspects of the document without reading it in full.
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
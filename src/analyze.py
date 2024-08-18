import json
from groq import Groq

from dotenv import load_dotenv
load_dotenv()


PROMPT = """You are a legal expert tasked with analyzing a legal document for the average user who doesn't have time to read the entire document. Your goal is to provide a detailed, specific analysis that highlights exactly what users should be aware of and what actions they should take.

Analyze the given document using the following framework and provide output in JSON format. Give detailed, specific explanations and ensure all text is clear, concise, and free of legal jargon.

<framework>
1. Readability and Clarity
   * Identify specific sections that are particularly clear or unclear
   * Point out any ambiguous terms or phrases
   * Highlight areas where key terms are not well-defined

2. User Rights and Protections
   * Specify exact clauses related to data privacy and protection
   * Detail user content ownership rights and limitations
   * Explain account termination policies and their implications

3. Company Rights and Limitations
   * Outline specific services covered and not covered
   * Detail the company's intellectual property claims
   * Highlight exact clauses limiting company liability

4. Legal Compliance
   * Identify specific laws referenced (e.g., GDPR, CCPA) and explain their relevance
   * Detail the dispute resolution process and what it means for users
   * Specify the jurisdiction and governing law and its implications

5. Fairness and Balance
   * Highlight any clauses that seem particularly one-sided
   * Identify specific limitations on user actions and their reasonableness
   * Detail pricing and refund policies, if applicable

Grading Process
1. For each category, provide at least 3-5 specific examples from the document, quoting relevant passages when necessary.
2. Assign scores for each category (1-10, with 10 being the best) and justify each score with specific reasons.
3. For each category, list at least 2 potentially concerning or annoying clauses, explaining exactly why they are problematic and what users should do about them.
4. Calculate an overall grade based on the average score.
5. In the user-friendly summary, prioritize the most important things users need to know and do.
6. For key takeaways and unusual clauses, list at least 3-4 top takeways and concerning one, be specific about what users should be aware of or take action on.
</framework>

Follow this JSON structure:

{{
    "document_type": "string",
    "company": "string",
    "last_updated": "string (YYYY-MM-DD or 'Not specified')",
    "analysis": {{
        "readability_and_clarity": {{
            "score": "integer (1-10)",
            "justification": "string",
            "key_points": [
                {{
                    "point": "string",
                    "example": "string (quote from document)",
                    "explanation": "string"
                }}
            ],
            "concerning_clauses": [
                {{
                    "clause": "string (quote from document)",
                    "explanation": "string",
                    "user_action": "string"
                }}
            ]
        }},
        "user_rights_and_protections": {{
            "score": "integer (1-10)",
            "justification": "string",
            "key_points": [
                {{
                    "point": "string",
                    "example": "string (quote from document)",
                    "explanation": "string"
                }}
            ],
            "concerning_clauses": [
                {{
                    "clause": "string (quote from document)",
                    "explanation": "string",
                    "user_action": "string"
                }}
            ]
        }},
        "company_rights_and_limitations": {{
            "score": "integer (1-10)",
            "justification": "string",
            "key_points": [
                {{
                    "point": "string",
                    "example": "string (quote from document)",
                    "explanation": "string"
                }}
            ],
            "concerning_clauses": [
                {{
                    "clause": "string (quote from document)",
                    "explanation": "string",
                    "user_action": "string"
                }}
            ]
        }},
        "legal_compliance": {{
            "score": "integer (1-10)",
            "justification": "string",
            "key_points": [
                {{
                    "point": "string",
                    "example": "string (quote from document)",
                    "explanation": "string"
                }}
            ],
            "concerning_clauses": [
                {{
                    "clause": "string (quote from document)",
                    "explanation": "string",
                    "user_action": "string"
                }}
            ]
        }},
        "fairness_and_balance": {{
            "score": "integer (1-10)",
            "justification": "string",
            "key_points": [
                {{
                    "point": "string",
                    "example": "string (quote from document)",
                    "explanation": "string"
                }}
            ],
            "concerning_clauses": [
                {{
                    "clause": "string (quote from document)",
                    "explanation": "string",
                    "user_action": "string"
                }}
            ]
        }}
    }},
    "overall_grade": "float (average of all scores out of 10)",
    "summary": {{
        "key_takeaways": [
            {{
                "point": "string",
                "importance": "string",
                "user_action": "string"
            }}
        ],
        "unusual_clauses": [
            {{
                "clause": "string (quote from document)",
                "explanation": "string",
                "user_action": "string"
            }}
        ],
        "user_friendly_summary": "string"
    }}
}}

Additional Context:
- Focus on specific clauses and their real-world implications for users.
- Clearly state what actions users should take for each concerning point.
- Consider regional laws and explain their relevance to users.
- Highlight any unusual clauses compared to similar documents from other companies.

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
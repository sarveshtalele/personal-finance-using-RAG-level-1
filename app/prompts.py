OUTLINE_PROMPT = """
Extract a detailed table of contents from the document.
Structure it as:

- Module with page number 
    - Concept
        - Topic

Return clean bullet points.
"""

FORMULA_PROMPT = """
You are answering based ONLY on the provided document context from the PDF.

Extract all financial formulas explicitly mentioned in the document.

For each formula, return:

1. Formula (exact as written in document)
2. Explanation (based strictly on document content)
3. Real-life use case (derived from document discussion)

Important rules:
- Do NOT say you don't have access to the PDF.
- Do NOT mention external databases.
- If a formula is not found in the retrieved context, say: "No formula found in the provided document context."
- Use only information grounded in the retrieved text.
"""

TEACH_PROMPT = """
Teach the following topic clearly and simply.

Topic: {topic}

Include:
- Concept explanation
- Step-by-step breakdown
- Example
- Real-life application
- Common mistakes
"""
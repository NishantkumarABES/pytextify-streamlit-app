input_text_video = """
PROMPT: 
You are tasked withconverting a transcript of a multi-speaker discussion or a single speaker into a well-structured and detailed document.
The conversation may include multiple topics, different opinions, and varied levels of detail. The goal is to transform the raw conversation into
a professional document that is organized, coherent, and easy to read.

Here’s what I need you to do:

1. Identify and Attribute Speakers:
Each speaker in the conversation should be clearly identified and their contributions attributed to them. Use their names
or roles (e.g., Speaker 1, Moderator, etc.), and make sure the speaker transitions are smooth and clear.

2. Summarize Key Points: For each section of the conversation, extract and summarize the key points.
Organize the summaries in a way that flows logically and highlights the most important aspects of the discussion.

3. Organize the Document into Sections:
   Introduction: Briefly introduce the purpose of the discussion and provide context.
   Discussion Topics: Break down the conversation into major topics or themes. For each theme:
        . Create a heading for the topic.
        . Summarize the main points discussed under that topic, including any differing opinions or conclusions reached.
        . Highlight specific contributions from each speaker, especially if they bring unique perspectives.
   Conclusion: Provide a concise summary of the overall discussion, including key takeaways or action items that were mentioned by the participants.
   Add Structure to Long Responses: If a speaker's response is particularly long, break it down into paragraphs. Use bullet points or numbered lists where necessary to improve readability.

4. Clarify Technical Terms: If technical terms or jargon are used, provide a brief explanation to make the document more accessible to a general audience.
5. Eliminate Redundancies: If any points are repeated throughout the discussion, consolidate them. Focus on creating a clean and concise narrative without unnecessary repetition.
6. Include Speaker Insights: Highlight any important insights or expertise shared by specific speakers. Emphasize expert opinions, recommendations, or unique contributions.
7. Maintain Objectivity: Ensure that the document remains neutral and factual. If there are differing opinions, present them without bias and allow the reader to form their own conclusions.

TRANSCRIPT:
"""

input_text = """
Prompt:

"Summarize the contents of the uploaded file. 
The file may be in PDF or DOC format and contains structured information or textual content, 
including paragraphs, bullet points, tables, or images. Break down the key points, insights, 
and important details clearly and concisely. Provide a summary that covers the following aspects:

1. Main Topics or Themes – Highlight the major themes or topics covered in the document.
2. Key Findings or Insights – Extract any essential findings or insights from the text.
3. Summary of Sections – Briefly summarize each section or chapter (if applicable).
4. Notable Quotes or Statements – Include any important quotes or key statements made in the document.
5. Actionable Items (if any) – Identify any steps, recommendations, or actions suggested in the text.
6. Ensure the summary is precise and reflects the structure of the original document, maintaining the logical flow of information."

DOCUMENT:

"""






import google.generativeai as genai

genai.configure(api_key="AIzaSyCBpgo3aO4hYBbGjG2ULR0eZ2kY2G740wU")
model = genai.GenerativeModel("gemini-1.5-flash")
def generate_documnet(text, type):
   if type == "video":
      return model.generate_content(input_text_video + text)
   else: return model.generate_content(input_text + text)
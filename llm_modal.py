input_text = """
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
import google.generativeai as genai

genai.configure(api_key="AIzaSyCBpgo3aO4hYBbGjG2ULR0eZ2kY2G740wU")
model = genai.GenerativeModel("gemini-1.5-flash")
def generate_documnet(text):
    return model.generate_content(input_text + text)
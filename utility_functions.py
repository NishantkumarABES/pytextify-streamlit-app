import requests

def is_valid_email(email):
    if '@' not in email or email.startswith('@') or email.endswith('@'):
        return False
    local_part, domain_part = email.split('@')
    if not local_part or not domain_part:
        return False
    if '.' not in domain_part or domain_part.startswith('.') or domain_part.endswith('.'):
        return False
    if len(local_part) > 64 or len(domain_part) > 255:
        return False
    return True


def fetch_transcript(video_url):
    url = "http://127.0.0.1:5000/fetch_transcript"  # Replace with your Flask app's URL if different
    data = {'video_url': video_url}
    
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()  # Raises an error for HTTP codes 4xx/5xx
        result = response.json()  # Parse the response JSON
        return result
        # print("Video Title:", result['video_title'])
        # print("\nTranscription:\n", result['transcription'])

    except requests.exceptions.RequestException as e:
        print(f"Error fetching transcript: {e}")
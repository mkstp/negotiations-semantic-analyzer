"""
Marc St. Pierre 1/13/2025
This module pre-processes transcript outputs (in txt format) from the Fathom video conferencing software.
"""

import re
import datetime
import time

# Helper functions
def convert_time(time_list, total_time):
    """Convert string timestamps to total seconds elapsed."""
    temp_list = []
    for t in time_list:
        x = time.strptime(t.strip(), '%M:%S')
        x = int(datetime.timedelta(minutes=x.tm_min, seconds=x.tm_sec).total_seconds())
        temp_list.append(x)

    # Append total time 
    temp_list.append(total_time)

    # Convert total seconds elapsed to total seconds spoken on each turn
    output_list = []
    for i in range(1, len(temp_list)):
        diff = temp_list[i] - temp_list[i - 1]
        output_list.append(diff if diff > 0 else 1)

    return output_list


def process_speaker_names(name_list, anonymize_flag=True):
    """Anonymize or clean speaker names."""
    output_list = name_list
    if anonymize_flag:
        for idx, speaker in enumerate(set(output_list)):
            output_list = [name.replace(speaker, f"Speaker{idx}") for name in output_list]
    else:
        for idx, speaker in enumerate(set(output_list)):
            output_list = [name.replace(speaker, speaker.strip('- \n\r')) for name in output_list]
    return output_list


def clean_text(transcription_list):
    """Clean up transcription values."""
    transcription_list = [t.strip().replace('\n', ' ') for t in transcription_list]

    # Replace multiple spaces with a single space
    transcription_list = [re.sub(r'\s{2,}', ' ', t) for t in transcription_list]

    # Remove filler words like "like"
    transcription_list = [re.sub(r'(?: like )|(?: like, )', ' ', t) for t in transcription_list]
    return transcription_list


# Main function
def prep_file(content, anonymize_flag=True):
    """Prepare and clean transcript content."""
    # Extract and convert the total time of the conversation from minutes to seconds
    total_convo_time = re.search(r'(?:VIEW RECORDING)\s-\s\d{1,}', content)
    if total_convo_time:
        total_convo_time = int(total_convo_time.group().split(" ")[-1]) * 60
    else:
        total_convo_time = 0

    # Remove hyperlinks and irrelevant content
    content = re.sub(r'[A-Z]+:.+=\d{1,}\.\d{1,}', ' ', content)
    content = content[content.find("---"):]

    # Split content by timestamps or speaker identifiers
    content = re.split(r'(\d{1,2}\:\d{2}\s?)|(\-+\s.+\D\n)', content)[1:]
    content = list(filter(None, content))

    # Initialize basic info lists
    timestamps = []
    speakers = []
    transcripts = []

    # Assign values to individual lists
    for idx, item in enumerate(content):
        [timestamps, speakers, transcripts][idx % 3].append(item)

    # Process and clean data
    timespans = convert_time(timestamps, total_convo_time)
    speakers = process_speaker_names(speakers, anonymize_flag)
    transcripts = clean_text(transcripts)

    return [speakers, timespans, transcripts]

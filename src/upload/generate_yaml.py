# Copyright (c) 2024 bilive.

import os
import time
import yaml
import codecs
from datetime import datetime
from src.upload.extract_video_info import generate_title, generate_desc, generate_tag, generate_source
import subprocess
import json

def generate_yaml_template(video_path):
    source = generate_source(video_path)
    title = generate_title(video_path)
    desc = generate_desc(video_path)
    tag = generate_tag(video_path)
    data = {
        "line": "bda2",
        "limit": 5,
        "streamers": {
            video_path: {
                "copyright": 1,
                "source": source,
                "tid": 138,
                "cover": "",
                "title": title,
                "desc_format_id": 0,
                "desc": desc,
                "dynamic": "",
                "tag": tag
            }
        }
    }
    return yaml.dump(data, default_flow_style=False, sort_keys=False)

def generate_slice_yaml_template(video_path):
    command = [
        "ffprobe",
        "-v", "quiet",
        "-print_format", "json",
        "-show_format",
        video_path
    ]
    output = subprocess.check_output(command, stderr=subprocess.STDOUT).decode('utf-8')
    parsed_output = json.loads(output)
    title = parsed_output["format"]["tags"]["generate"]
    data = {
        "line": "bda2",
        "limit": 5,
        "streamers": {
            video_path: {
                "copyright": 1,
                "source": "",
                "tid": 138,
                "cover": "",
                "title": title,
                "desc_format_id": 0,
                "desc": "",
                "dynamic": "",
                "tag": "直播切片"
            }
        }
    }
    return yaml.dump(data, default_flow_style=False, sort_keys=False)

if __name__ == "__main__":    
    # read the queue and upload the video
    yaml_template = generate_yaml_template("")
    with open('upload.yaml', 'w', encoding='utf-8') as file:
        file.write(yaml_template)

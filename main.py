import xml.etree.ElementTree as ET
import openai
import json
import pandas as pd
import openpyxl

file_path = r"savefile.rws"

def get_unique_hierarchy(node, seen_tags, indent=0):
    '''
    XML 노드의 계층 구조를 출력하는 함수. 이미 출력된 태그는 무시합니다.
    '''
    hierarchy = []
    if node.tag not in seen_tags:
        hierarchy.append('  ' * indent + node.tag)
        seen_tags.add(node.tag)
    for child in node:
        hierarchy.extend(get_unique_hierarchy(child, seen_tags, indent + 1))
    return hierarchy
    
def save_rimworld_save_hierarchy(file_path):
    '''
    load rimworld save file: exapansion.rws
    Location @ Window : C:/Users/{User}/AppData/LocalLow/Ludeon Studios/RimWorld by Ludeon Studios/Saves
    '''
    # Load the XML file
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    # Get the unique hierarchy of the XML file
    hierarchy = get_unique_hierarchy(root, set())

    # Save the hierarchy to a JSON file
    with open('unique_hierarchy.json', 'w', encoding='utf-8') as f:
        json.dump(hierarchy, f, ensure_ascii=False, indent=4)
# save_rimworld_save_hierarchy(file_path)

def parse_node(node):
    '''
    XML 노드를 파싱하고, 태그와 텍스트를 포함하는 딕셔너리를 반환합니다.
    '''
    data = {}
    for child in node:
        if child.text:
            data[child.tag] = child.text
    return data


def get_history(file_path):
    '''
    get history from rws file to excel file
    history @ 624 line in rws
    '''
    # Load the XML file
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    # Parse the XML data
    data = []
    for archive in root.findall('.//archive'):
        for li in archive.findall('.//li'):
            data.append(parse_node(li))
    
    # Convert the data to a pandas DataFrame
    df = pd.DataFrame(data)
    
    # Save the DataFrame to an Excel file
    df.to_excel(f'old_history.xlsx', index=False)
# get_history(file_path)
get_history('./savefile_old.rws')

def print_description_tags(file_path, tag = 'description'):
    '''
    rws파일의 description 태그를 출력하는 함수
    '''
    tree = ET.parse(file_path)
    root = tree.getroot()

    data = root.findall('.//{}'.format(tag))

    txt = [datum.text for datum in data]

    with open(f'./{tag}.json', 'w',encoding = 'utf-8') as f:
        json.dump(txt,f, ensure_ascii = False)
# print_description_tags(file_path)

def print_pawn_info(file_path):
    '''
    rws파일에서 정착민들의 정보를 출력하는 함수
    '''
    tree = ET.parse(file_path)
    root = tree.getroot()

    # 'Pawn' 태그를 찾습니다.
    for pawn in root.findall('.//Pawn'):
        name = pawn.find('name').text
        age = pawn.find('age').text
        gender = pawn.find('gender').text
        health = pawn.find('health').text

        print(f"Name: {name}, Age: {age}, Gender: {gender}, Health: {health}")
    

#print_description_tags(file_path)

def summarize_description(file_path):
    api_key = 'sk-proj-RB265txW8rQS3jr44cJiT3BlbkFJaNnvartQEnkpbUURxnkK'

    client = openai.OpenAI(api_key=api_key)
    tree = ET.parse(file_path)
    root = tree.getroot()

    for description in root.findall('.//description'):
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes text."},
                {"role": "user", "content": f"Summarize the following description: {description.text}"}
            ],
            temperature=0.3,
            max_tokens=60
        )
        print(type(response))
        print(response)
        with open('./response.json', 'a') as f:
            for choice in response.choices:
                f.write(json.dumps(choice.message.content) + '\n')
        # summary = response.choices[0].message['content'].strip()
        # print(f"Original: {description.text}")


# 예제 파일 경로


# description 태그 출력
# summarize_description(file_path)


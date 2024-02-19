# General imports ..
import os
import random
import logging
import urllib3
import warnings
import json
import requests

# langchain imports ..
from langchain.retrievers import WikipediaRetriever
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI

from urls import base_url, api_url, get_sub_url, get_sub_chap_url, add_ai_url
from logger import setup_logger

# surpress warnings ..
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
warnings.filterwarnings("ignore", category=UserWarning, module="langchain")

# Setting up logger ..
try:
    # Create 'logs' directory if it doesn't exist
    logs_directory = 'logs'
    if not os.path.exists(logs_directory):
        os.makedirs(logs_directory)

    # Set up logger with the log file inside the 'logs' directory
    log_file_path = os.path.join(logs_directory, 'add_chap_topics.log')
    logger = setup_logger('get_topics', log_file_path)
    logger.info('Logger is activated for GENERATING Chapter & topics ..')
except Exception as e:
    # Log the exception if there is an error during logger setup
    logger.error(e)

# Languages list ..
lang_list = ["english", "hindi", "bengali", "marathi", "telugu", "tamil", "gujarati", "urdu", "kannada", "malayalam", "oriya", "punjabi", "assamese", "sinhala"]
lang_codes = {'english': 1, 'hindi': 6}

# 1. Getting Subjects list from database ..  
def get_subjects():
    try:
        logger.info('Triggering GET Subjects List API ..')
        subject_response = requests.get(get_sub_url, verify=False)
        if subject_response.status_code==200:
            logger.info(f"GET Request for added Subjects list successfull with status code {subject_response.status_code}")
            logger.info("Subjects list has been retrieved successfully .. ")
            
            response_str = subject_response.content.decode('utf-8')
            subjects = json.loads(response_str)['data']
            return subjects
        else:
            logger.error(f"GET Request failed with status code {subject_response.status_code}")
    except Exception as e:
        logger.error("GET Subjects API is down .. ")

# 2.  Getting Subject info ..
def get_subject_info(subject_name, subject_list=get_subjects()):
    for subject in subject_list:
        if subject['name'] == subject_name:
            return (subject['_id'], subject['name'])

# 3.  Getting chapters list ..
def get_chapters(subject):
    subject_name = subject[1]
    logger.info(f"Processing subject - {subject_name}")
        
    try:
        logger.info('Triggering GET Chapters List API ..')
        url = get_sub_chap_url + subject[0]
        chapters_response = requests.get(url, verify=False)
        if chapters_response.status_code==200:
            logger.info(f"GET Request for added Chapters list successfull with status code {chapters_response.status_code}")
            logger.info(f"Chapters list for subject - {subject_name} has been retrieved successfully .. ")
        
            response_str = chapters_response.content.decode('utf-8')
            chapters = json.loads(response_str)['data']
            return chapters
        else:
            logger.error(f"GET Request for subject - {subject_name} failed with status code {chapters_response.status_code}")

    except Exception as e:
        logger.error("GET Chapters API is down .. ")
        
def find_grade_by_id(grade_id):
    grades_data = {
        "6": "80c7a75f-3060-11ee-bb86-000c29539bc1",
        "7": "92673410-3060-11ee-bb86-000c29539bc1",
        "8": "a17f9d23-3060-11ee-bb86-000c29539bc1",
        "9": "b2f6496b-3060-11ee-bb86-000c29539bc1",
        "10": "c114adfe-3060-11ee-bb86-000c29539bc1",
        "11 (Science)": "d64aca1f-3060-11ee-bb86-000c29539bc1",
        "11 (Commerce)": "e8404d03-3060-11ee-bb86-000c29539bc1",
        "11 (Arts)": "f971156a-3060-11ee-bb86-000c29539bc1",
        "12 (Science)": "2a79e82a-3061-11ee-bb86-000c29539bc1",
        "12 (Commerce)": "55acd452-3061-11ee-bb86-000c29539bc1",
        "12 (Arts)": "81dbdcdb-3061-11ee-bb86-000c29539bc1"
    }
    # matching with IDs ..
    for key, value in grades_data.items():
        if value == grade_id:
            return key
        
# Getting topics subject-wise ..  ..
def get_topics_subject_wise(subject):
    subject_info = get_subject_info(subject, get_subjects())
    chapters = get_chapters(subject_info)
    dicts = []
    for chapter in chapters:
        chapter_name = chapter['name']

        # Getting Topics dict ..
        for item in chapter['topics']:
            grade_id = item['cur_tag'][0]['grd_id']
            topic_grade = find_grade_by_id(grade_id)
            data_dict = {"chapterName":chapter_name, "topicName": item['name'], "topic_grade":topic_grade, "subject":subject}
            dicts.append(data_dict)

    return dicts

# Getting topics grade-wise ..  ..
def get_topics_grade_wise(subject, grade):
    subject_info = get_subject_info(subject, get_subjects())
    chapters = get_chapters(subject_info)
    dicts = []
    for chapter in chapters:
        chapter_name = chapter['name']

        # Getting Topics dict ..
        for item in chapter['topics']:
            grade_id = item['cur_tag'][0]['grd_id']
            topic_grade = find_grade_by_id(grade_id)
            if int(topic_grade.split(' ')[0]) != grade:
                continue
            else:
                data_dict = {"chapterName":chapter_name, "topicName": item['name'], "topic_grade":topic_grade, "subject":subject}
                dicts.append(data_dict)

    return dicts

if __name__=='__main__':
    topics = get_topics_grade_wise('Mathematics', 6)
    print(topics)
            
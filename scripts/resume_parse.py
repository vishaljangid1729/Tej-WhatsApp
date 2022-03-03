
from pyresparser import ResumeParser
import os
# import en_core_web_sm
import spacy

# spacy.load('en_core_web_sm')


def Hello ():

    main_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    resume_path = f'{main_dir}/Resume/vishal_jangid.pdf'
    data = ResumeParser(resume_path).get_extracted_data()

    print(data)
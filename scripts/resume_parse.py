
import time
from pyresparser import ResumeParser
import os
from scripts.whatsapp import WhatsApp
# spacy.load('en_core_web_sm')


def Hello ():

    main_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    resume_path = f'{main_dir}/Resume/vishal_jangid.pdf'
    data = ResumeParser(resume_path).get_extracted_data()
    print(data['mobile_number'])

    messsanger = WhatsApp()
    # input()
    messsanger.find_user("919663600101")
    # time.sleep(3)

    print("hewrwefrfs")
    messsanger.send_message("This is the bot")
    print("fsdafasdfasfasfasf")
    # input()
    # messsanger.send_message("hello")``
    # print(data)





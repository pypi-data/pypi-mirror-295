"""
payload-generator

A package for generating payloads for sending to the Ingestion Gateway.
"""

__version__ = "0.1.0"
__author__ = 'Zeshan Khatri'
__credits__ = 'Qualtrics'

from faker import Faker
from pkg_resources import resource_filename
import random
import datetime
import uuid
import json
import sys

fake = Faker()
source = "XM Discover Link"

attributes_template = {
      "acdid": None,
      "agent_channel": 1,
      "agent_clarity": 0.972,
      "agentid": None, # company email
      "agentname": None,
      "agentusername": None,
      "ani": None, # ANI Number
      "associate_tenure": "1",
      "batchlabel": "VIP-241.2",
      "businessarea": "GBO",
      "calldirection": "1",
      "callid": None,
      "calllengthsec": 378.15,
      "callskill": "GBO | Dental | MTV | Member | English",
      "callstarttimeutc": None,
      "cb_vtt_file_id": None,
      "client_channel": 0,
      "confidence": 0.97,
      "cost_center_hierarchy": "86 Group Business Operations",
      "cost_center_name": "33301 GBO-Calls-Den-MTV",
      "dnis": None, # DNIS
      "donedate": None,
      "duration_m": 6.3,
      "duration_s": 378.049,
      "employee_id": None,
      "externalcallid": None,
      "feedback_provider": None,
      "feedback_type": "call",
      "hire_date": None,
      "job_name": None,
      "language_model": "en-US,en-US",
      "level_1_name": None,
      "loaddate": None,
      "location": "Offshore Location",
      "manager_level_1_name": None,
      "manager_level_2_name": None,
      "manager_level_3_name": None,
      "organization": "SPECIALTY",
      "orig_vtt_source": "Mattersight",
      "role": None,
      "scrubbed": 1,
      "ucid": None,
      "vendor_name": None,
      "worker_type": "Contingent Worker"
}

participants = [
    {
        "participant_id": 1,
        "type": "CLIENT",
        "gender": "UNKNOWN",
        "isBot": False,
        "speechRate": 0,
        "issueResolutionParticipantOutcome": "IR_PO_UNKNOWN",
        "empathyScore": 0,
        "attributes": {}
    },
    {
        "participant_id": 2,
        "type": "AGENT",
        "gender": "UNKNOWN",
        "isBot": False,
        "speechRate": 0,
        "issueResolutionParticipantOutcome": "IR_PO_UNKNOWN",
        "empathyScore": 0,
        "attributes": {}
    }
]

template = {
    "uuid": None,
    "project_id": None,
    "document": {
        "attributes": {},
        "verbatims": [
            {
                "call": {
                    "verbatim_types": [
                        "clientverbatim",
                        "agentverbatim",
                        "unknownverbatim"
                    ],
                    "body": {
                        "duration": "378049",
                        "total_silence": "13898",
                        "total_dead_air": "11268",
                        "total_overtalk": "42408",
                        "total_hesitation": "0",
                        "percent_silence": 0.037,
                        "processingOpts": {
                            "reason_enabled": True
                        },
                        "source_system": "aws-default",
                        "special_events": [],
                        "participants": participants,
                        "segment_type": "SENTENCE",
                        "segments": [] # no verbatims yet
                    },
                    "source_system": source,
                    "source": "SOURCE_CALL",
                    "allRelations": True,
                    "reasonEnabled": True,
                    "processingStage": "PROCESSING_STAGE_SYNTAX"
                }
            }
        ]
    },
    "natural_id": None,
    "source": source,
    "document_date": None,
}

def get_random_timestamp():
    start_datetime = datetime.datetime.strptime("2020-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")
    end_datetime = datetime.datetime.today()
    
    time_diff = end_datetime - start_datetime
    random_seconds = random.randint(0, int(time_diff.total_seconds()))
    
    random_timestamp = start_datetime + datetime.timedelta(seconds=random_seconds)
    return random_timestamp.strftime("%Y-%m-%dZ%H:%M:%S+0000")


def set_attributes():
    allowed_letters = 'abcdefghijklmnpqrstuvwxyz' # used for bothify method

    attributes = attributes_template

    attributes['acdid'] = fake.company().replace(" ", "_").replace("-", "_") + '_Prod'
    attributes['agentid'] = fake.company_email()
    attributes['agentname'] = fake.name()
    attributes['agentusername'] = f'CLB{fake.random_number(digits=4, fix_len=True)}'
    attributes['ani'] = f'{fake.random_number(digits=10, fix_len=True)}'
    attributes['callid'] = f'{fake.random_number(digits=9, fix_len=True)}'
    attributes['callstarttimeutc'] = get_random_timestamp()
    attributes['cb_vtt_file_id'] = fake.bothify(text='%??%%?%?-%%%%-%??%-?%?%-?%%%%%%??%%%', letters=allowed_letters)
    attributes['dnis'] = f'{fake.random_number(digits=10, fix_len=True)}'
    attributes['donedate'] = get_random_timestamp()
    attributes['employee_id'] = f'{fake.random_number(digits=7, fix_len=True)}'
    attributes['externalcallid'] = attributes['ucid'] = fake.bothify(text='??%%%%%?-%???-%?%%-%%??-%?%%?%%%?%?%', letters=allowed_letters) # both reference same value
    attributes['feedback_provider'] = source
    attributes['hire_date'] = get_random_timestamp()
    attributes['job_name'] = fake.company().upper().replace(" ", "_").replace("-", "_") + '_Prod_Gen'
    attributes['level_1_name'] = fake.name()
    attributes['loaddate'] = get_random_timestamp()
    attributes['manager_level_1_name'] = fake.name()
    attributes['manager_level_2_name'] = fake.name()
    attributes['manager_level_3_name'] = fake.name()
    attributes['role'] = fake.job()
    attributes['vendor_name'] = fake.company()

    return attributes


def generate_verbatims(count):
    with open(resource_filename('payload_generator', 'word_list.txt'), 'r') as word_list:
                words = word_list.read().split()

    segments = []
    start = fake.random_int(min=1000, max=2500) # random verbatim start timestamp

    for j in range(count):
        sentence = fake.sentence(nb_words=10, variable_nb_words=True, ext_word_list=words) # generates sentences of around 10 words from word_list file
        end = start + fake.random_int(min=100, max=1500)
        verbatim = {
            "participant_id": (j % 2) + 1,
            "text": sentence,
            "start": start,
            "end": end
        }
        segments.append(verbatim)
        start = end

    return segments


def generate_payloads():
    if(len(sys.argv) < 4):
        raise IndexError(f'Expected 3 arguments but received {len(sys.argv) - 1}! Payload count, project ID, and target folder must all be specified')
    
    count=int(sys.argv[1])
    project_id=int(sys.argv[2])
    folder=sys.argv[3]

    with open(f'{folder}/payload.json', 'w') as file:
        file.write('[')
        for i in range(1, count+1):
            payload = template
            natural_id = str(uuid.uuid4())
            payload['uuid'] = natural_id
            payload['project_id'] = project_id
            payload['natural_id'] = f'Audio;{natural_id}'
            payload['document_date'] = get_random_timestamp()

            document = payload['document']
            
            # Set attributes
            attributes = set_attributes()
            document['attributes'] = attributes

            verbatims = document['verbatims'][0]['call']['body']
            
            # Generate verbatims
            payload_size = fake.random_int(min=25, max=300, step=25) # number of verbatims to generate
            segments = generate_verbatims(count=payload_size)
            verbatims['segments'] = segments

            file.write(json.dumps(payload))
            file.write(',' if i != count else '\n')

            if(count < 20): # to avoid making output too verbose
                print(f"Generated Payload {i} with {payload_size} verbatims as payload{i}.json")
        file.write(']')
    print(f'Generated array of {count} payloads of variable sizes in {folder}/payload.json')
    
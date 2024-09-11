from fastapi import FastAPI, File, UploadFile

from pydantic import BaseModel
import xml.etree.ElementTree as ET
from langchain.output_parsers.openai_tools import PydanticToolsParser
from pydantic import BaseModel as BaseModelPydantic
from langchain.pydantic_v1 import BaseModel, Field
from typing import Optional, List
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
import uvicorn
import json
import os

os.environ['GROQ_API_KEY']='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'

app = FastAPI()


class XMLData(BaseModelPydantic):
    xml_string: str


class anomaly_parser(BaseModel):
    user_entered_values: Optional[List[str]] = Field(None, description="The values that have been filled by user")
    entered_values_decriptions: Optional[List[str]] = Field(None,
                                                            description="the description of the fields  in the same order as user_entered_values , if there is no description then '' ")
    is_anomaly: Optional[str] = Field(None,
                                      description="decision, if there is anomaly it should be True else it should be False")
    reason: Optional[List[str]] = Field(None, description="List of reasons stating why is this marked as anomaly")


def extract_data_from_xml(xml_string):
    root = ET.fromstring(xml_string)
    data = {}

    # Extract data from CoreModel
    core_model = root.find('CoreModel')
    if core_model is not None:
        data['IsDraftLoaded'] = core_model.find('Properties/IsDraftLoaded').text
        comments = core_model.findall('Comments')
        if comments:
            data['Comments'] = {
                'ControlID': comments[0].find('ControlID').text,
                'UserFullName': comments[0].find('UserFullName').text,
                'LoginName': comments[0].find('LoginName').text,
                'Date': comments[0].find('Date').text,
                'Text': comments[0].find('Text').text
            }
        documents = core_model.findall('Documents')
        if documents:
            data['Documents'] = []
            for doc in documents:
                data['Documents'].append({
                    'DocumentSubType': doc.find('DocumentSubType').text,
                    'Content': doc.find('Content').text,
                    'Verified': doc.find('Verified').text,
                    'Uploaded': doc.find('Uploaded').text,
                    'Requested': doc.find('Requested').text,
                    'DocumentID': doc.find('DocumentID').text,
                    'DocumentType': doc.find('DocumentType').text,
                    'Status': doc.find('Status').text,
                    'ExternalLink': doc.find('ExternalLink').text
                })
        header = core_model.find('Header')
        if header is not None:
            data['FormComment'] = header.find('FormComment').text

    # Extract data from ModelProcessData
    model_process_data = root.find('ModelProcessData')
    if model_process_data is not None:
        details2 = model_process_data.findall('Detail2')
        if details2:
            data['Detail2'] = []
            for detail in details2:
                data['Detail2'].append({
                    'MilageType': detail.find('MilageType').text,
                    'MilageError': detail.find('MilageError').text,
                    'Capacity': detail.find('Capacity').text,
                    'DateValue': detail.find('DateValue').text,
                    'No': detail.find('No').text,
                    'Milage': detail.find('Milage').text,
                    'DescriptionValue': detail.find('DescriptionValue').text
                })
        details = model_process_data.findall('Detail')
        if details:
            data['Detail'] = []
            for detail in details:
                data['Detail'].append({
                    'TypeValue': detail.find('TypeValue').text,
                    'DirectPayment': detail.find('DirectPayment').text,
                    'Feedback': detail.find('Feedback').text,
                    'ExpenseType': detail.find('ExpenseType').text,
                    'ExpenseError': detail.find('ExpenseError').text,
                    'DateValue': detail.find('DateValue').text,
                    'NoDocument': detail.find('NoDocument').text,
                    'CurrencyValue': detail.find('CurrencyValue').text,
                    'No': detail.find('No').text,
                    'Amount': detail.find('Amount').text,
                    'DescriptionValue': detail.find('DescriptionValue').text,
                    'Verify': detail.find('Verify').text
                })
        header_data = model_process_data.find('HeaderData')
        if header_data is not None:
            data['HeaderData'] = {
                'TypeValue': header_data.find('TypeValue').text,
                'Location': header_data.find('Location').text,
                'Reimbursment': header_data.find('Reimbursment').text,
                'EndDate': header_data.find('EndDate').text,
                'CurrencyType': header_data.find('CurrencyType').text,
                'ExpenseID': header_data.find('ExpenseID').text,
                'UserId': header_data.find('UserId').text,
                'ApprovalNo': header_data.find('ApprovalNo').text,
                'EmployeeCurrency': header_data.find('EmployeeCurrency').text,
                'ExpenseInternalId': header_data.find('ExpenseInternalId').text,
                'FormComments': header_data.find('FormComments').text,
                'Reason': header_data.find('Reason').text,
                'EmployeeName': header_data.find('EmployeeName').text,
                'ClassName': header_data.find('ClassName').text,
                'NoProject': header_data.find('NoProject').text,
                'ProjectNo': header_data.find('ProjectNo').text,
                'StartDate': header_data.find('StartDate').text
            }

    return data


parser = PydanticToolsParser(tools=[anomaly_parser])
model = ChatGroq(model="llama-3.1-70b-versatile", temperature=0).bind_tools([anomaly_parser])

prompt = ChatPromptTemplate.from_messages(
    [("system", """
    You are expert at analyzing the given expense data filled by company employees, employees are filling data and they can be confident that they are not going to make mistakes. You need to find the user filled fields, and then on basis of the field and field type and description you need to detect the anomalies, if there is anomaly found then mark "is_anomaly" as True and also give the list of reasons why it is anomaly

    Here are some examples:


    | Field Type | Field Description | User Entered Value | |------------|------------------|---------------------| | Date | Date of expense | 2022-12-31 | | Category | Type of expense | Food | | Amount | Expense amount | 200.00 | | Description| Brief description| Lunch with clients |

| Field Type | Field Description | User Entered Value | |------------|------------------|---------------------| | Date | Date of expense | 2023-02-01 | | Category | Type of expense | Transportation | | Amount | Expense amount | 5000.00 | | Description| Brief description| Flight to NY |

| Field Type | Field Description | User Entered Value | |------------|------------------|---------------------| | Date | Date of expense | 2022-12-35 | | Category | Type of expense | Hotel | | Amount | Expense amount | 800.00 | | Description| Brief description| Stay at Hilton |

Anomalous value: Date is invalid

| Field Type | Field Description | User Entered Value | |------------|------------------|---------------------| | Date | Date of expense | 2023-01-15 | | Category | Type of expense | Miscellaneous | | Amount | Expense amount | 100000.00 | | Description| Brief description| Gift for friend |

Anomalous value: Amount is unusually high

| Field Type | Field Description | User Entered Value | |------------|------------------|---------------------| | Date | Date of expense | 2022-12-20 | | Category | Type of expense | Entertainment | | Amount | Expense amount | 50.00 | | Description| Brief description| Dinner with family |

| Field Type | Field Description | User Entered Value | |------------|------------------|---------------------| | Date | Date of expense | 2023-03-01 | | Category | Type of expense | Office Supplies | | Amount | Expense amount | 10000.00 | | Description| Brief description| Purchased chairs |

Anomalous value: Amount is unusually high for office supplies

| Field Type | Field Description | User Entered Value | |------------|------------------|---------------------| | Date | Date of expense | 2022-11-30 | | Category | Type of expense | Travel | | Amount | Expense amount | 200.00 | | Description| Brief description| Cab fare |

| Field Type | Field Description | User Entered Value | |------------|------------------|---------------------| | Date | Date of expense | 2023-01-31 | | Category | Type of expense | Education | | Amount | Expense amount | 500.00 | | Description| Brief description| Online courses |

| Field Type | Field Description | User Entered Value | |------------|------------------|---------------------| | Date | Date of expense | 2022-12-32 | | Category | Type of expense | Networking | | Amount | Expense amount | 150.00 | | Description| Brief description| Conference attendance|

Anomalous value: Date is invalid

| Field Type | Field Description | User Entered Value | |------------|------------------|---------------------| | Date | Date of expense | 2023-02-28 | | Category | Type of expense | Software | | Amount | Expense amount | 2000.00 | | Description| Brief description| Adobe subscription |

    Your answer should be a simple True/False and a list of reasons why its anomaly, and the fields filled by user


    """),

     ("user", "Here is the single long form that user entered:\n{xml_extracted}")]
)

chain = prompt | model | parser

@app.post("/detect_anomaly")
async def detect_anomaly(xml_file: UploadFile = File(...)):
    xml_string = await xml_file.read()
    xml_string = xml_string.decode("utf-8")  # Specify the correct encoding here
    data_as_dict = extract_data_from_xml(xml_string)
    results = chain.invoke({"xml_extracted": json.dumps(data_as_dict)})
    results = [k.__dict__ for k in results]
    return results
def main():
    uvicorn.run(app, host='0.0.0.0', port=8357, log_level="debug")

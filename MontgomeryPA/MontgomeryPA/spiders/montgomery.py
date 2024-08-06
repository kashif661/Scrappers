import json
import re
from typing import Any, Iterable
from scrapy.http import HtmlResponse, Request, Response
import scrapy
from dotenv import load_dotenv
from urllib.parse import urlencode
from ..address_parser import Address_parser
from .. import name_parser
from datetime import datetime, timedelta
from scrapy.utils.response import open_in_browser
from ..items import MontgomerypaItem   
import os
import pandas as pd





load_dotenv()    


parser = Address_parser()


def process_zip_code(zip_code):
    zip_code = str(zip_code)
    if zip_code is None or pd.isna(zip_code):
        return ''
    digits_match = re.search(r'\b\d{5}\b', str(zip_code))

    if digits_match:
        return digits_match.group()
    else:
        digits_match = re.search(r'\b\d{4}\b', str(zip_code))
        if digits_match:
            return digits_match.group()
        else:
            return ''
        
def calculate_age(date_of_birth, date_of_death):
    if not date_of_birth or not date_of_death or "Not Authorized" in (date_of_birth, date_of_death):
        return None
    
    dob = datetime.strptime(date_of_birth, "%m/%d/%Y")
    dod = datetime.strptime(date_of_death, "%m/%d/%Y")
    age = dod.year - dob.year - ((dod.month, dod.day) < (dob.month, dob.day))
    return age

    
class MontgomerySpider(scrapy.Spider):
    name = "montgomery"

    start_urls = ["https://courtsapp.montcopa.org/psi/v/search/case"]
    def __init__(self, *args, **kwargs):
        super(MontgomerySpider, self).__init__(*args, **kwargs)
        self.datefrom_str = kwargs.get('datefrom_str')
        self.dateto_str = kwargs.get('dateto_str')

    cookies = {
        'ASP.NET_SessionId': 't1slmouclfu4uylhxvgvkh30',
        'PSIUserGuid': '72452016-9ba4-45b9-8eb9-28e2bcfc282a',
        'PSIViewerLastSearchUrl2': 'https://courtsapp.montcopa.org/psi3/v/search/case',
        'SearchResultsAsGrid': 'True',
        'PSIAuthMontco': 'E7A29B32F85505679A4097E9AA1155E98B623D64643D51DCAFD5AEBB1CDC8CCD66F240D5E17AF020774C05E911FCDF2794233F9C0AC9E13848D3D7CB72ECFFFE7A66BC2B935082F000DF9CE52AB2D2A92386E0D26828868913B8C89A63E92BD4A5603AA8A02019276021833A87663D728C130084E150F1A1B0420FE449C7EA246F06C4F8C21006DC1654ED0DCA14D936769629E76A76A864FC82EB4EFA5C67F9E8A1EE34'
    }

    headers = {
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json;charset=UTF-8",

    }

    def parse(self, response):
        
        # Define the start date
        start_date = datetime(2023, 1, 1)

        # Define the end date
        end_date = datetime(2023, 10, 31)  # Change this to the last date you want

        # Define the increment (4 days)
        increment = timedelta(days=4)

        # Initialize the current date
        current_date = start_date

        params = {
            'Q': '',
            'IncludeSoundsLike': False,
            'Count': 20,
            'fromAdv': 1,
            'CaseCategory': 1,
            'CaseNumber': '',
            'LegacyCaseNumber': '',
            'CaseType': '', 
            'DateCommencedFrom': '',
            'DateCommencedTo': '',
            'IncludeInitialFilings': False,
            'IncludeInitialEFilings': False,
            'FilingType': '',
            'FilingDateFrom': self.datefrom_str,
            'FilingDateTo': self.dateto_str,
            'IncludeSubsequentFilings': False,
            'IncludeSubsequentEFilings': False,
            'JudgeID': '',
            'Attorney': '',
            'AttorneyID': '',
            'Grid': False
        }
        url = "https://courtsapp.montcopa.org/psi3/v/search/case?" + urlencode(params)
        meta_data = {
            'count': '20',
        }
        yield scrapy.Request(url=url, callback=self.case_listing, meta=meta_data)

    def case_listing(self, response):

        links = response.css('br+ a').xpath('@href').extract()
        for link in links:
            url = "https://courtsapp.montcopa.org" + link
            yield scrapy.Request(url=url, callback=self.case)

        total_num_records = response.css('span+ span').css('::text').extract()

        next_button = response.css('total_records').xpath('@href').extract_first()
        if not next_button:
            next_button = response.css('a:nth-child(175)').xpath('@href').extract_first()
        total_records = total_num_records[1].replace(' Results', '')
        total_records = int(total_records)
        count = response.meta['count']
        count = int(count)
        if total_records > count:
            params = {
                'Q': '',
                'IncludeSoundsLike': False,
                'Count': 20,
                'fromAdv': 1,
                'CaseCategory': 1,
                'CaseNumber': '',
                'LegacyCaseNumber': '',
                'CaseType': '',
                'DateCommencedFrom': '',
                'DateCommencedTo': '',
                'IncludeInitialFilings': False,
                'IncludeInitialEFilings': False,
                'FilingType': '',
                'FilingDateFrom': self.datefrom_str,
                'FilingDateTo': self.dateto_str,
                'IncludeSubsequentFilings': False,
                'IncludeSubsequentEFilings': False,
                'JudgeID': '',
                'Attorney': '',
                'AttorneyID': '',
                'Grid': False,
                'Skip': count
            }
            url = "https://courtsapp.montcopa.org/psi3/v/search/case?" + urlencode(params)
            count = count + 20
            meta_data = {
                'count': count,
            }
            # print(count)
            yield scrapy.Request(url=url, callback=self.case_listing, meta=meta_data)

        # url = 'https://courtsapp.montcopa.org/psi3/v/detail/Case/199937'
        # yield scrapy.Request(url=url, callback=self.case)

    def case(self, response):
        case_number = response.css('.ViewerDetail tr:nth-child(1) td').css('::text').extract_first()
        filling_date = response.css('tr:nth-child(3) td').css('::text').extract_first()
        if filling_date:
            date_object = datetime.strptime(filling_date, "%m/%d/%Y")
            filling_date = date_object.strftime("%Y-%m-%d")
        else:
            filling_date = ""
        case_title = response.css('.ViewerDetail tr:nth-child(6) td').css('::text').extract_first()
        if case_title is not None:
            case_title = case_title.title()
        else:   
            case_title = ""
        case_type = response.css('tr:nth-child(8) td').css('::text').extract_first()
        if case_type is not None:
            case_type = case_type.title()
        else:
            case_type = ""
        case_status = response.css('tr:nth-child(5) td').css('::text').extract_first()
        my_data = {
            "State": "PA",
            "Address":"",
            "County": "Montgomery",
            "City": "",
            "Zip": "",
            "Status": case_status,
            "Filing_Date": filling_date,
            "Case_Number": case_number,
            "Case_Title": case_title,
            "Case_Type": case_type,
            "DOB": "",
            "DOD": "",
            "Age": "",
            "Decedent_Full_Name": "",
            "Decedent_First_Name": "",
            "Decedent_Middle_Name": "",
            "Decedent_Last_Name": "",
            "Decedent_Suffix": "",
            "Decedent_Emails": None,
            "Decedent_Phones": None,
            "Decedent_Address": "",
            "Decedent_City": "",
            "Decedent_State": "",
            "Decedent_Zip": "",
            "Petitioner1_Full_Name": "",
            "Petitioner1_First_Name": "",
            "Petitioner1_Middle_Name": "",
            "Petitioner1_Last_Name": "",
            "Petitioner1_Suffix": "",
            "Petitioner1_Address": "",
            "Petitioner1_City": "",
            "Petitioner1_State": "",
            "Petitioner1_Zip": "",
            "Petitioner1_Emails": None,
            "Petitioner1_Phones": None,
            "Petitioner2_Full_Name": "",
            "Petitioner2_First_Name": "",
            "Petitioner2_Middle_Name": "",
            "Petitioner2_Last_Name": "",
            "Petitioner2_Suffix": "",
            "Petitioner2_Address": "",
            "Petitioner2_City": "",
            "Petitioner2_State": "",
            "Petitioner2_Zip": "",
            "Petitioner2_Emails": None,
            "Petitioner2_Phones": None,
            "Attorney1_Full_Name": "",
            "Attorney1_First_Name": "",
            "Attorney1_Middle_Name": "",
            "Attorney1_Last_Name": "",
            "Attorney1_Suffix": "",
            "Attorney1_Address": "",
            "Attorney1_City": "",
            "Attorney1_State": "",
            "Attorney1_Zip": "",
            "Attorney1_Emails": None,
            "Attorney1_Phones": None,
            "Attorney2_Full_Name": "",
            "Attorney2_First_Name": "",
            "Attorney2_Middle_Name": "",
            "Attorney2_Last_Name": "",
            "Attorney2_Suffix": "",
            "Attorney2_Address": "",
            "Attorney2_City": "",
            "Attorney2_State": "",
            "Attorney2_Zip": "",
            "Attorney2_Emails": None,
            "Attorney2_Phones": None,
            "Relatives1_Full_Name": "",
            "Relatives1_First_Name": "",
            "Relatives1_Middle_Name": "",
            "Relatives1_Last_Name": "",
            "Relatives1_Suffix": "",
            "Relatives1_Emails": None,
            "Relatives1_Phones": None,
            "Relatives1_Address": "",
            "Relatives1_City": "",
            "Relatives1_State": "",
            "Relatives1_Zip": "",
            "Relatives2_Full_Name": "",
            "Relatives2_First_Name": "",
            "Relatives2_Middle_Name": "",
            "Relatives2_Last_Name": "",
            "Relatives2_Suffix": "",
            "Relatives2_Emails": None,
            "Relatives2_Phones": None,
            "Relatives2_Address": "",
            "Relatives2_City": "",
            "Relatives2_State": "",
            "Relatives2_Zip": "",
            "Relatives3_Full_Name": "",
            "Relatives3_First_Name": "",
            "Relatives3_Middle_Name": "",
            "Relatives3_Last_Name": "",
            "Relatives3_Suffix": "",
            "Relatives3_Emails": None,
            "Relatives3_Phones": None,
            "Relatives3_Address": "",
            "Relatives3_City": "",
            "Relatives3_State": "",
            "Relatives3_Zip": "",
            "Relatives4_Full_Name": "",
            "Relatives4_First_Name": "",
            "Relatives4_Middle_Name": "",
            "Relatives4_Last_Name": "",
            "Relatives4_Suffix": "",
            "Relatives4_Emails": None,
            "Relatives4_Phones": None,
            "Relatives4_Address": "",
            "Relatives4_City": "",
            "Relatives4_State": "",
            "Relatives4_Zip": "",
            "Relatives5_Full_Name": "",
            "Relatives5_First_Name": "",
            "Relatives5_Middle_Name": "",
            "Relatives5_Last_Name": "",
            "Relatives5_Suffix": "",
            "Relatives5_Emails": None,
            "Relatives5_Phones": None,
            "Relatives5_Address": "",
            "Relatives5_City": "",
            "Relatives5_State": "",
            "Relatives5_Zip": "",
            "Url": response.url
        }

        payload = json.dumps({
            "DocketRange": "50",
            "token": None
        })
        url = response.url + "/data"
        yield scrapy.FormRequest(url=url,
                                 callback=self.case_details, meta=my_data, method='POST',
                                 headers=self.headers, body=payload,
                                 # cookies=self.cookies
                                 )
                                
    def case_details(self, response):

        url = response.url
        try:
            data = response.json()
        except json.JSONDecodeError as e:
            # self.logger.error(f"JSON parsing error: {e}")
            return
        my_data = response.meta

        response = HtmlResponse(url='about:blank', body=data['Detail'].encode('utf-8'))

        response = HtmlResponse(url='about:blank', body=data['Relates'][0].encode('utf-8'))

        link_case = response.css('#table_LinkedCases h4').css('::text').extract()
        if link_case:
            data['Relates'].pop(0)
            response = HtmlResponse(url='about:blank', body=data['Relates'][0].encode('utf-8'))

        decedent = response.css('#table_CaseFoundationParties .selcol+ td').css('::text').extract_first()
        pattern = r'\([^)]*\)'
        result = re.sub(pattern, '', decedent)
        input_string = result.strip()
        input_string = input_string.replace("ESQ", "").strip()
        decedent = re.sub(r'\([^)]*\)', '', input_string)
        match = re.search(r'\(([^)]*)\)', input_string)
        if match:
            decedent1 = match.group(1)
        try:
            if decedent1 is not None:
                if len(decedent) >= len(decedent1):
                    decedent = decedent
                else:
                    decedent = decedent1
            else:
                decedent = decedent
        except:
            pass
        date_of_death = response.css('#table_CaseFoundationParties td:nth-child(3)').css('::text').extract_first()
        date_of_birth = response.css('#table_CaseFoundationParties td:nth-child(4)').css('::text').extract_first()
        decedent_address = response.css('#table_CaseFoundationParties td:nth-child(5)').css('::text').extract()

        if date_of_death is None or "Not Authorized" in date_of_death:
            date_of_death = ""

        if date_of_birth is None or "Not Authorized" in date_of_birth:
            date_of_birth = ""

        # Calculating Age
        if date_of_birth and date_of_death:
            my_data['Age'] = calculate_age(date_of_birth=date_of_birth, date_of_death=date_of_death)

        response = HtmlResponse(url='about:blank', body=data['Relates'][1].encode('utf-8'))
        personal_representatives = response.css('#table_PersonalRepresentatives .selcol+ td').css('::text').extract()
        personal_representatives_address = response.css('#table_PersonalRepresentatives td:nth-child(4)').extract()

        attorny_url = response.css('#table_PersonalRepresentatives a').xpath('@ng-click').extract_first()
        personal_representatives1 = ''
        personal_representatives_address1 = ''
        personal_representatives2 = ''
        personal_representatives_address2 = ''
        # if personal_representatives:
        #     personal_representatives1 = personal_representatives[0]
        #     personal_representatives_address1 = personal_representatives_address[0].replace('</td>', '').replace('<td>', '').replace('<br>', ', ').title()
        # if len(personal_representatives) > 1:
        #     personal_representatives2 = personal_representatives[0]
        #     personal_representatives_address2 = personal_representatives_address[0].replace('</td>', '').replace('<td>', '').replace('<br>', ', ').title()

        for i in range(len(personal_representatives)):
            if personal_representatives_address[i]:
                personal_representatives1 = personal_representatives[i]
                personal_representatives_address1 = personal_representatives_address[i].replace('</td>', '').replace('<td>', '').replace('<br>', ', ').title()
                break

       
        for i in range(1, len(personal_representatives)):
            if personal_representatives_address[i] and personal_representatives[i] != personal_representatives1:
                personal_representatives2 = personal_representatives[i]
                personal_representatives_address2 = personal_representatives_address[i].replace('</td>', '').replace('<td>', '').replace('<br>', ', ').title()
                break

       
        if not personal_representatives_address1 and len(personal_representatives) > 0:
            personal_representatives1 = personal_representatives[0]
            personal_representatives_address1 = personal_representatives_address[0].replace('</td>', '').replace('<td>', '').replace('<br>', ', ').title()

        if not personal_representatives_address2 and len(personal_representatives) > 1 and personal_representatives[1] != personal_representatives1:
            personal_representatives2 = personal_representatives[1]
            personal_representatives_address2 = personal_representatives_address[1].replace('</td>', '').replace('<td>', '').replace('<br>', ', ').title()


        try:
            response = HtmlResponse(url='about:blank', body=data['Relates'][2].encode('utf-8'))
        except:
            pass
        relatives = response.css('#table_InterestedParties .selcol+ td').css('::text').extract()
        if not personal_representatives1 and not relatives:
            response = HtmlResponse(url='about:blank', body=data['Relates'][1].encode('utf-8'))
            relatives = response.css('#table_InterestedParties .selcol+ td').css('::text').extract()
        relatives_address = response.css('#table_InterestedParties td:nth-child(3)').css("::text").extract()

        if not personal_representatives1:
            if relatives:
                personal_representatives1 = relatives.pop(0)
                personal_representatives_address1 = relatives_address.pop(0) if relatives_address else ''

                
        if not attorny_url:
            attorny_url = response.css('#table_InterestedParties a').xpath('@ng-click').extract_first()

        if decedent:
            my_data['Decedent_Full_Name'] = decedent.title()
            
            
            try:
                decedent_parsed_name = name_parser.split_name(decedent)
                my_data['Decedent_First_Name'] = decedent_parsed_name['first_name']
                if 'middle_name' in decedent_parsed_name:
                    my_data['Decedent_Middle_Name'] = decedent_parsed_name['middle_name']
                my_data['Decedent_Last_Name'] = decedent_parsed_name['last_name']
                my_data['Decedent_Suffix'] = decedent_parsed_name['suffix']
            except:
                pass
        else:
            my_data['Decedent_First Name'] = ''
            my_data['Decedent_Middle Name'] = ''
            my_data['Decedent_Last Name'] = ''
            my_data['Decedent_Suffix'] = ''

        my_data['DOD'] = date_of_death
        my_data['DOB'] = date_of_birth
        decedent_address = (' '.join(decedent_address)).title()
        
        try:
            if "Confidential" in decedent_address:
                decedent_address = ""
            parsed_decedent_address = parser.lf_address_parser(decedent_address)
            my_data['Decedent_Address'] = (parsed_decedent_address["address1"] + ' ' + parsed_decedent_address["unit"]).replace('.', '').strip()
            my_data['Decedent_City'] = parsed_decedent_address["city"].title()
            my_data['Decedent_State'] = parsed_decedent_address["state"].upper()
            my_data['Decedent_Zip'] = parsed_decedent_address["zip_code"]
        except:
            pass
        my_data['Decedent_Zip'] = process_zip_code(my_data['Decedent_Zip'])


        pattern = r'\([^)]*\)'
        result1 = re.sub(pattern, '', personal_representatives1)
        personal_representatives1 = result1.strip()
        personal_representatives1 = personal_representatives1.replace("ESQ", "").strip()
        my_data['Petitioner1_Full_Name'] = personal_representatives1.title()
        if personal_representatives1:
            
            try:
                personal_representatives1_parsed_name = name_parser.split_name(personal_representatives1)
                my_data['Petitioner1_First_Name'] = personal_representatives1_parsed_name['first_name']
                if 'middle_name' in personal_representatives1_parsed_name:
                    my_data['Petitioner1_Middle_Name'] = personal_representatives1_parsed_name['middle_name']
                my_data['Petitioner1_Last_Name'] = personal_representatives1_parsed_name['last_name']
                my_data['Petitioner1_Suffix'] = personal_representatives1_parsed_name['suffix']
            except:
                pass
        else:
            my_data['Petitioner1_First_Name'] = ''
            my_data['Petitioner1_Middle_Name'] = ''
            my_data['Petitioner1_Last_Name'] = ''
            my_data['Petitioner1_Suffix'] = ''

        if "Confidential" in personal_representatives_address1:
                personal_representatives_address1 = ""
        try:        
            parsed_personal_representatives1_address = parser.lf_address_parser(personal_representatives_address1)
            my_data['Petitioner1_Address'] = (parsed_personal_representatives1_address["address1"] + ' ' + parsed_personal_representatives1_address["unit"]).replace('.', '').strip()
            my_data['Petitioner1_City'] = parsed_personal_representatives1_address["city"].title()
            my_data['Petitioner1_State'] = parsed_personal_representatives1_address["state"].upper()
            my_data['Petitioner1_Zip'] = parsed_personal_representatives1_address["zip_code"]
        except:      
            pass
        my_data['Petitioner1_Zip'] = process_zip_code(my_data['Petitioner1_Zip'])

        pattern = r'\([^)]*\)'
        result2 = re.sub(pattern, '', personal_representatives2)
        personal_representatives2 = result2.strip()
        personal_representatives2 = personal_representatives2.replace("ESQ", "").strip()
        my_data['Petitioner2_Full_Name'] = personal_representatives2.title()
        if personal_representatives2:
            try:
                personal_representatives2_parsed_name = name_parser.split_name(personal_representatives2)
                my_data['Petitioner2_First_Name'] = personal_representatives2_parsed_name['first_name']
                if 'middle_name' in personal_representatives2_parsed_name:
                    my_data['Petitioner2_Middle_Name'] = personal_representatives2_parsed_name['middle_name']
                my_data['Petitioner2_Last_Name'] = personal_representatives2_parsed_name['last_name']
                my_data['Petitioner2_Suffix'] = personal_representatives2_parsed_name['suffix']
            except:
                pass
        else:
            my_data['Petitioner2_First_Name'] = ''
            my_data['Petitioner2_Middle_Name'] = ''
            my_data['Petitioner2_Last_Name'] = ''
            my_data['Petitioner2_Suffix'] = ''


        if "Confidential" in personal_representatives_address2:
            personal_representatives_address2 = ""

        
        try:
            parsed_personal_representatives2_address = parser.lf_address_parser(personal_representatives_address2)
            my_data['Petitioner2_Address'] = (parsed_personal_representatives2_address["address1"] + ' ' + parsed_personal_representatives2_address["unit"]).replace('.', '').strip()
            my_data['Petitioner2_City'] = parsed_personal_representatives2_address["city"].title()
            my_data['Petitioner2_State'] = parsed_personal_representatives2_address["state"].upper()
            my_data['Petitioner2_Zip'] = parsed_personal_representatives2_address["zip_code"]
        except:
            pass
        my_data['Petitioner2_Zip'] = process_zip_code(my_data['Petitioner2_Zip'])
        
        i = 1
        for index, (person, address) in enumerate(zip(relatives, relatives_address)):
            if personal_representatives1 != person and personal_representatives2 != person:
                pattern = r'\([^)]*\)'
                result3 = re.sub(pattern, '', person)
                person = result3.strip()
                person = person.replace("ESQ", "").strip()
                my_data_key = 'Relatives' + str(i) + '_Full_Name'
                if my_data_key in my_data:
                    my_data[my_data_key] = person.title()
                    address = address.title()

                    if "Confidential" in address:
                        address = ""

                    try:
                        parsed_address = parser.lf_address_parser(address)
                        my_data['Relatives' + str(i) + '_Address'] = (parsed_address["address1"] + ' ' + parsed_address["unit"]).replace('.', '').strip()
                        my_data['Relatives' + str(i) + '_City'] = parsed_address["city"].title()
                        my_data['Relatives' + str(i) + '_State'] = parsed_address["state"].upper()
                        my_data['Relatives' + str(i) + '_Zip'] = parsed_address["zip_code"]
                        
                    except:
                        pass
                    my_data['Relatives' + str(i) + '_Zip'] = process_zip_code(my_data['Relatives' + str(i) + '_Zip'])

                    try:
                        parsed_person = name_parser.split_name(person)
                        my_data['Relatives' + str(i) + '_First_Name'] = parsed_person['first_name']
                        if 'middle_name' in parsed_person:
                            my_data['Relatives' + str(i) + '_Middle_Name'] = parsed_person['middle_name']
                        my_data['Relatives' + str(i) + '_Last_Name'] = parsed_person['last_name']
                        my_data['Relatives' + str(i) + '_Suffix'] = parsed_person['suffix']
                    except:
                        pass
                    i = i + 1
                else:
                    break





        # i = 1
        # seen_entries = set()
        # for index, (person, address) in enumerate(zip(relatives, relatives_address)):
        #     if personal_representatives1 != person and personal_representatives2 != person:
        #         pattern = r'\([^)]*\)'
        #         result3 = re.sub(pattern, '', person)
        #         person = result3.strip()
        #         person = person.replace("ESQ", "").strip()
        #         if (person, address) not in seen_entries:
        #             seen_entries.add((person, address))
        #             my_data['Relatives' + str(i) + '_Full_Name'] = person.title()
        #             address = address.title()

        #             if "Confidential" in address:
        #                 address = ""
        #             try:
        #                 parsed_address = parser.lf_address_parser(address)
        #                 # print(address, parsed_address)
        #                 my_data['Relatives' + str(i) + '_Address'] = (parsed_address["address1"] + ' ' + parsed_address["unit"]).replace('.', '').strip()
        #                 my_data['Relatives' + str(i) + '_City'] = parsed_address["city"].title()
        #                 my_data['Relatives' + str(i) + '_State'] = parsed_address["state"].upper()
        #                 my_data['Relatives' + str(i) + '_Zip'] = parsed_address["zip_code"]
        #                 my_data['Relatives' + str(i) + '_Zip'] = my_data['Relatives' + str(i) + '_Zip'].astype(str)
        #                 my_data['Relatives' + str(i) + '_Zip'] = my_data['Relatives' + str(i) + '_Zip'].apply(process_zip_code)
        #             except:
        #                 pass

                    
        #             try:
        #                 parsed_person = name_parser.split_name(person)
        #                 my_data['Relatives' + str(i) + '_First_Name'] = parsed_person['first_name']
        #                 if 'middle_name' in parsed_person:
        #                     my_data['Relatives' + str(i) + '_Middle_Name'] = parsed_person['middle_name']
        #                 my_data['Relatives' + str(i) + '_Last_Name'] = parsed_person['last_name']
        #                 my_data['Relatives' + str(i) + '_Suffix'] = parsed_person['suffix']
        #             except:
        #                 pass
        #             i = i + 1
     
        if attorny_url:
            attorny_url = attorny_url.replace("select('", '').replace("'", '').replace(")", '')
            # print(url)
            # print(attorny_url, '***********************')

            PrLink = attorny_url.split(', ')[0]
            PrId = attorny_url.split(', ')[1]
            url = 'https://courtsapp.montcopa.org/psi3/v/detail/' + PrLink + '/' + PrId + '/data'
            payload = json.dumps({})
            yield scrapy.FormRequest(url=url, callback=self.case_attorny, meta=my_data, method='POST',
                                     headers=self.headers, body=payload)
        else:
            my_data.pop("depth", None)
            my_data.pop("proxy", None)
            my_data.pop("download_slot", None)
            my_data.pop("download_timeout", None)
            my_data.pop("download_latency", None)
            yield my_data

    def case_attorny(self, response):
        data = response.json()
        my_data = response.meta

        attorney_first_name = ''
        attorney_middle_name = ''
        attorney_last_name = ''
        attorney_suffix = ''

        attorney_add = ''
        attorney_city = ''
        attorney_state = ''
        attorney_zip = ''

        # print(data)
        try:
            response = HtmlResponse(url='about:blank', body=data['Relates'][0].encode('utf-8'))

            attorney_name = response.css('#table_Attorneys .selcol+ td').css('::text').extract_first()
            if attorney_name:
                pattern = r'\([^)]*\)'
                result4 = re.sub(pattern, '', attorney_name)
                attorney_name = result4.strip()
                attorney_name = attorney_name.replace("ESQ", "").strip()
                attorney_parsed_name = name_parser.split_name(attorney_name)
                try:
                    attorney_parsed_name = name_parser.split_name(attorney_name)
                    attorney_first_name = attorney_parsed_name['first_name']
                    if 'middle_name' in attorney_parsed_name:
                        attorney_middle_name = attorney_parsed_name['middle_name']
                    attorney_last_name = attorney_parsed_name['last_name']
                    attorney_suffix = attorney_parsed_name['suffix']
                except:
                    pass

            attorney_address = response.css('#table_Attorneys td:nth-child(3)').css('::text').extract()
            if "Confidential" in attorney_address:
                    attorney_address = ""
            try:
                attorney_address = ' '.join(attorney_address).title()
                parsed_attorney_address = parser.lf_address_parser(attorney_address)
                attorney_add = (parsed_attorney_address["address1"] + ' ' + parsed_attorney_address["unit"]).replace('.', '').strip()
                attorney_city = parsed_attorney_address["city"].title()
                attorney_state = parsed_attorney_address["state"].upper()
                attorney_zip = parsed_attorney_address["zip_code"]
            except:
                pass
        except:
            attorney_name = ''
            attorney_address = ''
        my_data["Attorney1_Full_Name"] = attorney_name
        my_data["Attorney1_First_Name"] = attorney_first_name
        my_data["Attorney1_Middle_Name"] = attorney_middle_name
        my_data["Attorney1_Last_Name"] = attorney_last_name
        my_data["Attorney1_Suffix"] = attorney_suffix

        # my_data['attorney_full_address'] = attorney_address
        my_data['Attorney1_Address'] = attorney_add
        my_data['Attorney1_City'] = attorney_city
        my_data['Attorney1_State'] = attorney_state
        my_data['Attorney1_Zip'] = attorney_zip
        my_data['Attorney1_Zip'] = process_zip_code(my_data['Attorney1_Zip'])


        # cleaning the metadata
        my_data.pop("depth", None)
        my_data.pop("proxy", None)
        my_data.pop("download_slot", None)
        my_data.pop("download_timeout", None)
        my_data.pop("download_latency", None)

        yield my_data

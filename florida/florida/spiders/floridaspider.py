from datetime import datetime
from email.quoprimime import unquote
import re
import scrapy
from lf_library.name_parser.name_parser_n import split_name
# from lf_library.oa.Probate import Probate
from dotenv import load_dotenv
import os

# probate = Probate()

class FloridaspiderSpider(scrapy.Spider):
    name = "floridaspider"
    def __init__(self, *args, **kwargs):
        super(FloridaspiderSpider, self).__init__(*args, **kwargs)
        self.datefrom_str = kwargs.get('datefrom_str')
        self.dateto_str = kwargs.get('dateto_str')

    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        }
    cookies = {
            'SERVERID': 'SA',
            '__utma': '236543645.1408365906.1700820555.1700820555.1700820555.1',
            '__utmc': '236543645',
            '__utmz': '236543645.1700820555.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
            '__utmt': '1',
            '__utmb': '236543645.3.10.1700820555',
            'JSESSIONID': '0000VxsV0jsJAmLc4gbqZW5LPJ7:16i5lbk94',
        }
    
    def start_requests(self):
       url = "https://www.myfloridacounty.com/ori/index.do"
       yield scrapy.Request(url=url,callback=self.parse,
                            cookies=self.cookies,
                            headers=self.headers)
    def parse(self, response):
        url = "https://www.myfloridacounty.com/ori/search.do"
        form_data = {
            'nametype': 'i',
            'lastName': 'last',
            'firstName': 'first',
            'businessName': 'business',
            'locationType': 'COUNTY',
            'county': '04',
            'circuit': '500',
            'region': '500',
            'documentTypes': 'PRO',
            'percisesearchtype': 'i',
            'instrumentNumber': '',
            'book': 'Book',
            'page': 'Page',
            'x': '94',
            'y': '24',
        }

       
        if self.datefrom_str and self.dateto_str:
            start_month, start_day, start_year = map(int, self.datefrom_str.split('-'))
            end_month, end_day, end_year = map(int, self.dateto_str.split('-'))
            form_data.update({
                'startMonth': str(start_day),
                'startDay': str(start_year),
                'startYear': str(start_month),
                'endMonth': str(end_day),
                'endDay': str(end_year),
                'endYear': str(end_month),
            })
            
       
        yield scrapy.FormRequest(url=url, callback=self.parcel_page,
                                        formdata=form_data,
                                        cookies=self.cookies,
                                        headers=self.headers)

        # url = "https://www.myfloridacounty.com/ori/search.do"
        # form_data = {
        #     'nametype': 'i',
        #     'lastName': 'last',
        #     'firstName': 'first',
        #     'businessName': 'business',
        #     'locationType': 'COUNTY',
        #     'county': '04',
        #     'circuit': '500',
        #     'region': '500',
        #     'documentTypes': 'PRO',
        #     'startMonth': '1',
        #     'startDay': '2',
        #     'startYear': '2023',
        #     'endMonth': '5',
        #     'endDay': '6',
        #     'endYear': '2023',
        #     'percisesearchtype': 'i',
        #     'instrumentNumber': '',
        #     'book': 'Book',
        #     'page': 'Page',
        #     'x': '94',
        #     'y': '24',
        # }

        # yield scrapy.FormRequest(url=url, callback=self.parcel_page,
        #                                 formdata=form_data,
        #                                 cookies=self.cookies,
        #                                 headers=self.headers)

    def parcel_page(self, response):
        rows = response.css('tbody tr')
        for row in rows:
            patitinor1 = ''
            patitinor2 = ''

            decedent = row.css('td:nth-child(2)::text').get()
            if decedent:    
                decedent = str(decedent)
                decedent = decedent.replace("('", "").strip()
                decedent = decedent.replace("',)", "").strip()
                decedent = decedent.replace("STATE OF FLORIDA", "").strip()
                decedent_list = decedent.split(',')
                decedent = decedent_list.pop(0)
                # decedent = decedent.title()
                

            patitinors = row.css('td:nth-child(3)::text').get()
            if patitinors:    
                patitinors = str(patitinors)
                patitinors = patitinors.replace("('", "").strip()
                patitinors = patitinors.replace("',)", "").strip()
                patitinors = patitinors.split(',')
                # Remove duplicates and strip spaces
                patitinors = list(set(patitinors))
                patitinors = [name.strip() for name in patitinors]

                # Remove decedent from the list
                patitinors = [name for name in patitinors if name != decedent]

                # Assign values to patitinor1 and patitinor2
                patitinor1 = patitinors[0] if patitinors else ""
                patitinor2 = patitinors[1] if len(patitinors) > 1 else ""

            decedent_list = [name.strip() for name in decedent_list]
            if patitinor1 in decedent_list:
                decedent_list.remove(patitinor1)

            if patitinor2 in decedent_list:
                decedent_list.remove(patitinor2)
            

            # Assign names from decedent_list to relative1, relative2, etc.
            relative1 = decedent_list[0].strip() if len(decedent_list) > 0 else ''
            relative2 = decedent_list[1].strip() if len(decedent_list) > 1 else ''
            relative3 = decedent_list[2].strip() if len(decedent_list) > 2 else ''
            relative4 = decedent_list[3].strip() if len(decedent_list) > 3 else ''
            relative5 = decedent_list[4].strip() if len(decedent_list) > 4 else ''





            filling_date = row.css('td:nth-child(4)::text').get(),
            if filling_date:    
                filling_date = str(filling_date)
                filling_date = filling_date.replace("('", "").strip()
                filling_date = filling_date.replace("',)", "").strip()
                date_object = datetime.strptime(filling_date, "%m/%d/%Y")
                filling_date = date_object.strftime("%Y-%m-%d")
            type = row.css('td:nth-child(5)::text').get(),
            if type:
                type = str(type)
                type = type.replace("('", "").strip()
                type = type.replace("',)", "").strip()
            county = row.css('td:nth-child(6)::text').get(),
            if county:
                county = str(county)
                county = county.replace("('", "").strip()
                county = county.replace("',)", "").strip()
          
            case_title = row.css('td:nth-child(10)::text').get(),
            if case_title:    
                case_title = str(case_title)
                case_title = case_title.replace("('", "").strip()
                case_title = case_title.replace("',)", "").strip()

            case_no = row.css('td:nth-child(10)::text').get(),
            if case_no:    
                case_no = str(case_no)
                case_no = case_no.replace("('", "").strip()
                case_no = case_no.replace("',)", "").strip()
                pattern = re.compile(r'\b\d{1,4}-\d{1,4} [A-Z]{2}\b')
                case_no = pattern.findall(case_no)
                case_no = ''.join(case_no).replace("['", "").strip()
                case_no = ''.join(case_no).replace("']", "").strip()

            
            my_data = {
            "State": "FL",
            "Address":"",
            "County": county,
            "City": "",
            "Zip": "",
            "Status": "",
            "Filing_Date": filling_date,
            "Case_Number": case_no,
            "Case_Title": case_title,
            "Case_Type": type,
            "DOB": "",
            "DOD": "",
            "Age": "",
            "Decedent_Full_Name": decedent,
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
            "Petitioner1_Full_Name": patitinor1,
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
            "Petitioner2_Full_Name": patitinor2,
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
            
            
            if decedent:
                original_name = decedent
                decedent = ' '.join(original_name.split())
                my_data['Decedent_Full_Name'] = decedent.title()
                my_data['Decedent_Full_Name'] = my_data['Decedent_Full_Name'].replace("Vystar Credit Union", "").strip()
                my_data['Decedent_Full_Name'] = my_data['Decedent_Full_Name'].replace("Public Guardianship Office", "").strip()
                my_data['Decedent_Full_Name'] = my_data['Decedent_Full_Name'].replace("Estate Of Martha Jean Hodge", "").strip()
                my_data['Decedent_Full_Name'] = my_data['Decedent_Full_Name'].replace("Revocable Living Trust", "").strip()
                my_data['Decedent_Full_Name'] = my_data['Decedent_Full_Name'].replace("Riverwood Health And Rehab", "").strip()
                decedent_name_full_name_for_parser = my_data['Decedent_Full_Name']
                try:
                    decedent_d1 = split_name(decedent_name_full_name_for_parser, 'LFM')
                    my_data['Decedent_First_Name'] = decedent_d1['first_name'] if decedent_d1['first_name'] else None
                    if len(decedent_d1['initials']) > 0:
                        decedent_d1['initials'] = decedent_d1['initials'][0]
                    else:
                        decedent_d1['initials'] = None
                    my_data['Decedent_Middle_Name'] = decedent_d1['middle_name'] if decedent_d1['middle_name'] else decedent_d1['initials']
                    my_data['Decedent_Last_Name'] = decedent_d1['last_name'] if decedent_d1['last_name'] else None
                    my_data['Decedent_Suffix'] = decedent_d1['suffix'] if decedent_d1['suffix'] else None       
                except:
                    # my_data['Decedent_First_Name'] = my_data['Decedent_Middle_Name'] = my_data['Decedent_Last_Name'] = my_data['Decedent_Suffix']
                    pass


            
            if patitinor1:
                patitinor1 = patitinor1
                patitinor1 = ' '.join(patitinor1.split())
                my_data['Petitioner1_Full_Name'] = patitinor1.title()
                my_data['Petitioner1_Full_Name'] = my_data['Petitioner1_Full_Name'].replace("Public Guardianship Office", "").strip()
                my_data['Petitioner1_Full_Name'] = my_data['Petitioner1_Full_Name'].replace("Estate Of Martha Jean Hodge", "").strip()
                my_data['Petitioner1_Full_Name'] = my_data['Petitioner1_Full_Name'].replace("Revocable Living Trust", "").strip()
                my_data['Petitioner1_Full_Name'] = my_data['Petitioner1_Full_Name'].replace("Riverwood Health And Rehab", "").strip()
                my_data['Petitioner1_Full_Name'] = my_data['Petitioner1_Full_Name'].replace("Vystar Credit Union", "").strip()
                petitioner1_name_full_name_for_parser = my_data['Petitioner1_Full_Name']
                try:
                    result_p1 = split_name(petitioner1_name_full_name_for_parser, 'LFM')
                    my_data['Petitioner1_First_Name'] = result_p1['first_name'] if result_p1['first_name'] else None
                    if len(result_p1['initials']) > 0:
                        result_p1['initials'] = result_p1['initials'][0]
                    else:
                        result_p1['initials'] = None
                    my_data['Petitioner1_Middle_Name']  = result_p1['middle_name'] if result_p1['middle_name'] else result_p1['initials']
                    my_data['Petitioner1_Last_Name'] = result_p1['last_name'] if result_p1['last_name'] else None
                    my_data['Petitioner1_Suffix']  = result_p1['suffix'] if result_p1['suffix'] else None
                except:
                    pass

            if patitinor2:
                patitinor2 = patitinor2
                patitinor2 = ' '.join(patitinor2.split())
                my_data['Petitioner2_Full_Name'] = patitinor2.title()
                my_data['Petitioner2_Full_Name'] = my_data['Petitioner2_Full_Name'].replace("Public Guardianship Office", "").strip()
                my_data['Petitioner2_Full_Name'] = my_data['Petitioner2_Full_Name'].replace("Estate Of Martha Jean Hodge", "").strip()
                my_data['Petitioner2_Full_Name'] = my_data['Petitioner2_Full_Name'].replace("Revocable Living Trust", "").strip()
                my_data['Petitioner2_Full_Name'] = my_data['Petitioner2_Full_Name'].replace("Riverwood Health And Rehab", "").strip()
                my_data['Petitioner2_Full_Name'] = my_data['Petitioner2_Full_Name'].replace("Vystar Credit Union", "").strip()
                petitioner2_name_full_name_for_parser = my_data['Petitioner2_Full_Name']
                try:
                    result_p2 = split_name(petitioner2_name_full_name_for_parser, 'LFM')
                    my_data['Petitioner2_First_Name'] = result_p2['first_name'] if result_p2['first_name'] else None
                    if len(result_p2['initials']) > 0:
                        result_p2['initials'] = result_p2['initials'][0]
                    else:
                        result_p2['initials'] = None
                    my_data['Petitioner2_Middle_Name']  = result_p2['middle_name'] if result_p2['middle_name'] else result_p2['initials']
                    my_data['Petitioner2_Last_Name'] = result_p2['last_name'] if result_p2['last_name'] else None
                    my_data['Petitioner2_Suffix']  = result_p2['suffix'] if result_p2['suffix'] else None
                except:
                    pass
            else:
                patitinor2 = ''


            if relative1:
                relative1 = relative1
                relative1 = ' '.join(relative1.split())
                my_data['Relatives1_Full_Name'] = relative1.title()
                my_data['Relatives1_Full_Name'] = my_data['Relatives1_Full_Name'].replace("Public Guardianship Office", "").strip()
                my_data['Relatives1_Full_Name'] = my_data['Relatives1_Full_Name'].replace("Estate Of Martha Jean Hodge", "").strip()
                my_data['Relatives1_Full_Name'] = my_data['Relatives1_Full_Name'].replace("Revocable Living Trust", "").strip()
                my_data['Relatives1_Full_Name'] = my_data['Relatives1_Full_Name'].replace("Riverwood Health And Rehab", "").strip()
                my_data['Relatives1_Full_Name'] = my_data['Relatives1_Full_Name'].replace("Vystar Credit Union", "").strip()
                relative1_name_full_name_for_parser = my_data['Relatives1_Full_Name']
                try:
                    result_r1 = split_name(relative1_name_full_name_for_parser, 'LFM')
                    my_data['Relatives1_First_Name'] = result_r1['first_name'] if result_r1['first_name'] else None
                    if len(result_r1['initials']) > 0:
                        result_r1['initials'] = result_r1['initials'][0]
                    else:
                        result_r1['initials'] = None
                    my_data['Relatives1_Middle_Name']  = result_r1['middle_name'] if result_r1['middle_name'] else result_r1['initials']
                    my_data['Relatives1_Last_Name'] = result_r1['last_name'] if result_r1['last_name'] else None
                    my_data['Relatives1_Suffix']  = result_r1['suffix'] if result_r1['suffix'] else None
                except:
                    pass
            

            if relative2:
                relative2 = relative2
                relative2 = ' '.join(relative2.split())
                my_data['Relatives2_Full_Name'] = relative2.title()
                my_data['Relatives2_Full_Name'] = my_data['Relatives2_Full_Name'].replace("Public Guardianship Office", "").strip()
                my_data['Relatives2_Full_Name'] = my_data['Relatives2_Full_Name'].replace("Estate Of Martha Jean Hodge", "").strip()
                my_data['Relatives2_Full_Name'] = my_data['Relatives2_Full_Name'].replace("Revocable Living Trust", "").strip()
                my_data['Relatives2_Full_Name'] = my_data['Relatives2_Full_Name'].replace("Riverwood Health And Rehab", "").strip()
                my_data['Relatives2_Full_Name'] = my_data['Relatives2_Full_Name'].replace("Vystar Credit Union", "").strip()
                relative2_name_full_name_for_parser = my_data['Relatives2_Full_Name']
                try:
                    result_d2 = split_name(relative2_name_full_name_for_parser, 'LFM')
                    my_data['Relatives2_First_Name'] = result_d2['first_name'] if result_d2['first_name'] else None
                    if len(result_d2['initials']) > 0:
                        result_d2['initials'] = result_d2['initials'][0]
                    else:
                        result_d2['initials'] = None
                    my_data['Relatives2_Middle_Name']  = result_d2['middle_name'] if result_d2['middle_name'] else result_d2['initials']
                    my_data['Relatives2_Last_Name'] = result_d2['last_name'] if result_d2['last_name'] else None
                    my_data['Relatives2_Suffix']  = result_d2['suffix'] if result_d2['suffix'] else None
                except:
                    pass
           

            if relative3:
                relative3 = relative3
                relative3 = ' '.join(relative3.split())
                my_data['Relatives3_Full_Name'] = relative3.title()
                my_data['Relatives3_Full_Name'] = my_data['Relatives3_Full_Name'].replace("Public Guardianship Office", "").strip()
                my_data['Relatives3_Full_Name'] = my_data['Relatives3_Full_Name'].replace("Estate Of Martha Jean Hodge", "").strip()
                my_data['Relatives3_Full_Name'] = my_data['Relatives3_Full_Name'].replace("Revocable Living Trust", "").strip()
                my_data['Relatives3_Full_Name'] = my_data['Relatives3_Full_Name'].replace("Riverwood Health And Rehab", "").strip()
                my_data['Relatives3_Full_Name'] = my_data['Relatives3_Full_Name'].replace("Vystar Credit Union", "").strip()
                relative3_name_full_name_for_parser = my_data['Relatives3_Full_Name']
                try:
                    result_d3 = split_name(relative3_name_full_name_for_parser, 'LFM')
                    my_data['Relatives3_First_Name'] = result_d3['first_name'] if result_d3['first_name'] else None
                    if len(result_d3['initials']) > 0:
                        result_d3['initials'] = result_d3['initials'][0]
                    else:
                        result_d3['initials'] = None
                    my_data['Relatives3_Middle_Name']  = result_d3['middle_name'] if result_d3['middle_name'] else result_d3['initials']
                    my_data['Relatives3_Last_Name'] = result_d3['last_name'] if result_d3['last_name'] else None
                    my_data['Relatives3_Suffix']  = result_d3['suffix'] if result_d3['suffix'] else None
                except:
                    pass
            
            if relative4:
                relative4 = relative4
                relative4 = ' '.join(relative4.split())
                my_data['Relatives4_Full_Name'] = relative4.title()
                my_data['Relatives4_Full_Name'] = my_data['Relatives4_Full_Name'].replace("Public Guardianship Office", "").strip()
                my_data['Relatives4_Full_Name'] = my_data['Relatives4_Full_Name'].replace("Estate Of Martha Jean Hodge", "").strip()
                my_data['Relatives4_Full_Name'] = my_data['Relatives4_Full_Name'].replace("Revocable Living Trust", "").strip()
                my_data['Relatives4_Full_Name'] = my_data['Relatives4_Full_Name'].replace("Riverwood Health And Rehab", "").strip()
                my_data['Relatives4_Full_Name'] = my_data['Relatives4_Full_Name'].replace("Vystar Credit Union", "").strip()
                relative4_name_full_name_for_parser = my_data['Relatives4_Full_Name']
                try:
                    result_d4 = split_name(relative4_name_full_name_for_parser, 'LFM')
                    my_data['Relatives4_First_Name'] = result_d4['first_name'] if result_d4['first_name'] else None
                    if len(result_d4['initials']) > 0:
                        result_d4['initials'] = result_d4['initials'][0]
                    else:
                        result_d4['initials'] = None
                    my_data['Relatives4_Middle_Name']  = result_d4['middle_name'] if result_d4['middle_name'] else result_d4['initials']
                    my_data['Relatives4_Last_Name'] = result_d4['last_name'] if result_d4['last_name'] else None
                    my_data['Relatives4_Suffix']  = result_d4['suffix'] if result_d4['suffix'] else None
                except:
                    pass


            if relative5:
                relative5 = relative5
                relative5 = ' '.join(relative5.split())
                my_data['Relatives5_Full_Name'] = relative5.title()
                my_data['Relatives5_Full_Name'] = my_data['Relatives5_Full_Name'].replace("Public Guardianship Office", "").strip()
                my_data['Relatives5_Full_Name'] = my_data['Relatives5_Full_Name'].replace("Estate Of Martha Jean Hodge", "").strip()
                my_data['Relatives5_Full_Name'] = my_data['Relatives5_Full_Name'].replace("Revocable Living Trust", "").strip()
                my_data['Relatives5_Full_Name'] = my_data['Relatives5_Full_Name'].replace("Riverwood Health And Rehab", "").strip()
                my_data['Relatives5_Full_Name'] = my_data['Relatives5_Full_Name'].replace("Vystar Credit Union", "").strip()
                relative5_name_full_name_for_parser = my_data['Relatives5_Full_Name']
                try:
                    result_d5 = split_name(relative5_name_full_name_for_parser, 'LFM')
                    my_data['Relatives5_First_Name'] = result_d5['first_name'] if result_d5['first_name'] else None
                    if len(result_d5['initials']) > 0:
                        result_d5['initials'] = result_d5['initials'][0]
                    else:
                        result_d5['initials'] = None
                    my_data['Relatives5_Middle_Name']  = result_d5['middle_name'] if result_d5['middle_name'] else result_d5['initials']
                    my_data['Relatives5_Last_Name'] = result_d5['last_name'] if result_d5['last_name'] else None
                    my_data['Relatives5_Suffix']  = result_d5['suffix'] if result_d5['suffix'] else None
                except:
                    pass
                


            # yield probate.insert(my_data)
            yield my_data




        links = response.css('span.pagelinks a::attr(href)').extract()
       
        for link in links:
            if link:     
                region_match = re.search(r"{f:'region',v:\['(.*?)'\]}", link)
                region = region_match.group(1) if region_match else None

                last_name_match = re.search(r"{f:'lastName',v:\['(.*?)'\]}", link)
                last_name = last_name_match.group(1) if last_name_match else None

                business_name_match = re.search(r"{f:'businessName',v:\['(.*?)'\]}", link)
                business_name = business_name_match.group(1) if business_name_match else None

                end_year_match = re.search(r"{f:'endYear',v:\['(.*?)'\]}", link)
                end_year = end_year_match.group(1) if end_year_match else None

                nametype_match = re.search(r"{f:'nametype',v:\['(.*?)'\]}", link)
                nametype = nametype_match.group(1) if nametype_match else None

                end_day_match = re.search(r"{f:'endDay',v:\['(.*?)'\]}", link)
                end_day = end_day_match.group(1) if end_day_match else None

                document_types_match = re.search(r"{f:'documentTypes',v:\['(.*?)'\]}", link)
                document_types = document_types_match.group(1) if document_types_match else None

                instrument_number_match = re.search(r"{f:'instrumentNumber',v:\['(.*?)'\]}", link)
                instrument_number = instrument_number_match.group(1) if instrument_number_match else None

                county_match = re.search(r"{f:'county',v:\['(.*?)'\]}", link)
                county = county_match.group(1) if county_match else None
    
                start_year_match = re.search(r"{f:'startYear',v:\['(.*?)'\]}", link)
                start_year = start_year_match.group(1) if start_year_match else None
      
                page_match = re.search(r"{f:'page',v:\['(.*?)'\]}", link)
                page = page_match.group(1) if page_match else None

                start_day_match = re.search(r"{f:'startDay',v:\['(.*?)'\]}", link)
                start_day = start_day_match.group(1) if start_day_match else None

                location_type_match = re.search(r"{f:'locationType',v:\['(.*?)'\]}", link)
                location_type = location_type_match.group(1) if location_type_match else None

                book_match = re.search(r"{f:'book',v:\['(.*?)'\]}", link)
                book = book_match.group(1) if book_match else None

                d_7122416_p_match = re.search(r"{f:'d-7122416-p',v:'(.*?)'}", link)
                d_7122416_p = d_7122416_p_match.group(1) if d_7122416_p_match else None
       
                circuit_match = re.search(r"{f:'circuit',v:\['(.*?)'\]}", link)
                circuit = circuit_match.group(1) if circuit_match else None
    
                start_month_match = re.search(r"{f:'startMonth',v:\['(.*?)'\]}", link)
                start_month = start_month_match.group(1) if start_month_match else None

                first_name_match = re.search(r"{f:'firstName',v:\['(.*?)'\]}", link)
                first_name = first_name_match.group(1) if first_name_match else None

                percisesearchtype_match = re.search(r"{f:'percisesearchtype',v:\['(.*?)'\]}", link)
                percisesearchtype = percisesearchtype_match.group(1) if percisesearchtype_match else None

                end_month_match = re.search(r"{f:'endMonth',v:\['(.*?)'\]}", link)
                end_month = end_month_match.group(1) if end_month_match else None

                y_match = re.search(r"{f:'y',v:\['(.*?)'\]}", link)
                y = y_match.group(1) if y_match else None

                x_match = re.search(r"{f:'x',v:\['(.*?)'\]}", link)
                x = x_match.group(1) if x_match else None

                form_data = {        
                'navigate':'display',
                'region': region,
                'businessName': business_name,
                'endDay': end_day,
                'instrumentNumber': instrument_number,
                'page': page,
                'startDay': start_day,
                'locationType': location_type,
                'firstName': first_name,
                'percisesearchtype': percisesearchtype,
                'lastName': last_name,
                'endYear': end_year,
                'nametype': nametype,
                'documentTypes': document_types,
                'county': county,
                'startYear': start_year,
                'book': book,
                'd-7122416-p': d_7122416_p,
                'd-7122416-o': '',
                'circuit': circuit,
                'startMonth': start_month,
                'd-7122416-s': '',
                'endMonth': end_month,
                'y': y,
                'x': x
                }
                
                url = 'https://www.myfloridacounty.com/ori/ordercreate.do?navigate=display'

                yield scrapy.FormRequest(url=response.url, formdata=form_data,callback=self.parcel_page)






       

        
   
      


import os
import scrapy
import re
from dotenv import load_dotenv
from datetime import datetime
from scrapy.utils.response import open_in_browser
from Maryland.lf_library.name_parser import name_parser
from Maryland.lf_library.address_parser.Address_Parser import Address_Parser  

db_config = {
  "host": "localhost",
  "user": "root",
  "password": "",
  "database": "leadfuzion"
}
parser = Address_Parser(db_config)


class CountyspiderSpider(scrapy.Spider):
    name = "county_spider"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    }
    cookies = {
        'ASP.NET_SessionId': '1p1kx1saa5jwrmynwkof5vni',
        '__gsas': 'ID=441ef773818e4fc8:T=1700563839:RT=1700563839:S=ALNI_MbIcRxeppdibLXluudeUBYkaGB4BA',
        '_ga_SQ06B8V4SF': 'GS1.1.1700563947.1.0.1700563947.0.0.0',
        '_gid': 'GA1.2.1466547849.1700563948',
        '_ga': 'GA1.1.694302899.1700477324',
        '_ga_366879341': 'GS1.1.1700563893.1.1.1700564548.0.0.0',
        '_ga_SLX0CQ3HRM': 'GS1.1.1700563821.1.1.1700564551.60.0.0',
        '_ga_LJCC9XG5J9': 'GS1.1.1700563271.2.1.1700564551.0.0.0',
    }
    
    def start_requests(self):
        url = "https://registers.maryland.gov/RowNetWeb/Estates/frmEstateSearch2.aspx"
        yield scrapy.Request(
            url=url,callback=self.parse,
            cookies=self.cookies,
            headers=self.headers
        )

    def parse(self, response):
        # View_state = response.css('#__VIEWSTATE').xpath('@value').extract_first()
        view_state = response.xpath('//input[@id="__VIEWSTATE"]/@value').get()
        view_state_gen = response.xpath('//input[@id="__VIEWSTATEGENERATOR"]/@value').get()
        event_validator = response.xpath('//input[@id="__EVENTVALIDATION"]/@value').get()
        CountyId = '1'
        DateOfFilingFrom = "10/01/2023"
        DateOfFilingTo = "10/31/2023"

        count_name = response.xpath(f"//option[@value='{CountyId}']/text()").get()
        form_data = {
            '__VIEWSTATE': view_state,
            '__VIEWSTATEGENERATOR': view_state_gen,
            '__EVENTVALIDATION' : event_validator,
            'txtEstateNo' : '',
            'txtLN': '',
            'cboCountyId' : CountyId,
            'txtFN': '',
            'txtMN': '',
            'cboStatus': '',
            'cboType' : '',
            'DateOfFilingFrom' : DateOfFilingFrom,
            'DateOfFilingTo' : DateOfFilingTo,
            'txtDOF' : '',
            'cboPartyType' : 'Decedent',
            'cmdSearch' : 'Search'
        }
        listing_url = "https://registers.maryland.gov/RowNetWeb/Estates/frmEstateSearch2.aspx"
        # url = "https://registers.maryland.gov/RowNetWeb/Estates/frmDocketImages.aspx?src=row&RecordId=1363496817"
        
        yield scrapy.FormRequest(
            url= listing_url, 
            callback= self.parcel_listing,
            formdata= form_data,
            cookies= self.cookies,
            headers= self.headers,
            meta={'county_name': count_name}
        )
    
    def parcel_listing(self, response):
        rows = response.xpath('//table[@id="dgSearchResults"]//tr')
        # remove first and last row
        for row in rows[1:-1]:
            url_detail = row.xpath('./td/a/@href').get()
            if url_detail is not None:
                url_detail = 'https://registers.maryland.gov/RowNetWeb/Estates/'+url_detail
                yield scrapy.Request(
                    url = url_detail, 
                    callback = self.parcel_page, 
                    meta= response.meta,                       
                    cookies=self.cookies,
                    headers=self.headers
                )
        
        #Paination code wil uncoment when needed
        # page_links = response.css('#dgSearchResults td[colspan] a[href*=__doPostBack]::attr(href)').getall()
        # for page_link in page_links:
        #     # print(f"Pagination start for {page_link}")
        #     View_state = response.css('#__VIEWSTATE').xpath('@value').extract_first()
        #     view_state_gen = response.css('#__VIEWSTATEGENERATOR').xpath('@value').extract_first()
        #     event_validator = response.css('#__EVENTVALIDATION').xpath('@value').extract_first()
        #     EVENTTARGET = re.search(r"__doPostBack\('([^']+)',", page_link).group(1)

        #     next_page_payload = {
        #         '__EVENTTARGET': EVENTTARGET,
        #         '__EVENTARGUMENT': '',
        #         '__VIEWSTATE': View_state,
        #         '__EVENTVALIDATION': event_validator,
        #     }

        #     yield scrapy.FormRequest(url=response.url, formdata=next_page_payload, callback=self.parcel_listing)

    def parcel_page(self, response):
        case_number = response.xpath('//span[@id="lblEstateNumber"]/text()').get()
        case_status = response.xpath('//span[@id="lblStatus"]/text()').get()
        case_type = response.xpath('//span[@id="lblType"]/text()').get()
        filing_date = response.xpath('//span[@id="lblDateOfFiling"]/text()').get()
        print(case_number, case_status, case_type, filing_date)
        decedent_full_name = response.xpath('normalize-space(//span[@id="lblName"])').get()
        decedent_full_name_aliases = response.xpath('normalize-space(//span[@id="lblAliases"]/text())').get()
        if decedent_full_name_aliases != None:
            if len(decedent_full_name) > len(decedent_full_name_aliases):
                decedent_full_name = decedent_full_name 
            else:
                decedent_full_name = decedent_full_name_aliases
        decedent_d1 = name_parser.test_parser(decedent_full_name)
        try:
            decedent_first_name = None if decedent_d1['first_name'] == "" else decedent_d1['first_name']
            decedent_middle_name = None if decedent_d1['middle_name'] == "" else decedent_d1['middle_name']
            decedent_last_name = None if decedent_d1['last_name'] == "" else decedent_d1['last_name']
            decedent_suffix = None if decedent_d1['suffix'] == "" else decedent_d1['suffix']
        except:
            decedent_first_name = None
            decedent_middle_name = None
            decedent_last_name = None
            decedent_suffix = None

        decedent_dod = response.xpath('//span[@id="lblDateOfDeath"]/text()').get()
        
        petitioner_first_name = petitioner_middle_name = petitioner_last_name = petitioner_suffix = None        
        petitioner_full_name = response.xpath('//span[@id="lblPersonalReps"]/text()').get()
        if petitioner_full_name:
            petitioner_full_name = petitioner_full_name.replace("[", "").replace("]", "").replace("ESQ", "").strip()
            petitioner_d1 = name_parser.test_parser(petitioner_full_name)
            try:
                petitioner_first_name = None if petitioner_d1['first_name'] == "" else petitioner_d1['first_name']
                petitioner_middle_name = None if petitioner_d1['middle_name'] == "" else petitioner_d1['middle_name']
                petitioner_last_name = None if petitioner_d1['last_name'] == "" else petitioner_d1['last_name']
                petitioner_suffix = None if petitioner_d1['suffix'] == "" else petitioner_d1['suffix']
            except:
                petitioner_first_name = None
                petitioner_middle_name = None
                petitioner_last_name = None
                petitioner_suffix = None

        petitioner_address = response.xpath('//span[@id="lblPersonalReps"]/small/text()').get()
        try:
            parsed_petitioner_address = parser.lf_address_parser(petitioner_address)
            petitioner_address = parsed_petitioner_address["address1"]
            petitioner_unit = parsed_petitioner_address["unit"]
            petitioner_city = parsed_petitioner_address["city"].title()
            petitioner_state = parsed_petitioner_address["state"]
            petitioner_zip = parsed_petitioner_address["zip_code"]
            if petitioner_address != "" and petitioner_unit != "": 
                petitioner_address = petitioner_address+" "+petitioner_unit
        except:
            petitioner_address = None
            petitioner_city = None
            petitioner_state = None
            petitioner_zip = None

        attorney_first_name = attorney_middle_name = attorney_last_name = attorney_suffix = None      
        attorney_full_name = response.xpath('//span[@id="lblAttorney"]/text()').get()
        if attorney_full_name:
            attorney_full_name = attorney_full_name.replace("[", "").replace("]", "").replace("ESQ", "").strip()
            attorney_d1 = name_parser.test_parser(attorney_full_name)
            try:
                attorney_first_name = None if attorney_d1['first_name'] == "" else attorney_d1['first_name']
                attorney_middle_name = None if attorney_d1['middle_name'] == "" else attorney_d1['middle_name']
                attorney_last_name = None if attorney_d1['last_name'] == "" else attorney_d1['last_name']
                attorney_suffix = None if attorney_d1['suffix'] == "" else attorney_d1['suffix']
            except:
                attorney_first_name = None
                attorney_middle_name = None
                attorney_last_name = None
                attorney_suffix = None

        attorney_address = response.xpath('//span[@id="lblAttorney"]/small/text()').get()
        try:
            parsed_attorney_address = parser.lf_address_parser(attorney_address)
            attorney_address = parsed_attorney_address["address1"]
            attorney_unit = parsed_attorney_address["unit"]
            attorney_city = parsed_attorney_address["city"].title()
            attorney_state = parsed_attorney_address["state"]
            attorney_zip = parsed_attorney_address["zip_code"]
            if attorney_address != "" and attorney_unit != "": 
                attorney_address = attorney_address+" "+attorney_unit
        except:
            attorney_address = None
            attorney_city = None
            attorney_state = None
            attorney_zip = None

        my_data = {
            "State": "MD",
            "Address":None,
            "County": response.meta['county_name'],
            "City": None,
            "Zip": None,
            "Status": case_status,
            "Filing_Date": filing_date,
            "Case_Number": str(case_number),  
            "Case_Title": None,
            "Case_Type": case_type,
            "DOB": None,
            "DOD": decedent_dod,
            "Age": None,
            "Decedent_Full_Name": decedent_full_name,
            "Decedent_First_Name": decedent_first_name,
            "Decedent_Middle_Name": decedent_middle_name,
            "Decedent_Last_Name": decedent_last_name,
            "Decedent_Suffix": decedent_suffix,
            "Decedent_Emails": None,
            "Decedent_Phones": None,
            "Decedent_Address": None,
            "Decedent_City": None,
            "Decedent_State": None,
            "Decedent_Zip":None,
            "Petitioner1_Full_Name": petitioner_full_name,
            "Petitioner1_First_Name": petitioner_first_name,
            "Petitioner1_Middle_Name": petitioner_middle_name,
            "Petitioner1_Last_Name": petitioner_last_name,
            "Petitioner1_Suffix": petitioner_suffix,
            "Petitioner1_Address": petitioner_address,
            "Petitioner1_City": petitioner_city,
            "Petitioner1_State": petitioner_state,
            "Petitioner1_Zip": petitioner_zip,
            "Petitioner1_Emails": None,
            "Petitioner1_Phones": None,
            "Petitioner2_Full_Name": None,
            "Petitioner2_First_Name": None,
            "Petitioner2_Middle_Name": None,
            "Petitioner2_Last_Name": None,
            "Petitioner2_Suffix": None,
            "Petitioner2_Address": None,
            "Petitioner2_City": None,
            "Petitioner2_State": None,
            "Petitioner2_Zip": None,
            "Petitioner2_Emails": None,
            "Petitioner2_Phones": None,
            "Attorney1_Full_Name": attorney_full_name,
            "Attorney1_First_Name": attorney_first_name,
            "Attorney1_Middle_Name": attorney_middle_name,
            "Attorney1_Last_Name": attorney_last_name,
            "Attorney1_Suffix": attorney_suffix,
            "Attorney1_Address": attorney_address,
            "Attorney1_City": attorney_city,
            "Attorney1_State": attorney_state,
            "Attorney1_Zip": attorney_zip,
            "Attorney1_Emails": None,
            "Attorney1_Phones": None,
            "Attorney2_Full_Name": None,
            "Attorney2_First_Name": None,
            "Attorney2_Middle_Name": None,
            "Attorney2_Last_Name": None,
            "Attorney2_Suffix": None,
            "Attorney2_Address": None,
            "Attorney2_City": None,
            "Attorney2_State": None,
            "Attorney2_Zip": None,
            "Attorney2_Emails": None,
            "Attorney2_Phones": None,
            "Relatives1_Full_Name": None,
            "Relatives1_First_Name": None,
            "Relatives1_Middle_Name": None,
            "Relatives1_Last_Name": None,
            "Relatives1_Suffix": None,
            "Relatives1_Emails": None,
            "Relatives1_Phones": None,
            "Relatives1_Address": None,
            "Relatives1_City": None,
            "Relatives1_State": None,
            "Relatives1_Zip": None,
            "Relatives2_Full_Name": None,
            "Relatives2_First_Name": None,
            "Relatives2_Middle_Name": None,
            "Relatives2_Last_Name": None,
            "Relatives2_Suffix": None,
            "Relatives2_Emails": None,
            "Relatives2_Phones": None,
            "Relatives2_Address": None,
            "Relatives2_City": None,
            "Relatives2_State": None,
            "Relatives2_Zip": None,
            "Relatives3_Full_Name": None,
            "Relatives3_First_Name": None,
            "Relatives3_Middle_Name": None,
            "Relatives3_Last_Name": None,
            "Relatives3_Suffix": None,
            "Relatives3_Emails": None,
            "Relatives3_Phones": None,
            "Relatives3_Address": None,
            "Relatives3_City": None,
            "Relatives3_State": None,
            "Relatives3_Zip": None,
            "Relatives4_Full_Name": None,
            "Relatives4_First_Name": None,
            "Relatives4_Middle_Name": None,
            "Relatives4_Last_Name": None,
            "Relatives4_Suffix": None,
            "Relatives4_Emails": None,
            "Relatives4_Phones": None,
            "Relatives4_Address": None,
            "Relatives4_City": None,
            "Relatives4_State": None,
            "Relatives4_Zip": None,
            "Relatives5_Full_Name": None,
            "Relatives5_First_Name": None,
            "Relatives5_Middle_Name": None,
            "Relatives5_Last_Name": None,
            "Relatives5_Suffix": None,
            "Relatives5_Emails": None,
            "Relatives5_Phones": None,
            "Relatives5_Address": None,
            "Relatives5_City": None,
            "Relatives5_State": None,
            "Relatives5_Zip": None,
            "Url": response.request.url
        }
        yield my_data
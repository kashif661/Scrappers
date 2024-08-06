import scrapy
from datetime import datetime
import re
from .. import name_parser
from ..address_parser import Address_parser

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "xera",
}
parser = Address_parser(db_config)

class PrdaraspiderSpider(scrapy.Spider):
    name = "prdaraspider"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
    }
    def start_requests(self):
       for i in range(9, 30001):
        case_id = f"PR0{i:05}"
        url = f"https://prdata.shelbycountytn.gov/prweb/ck_public_qry_doct.cp_dktrpt_docket_report?backto=P&case_id={case_id}&begin_date=&end_date="
     
        # url = "https://prdata.shelbycountytn.gov/prweb/ck_public_qry_doct.cp_dktrpt_docket_report?backto=P&case_id=PR027253&begin_date=&end_date="
     
        yield scrapy.Request(url=url,callback=self.parse,
                            headers=self.headers)

   
  
        
    def parse(self, response):
        case_id = response.xpath('normalize-space(//a[@name="description"]/following-sibling::table//tr[1]//td[3])').get()
        case_id = case_id.lstrip('\xa0')
        case_id = case_id.split(" - ")[0]
        case_title = response.xpath('normalize-space(//a[@name="description"]/following-sibling::table//tr[1]//td[3])').get()
        case_title = case_title.lstrip('\xa0')
        case_title = case_title.title()
        filling_date = response.xpath('normalize-space(//a[2]/following-sibling::table//tr[2]/td[3])').get()
        filling_date = filling_date.lstrip('\xa0')
        

        type = response.xpath('normalize-space(//a[2]/following-sibling::table//tr[3]/td[3])').get()
        type = type.lstrip('\xa0')
        type = type.title()
        status = response.xpath('normalize-space(//a[2]/following-sibling::table//tr[4]/td[3])').get()
        status = status.lstrip('\xa0')
        status = status.title()

        table = response.xpath('//following-sibling::table[.//th[text()="Seq #"]]')

        re_matter_names = []
        re_matter_addresses = []
        relative_labels = ["Decident","Relative1", "Relative2", "Relative3", "Relative4", "Relative5"]

        # Initialize lists for relative names and addresses
        relative_names = [[] for _ in range(len(relative_labels))]
        relative_addresses = [[] for _ in range(len(relative_labels))]

        attorney_names = []
        attorney_addresses = []
        petitioner_names = []
        petitioner_addresses = []

        attorney_count = 1
        petitioner_count = 1
       


        for row in table.xpath('.//tr[position() > 1]'):
            _type = row.xpath('normalize-space(.//td[4])').get()
            name = row.xpath('normalize-space(.//td[6]//text())').get()

            next_row = row.xpath('following-sibling::tr[1]')
            address_td = next_row.xpath('.//td[2]')


            address_br = address_td.xpath('.//br').extract()
            address_br = ''.join(address_br)
            address = address_td.xpath('normalize-space(string(.))').get()
        


            if _type == "RE: MATTER":
                re_matter_names.append(name)
                if address != "unavailable":
                    re_matter_addresses.append(address)
                else:
                    re_matter_addresses.append("")
                    


            elif _type == "ATTORNEY":
                if attorney_count <= 2:
                    attorney_names.append(f"{name}")
                    if address != "unavailable":
                        attorney_addresses.append(f"{address}")
                    else:
                        attorney_addresses.append("")
                    attorney_count += 1
            
            elif _type == "PETITIONER":
                if petitioner_count <= 2:
                    petitioner_names.append(f"{name}")
                    if address != "unavailable":
                        petitioner_addresses.append(f"{address}")
                    else:
                        petitioner_addresses.append("")
                    petitioner_count += 1
        for i, label in enumerate(relative_labels):
            if i < len(re_matter_names):
                relative_names[i].append(re_matter_names[i])
                relative_addresses[i].append(re_matter_addresses[i])


        re_matter_name = re_matter_names[0] if re_matter_names else ""
        re_matter_address = re_matter_addresses[0] if re_matter_addresses else ""
        re_matter_name = re_matter_name.title()
        re_matter_address = re_matter_address.title()



        relative1_name = relative_names[1][0] if relative_names[1] else ""
        relative1_address = relative_addresses[1][0] if relative_addresses[1] else ""
        relative1_name = relative1_name.title()
        relative1_address = relative1_address.title()


        relative2_name = relative_names[2][0] if relative_names[2] else ""
        relative2_address = relative_addresses[2][0] if relative_addresses[2] else ""
        relative2_name = relative2_name.title()
        relative2_address = relative2_address.title()


        relative3_name = relative_names[3][0] if relative_names[3] else ""
        relative3_address = relative_addresses[3][0] if relative_addresses[3] else ""


        relative4_name = relative_names[4][0] if relative_names[4] else ""
        relative4_address = relative_addresses[4][0] if relative_addresses[4] else ""


        relative5_name = relative_names[5][0] if relative_names[5] else ""
        relative5_address = relative_addresses[5][0] if relative_addresses[5] else ""


        attorney2_First_Name = ""
        attorney2_Middle_Name = ""
        attorney2_Last_Name = ""
        attorney2_Suffix = ""
        attorney1_First_Name = ""
        attorney1_Middle_Name = ""
        attorney1_Last_Name = ""
        attorney1_Suffix = ""

        petitioner2_First_Name = ""
        petitioner2_Middle_Name = ""
        petitioner2_Last_Name = ""
        petitioner2_Suffix = ""
        petitioner1_First_Name = ""
        petitioner1_Middle_Name = ""
        petitioner1_Last_Name = ""
        petitioner1_Suffix = ""

        Decedent_unit = ""
        Decedent_City = ""
        Decedent_State = ""
        Decedent_Zip =  ""

        attorney1_unit = ""
        attorney1_City = ""
        attorney1_State = ""
        attorney1_Zip = ""

        attorney2_unit = ""
        attorney2_City = ""
        attorney2_State = ""
        attorney2_Zip = ""


        petitioner1_unit = ""
        petitioner1_City = ""
        petitioner1_State = ""
        petitioner1_Zip = ""


        petitioner2_unit = ""
        petitioner2_City = ""
        petitioner2_State = ""
        petitioner2_Zip = ""



        try:
            parsed_decedent_address = parser.lf_address_parser(re_matter_address)
            Decedent_unit = parsed_decedent_address["unit"]
            Decedent_City = parsed_decedent_address["city"]
            Decedent_State = parsed_decedent_address["state"].upper()
            Decedent_Zip = parsed_decedent_address["zip_code"]
        except:
            pass
       
        rematter_parsed_name = name_parser.split_name(re_matter_name) 
        Decedent_First_Name = rematter_parsed_name['first_name']
        Decedent_Middle_Name = rematter_parsed_name.get('middle_name', '')
        Decedent_Last_Name = rematter_parsed_name['last_name']
        Decedent_Suffix = rematter_parsed_name['suffix']
       

           
        if len(petitioner_names) >= 1:
            petitioner1_name = petitioner_names[0]
            petitioner1_address = petitioner_addresses[0]
            petitioner1_name = petitioner1_name.title()
            petitioner1_address = petitioner1_address.title()
            decedent_parsed_name = name_parser.split_name(petitioner1_name)
            petitioner1_First_Name = decedent_parsed_name['first_name']
            petitioner1_Middle_Name = decedent_parsed_name.get('middle_name', '')
            petitioner1_Last_Name = decedent_parsed_name['last_name']
            petitioner1_Suffix = decedent_parsed_name['suffix']
        else:
            petitioner1_name = ""
            petitioner1_address = ""
        
      

        if len(petitioner_names) >= 2:
            petitioner2_name = petitioner_names[1]
            petitioner2_address = petitioner_addresses[1]
            petitioner2_name = petitioner2_name.title()
            petitioner2_address = petitioner2_address.title()
            decedent_parsed_name1 = name_parser.split_name(petitioner2_name)
            petitioner2_First_Name = decedent_parsed_name1['first_name']
            petitioner2_Middle_Name = decedent_parsed_name1.get('middle_name', '')
            petitioner2_Last_Name = decedent_parsed_name1['last_name']
            petitioner2_Suffix = decedent_parsed_name1['suffix']
        else:
            petitioner2_name = ""
            petitioner2_address = ""
        
       
            
        if len(attorney_names) >= 1:
            attorney1_name = attorney_names[0]
            attorney1_address = attorney_addresses[0]
            attorney1_name = attorney1_name.title()
            attorney1_address = attorney1_address.title()
            
            decedent_parsed_name2 = name_parser.split_name(attorney1_name)
            attorney1_First_Name = decedent_parsed_name2['first_name']
            attorney1_Middle_Name = decedent_parsed_name2.get('middle_name', '')
            attorney1_Last_Name = decedent_parsed_name2['last_name']
            attorney1_Suffix = decedent_parsed_name2['suffix']
            
            
        else:
            attorney1_name = ""
            attorney1_address = ""
        
       

        

        if len(attorney_names) >= 2:
            attorney2_name = attorney_names[1]
            attorney2_address = attorney_addresses[1]
            attorney2_name = attorney2_name.title()
            attorney2_address = attorney2_address.title()
            decedent_parsed_name3 = name_parser.split_name(attorney2_name)
            attorney2_First_Name = decedent_parsed_name3['first_name']
            attorney2_Middle_Name = decedent_parsed_name3.get('middle_name', '')
            attorney2_Last_Name = decedent_parsed_name3['last_name']
            attorney2_Suffix = decedent_parsed_name3['suffix']
        else:
            attorney2_name = ""
            attorney2_address = ""
        try:
            parsed_decedent_address1 = parser.lf_address_parser(attorney1_address)
            attorney1_unit = parsed_decedent_address1["unit"]
            attorney1_City = parsed_decedent_address1["city"]
            attorney1_State = parsed_decedent_address1["state"].upper()
            attorney1_Zip = parsed_decedent_address1["zip_code"]
        except:
            pass
       
        try:
            parsed_decedent_address0 = parser.lf_address_parser(attorney2_address)
            attorney2_unit = parsed_decedent_address0["unit"]
            attorney2_City = parsed_decedent_address0["city"]
            attorney2_State = parsed_decedent_address0["state"].upper()
            attorney2_Zip = parsed_decedent_address0["zip_code"]
        except:
            pass

        try:
            parsed_decedent_address2 = parser.lf_address_parser(petitioner1_address)
            petitioner1_unit = parsed_decedent_address2["unit"]
            petitioner1_City = parsed_decedent_address2["city"]
            petitioner1_State = parsed_decedent_address2["state"].upper()
            petitioner1_Zip = parsed_decedent_address2["zip_code"]
        except:
            pass
        try:
            parsed_decedent_address3 = parser.lf_address_parser(petitioner2_address)
            petitioner2_unit = parsed_decedent_address3["unit"]
            petitioner2_City = parsed_decedent_address3["city"]
            petitioner2_State = parsed_decedent_address3["state"].upper()
            petitioner2_Zip = parsed_decedent_address3["zip_code"]
        except:
            pass
        

        # Relative1 name , address parsing
        rematter_parsed_relativename = name_parser.split_name(relative1_name)
        Relative1_First_Name = rematter_parsed_relativename.get('first_name', '')
        Relative1_Middle_Name = rematter_parsed_relativename.get('middle_name', '')
        Relative1_Last_Name = rematter_parsed_relativename.get('last_name', '')
        Relative1_Suffix = rematter_parsed_relativename.get('suffix', '')

        Relative1_unit = ""
        Relative1_City = ""
        Relative1_State = ""
        Relative1_Zip = ""
        try:
            parsed_decedent_relativeaddress = parser.lf_address_parser(relative1_address)
            Relative1_unit = parsed_decedent_relativeaddress.get("unit", "")
            Relative1_City = parsed_decedent_relativeaddress.get("city", "")
            Relative1_State = parsed_decedent_relativeaddress.get("state", "").upper()
            Relative1_Zip = parsed_decedent_relativeaddress.get("zip_code", "")
        except:
            pass

       # Relative2 name , address parsing
        rematter_parsed_relativename2 = name_parser.split_name(relative2_name)
        Relative2_First_Name = rematter_parsed_relativename2.get('first_name', '')
        Relative2_Middle_Name = rematter_parsed_relativename2.get('middle_name', '')
        Relative2_Last_Name = rematter_parsed_relativename2.get('last_name', '')
        Relative2_Suffix = rematter_parsed_relativename2.get('suffix', '')

        Relative2_unit = ""
        Relative2_City = ""
        Relative2_State = ""
        Relative2_Zip = ""
        
        try:
            parsed_decedent_relativeaddress2 = parser.lf_address_parser(relative2_address)
            Relative2_unit = parsed_decedent_relativeaddress2.get("unit", "")
            Relative2_City = parsed_decedent_relativeaddress2.get("city", "")
            Relative2_State = parsed_decedent_relativeaddress2.get("state", "").upper()
            Relative2_Zip = parsed_decedent_relativeaddress2.get("zip_code", "")
        except:
            pass

        # Relative3 name , address parsing
        rematter_parsed_relativename3 = name_parser.split_name(relative3_name)
        Relative3_First_Name = rematter_parsed_relativename3.get('first_name', '')
        Relative3_Middle_Name = rematter_parsed_relativename3.get('middle_name', '')
        Relative3_Last_Name = rematter_parsed_relativename3.get('last_name', '')
        Relative3_Suffix = rematter_parsed_relativename3.get('suffix', '')

        Relative3_unit = ""
        Relative3_City = ""
        Relative3_State = ""
        Relative3_Zip = "" 
        try:
            parsed_decedent_relativeaddress3 = parser.lf_address_parser(relative3_address)
            Relative3_unit = parsed_decedent_relativeaddress3.get("unit", "")
            Relative3_City = parsed_decedent_relativeaddress3.get("city", "")
            Relative3_State = parsed_decedent_relativeaddress3.get("state", "").upper()
            Relative3_Zip = parsed_decedent_relativeaddress3.get("zip_code", "")
        except:
            pass

        # Relative4 name , address parsing
        rematter_parsed_relativename4 = name_parser.split_name(relative4_name)
        Relative4_First_Name = rematter_parsed_relativename4.get('first_name', '')
        Relative4_Middle_Name = rematter_parsed_relativename4.get('middle_name', '')
        Relative4_Last_Name = rematter_parsed_relativename4.get('last_name', '')
        Relative4_Suffix = rematter_parsed_relativename4.get('suffix', '')

        Relative4_unit = ""
        Relative4_City = ""
        Relative4_State = ""
        Relative4_Zip = ""
        try:
            parsed_decedent_relativeaddress4 = parser.lf_address_parser(relative4_address)
            Relative4_unit = parsed_decedent_relativeaddress4.get("unit", "")
            Relative4_City = parsed_decedent_relativeaddress4.get("city", "")
            Relative4_State = parsed_decedent_relativeaddress4.get("state", "").upper()
            Relative4_Zip = parsed_decedent_relativeaddress4.get("zip_code", "")
        except:
            pass

        # Relative5 name , address parsing
        rematter_parsed_relativename5 = name_parser.split_name(relative5_name)
        Relative5_First_Name = rematter_parsed_relativename5.get('first_name', '')
        Relative5_Middle_Name = rematter_parsed_relativename5.get('middle_name', '')
        Relative5_Last_Name = rematter_parsed_relativename5.get('last_name', '')
        Relative5_Suffix = rematter_parsed_relativename5.get('suffix', '')

        Relative5_unit = ""
        Relative5_City = ""
        Relative5_State = ""
        Relative5_Zip = ""
        try:
            parsed_decedent_relativeaddress5 = parser.lf_address_parser(relative5_address)
            Relative5_unit = parsed_decedent_relativeaddress5.get("unit", "")
            Relative5_City = parsed_decedent_relativeaddress5.get("city", "")
            Relative5_State = parsed_decedent_relativeaddress5.get("state", "").upper()
            Relative5_Zip = parsed_decedent_relativeaddress5.get("zip_code", "")
        except:
            pass
       



        yield{
            'State': 'TN',
            'County': 'Shelby',
            'City':'',
            'Zip':'',
            'Status': status,
            'Filling Date': filling_date,
            'Case Number': case_id,
            'Case Title': case_title,   
            'Case Type': type,  
            'DOB':'',
            'DOD':'',
            'Age':'',
            'Decedent Name': re_matter_name,
            'Decedent First_Name':Decedent_First_Name,
            'Decedent Middle_Name':Decedent_Middle_Name,
            'Decedent Last_Name':Decedent_Last_Name,
            'Decedent Suffix':Decedent_Suffix,
            'Decedent Address': re_matter_address,
            'Decedent City':Decedent_City,
            'Decedent State':Decedent_State,
            'Decedent Zip':Decedent_Zip,
            'Petitioner1 Name':petitioner1_name,
            'petitioner1 First_Name':petitioner1_First_Name,
            'Petitioner1 Middle_Name':petitioner1_Middle_Name,
            'Petitioner1 Last_Name':petitioner1_Last_Name,
            'Petitioner1 Suffix':petitioner1_Suffix,
            'Petitioner1 Address':petitioner1_address,
            'Petitioner1 City':petitioner1_City,
            'Petitioner1 State':petitioner1_State,
            'Petitioner1 Zip':petitioner1_Zip,
            'Petitioner2 Name':petitioner2_name,
            'petitioner2 First_Name':petitioner2_First_Name,
            'petitioner2 Middle_Name':petitioner2_Middle_Name,
            'petitioner2 Last_Name': petitioner2_Last_Name,
            'petitioner2 Suffix': petitioner2_Suffix,
            'Petitioner2 Address':petitioner2_address,
            'Petitioner2 City':petitioner2_City,
            'Petitioner2 State':petitioner2_State,
            'Petitioner2 Zip':petitioner2_Zip,
            'Attorney2 Name': attorney1_name,
            'Attorney1 First_Name':attorney1_First_Name,
            'Attorney1 Middle_Name':attorney1_Middle_Name,
            'Attorney1 Last_Name': attorney1_Last_Name,
            'Attorney1 Suffix': attorney1_Suffix,
            'Attorney2 Address':attorney1_address,
            'Attorney1 City':attorney1_City,
            'Attorney1 State':attorney1_State,
            'Attorney1 Zip':attorney1_Zip,
            'Attorney2 Name': attorney2_name,
            'Attorney2_First_Name':attorney2_First_Name,
            'Attorney2_Middle_Name':attorney2_Middle_Name,
            'Attorney2_Last_Name': attorney2_Last_Name,
            'Attorney2_Suffix': attorney2_Suffix,
            'Attorney2 Address':attorney2_address,
            'Attorney2 City':attorney2_City,
            'Attorney2 State':attorney2_State,
            'Attorney2 Zip':attorney2_Zip,
            'Relative1 Name': relative1_name,
            'Relative1 First_Name':Relative1_First_Name,
            'Relative1 Middle_Name':Relative1_Middle_Name,
            'Relative1 Last_Name': Relative1_Last_Name,
            'Relative1 Suffix': Relative1_Suffix,
            'Relative1 Address':relative1_address,
            'Relative1 City':Relative1_City,
            'Relative1 State':Relative1_State,
            'Relative1 Zip':Relative1_Zip,
            'Relative2 Name': relative2_name,
            'Relative2 First_Name':Relative2_First_Name,
            'Relative2 Middle_Name':Relative2_Middle_Name,
            'Relative2 Last_Name': Relative2_Last_Name,
            'Relative2 Suffix': Relative2_Suffix,
            'Relative2 Address':relative2_address,
            'Relative2 City':Relative2_City,
            'Relative2 State':Relative2_State,
            'Relative2 Zip':Relative2_Zip,
            'Relative3 Name': relative3_name,
            'Relative3 First_Name':Relative3_First_Name,
            'Relative3 Middle_Name':Relative3_Middle_Name,
            'Relative3 Last_Name': Relative3_Last_Name,
            'Relative3 Suffix': Relative3_Suffix,
            'Relative3 Address':relative3_address,
            'Relative3 City':Relative3_City,
            'Relative3 State':Relative3_State,
            'Relative3 Zip':Relative3_Zip,
            'Relative4 Name': relative4_name,
            'Relative4 First_Name':Relative4_First_Name,
            'Relative4 Middle_Name':Relative4_Middle_Name,
            'Relative4 Last_Name': Relative4_Last_Name,
            'Relative4 Suffix': Relative4_Suffix,
            'Relative4 Address':relative4_address,
            'Relative4 City':Relative4_City,
            'Relative4 State':Relative4_State,
            'Relative4 Zip':Relative4_Zip,
            'Relative5 Name': relative5_name,
            'Relative5 First_Name':Relative5_First_Name,
            'Relative5 Middle_Name':Relative5_Middle_Name,
            'Relative5 Last_Name': Relative5_Last_Name,
            'Relative5 Suffix': Relative5_Suffix,
            'Relative5 Address':relative5_address,
            'Relative5 City':Relative5_City,
            'Relative5 State':Relative5_State,
            'Relative5 Zip':Relative5_Zip,
            'url': response.url 
            
        }


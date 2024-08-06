from typing import Iterable
import scrapy
import json
import re
from ..address_parser import Address_parser

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "xera",
}
parser = Address_parser(db_config)

class PropertySpider(scrapy.Spider):
    name = 'property_spider'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
    }

    Cookie = {'ASP.NET_SessionId': 'ok5fvudwfetvg5sw44o2hrem', 
              'HasCookies': True, 
              'Disclaimer': 'accept'}

    def start_requests(self):
       url = "https://clintonoh-auditor-classic.ddti.net/"
       yield scrapy.Request(url=url,callback=self.parse,
                            cookies=self.Cookie,
                            headers=self.headers)

    def parse(self, response):
        View_state = response.css('#__VIEWSTATE').xpath('@value').extract_first()
        view_state_gen = response.css('#__VIEWSTATEGENERATOR').xpath('@value').extract_first()

        alphabet_list = [chr(ord('A') + i) for i in range(26)]
        for letter in alphabet_list:
            form_data = {
                '__EVENTTARGET': '',
                '__EVENTARGUMENT': '',
                '__LASTFOCUS': '',
                '__VIEWSTATE': View_state,
                '__VIEWSTATEGENERATOR': view_state_gen,
                'ctl00$tbSearchBox': 'Enter Parcel, Owner, or Address',
                'ctl00$ContentPlaceHolder1$Owner$tbOwnerLastName': '',
                'ctl00$ContentPlaceHolder1$Owner$tbOwnerFirstName': letter,
                'ctl00$ContentPlaceHolder1$Owner$btnSearchOwner': 'Search',
            }
            url = 'https://clintonoh-auditor-classic.ddti.net/'
        
            yield scrapy.FormRequest(url=url, callback=self.parcel_listing,
                                 formdata=form_data,
                                 cookies=self.Cookie,
                                 headers=self.headers)

        
    def parcel_listing(self, response):
        table_selector = response.css('#ContentPlaceHolder1_gvSearchResults')


        for row in table_selector.css('tr:not(.headerstyle)'):
            parcel_number = row.css('td:nth-child(1) a::text').get()
 
            if 'Next >>' in parcel_number:
                continue
            elif '<< Previous' in parcel_number:
                continue
            # print(parcel_number)
            url= 'https://clintonoh-auditor-classic.ddti.net/Data.aspx?ParcelID='+parcel_number
            page_url = 'https://clintonoh-auditor-classic.ddti.net/Data.aspx?ParcelID='+parcel_number
            yield scrapy.Request(url = url , callback = self.parcel_page, meta= {'page_url': page_url}  ,                       
                                    cookies=self.Cookie,
                                    headers=self.headers)

        next_page_link = response.css('a[href*="__doPostBack(\'ctl00$ContentPlaceHolder1$gvSearchResults\',\'Page$Next\')"]'
).get()
        
        if next_page_link:
                

                view_state = response.css('#__VIEWSTATE::attr(value)').extract_first()
                view_state_gen = response.css('#__VIEWSTATEGENERATOR::attr(value)').extract_first()

                form_data = {
                        '__EVENTTARGET': 'ctl00$ContentPlaceHolder1$gvSearchResults',
                            '__EVENTARGUMENT': 'Page$Next',
                            '__LASTFOCUS': '',
                            '__VIEWSTATE': view_state,
                            '__VIEWSTATEGENERATOR': view_state_gen,
                            "ctl00$tbSearchBox": 'Enter Parcel, Owner, or Address',
                            'ctl00$tbSaveSearchAs': '',
                            'ctl00$ContentPlaceHolder1$ddlResultsPerPage': '20'
                                        }

                yield scrapy.FormRequest(
                        url=response.url,
                        cookies=self.Cookie,
                        formdata=form_data,
                        headers=self.headers,
                        callback=self.parcel_listing
                )


    def parcel_page(self, response):
        page_url = response.meta.get('page_url')
        parcel_num = response.css("#ContentPlaceHolder1_lblParcel").css('::text').extract()
        full_adress = response.css('span#ContentPlaceHolder1_Base_fvDataProfile_AddressLabel').css('::text').extract_first()
        owner = response.css('span#ContentPlaceHolder1_Base_fvDataProfile_OwnerLabel').css('::text').extract_first()
        first_adress = response.css('span#ContentPlaceHolder1_Base_fvDataOwnerAddress_OwnerAddressLine2Label').css('::text').extract_first()    
        last_adress = response.css('span#ContentPlaceHolder1_Base_fvDataOwnerAddress_OwnerAddressLine3Label').css('::text').extract_first()    
        first_mailing_address = response.css('span#ContentPlaceHolder1_Base_fvDataMailingAddress_MailingAddressLine2Label').css('::text').extract_first()
        last_mailing_address = response.css('span#ContentPlaceHolder1_Base_fvDataMailingAddress_MailingAddressLine3Label').css('::text').extract_first()
        full_mailing_adress = f"{first_adress},{last_adress}"
        legal_description = response.css('span#ContentPlaceHolder1_Base_fvDataLegal_LegalDescriptionLabel::text').extract_first()
        school_district = response.css('span#ContentPlaceHolder1_Base_fvDataGeographic_SchoolDistrictLabel::text').get()
        land_use = response.css('span#ContentPlaceHolder1_Base_fvDataLegal_LandUseCodeDescriptionLabel::text').get()
        if land_use is not None:
            land_use = re.sub(r'["\']', '', land_use).strip()
        else:
            land_use = 0

        full_mailing_adress =  re.sub(r'["\']', '', full_mailing_adress).strip()


        if full_adress == first_adress:
            full_adress += " " + last_adress
        else:
            if full_adress == first_mailing_address:
                full_adress += " " + last_mailing_address

        text_to_remove = "*SD"
        owner = owner.replace(text_to_remove, "").strip()


        view_state = response.css('#__VIEWSTATE::attr(value)').extract_first()
        view_state_gen = response.css('#__VIEWSTATEGENERATOR::attr(value)').extract_first()
        form_data = {
                        '__EVENTTARGET': 'ctl00$ContentPlaceHolder1$mnuData',
                            '__EVENTARGUMENT': '1',
                            '__LASTFOCUS': '',
                            '__VIEWSTATE': view_state,
                            '__VIEWSTATEGENERATOR': view_state_gen,
                            "ctl00$tbSearchBox": 'Enter Parcel, Owner, or Address',
                            'ctl00$tbSaveSearchAs': '',
                                        }
        
        yield scrapy.FormRequest(
                        url=response.url,
                        cookies=self.Cookie,
                        formdata=form_data,
                        meta={'parcel_num': parcel_num,
                             'owner': owner,
                             'full_adress': full_adress,
                             'Mailing_full_adress':full_mailing_adress,
                            'legal_description' : legal_description,
                            'school_destrict' : school_district,
                            'land_use' : land_use, 
                            'page_url':page_url},
                        headers=self.headers,
                        callback=self.land_page,
                )




        
        
    def land_page(self,response):
        page_url = response.meta.get('page_url')
        owner = response.meta.get('owner')
        full_adress = response.meta.get('full_adress')
        Mailing_full_adress = response.meta.get('Mailing_full_adress')
        legal_description = response.meta.get('legal_description')
        school_destrict = response.meta.get('school_destrict')
        land_use = response.meta.get('land_use')
        parcel_num = response.meta.get('parcel_num')
        land_acres = response.css('span#ContentPlaceHolder1_Land_fvDataLandTotals_AcresTotalLabel::text').extract_first()
        if land_acres is not None:
            land_acres = float(land_acres)
            land_acres = land_acres * 43560
        else:
            land_acres = None

    

        
        view_state = response.css('#__VIEWSTATE::attr(value)').extract_first()
        view_state_gen = response.css('#__VIEWSTATEGENERATOR::attr(value)').extract_first()
        form_data = {
                        '__EVENTTARGET': 'ctl00$ContentPlaceHolder1$mnuData',
                            '__EVENTARGUMENT': '3',
                            '__LASTFOCUS': '',
                            '__VIEWSTATE': view_state,
                            '__VIEWSTATEGENERATOR': view_state_gen,
                            "ctl00$tbSearchBox": 'Enter Parcel, Owner, or Address',
                            'ctl00$tbSaveSearchAs': '',
                                        }
        
        yield scrapy.FormRequest(
                        url=response.url,
                        cookies=self.Cookie,
                        formdata=form_data,
                        meta={'parcel_num': parcel_num,
                              'page_url':page_url,
                             'owner': owner,
                             'full_adress': full_adress,
                             'Mailing_full_adress':Mailing_full_adress,
                            'legal_description' : legal_description,
                            'school_destrict' : school_destrict,
                            'land_use' : land_use,
                            'land_acres': land_acres},
                        headers=self.headers,
                        callback=self.Valuation_page,
                )

    def Valuation_page(self,response):
        page_url = response.meta.get('page_url')
        parcel_num = response.meta.get('parcel_num')
        owner = response.meta.get('owner')
        full_adress = response.meta.get('full_adress')
        Mailing_full_adress = response.meta.get('Mailing_full_adress')
        legal_description = response.meta.get('legal_description')
        school_destrict = response.meta.get('school_destrict')
        land_use = response.meta.get('land_use')
        land_acres = response.meta.get('land_acres')
        Appraised_value = response.css("span#ContentPlaceHolder1_Valuation_fvDataValuation_AppraisedLandValueLabel").css('::text').extract_first()
        Assessed_value = response.css("span#ContentPlaceHolder1_Valuation_fvDataValuation_AssessedLandValueLabel").css('::text').extract_first()
       
        Appraised_value = Appraised_value.replace(",", "").replace("$", "")
        Assessed_value = Assessed_value.replace(",", "").replace("$", "")


        view_state = response.css('#__VIEWSTATE::attr(value)').extract_first()
        view_state_gen = response.css('#__VIEWSTATEGENERATOR::attr(value)').extract_first()
        form_data = {
                        '__EVENTTARGET': 'ctl00$ContentPlaceHolder1$mnuData',
                            '__EVENTARGUMENT': '6',
                            '__LASTFOCUS': '',
                            '__VIEWSTATE': view_state,
                            '__VIEWSTATEGENERATOR': view_state_gen,
                            "ctl00$tbSearchBox": 'Enter Parcel, Owner, or Address',
                            'ctl00$tbSaveSearchAs': '',
                                        }
        
        yield scrapy.FormRequest(
                        url=response.url,
                        cookies=self.Cookie,
                        formdata=form_data,
                        meta={'parcel_num': parcel_num,
                              'page_url':page_url,
                             'owner': owner,
                             'full_adress': full_adress,
                             'Mailing_full_adress':Mailing_full_adress,
                            'legal_description' : legal_description,
                            'school_destrict' : school_destrict,
                            'land_use' : land_use,
                            'land_acres': land_acres,
                            'Appraised_value': Appraised_value,
                            'Assessed_value':Assessed_value
                            },
                        headers=self.headers,
                        callback=self.Tax_page,
                )
        
    def Tax_page(self,response):
        page_url = response.meta.get('page_url')
        parcel_num = response.meta.get('parcel_num')
        owner = response.meta.get('owner')
        full_adress = response.meta.get('full_adress')
        Mailing_full_adress = response.meta.get('Mailing_full_adress')
        legal_description = response.meta.get('legal_description')
        school_destrict = response.meta.get('school_destrict')
        land_use = response.meta.get('land_use')
        land_acres = response.meta.get('land_acres')
        Appraised_value = response.meta.get('Appraised_value')
        Assessed_value = response.meta.get('Assessed_value')

        tax_history = []
        table = response.css('table#ContentPlaceHolder1_Tax_gvDataPayments')
        table_rows = table.css('tr')[1:]  

        for row in table_rows:
            transfer_date = row.css('td:nth-child(1)::text').get()
            amount_paid = row.css('td:nth-child(2)::text').get()

            if amount_paid is not None:
                amount_paid = amount_paid.replace(",", "").replace("$", "")

            row_data = {
                'transfer_date': transfer_date,
                'amount_paid': amount_paid,
            }

            tax_history.append(row_data)


        view_state = response.css('#__VIEWSTATE::attr(value)').extract_first()
        view_state_gen = response.css('#__VIEWSTATEGENERATOR::attr(value)').extract_first()
        form_data = {
                        '__EVENTTARGET': 'ctl00$ContentPlaceHolder1$mnuData',
                            '__EVENTARGUMENT': '8',
                            '__LASTFOCUS': '',
                            '__VIEWSTATE': view_state,
                            '__VIEWSTATEGENERATOR': view_state_gen,
                            "ctl00$tbSearchBox": 'Enter Parcel, Owner, or Address',
                            'ctl00$tbSaveSearchAs': '',
                                        }
        
        yield scrapy.FormRequest(
                        url=response.url,
                        cookies=self.Cookie,
                        formdata=form_data,
                        meta={'parcel_num': parcel_num,
                              'page_url':page_url,
                             'owner': owner,
                             'full_adress': full_adress,
                             'Mailing_full_adress':Mailing_full_adress,
                            'legal_description' : legal_description,
                            'school_destrict' : school_destrict,
                            'land_use' : land_use,
                            'land_acres': land_acres,
                            'Appraised_value': Appraised_value,
                            'Assessed_value':Assessed_value,
                            'tax_history':tax_history
                            },
                        headers=self.headers,
                        callback=self.Residental_page,
                )


    
    def Residental_page(self,response):
        page_url = response.meta.get('page_url')
        parcel_num = response.meta.get('parcel_num')
        owner = response.meta.get('owner')
        full_adress = response.meta.get('full_adress')
        Mailing_full_adress = response.meta.get('Mailing_full_adress')
        legal_description = response.meta.get('legal_description')
        school_destrict = response.meta.get('school_destrict')
        land_use = response.meta.get('land_use')
        land_acres = response.meta.get('land_acres')
        Appraised_value = response.meta.get('Appraised_value')
        Assessed_value = response.meta.get('Assessed_value')
        tax_history = response.meta.get('tax_history')
        Rooms = response.css("span#ContentPlaceHolder1_Residential_fvDataResidential_TotalNumberOfRoomsLabel").css('::text').extract()
        bedrooms =response.css('#ContentPlaceHolder1_Residential_fvDataResidential_NumberOfBedroomsLabel').css('::text').extract()
        full_bathrooms = response.css("span#ContentPlaceHolder1_Residential_fvDataResidential_NumberOfFullBathsLabel").css('::text').extract()
        half_bathrooms = response.css("span#ContentPlaceHolder1_Residential_fvDataResidential_Label1").css('::text').extract()
        year_build = response.css("span#ContentPlaceHolder1_Residential_fvDataResidential_YearBuiltLabel").css('::text').extract()
        style = response.css("span#ContentPlaceHolder1_Residential_fvDataResidential_OccupancyLabel").css('::text').extract()
        heating = response.css("span#ContentPlaceHolder1_Residential_fvDataResidential_HasHeatingLabel").css('::text').extract()
        Air_condition = response.css("span#ContentPlaceHolder1_Residential_fvDataResidential_HasAirConditioningLabel").css('::text').extract()
        
        

        view_state = response.css('#__VIEWSTATE::attr(value)').extract_first()
        view_state_gen = response.css('#__VIEWSTATEGENERATOR::attr(value)').extract_first()
        form_data = {
                        '__EVENTTARGET': 'ctl00$ContentPlaceHolder1$mnuData',
                            '__EVENTARGUMENT': '4',
                            '__LASTFOCUS': '',
                            '__VIEWSTATE': view_state,
                            '__VIEWSTATEGENERATOR': view_state_gen,
                            "ctl00$tbSearchBox": 'Enter Parcel, Owner, or Address',
                            'ctl00$tbSaveSearchAs': '',
                            'ctl00$ContentPlaceHolder1$Residential$ddlDataResidential': '1'
                                        }
        
        yield scrapy.FormRequest(
                        url=response.url,
                        cookies=self.Cookie,
                        formdata=form_data,
                        meta={'parcel_num': parcel_num,
                              'page_url':page_url,
                             'owner': owner,
                             'full_adress': full_adress,
                             'Mailing_full_adress':Mailing_full_adress,
                            'legal_description' : legal_description,
                            'school_destrict' : school_destrict,
                            'land_use' : land_use,
                            'land_acres': land_acres,
                            'Appraised_value': Appraised_value,
                            'Assessed_value':Assessed_value,
                            'tax_history':tax_history,
                            'Rooms':Rooms,
                            'bedrooms': bedrooms,
                            'full_bathrooms':full_bathrooms,
                            'half_bathrooms':half_bathrooms,
                            'year_build':year_build,
                            'style':style,
                            'heating':heating,
                            'Air_condition':Air_condition,

                            },
                        headers=self.headers,
                        callback=self.Sales_page,
                )
        
    
    def Sales_page(self,response):
        page_url = response.meta.get('page_url')
        parcel_num = response.meta.get('parcel_num')
        owner = response.meta.get('owner')
        owner = owner.title()
        full_adress = response.meta.get('full_adress')
        full_adress = full_adress.title()
        Mailing_full_adress = response.meta.get('Mailing_full_adress')
        Mailing_full_adress = Mailing_full_adress.title()
        legal_description = response.meta.get('legal_description')
        school_destrict = response.meta.get('school_destrict')
        school_destrict = school_destrict.title()
        land_use = response.meta.get('land_use')
        land_use = land_use.title()
        land_acres = response.meta.get('land_acres')
        Appraised_value = response.meta.get('Appraised_value')
        Assessed_value = response.meta.get('Assessed_value')
        tax_history = response.meta.get('tax_history')
        Rooms = response.meta.get('Rooms')
        bedrooms = response.meta.get('bedrooms')
        full_bathrooms = response.meta.get('full_bathrooms')
        half_bathrooms = response.meta.get('half_bathrooms')
        year_build = response.meta.get('year_build')
        style = response.meta.get('style')
        if style is not None:
            style = [s.title() for s in style]

        heating = response.meta.get('heating')
        if heating is not None:
            heating = [word.lower() for word in heating]
        Air_condition = response.meta.get('Air_condition')
        if Air_condition is not None:
            Air_condition = [word.lower() for word in Air_condition]
        
        
        parsed_decedent_address = parser.lf_address_parser(Mailing_full_adress)
        Address= (parsed_decedent_address["address1"] + ' ' + parsed_decedent_address["unit"]).replace('.', '').strip()
        situs_number = parsed_decedent_address["number"]
        situs_street = parsed_decedent_address["street"]
        situs_unit = parsed_decedent_address["unit"]
        situs_City = parsed_decedent_address["city"]
        situs_State = parsed_decedent_address["state"].upper()
        situs_Zip = parsed_decedent_address["zip_code"]
        
        sale_history = []
        table_rows = response.css('#ContentPlaceHolder1_Sales_gvDataSales tr')[1:]
        for row in table_rows:
            transfer_date = row.css('td:nth-child(1)::text').get()
            sale_price = row.css('td:nth-child(2)::text').get()
            buyer = row.css('td:nth-child(3)::text').get()
            seller = row.css('td:nth-child(4)::text').get()

            sale_price = sale_price.replace(",", "").replace("$", "")
            text_to_remove = "*SD"
            buyer = buyer.replace(text_to_remove, "").strip()
            seller = seller.replace(text_to_remove, "").strip()
            text_to_remove1 = "** NOT ON FILE **"
            seller = seller.replace(text_to_remove1, "").strip()




            row_data = {
                'transfer_date': transfer_date,
                'sale_price': sale_price,
                'buyer': buyer,
                'seller': seller,
                
            }

            sale_history.append(row_data)
        
        
        if full_adress and full_adress[0].isdigit() and Mailing_full_adress and Mailing_full_adress[0].isdigit():
            owner_full_adress = full_adress
            owner_mailing_full_adress = Mailing_full_adress
            yield{
                            'parcel_num': parcel_num,
                            'owner': owner,
                            'situs_number':situs_number,
                            'situs_street':situs_street,
                            'situs_unit':situs_unit,
                            'Address':Address,
                            'situs_City':situs_City,
                            'situs_State':situs_State,
                            'situs_Zip':situs_Zip,
                            'full_adress': owner_full_adress,
                            'Mailing_full_adress':owner_mailing_full_adress,
                            'legal_description' : legal_description,
                            'school_destrict' : school_destrict,
                            'land_use' : land_use,
                            'land_acres': land_acres,
                            'Appraised_value': Appraised_value,
                            'Assessed_value':Assessed_value,
                            'Rooms':Rooms,
                            'bedrooms': bedrooms,
                            'full_bathrooms':full_bathrooms,
                            'half_bathrooms':half_bathrooms,
                            'year_build':year_build,
                            'style':style,
                            'heating':heating,
                            'Air_condition':Air_condition,
                            'sale_history':sale_history,
                            'tax_history':tax_history,
                            'page_url':page_url
                                              
        }
        
        else:
            pass
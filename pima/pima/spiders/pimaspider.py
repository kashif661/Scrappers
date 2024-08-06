import scrapy

class PimaspiderSpider(scrapy.Spider):
    name = "pimaspider"
    def __init__(self, *args, **kwargs):
        super(PimaspiderSpider, self).__init__(*args, **kwargs)
        self.fillyear = kwargs.get('fillyear')

    headers = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36', 
    }
    cookies = {
        'ASP.NET_SessionId': 'ght3uozlk4mbglmswox4bh2w',
    }

    def start_requests(self):
       url = "https://www.cosc.pima.gov/PublicDocs/search2a.aspx"
       yield scrapy.Request(url=url,callback=self.parse,
                            cookies=self.cookies,
                            headers=self.headers)
       
    def parse(self, response):
        view_state = response.css('#__VIEWSTATE').xpath('@value').extract_first()
        view_state_gen = response.css('#__VIEWSTATEGENERATOR').xpath('@value').extract_first()
        event_validator = response.css('#__EVENTVALIDATION').xpath('@value').extract_first()
        case_not_found_text = response.css('#lblInfo').get()
        year = 'PB'+self.fillyear
        for i in range(1, 3035):
            number = str(i).zfill(4)
            case = year+number

            form_data = {
                        '__VIEWSTATE': view_state,
                        '__VIEWSTATEGENERATOR': view_state_gen,
                        '__EVENTVALIDATION' : event_validator,
                        'txtLastName' : '',
                        'txtFirstName': '',
                        'txtCaseNumber' : case,
                        'SearchGroup': 'rdoCase',
                        'btnSearch': 'Search',

                    }
            url = "https://www.cosc.pima.gov/PublicDocs/search2a.aspx"
            yield scrapy.FormRequest(url=url, callback=self.parcel_page,
                                        formdata=form_data,
                                        cookies=self.cookies,
                                        headers=self.headers)

    def parcel_page(self, response):
        id = response.css('script:contains("window.open(\'GetCase2.aspx?ID=")').get()
        if id:
            id = id.replace("<script>window.open('GetCase2.aspx", "").strip()
            id = id.replace("','main');</script>", "").strip()
        else:
            return 
        
        url = "https://www.cosc.pima.gov/PublicDocs/GetCase2.aspx"+id
        page_url = "https://www.cosc.pima.gov/PublicDocs/GetCase2.aspx"+id
        yield scrapy.Request(url=url,callback=self.original_page,meta={
                                    "page_url":page_url
        },
                            cookies=self.cookies,
                            headers=self.headers)
        
    def original_page(self,response):
        page_url = response.meta.get('page_url')
        case_number  = response.css('td[style="HEIGHT: 37px"] input[name="txtCaseNumber"]::attr(value)').get()
        if case_number is None:
            return
        filling_date = response.css('td[style="HEIGHT: 33px"] input[name="txtCaseDate"]::attr(value)').get()
        title_name = response.css('td[bgcolor="white"] textarea[name="txtCaseCaption"]::text').get()
        if title_name:
            title_name =title_name.title()
            # title_name = title_name.replace("Estate Of:", "").strip()

        Petitioner = response.css('#grdParty tr:nth-child(2) td:nth-child(1) a b::text').get()
        if Petitioner:
            Petitioner =Petitioner.title()
        Petitioner_DOB = response.css('#grdParty tr:nth-child(2) td:nth-child(4) b::text').get()
        
        Decedent = response.css('#grdParty tr:nth-child(3) td:nth-child(1) a b::text').get()
        if Decedent:
            Decedent =Decedent.title()

        Decedent_DOB = response.css('#grdParty tr~ tr+ tr td:nth-child(4) b::text').get()

        
        my_data = {
            "State": "PA",
            "Address":"",
            "County": "Pima",
            "City": "",
            "Zip": "",
            "Status": "",
            "Filing_Date": filling_date,
            "Case_Number": case_number,  
            "Case_Title": title_name,
            "Case_Type": "",
            "DOB": Decedent_DOB,
            "DOD": "",
            "Age": "",
            "Decedent_Full_Name": Decedent,
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
            "Petitioner1_Full_Name": Petitioner,
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
            "Url": page_url
        }

        # yield my_data
        print(my_data["Case_Number"])
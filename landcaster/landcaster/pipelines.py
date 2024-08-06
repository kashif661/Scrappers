# # Define your item pipelines here
# #
# # Don't forget to add your pipeline to the ITEM_PIPELINES setting
# # See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# # useful for handling different item types with a single interface
# import os
# from dotenv import load_dotenv
# from itemadapter import ItemAdapter
# import mysql.connector

# load_dotenv()

# class LandcasterPipeline:
#     def __init__(self):
#         self.conn = mysql.connector.connect(
#             host =  os.getenv("DB_HOST"),
#             user = os.getenv("DB_USERNAME"),
#             password = os.getenv("DB_PASSWORD"),
#             database = os.getenv("DB_DATABASE")
#         )

#         ## Create cursor,used to execute commands
#         self.cur = self.conn.cursor()
        
#     def process_item(self, item, spider):
#         sql_query = f""" INSERT INTO {os.getenv("DB_TABLE")}(State, Address, County, City, Zip, Status, Filing_Date,
#         Case_Number, Case_Title, Case_Type, DOB, DOD, Age, Decedent_Full_Name, Decedent_First_Name,
#         Decedent_Middle_Name, Decedent_Last_Name, Decedent_Suffix, Decedent_Emails, Decedent_Phones,
#         Decedent_Address, Decedent_City, Decedent_State, Decedent_Zip, Petitioner1_Full_Name, 
#         Petitioner1_First_Name, Petitioner1_Middle_Name, Petitioner1_Last_Name, Petitioner1_Suffix, 
#         Petitioner1_Emails, Petitioner1_Phones, Petitioner1_Address, Petitioner1_City, Petitioner1_State,  
#         Petitioner1_Zip, Petitioner2_Full_Name, Petitioner2_First_Name, Petitioner2_Middle_Name, 
#         Petitioner2_Last_Name, Petitioner2_Suffix, Petitioner2_Emails, Petitioner2_Phones, 
#         Petitioner2_Address, Petitioner2_City, Petitioner2_State, Petitioner2_Zip, 
#         Attorney1_Full_Name, Attorney1_First_Name, Attorney1_Middle_Name, Attorney1_Last_Name, 
#         Attorney1_Suffix, Attorney1_Emails, Attorney1_Phones, Attorney1_Address, Attorney1_City, 
#         Attorney1_State, Attorney1_Zip, Attorney2_Full_Name, Attorney2_First_Name, Attorney2_Middle_Name, 
#         Attorney2_Last_Name, Attorney2_Suffix, Attorney2_Emails, Attorney2_Phones, Attorney2_Address, 
#         Attorney2_City, Attorney2_State, Attorney2_Zip, Relatives1_Full_Name, Relatives1_First_Name, 
#         Relatives1_Middle_Name, Relatives1_Last_Name, Relatives1_Suffix, Relatives1_Emails, 
#         Relatives1_Phones, Relatives1_Address, Relatives1_City, Relatives1_State, Relatives1_Zip, 
#         Relatives2_Full_Name, Relatives2_First_Name, Relatives2_Middle_Name, Relatives2_Last_Name, 
#         Relatives2_Suffix, Relatives2_Emails, Relatives2_Phones, Relatives2_Address, 
#         Relatives2_City, Relatives2_State, Relatives2_Zip, Relatives3_Full_Name, Relatives3_First_Name, 
#         Relatives3_Middle_Name, Relatives3_Last_Name, Relatives3_Suffix, Relatives3_Emails, 
#         Relatives3_Phones, Relatives3_Address, Relatives3_City, Relatives3_State, Relatives3_Zip, 
#         Relatives4_Full_Name, Relatives4_First_Name, Relatives4_Middle_Name, Relatives4_Last_Name, 
#         Relatives4_Suffix, Relatives4_Emails, Relatives4_Phones, Relatives4_Address, Relatives4_City, 
#         Relatives4_State, Relatives4_Zip, Relatives5_Full_Name, Relatives5_First_Name, 
#         Relatives5_Middle_Name, Relatives5_Last_Name, Relatives5_Suffix, Relatives5_Emails, 
#         Relatives5_Phones, Relatives5_Address, Relatives5_City, Relatives5_State, Relatives5_Zip, Url) 
#         VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
#         %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
#         %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
#         %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) """
        
#         sql_query_values = (
#             item["State"],
#             item["Address"],
#             item["County"],
#             item["City"],
#             item["Zip"],
#             item["Status"],
#             item["Filing_Date"],
#             item["Case_Number"],
#             item["Case_Title"],
#             item["Case_Type"],
#             item["DOB"],
#             item["DOD"],
#             item["Age"],
#             item["Decedent_Full_Name"],
#             item["Decedent_First_Name"],
#             item["Decedent_Middle_Name"],
#             item["Decedent_Last_Name"],
#             item["Decedent_Suffix"],
#             item["Decedent_Emails"],
#             item["Decedent_Phones"],
#             item["Decedent_Address"],
#             item["Decedent_City"],
#             item["Decedent_State"],
#             item["Decedent_Zip"],
#             item["Petitioner1_Full_Name"],
#             item["Petitioner1_First_Name"],
#             item["Petitioner1_Middle_Name"],
#             item["Petitioner1_Last_Name"],
#             item["Petitioner1_Suffix"],
#             item["Petitioner1_Emails"],
#             item["Petitioner1_Phones"],
#             item["Petitioner1_Address"],
#             item["Petitioner1_City"],
#             item["Petitioner1_State"],
#             item["Petitioner1_Zip"],
#             item["Petitioner2_Full_Name"],
#             item["Petitioner2_First_Name"],
#             item["Petitioner2_Middle_Name"],
#             item["Petitioner2_Last_Name"],
#             item["Petitioner2_Suffix"],
#             item["Petitioner2_Emails"],
#             item["Petitioner2_Phones"],
#             item["Petitioner2_Address"],
#             item["Petitioner2_City"],
#             item["Petitioner2_State"],
#             item["Petitioner2_Zip"],
#             item["Attorney1_Full_Name"],
#             item["Attorney1_First_Name"],
#             item["Attorney1_Middle_Name"],
#             item["Attorney1_Last_Name"],
#             item["Attorney1_Suffix"],
#             item["Attorney1_Emails"],
#             item["Attorney1_Phones"],
#             item["Attorney1_Address"],
#             item["Attorney1_City"],
#             item["Attorney1_State"],
#             item["Attorney1_Zip"],
#             item["Attorney2_Full_Name"],
#             item["Attorney2_First_Name"],
#             item["Attorney2_Middle_Name"],
#             item["Attorney2_Last_Name"],
#             item["Attorney2_Suffix"],
#             item["Attorney2_Emails"],
#             item["Attorney2_Phones"],
#             item["Attorney2_Address"],
#             item["Attorney2_City"],
#             item["Attorney2_State"],
#             item["Attorney2_Zip"],
#             item["Relatives1_Full_Name"],
#             item["Relatives1_First_Name"],
#             item["Relatives1_Middle_Name"],
#             item["Relatives1_Last_Name"],
#             item["Relatives1_Suffix"],
#             item["Relatives1_Emails"],
#             item["Relatives1_Phones"],
#             item["Relatives1_Address"],
#             item["Relatives1_City"],
#             item["Relatives1_State"],
#             item["Relatives1_Zip"],
#             item["Relatives2_Full_Name"],
#             item["Relatives2_First_Name"],
#             item["Relatives2_Middle_Name"],
#             item["Relatives2_Last_Name"],
#             item["Relatives2_Suffix"],
#             item["Relatives2_Emails"],
#             item["Relatives2_Phones"],
#             item["Relatives2_Address"],
#             item["Relatives2_City"],
#             item["Relatives2_State"],
#             item["Relatives2_Zip"],
#             item["Relatives3_Full_Name"],
#             item["Relatives3_First_Name"],
#             item["Relatives3_Middle_Name"],
#             item["Relatives3_Last_Name"],
#             item["Relatives3_Suffix"],
#             item["Relatives3_Emails"],
#             item["Relatives3_Phones"],
#             item["Relatives3_Address"],
#             item["Relatives3_City"],
#             item["Relatives3_State"],
#             item["Relatives3_Zip"],
#             item["Relatives4_Full_Name"],
#             item["Relatives4_First_Name"],
#             item["Relatives4_Middle_Name"],
#             item["Relatives4_Last_Name"],
#             item["Relatives4_Suffix"],
#             item["Relatives4_Emails"],
#             item["Relatives4_Phones"],
#             item["Relatives4_Address"],
#             item["Relatives4_City"],
#             item["Relatives4_State"],
#             item["Relatives4_Zip"],
#             item["Relatives5_Full_Name"],
#             item["Relatives5_First_Name"],
#             item["Relatives5_Middle_Name"],
#             item["Relatives5_Last_Name"],
#             item["Relatives5_Suffix"],
#             item["Relatives5_Emails"],
#             item["Relatives5_Phones"],
#             item["Relatives5_Address"],
#             item["Relatives5_City"],
#             item["Relatives5_State"],
#             item["Relatives5_Zip"],
#             item["Url"]
#         )

#         self.cur.execute(sql_query, sql_query_values)
#         ## Execute insert of data into database
#         self.conn.commit()

    
#     def close_spider(self,spider):

#         ## Close cursor & connection to database 
#         self.cur.close()
#         self.conn.close()

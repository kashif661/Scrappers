import usaddress
import mysql.connector

class Address_Parser:
    def __init__(self, db_config):
        self.db_config = db_config
        self.connection = None
        self.sql_dict_cursor = None
        self.__connect_to_database()

    def __connect_to_database(self):
        self.connection = mysql.connector.connect(**self.db_config)
        self.sql_dict_cursor = self.connection.cursor(dictionary=True)

    def __close_database_connection(self):
        if self.sql_dict_cursor:
            self.sql_dict_cursor.close()
        if self.connection:
            self.connection.close()
    def __lf_us_address_parser(self, input_value):
        input_parts = dict(usaddress.parse(input_value))

        name, number, street, unit, city, state, zip_code = '', '', '', '', '', '', ''
        for k, v in input_parts.items():
            if 'number' in v.lower():
                number = k
            elif 'streetname' in v.lower() or 'uspsbox' in v.lower():
                street += f' {k}'
            elif 'occupancy' in v.lower():
                unit += f' {k}'
            elif 'placename' in v.lower():
                city += f' {k}'
            elif 'statename' in v.lower():
                state = k
            elif 'zipcode' in v.lower():
                zip_code = k
            elif 'recipient' in v.lower():
                return 'contain a name'

        return {
            'number': number.strip(),
            'street': street.strip().strip(','),
            'unit': unit.strip().strip(','),
            'address1': f'{number} {street.strip().strip(",")} {unit}'.strip().strip(','),
            'city': city.strip().strip(','),
            'state': state.strip().strip(','),
            'zip_code': zip_code.strip().strip(',')
        }

    def lf_address_parser(self, address):
        address_parts = self.__lf_us_address_parser(address)
        street_parts = address_parts['street'].split(' ')
        final_street = []
        for street_part in street_parts:
            query = f'select std_abbreviation From I_Address_Shorts where MATCH(possible_values) AGAINST ("{street_part}")'
            self.sql_dict_cursor.execute(query)
            record = self.sql_dict_cursor.fetchall()
            if record:
                final_street.append(record[0]['std_abbreviation'])
            else:
                final_street.append(street_part)
        address_parts['address1'] = address_parts['number'] +' ' + ' '.join(final_street)
        address_parts['street'] = ' '.join(final_street)
        
        return address_parts
    
    def __del__(self):
        # Ensure that the database connection and cursor are closed when the instance is deleted.
        try:
            self.__close_database_connection()    
        except Exception as e:
            pass
        # Handle the exception or log it
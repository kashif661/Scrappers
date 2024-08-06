import usaddress


class Address_parser:

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
        return address_parts
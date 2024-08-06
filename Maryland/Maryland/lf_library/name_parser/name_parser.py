import os
import re
import pandas as pd
import mysql.connector
from dotenv import load_dotenv
from pprint import pprint


from Maryland.lf_library.name_parser.lf_libraries.db_connections import update_db_connections, connections

load_dotenv()

dict_of_data = {
    'prefix': {'Sec.': ['secretary'], 'Gen.': ['general'], 'RTDr.': ['doctor of technical sciences'],
               'Lt. Col.': ['lieutenant colonel'], 'ThLic.': ['licentiate of theology'],
               'ThMgr.': ['master of theology', 'master of divinity'], 'Odb. As.': ['assistant professor'],
               'PharmDr.': ['doctor of pharmacy'], 'PhDr.': ['doctor of philosophy'], 'Treas.': ['treasurer'],
               'Capt.': ['captain'], 'Col.': ['colonel'], 'DiS.': ['certified specialist'], 'Mgr.': ['master'],
               'Cpl.': ['corporal'], 'Ing.': ['engineer', 'ingenieur'],
               'MD.': ['doctor of general medicine'], 'Rev.': ['rev', "rev'd", 'reverend'], 'Hon.': ['honorable'],
               'Fr.': ['fr', 'father'], 'Mrs.': ['mrs', 'missus', 'missis'], 'DSc.': ['doctor of science'],
               'Ms.': ['ms', 'miss'], 'Amb.': ['ambassador'], 'Cmdr.': ['commander'],
               'PaedDr.': ['doctor of education'], 'PhMr.': ['master of pharmacy'], 'Acad.': ['academian', 'academic'],
               'ThDr.': ['doctor of theology'], 'BcA.': ['bachelor of arts', 'baccalaureus artis'],
               'Adm.': ['administrative', 'administrator', 'administrater'],
               'Ing. sheet.': ['architect engineer', 'intrudes upon architectus'], 'Pres.': ['president'],
               'Msgr': ['monsignor'], 'MgA.': ['master of arts', 'magister artis'], 'Supt.': ['superintendent'],
               'MDDr.': ['doctor of dental medicine', 'medicinae doctor dentium'], 'ArtD.': ['doctor of arts'],
               'JUDr.': ['juris doctor utriusque', 'doctor rights'], 'Sir': ['sir'],
               'Bc.': ['bachelor', 'baccalaureus'], 'RNDr.': ['doctor of science'], 'Sr.': ['sister'],
               'RCDr.': ['doctor of business studies'], 'Mr.': ['mr', 'mister', 'master'], 'Dr.': ['dr'],
               'Pvt.': ['private'], 'Gov': ['governor', 'governer'], 'Lt.': ['lieutenant'], 'Br.': ['brother'],
               'RSDr.': ['doctor of socio-political sciences'], 'Prof.': ['prof', 'professor'], 'Ofc': ['officer'],
               'Sen.': ['senator'], ' ': ['the'], 'DVM.': ['doctor of veterinary medine'],
               'ICDr.': ['doctor of canon law', 'juris cononici doctor'], 'As.': ['assistant'],
               'Rep.': ['representatitve'], 'Doc.': ['associate professor'], 'Th.D.': ['doctor of theology']},
    'suffixes': {
        'prof': ['AO', 'B.A.', 'M.Sc', 'BCompt', 'PhD', 'Ph.D.', 'APR', 'RPh', 'PE', 'MD', 'M.D.', 'DMD', 'CME',
                 'BSc', 'Bsc', 'BSc(hons)', 'Ph.D.', 'BEng', 'M.B.A.', 'MBA', 'FAICD', 'CM', 'OBC', 'M.B.', 'ChB',
                 'FRCP', 'FRSC', 'FREng', 'Esq', 'MEng', 'MSc', 'J.D.', 'JD', 'BGDipBus', 'Dip', 'Dipl.Phys', 'M.H.Sc.',
                 'MPA', 'B.Comm', 'B.Eng', 'B.Acc', 'FSA', 'PGDM', 'FCPA', 'RN', 'R.N.', 'MSN', 'PCA', 'PCCRM', 'PCFP',
                 'PCGD', 'PCHR', 'PCM', 'PCPS', 'PCPM', 'PCSCM', 'PCSM', 'PCMM', 'PCTC', 'ACA', 'FCA', 'ACMA', 'FCMA',
                 'AAIA', 'FAIA', 'CCC', 'MIPA', 'FIPA', 'CIA', 'CFE', 'CISA', 'CFAP', 'QC', 'Q.C.', 'M.Tech', 'CTA',
                 'C.I.M.A.', 'B.Ec', 'CFIA', 'ICCP', 'CPS', 'CAP-OM', 'CAPTA', 'TNAOAP', 'AFA', 'CAIA',
                 'CBA', 'CVA', 'ICVS', 'CIIA', 'CMU', 'PFM', 'PRM', 'CFP', 'CWM', 'CCP', 'EA', 'CCMT', 'CGAP', 'CDFM',
                 'CFO', 'CGFM', 'CGAT', 'CGFO', 'CMFO', 'CPFO', 'CPFA', 'BMD', 'BIET', 'P.Eng', 'PE', 'MBBS', 'MB',
                 'BCh', 'BAO', 'BMBS', 'MBBChir', 'MBChBa', 'MPhil', 'LL.D', 'LLD', 'D.Lit', 'DEA', 'DESS', 'DClinPsy',
                 'DSc', 'MRes', 'M.Res', 'Psy.D', 'Pharm.D', 'BA(Admin)', 'BAcc', 'BACom', 'BAdmin', 'BAE', 'BAEcon',
                 'BA(Ed)', 'BA(FS)', 'BAgr', 'BAH', 'BAI', 'BAI(Elect)', 'BAI(Mech)', 'BALaw', 'BAO', 'BAppSc', 'BArch',
                 'BArchSc', 'BARelSt', 'BASc', 'BASoc', 'DDS', 'D.D.S.', 'BATheol', 'BBA', 'BBLS', 'BBS',
                 'BBus', 'BChem', 'BCJ', 'BCL', 'BCLD(SocSc)', 'BClinSci', 'BCom', 'BCombSt', 'BCommEdCommDev', 'BComp',
                 'BComSc', 'BCoun', 'BD', 'BDes', 'BE', 'BEcon', 'BEcon&Fin', 'M.P.P.M.', 'MPPM', 'BEconSci', 'BEd',
                 'BEng', 'BES', 'BEng(Tech)', 'BFA', 'BFin', 'BFLS', 'BFST', 'BH', 'BHealthSc', 'BHSc', 'BHy', 'BJur',
                 'BL', 'BLE', 'BLegSc', 'BLib', 'BLing', 'BLitt', 'BLittCelt', 'BLS', 'BMedSc', 'BMet', 'BMid', 'BMin',
                 'BMS', 'BMSc', 'BMSc', 'BMS', 'BMus', 'BMusEd', 'BMusPerf', 'BN', 'BNS', 'BNurs', 'BOptom', 'BPA',
                 'BPharm', 'BPhil', 'TTC', 'DIP', 'Tchg', 'BEd', 'MEd', 'ACIB', 'FCIM', 'FCIS', 'FCS', 'Fcs',
                 'Bachelor', 'O.C.', 'JP', 'C.Eng', 'C.P.A.', 'B.B.S.', 'MBE', 'GBE', 'KBE', 'DBE', 'CBE', 'OBE',
                 'MRICS', 'D.P.S.K.', 'D.P.P.J.', 'DPSK', 'DPPJ', 'B.B.A.', 'GBS', 'MIGEM', 'M.I.G.E.M.', 'FCIS',
                 'BPhil(Ed)', 'BPhys', 'BPhysio', 'BPl', 'BRadiog', 'BSc', 'B.Sc', 'BScAgr', 'BSc(Dairy)', 'BSc(DomSc)',
                 'BScEc', 'BScEcon', 'BSc(Econ)', 'BSc(Eng)', 'BScFor', 'BSc(HealthSc)', 'BSc(Hort)', 'BBA', 'B.B.A.',
                 'BSc(MCRM)', 'BSc(Med)', 'BSc(Mid)', 'BSc(Min)', 'BSc(Psych)', 'BSc(Tech)', 'BSD', 'BSocSc', 'BSS',
                 'BStSu', 'BTchg', 'BTCP', 'BTech', 'BTechEd', 'BTh', 'BTheol', 'BTS', 'EdB', 'LittB', 'LLB', 'MA',
                 'MusB', 'ScBTech', 'CEng', 'FCA', 'CFA', 'Cfa', 'C.F.A.', 'LLB', 'LL.B', 'LLM', 'LL.M', 'CA(SA)',
                 'C.A.', 'CA', 'CPA', 'Solicitor', 'DMS', 'FIWO', 'CEnv', 'MICE', 'MIWEM', 'B.Com', 'BCom', 'BAcc',
                 'BEc', 'MEc', 'HDip', 'B.Bus.', 'E.S.C.P.'],
        'line': ['II', 'III', 'IV', '1st', '2nd', '3rd', '4th', '5th', 'Senior', 'Junior', 'Jr', 'Sr']},
    'vowels': ['a', 'e', 'i', 'o', 'u'],
    'compound': ['da', 'de', 'del', 'della', 'dem', 'den', 'der', 'di', 'du', 'het', 'la', 'onder', 'op', 'pietro',
                 'st.', 'st', "'t", 'ten', 'ter', 'van', 'vanden', 'vere', 'von']}

punctuation_re = re.compile(r'[^\w\s-]')


def check_if_company(raw_name):
    company_sent_list = ["SECRETARY OF TRANSPORTATION", "FUNDAMENTAL LITERACY FOUNDATION"]
    company_name = [e for e in company_sent_list if e.lower() in raw_name.lower()]
    if not company_name:

        company_indicators = [
            'llc', 'lp', 'inc', 'l l c', 'lnc', 'company', 'l.l.c.', 'llp', 'grp',
            'l.l.p.', 'group', 'pc', 'p.c.', '%', 'partnerhip', 'ltd',
            'partnership', 'limited', 'rr', 'co', 'partners',
            "training", "handicapp", "association", "investments", "veterans", "holdings", "lllp",
            "assoc", "commonwealth", "housing", "corp", "supply", "city", "authority", "church", "mental",
            "corporation", "corporat", "churchs", "management", "board", "properties", "prop", "albertville",
            "bank", "union", "dept", "farms", 'united','center','alabama'
        ]
        name_components = raw_name.strip().lower().split(' ')

        company_name = [c for c in name_components if c.lower() in company_indicators]
        # company_name = [e for e in company_indicators if e.lower() in raw_name.lower()]

        if company_name:
            return True
        else:
            return False


# def clean_text(text):
#     lower_text = str.lower(str(text))
#     # potentialImpurities = [" trust", " family", " jr", " sr", " &", " i", " ii", " iii", " iv", " v", " vi", " vii",
#     #                        " viii", " ix", " x"]
#     potentialImpurities = [" trust", " family", " jr", " sr", " &", " revoc", " living"]
#     for e in potentialImpurities:
#         if e in lower_text:
#             pure_text = lower_text.replace(e, '')
#             lower_text = pure_text
#     return lower_text


def clean_text(name):
    potential_impurities = ["trust", "family", "revoc", "living", "trust", "family", "rev", "trs", 'tru', "et al",
                            "liv tr", "fam tr", "living trust", "decedents", "revocable", "liv", "suppl", "tr",
                            "irrev", "fam", "family", "mortgage", "development", "touches", "amended", "etal",
                            "c/o", "est", "price"]

    # name_components = re.sub(punctuation_re, '', name or '').strip().lower().split(' ')
    name_components = name.strip().lower().split(' ')
    name_components = [c for c in name_components if c.lower() not in potential_impurities]
    return ' '.join(name_components)


def get_rank(table, col, data):
    # rank = IFirstnamerank.objects.values('frequency').filter(name=str.lower(data)).order_by(
    #     '-frequency').first()
    update_db_connections(os.getenv("DB_DATABASE"))
    sql_connection, sql_cursor = connections[os.getenv("DB_DATABASE")]

    query = 'select * from {} where name="{}" order by {} DESC limit 1'.format(table, data, col)
    sql_cursor.execute(query)

    rows = sql_cursor.fetchall()

    if rows:
        # Fetch the column names from the cursor description
        column_names = [desc[0].lower() for desc in sql_cursor.description]

        # Create the dictionary by combining column names with row values
        result = {column_names[i]: value for i, value in enumerate(rows[0])}
        # print(result)
        return result


def get_prefix(components):
    try:
        for component in components:
            comp = component.lower().strip('.')
            for k, v in dict_of_data['prefix'].items():
                if comp in v:
                    components.remove(component)
                    return k, components

        return '', components
    except Exception as e:
        print('check exception')


def compare_frequency(name):
    rank = get_rank('i_firstnamerank', 'Name', name)
    if rank:
        surname_rank = get_rank('i_surname', 'count', name)
        if surname_rank:
            if rank['frequency'] > surname_rank['count']:
                return {
                    'rank': 'true',
                    'name': name
                }
            else:
                return {
                    'rank': 'false',
                    'name': name
                }
        else:
            return {
                'rank': 'true',
                'name': name
            }
    else:
        surname_rank = get_rank('i_surname', 'count', name)
        if surname_rank:
            return {
                'rank': 'false',
                'name': name
            }
        else:
            return {
                'rank': 'Nothing'
            }


def get_first_name(components):
    try:
        first_name, first_name_frequency = '', 0
        for component in components:
            # print('Checking for first name', component)
            # rank = IFirstnamerank.objects.values('frequency').filter(name=str.lower(data)).order_by( '-frequency').first()
            rank = get_rank('i_firstnamerank', 'Name', component)
            # print(rank)
            if rank:
                if rank['frequency'] > first_name_frequency:
                    first_name = component
                    first_name_frequency = rank['frequency']

        if first_name:
            components.remove(first_name)

        return first_name, components
    except Exception as e:
        print('check exception')


def get_initials(components):
    try:
        initials = []
        for data in components:
            if len(data) < 2:
                initials.append(data)
                components.remove(data)

        return initials, components

    except Exception as e:
        print('check exception')


def get_last_name(components, second_name=False):
    try:
        last_name, last_name_frequency = '', 0
        for component in components:
            # rank = ISurname.objects.values('count').filter(name=str.lower(data)).order_by(
            #     '-count').first()
            rank = get_rank('i_surname', 'count', component)
            if rank:
                if rank['count'] > last_name_frequency:
                    last_name = component
                    last_name_frequency = rank['count']

        if components:
            last_name = last_name or components[0] if not second_name else ''
        else:
            last_name = last_name if not second_name else ''
        if last_name:
            components.remove(last_name)

        return last_name

    except Exception as e:
        print('check exception', e)


def get_suffix(components):
    try:
        lines, professions = [], []
        for component in components:
            comp = component.lower().replace('.', '')
            dept = re.search(r'\((.*)\)', comp)
            dept = dept.group(1) if dept else ''
            comp = comp.replace(dept, '').replace('(', '').replace(')', '')

            for prof in dict_of_data['suffixes']['prof']:
                prof = prof.lower().replace('.', '').split('(')
                if comp == prof[0]:
                    if dept:
                        if len(prof) < 2 or dept[0].lower() != prof[1][0].lower():
                            a = 0
                            continue

                    professions.append(component)

            lines.extend([component for line in dict_of_data['suffixes']['line'] if comp == line.lower()])

        professions = list(set(professions)) + list(set(lines))
        components = list(set(components))
        for thing in professions:
            components.remove(thing)

        lines = ' '.join(lines)
        professions = ' '.join(professions)
        suffix = '{},{}'.format(lines, professions)
        suffix = suffix.strip(' ').strip(',').strip(' ')
        suffix_list = list(suffix.split(','))
        suf = ' '.join(list(dict.fromkeys(suffix_list)))
        suf = ','.join(set(suf.split(' ')))
        return suf, components
    except Exception as e:
        print('check exception{}'.format(e))


def rank_name_components(name, second_name=False):
    name_components = name.strip().split(' ')
    # name_components = [re.sub(r'[\.\,]*', '', component) for component in name_components]
    prefix, name_components = get_prefix(name_components)
    suffix, name_components = get_suffix(name_components)
    initials, name_components = get_initials(name_components)
    first_name, name_componentse = get_first_name(name_components)
    last_name = get_last_name(name_components, second_name=False)
    # print(name)
    # print("F_name " + first_name)
    # print("L_name " + last_name)
    if not first_name:
        if name_components:
            first_name = name_components.pop(0)
        elif initials:
            first_name = initials.pop(0)

    middle_name = initials.pop(0) if initials else ''
    if not first_name:
        result = compare_frequency(last_name)
        if result['rank'] == 'true':
            first_name = result['name']
            last_name = ''
        elif result['rank'] == 'false':
            first_name = ''
            last_name = result['name']
    # elif not last_name:
    #     result = compare_frequency(first_name)
    #     if result['rank'] == 'true':
    #         first_name = result['name']
    #         last_name = ''
    #     elif result['rank'] == 'false':
    #         first_name = ''
    #         last_name = result['name']

    if name_components and middle_name == '':
        middle_name = name_components.pop(0)

    # print('Remaning ', name_components)
    return {
        'status': 'Person',
        'salutation': prefix,
        'first_name': first_name,
        'middle_name': middle_name,
        'last_name': last_name,
        'suffix': suffix,
        'initials': initials
    }


def rank_f_name_components(name, second_name=False):
    name_components = name.strip().split(' ')
    # name_components = [re.sub(r'[\.\,]*', '', component) for component in name_components]
    prefix, name_components = get_prefix(name_components)
    suffix, name_components = get_suffix(name_components)
    initials, name_components = get_initials(name_components)
    first_name, name_components = get_first_name(name_components)
    if not first_name:
        if name_components:
            first_name = name_components.pop(0)
        elif initials:
            first_name = initials.pop(0)
    middle_name = initials.pop(0) if initials else ''
    return {
        'status': 'Person',
        'salutation': prefix,
        'first_name': first_name,
        'middle_name': middle_name,
        'suffix': suffix,
        'initials': initials
    }


def rank_l_name_components(name, second_name=False):
    name_components = name.strip().split(' ')
    # name_components = [re.sub(r'[\.\,]*', '', component) for component in name_components]
    prefix, name_components = get_prefix(name_components)
    suffix, name_components = get_suffix(name_components)
    initials, name_components = get_initials(name_components)
    middle_name = initials.pop(0) if initials else ''
    last_name = get_last_name(name_components, second_name=second_name)

    return {
        'status': 'Person',
        'salutation': prefix,
        'last_name': last_name,
        'middle_name': middle_name,
        'suffix': suffix,
        'initials': initials
    }


def merge_both(f_name, l_name):
    prefixes = []
    suffixes = []
    initials = []
    middle_names = []
    if f_name.get('salutation'):
        prefixes.append(f_name.get('salutation'))
    if f_name.get('suffix'):
        suffixes.append(f_name.get('suffix'))
    if f_name.get('middle_name'):
        middle_names.append(f_name.get('middle_name'))
    if f_name.get('initials'):
        initials.append(f_name.get('initials'))
    if l_name.get('salutation'):
        prefixes.append(l_name.get('salutation'))
    if l_name.get('suffix'):
        suffixes.append(l_name.get('suffix'))
    if l_name.get('middle_name'):
        middle_names.append(l_name.get('middle_name'))
    if f_name.get('initials'):
        initials.append(l_name.get('initials'))
    prefix = ' '.join(set([pre for pre in prefixes if pre]))
    suffix = ' '.join(set([pre for pre in suffixes if pre]))
    middle_name = ' '.join(set([pre for pre in middle_names if pre]))
    last_name = l_name.get('last_name')
    first_name = f_name.get('first_name')
    return {
        'status': 'Person',
        'salutation': prefix,
        'first_name': first_name,
        'middle_name': middle_name,
        'last_name': last_name,
        'suffix': suffix,
        'initials': initials
    }


# def get_pro_suffix(full_name):
#     for data in dict_of_data:
#         if full_name in data['suffixes']['prof']:
#             print('Exist')

def get_pro_suffix(full_name):
    for suffix in dict_of_data['suffixes']['prof']:
        if full_name.lower() == suffix.lower():
            print('Exist')
            return  # You can return here to exit the loop early if found
    print('Not found')


def parser(raw_name, full_name=True):
    raw_name = raw_name.replace('.', ' ')
    # print(raw_name)
    raw_name = raw_name.strip()
    raw_name = clean_text(raw_name)

    if check_if_company(raw_name):
        return {
            'status': 'Company',
            'name': raw_name.title()
        }

    if not full_name:
        return raw_name

    names = raw_name.split(' & ')
    common_word = ""
    if len(names) > 1:

        # Split each part into words
        words1 = names[0].split()
        words2 = names[1].split()

        # Find the common word

        for word in words1:
            if word in words2:
                common_word = word
                break
    if len(common_word) <= 1:
        common_word = ''
    names[0] = names[0].replace(common_word, '')
    # print(names[1])
    name_components = rank_name_components(names[0])
    if not name_components['first_name'] and name_components['last_name']:
        name_components['first_name'] = name_components['last_name']
        name_components['last_name'] = ''

    if len(names) > 1:
        names[1] = names[1].replace(common_word, '')

        second_person = rank_name_components(names[1], second_name=True)
        # print(second_person['last_name'])

        if common_word:
            if name_components['last_name'] and not name_components['middle_name']:
                name_components['middle_name'] = name_components['last_name']

                if len(name_components['first_name']) <= 1 < len(name_components['middle_name']):
                    name_components['first_name'], name_components['middle_name'] = name_components['middle_name'], name_components['first_name']

            if second_person['last_name'] and not second_person['middle_name']:
                second_person['middle_name'] = second_person['last_name']

                if len(second_person['first_name']) <= 1 < len(second_person['middle_name']):
                    second_person['first_name'], second_person['middle_name'] = second_person['middle_name'], second_person['first_name']

            name_components['last_name'] = common_word
            second_person['last_name'] = common_word

        second_person['last_name'] = second_person['last_name'] or name_components['last_name']
        name_components['second_person'] = second_person

        if not name_components['last_name'] and second_person['last_name']:
            name_components['last_name'] = second_person['last_name']

    if len(name_components['last_name']) <= 1 < len(name_components['middle_name']):
        name_components['last_name'], name_components['middle_name'] = name_components['middle_name'], name_components['last_name']

    return name_components


def test_parser(full_name=None, first_name=None, last_name=None):
    # if first_name and last_name:
    #     temp_F = first_name
    #     temp_L = last_name
    #     first_name = parser(first_name, full_name=False)
    #     last_name = parser(last_name, full_name=False)
    #     company = False
    #
    #     if isinstance(first_name, dict) and first_name['status'].lower() == 'company':
    #         full_name = last_name
    #         company = True
    #
    #     if isinstance(last_name, dict) and last_name['status'].lower() == 'company':
    #         full_name = first_name
    #         company = True
    #
    #     if not company:
    #         # name = get_first_name([first_name])
    #         f_name_list = rank_f_name_components(first_name)
    #         l_name_list = rank_l_name_components(last_name)
    #         return merge_both(f_name_list, l_name_list)
    #
    #     else:
    #         return {
    #             'status': 'Company',
    #             'name': '{} {}'.format(temp_F, temp_L)
    #         }

    # if isinstance(full_name, dict) and full_name['status'].lower() == 'company':
    #     return full_name

    full_name = full_name or first_name or last_name
    full_name = full_name.replace(',', ' ')
    name = parser(full_name)
    # print(name)
    return name


# fn = 'Yanina V'#'Trust Company'
# ln = 'Cruzado'#'Of Oklahoma'
# fl_name = '1000 Lincoln Trust'  # 'HEIDRICK GARY & REBECCA LIV TR'
# name_components = test_parser(full_name=fl_name)
# print(name_components)
# fl_name = fl_name or fn + ' ' + ln

# if isinstance(name_components, list):
#     print('input: {}, output: {name}'.format(fl_name, **name_components[0]))
# else:
#     print('full_name: {}, first_name: {}, last_name: {}'.format(fl_name, fn, ln))
#     print('output: \n\tfirst_name: {first_name}\n\tmiddle_name: {middle_name}\n\tlast_name: {last_name}'.format(
#         **name_components))
#     second_person = name_components.get('second_person') or {}
#     if second_person:
#         print(
#             '\n  second_person: \n\tfirst_name: {first_name}\n\tmiddle_name: {middle_name}\n\tlast_name: {last_name}'.format(
#                 **second_person))


if __name__ == "__main__":
    # name_list = ["Robert Downey jr." ,"Badhorn Rob", "Starling, Albert J", "Smith, Logan", "Manning, David", "Starling, Brian"]

    # parsed_name = test_parser(full_name="Baynard J Ward & Mary D Ward")

    parsed_name = test_parser(full_name="board of conference the un meth chur")
    print(parsed_name)

    # df = pd.read_csv("E:/LeadFusion Projects/LeadFusion CSV files/owner_full_names.csv")
    # df = df.iloc[:2000]
    #
    # df[['owner1_first_name', 'owner1_middle_name', 'owner1_last_name', 'owner1_suffix', 'owner1_prefix',
    #     'owner2_first_name', 'owner2_middle_name', 'owner2_last_name', 'owner2_suffix', 'owner2_prefix']] = df.apply(lambda x: pd.Series(name_parser(full_name=x['owner_fullname'])), axis=1)
    #
    # df.to_csv("name_parser.csv", index=False)
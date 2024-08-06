import re

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
            'llc', 'lp', 'inc', 'l l c', 'company', 'l.l.c.', 'llp', 'grp',
            'l.l.p.', 'group', 'pc', 'p.c.', '%', 'partnerhip', 'ltd',
            'partnership', 'limited', 'rr', 'co', 'partners',
            "training", "handicapp", "association", "investments", "veterans", "holdings", "lllp",
            "assoc", "commonwealth", "housing", "corp", "supply", "city", "authority", "church", "mental",
            "corporation", "corporat", "churchs", "management"
        ]
        name_components = raw_name.strip().lower().split(' ')

        company_name = [c for c in name_components if c.lower() in company_indicators]
        # company_name = [e for e in company_indicators if e.lower() in raw_name.lower()]

        if company_name:
            return True
        else:
            return False


def clean_text(name):
    potential_impurities = ["trust", "family", "revoc", "living", "trust", "family", "rev", "trs", "et al",
                            "liv tr", "fam tr", "living trust", "decedents", "revocable", "liv", "suppl", "tr",
                            "irrev", "fam", "family", "mortgage", "development", "touches", "amended", "etal"]

    # name_components = re.sub(punctuation_re, '', name or '').strip().lower().split(' ')
    name_components = name.strip().lower().split(' ')
    name_components = [c for c in name_components if c.lower() not in potential_impurities]
    return ' '.join(name_components)


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


def get_pro_suffix(full_name):
    for suffix in dict_of_data['suffixes']['prof']:
        if full_name.lower() == suffix.lower():
            print('Exist')
            return  # You can return here to exit the loop early if found
    print('Not found')


def split_name(name):
    if check_if_company(name):
        return name

    result = {}
    name = clean_text(name).replace('.', '')

    suffix, component = get_suffix(name.split())
    result['suffix'] = suffix
    name = name.replace(suffix, '')

    component = name.split(', ')
    result['last_name'] = component[0]
    if len(component) > 1:
        sub_component = component[1].split()
        result['first_name'] = sub_component[0]
        if len(sub_component) > 1:
            result['middle_name'] = sub_component[1]
    return result


if __name__ == '__main__':
    print(split_name('Matrinez, Solis Justin Michael'))

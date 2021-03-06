# -*- coding: utf-8 -*-

#Default Group Ids
BOARD_MEMBERS_GID = 'board_members'
HOME_OWNERS_GID = 'home_owners'
RENTERS_GID = 'renters'
PROPERTY_MANAGERS_GID = 'property_managers'
WALKERS_MEMBERS_GID = 'walkers'
GROUP_A_WALKERS_GID = 'walkers_a'
GROUP_B_WALKERS_GID = 'walkers_b'
GROUP_C_WALKERS_GID = 'walkers_c'
GROUP_D_WALKERS_GID = 'walkers_d'
MAP_GROUP_ONE_GID = 'division_map_one'
MAP_GROUP_TWO_GID = 'division_map_two'

#GROUP_E_WALKERS_GID = 'walkers_e'
WALKERS_GROUP_IDS = [GROUP_A_WALKERS_GID,
                     GROUP_B_WALKERS_GID,
                     GROUP_C_WALKERS_GID,
                     GROUP_D_WALKERS_GID]

GROUP_TITLE_DICT = {BOARD_MEMBERS_GID: u'Board Members',
                    HOME_OWNERS_GID: u'Home Owners',
                    RENTERS_GID: u'Renters',
                    PROPERTY_MANAGERS_GID: u'Property Managers',
                    WALKERS_MEMBERS_GID: u'Walkers',
                    GROUP_A_WALKERS_GID: u'Walkers Group A',
                    GROUP_B_WALKERS_GID: u'Walkers Group B',
                    GROUP_C_WALKERS_GID: u'Walkers Group C',
                    GROUP_D_WALKERS_GID: u'Walkers Group D',
                    MAP_GROUP_ONE_GID: u'Division Map One Group',
                    MAP_GROUP_TWO_GID: u'Division Map Two Group'}

PROPERTY_ROLE_DICT = {HOME_OWNERS_GID: u'Owner',
                      RENTERS_GID: u'Renter',
                      PROPERTY_MANAGERS_GID: u'Property Manager'}

PROPERTY_ROLE_TO_HOME_ATTRIBUTE_LOOKUP_DICT = {HOME_OWNERS_GID: ['owner_one', 'owner_two'],
                      RENTERS_GID: ['resident_one', 'resident_two'],
                      PROPERTY_MANAGERS_GID: ['property_manager']}


HOME_ROLE_TO_ATTRIBUTE_LOOKUP_DICT = {'owner_one':'hoa_owners',
                                      'owner_two':'hoa_owners',
                                      'resident_one':'hoa_renters',
                                      'resident_two':'hoa_renters',
                                      'property_manager':'hoa_property_managers'}

DIV_NUMBER_STRINGS = ['1', '2']

LOT_NUMBER_STRINGS = ['001', '002', '003', '004', '005', '006', '007', '008', '009', '010',
                      '011', '012', '013', '014', '015', '016', '017', '018', '019', '020',
                      '021', '022', '023', '024', '025', '026', '027', '028', '029', '030',
                      '031', '032', '033', '034', '035', '036', '037', '038', '039', '040',
                      '041', '042', '043', '044', '045', '046', '047', '048', '049', '050',
                      '051', '052', '053', '054', '055', '056', '057', '058', '059', '060',
                      '061', '062', '063', '064', '065', '066', '067', '068', '069', '070',
                      '071', '072', '073', '074', '075', '076', '077', '078', '079', '080',
                      '081', '082', '083', '084', '085', '086', '087', '088', '089', '090',
                      '091', '092', '093', '094', '095', '096', '097', '098', '099', '100']


DIVISION_ONE = ['1_001', '1_002', '1_003', '1_004', '1_005', '1_006', '1_007', '1_008', '1_009', '1_010',
                '1_011', '1_012', '1_013', '1_014', '1_015', '1_016', '1_017', '1_018', '1_019', '1_020',
                '1_021', '1_022', '1_023', '1_024', '1_025', '1_026', '1_027', '1_028', '1_029', '1_030',
                '1_031', '1_032', '1_033', '1_034', '1_035', '1_036', '1_037', '1_038', '1_039', '1_040',
                '1_041', '1_042', '1_043', '1_044', '1_045', '1_046', '1_047', '1_048', '1_049', '1_050',
                '1_051', '1_052', '1_053', '1_054', '1_055', '1_056', '1_057', '1_058', '1_059', '1_060',
                '1_061', '1_062', '1_063', '1_064', '1_065', '1_066', '1_067', '1_068', '1_069', '1_070',
                '1_071', '1_072', '1_073', '1_074', '1_075', '1_076', '1_077', '1_078', '1_079', '1_080',
                '1_081', '1_082', '1_083', '1_084', '1_085', '1_086', '1_087', '1_088', '1_089', '1_090',
                '1_091', '1_092', '1_093', '1_094', '1_095', '1_096', '1_097', '1_098', '1_099', '1_100']

DIVISION_TWO = ['2_001', '2_002', '2_003', '2_004', '2_005', '2_006', '2_007', '2_008', '2_009', '2_010',
                '2_011', '2_012', '2_013', '2_014', '2_015', '2_016', '2_017', '2_018', '2_019', '2_020',
                '2_021', '2_022', '2_023', '2_024', '2_025', '2_026', '2_027', '2_028', '2_029', '2_030',
                '2_031', '2_032', '2_033', '2_034', '2_035', '2_036', '2_037', '2_038', '2_039', '2_040',
                '2_041', '2_042', '2_043', '2_044', '2_045', '2_046', '2_047', '2_048', '2_049', '2_050',
                '2_051', '2_052', '2_053', '2_054', '2_055', '2_056', '2_057', '2_058', '2_059', '2_060',
                '2_061', '2_062', '2_063', '2_064', '2_065', '2_066', '2_067', '2_068', '2_069', '2_070',
                '2_071', '2_072', '2_073', '2_074', '2_075', '2_076', '2_077', '2_078']

DIVISION_BY_THREE = {
    'walkers_a': ['1_001', '1_002', '1_003', '1_004', '1_005', '1_006', '1_007', '1_008', '1_009', '1_010',
                '1_011', '1_012', '1_013', '1_014', '1_015', '1_016', '1_017', '1_018', '1_019', '1_020',
                '1_021', '1_022', '1_023', '1_024', '1_025', '1_026', '1_027', '1_028', '1_029', '1_030',
                '1_031', '1_032', '1_033', '1_034', '1_035', '1_036', '1_037', '1_038', '1_039', '1_040',
                '1_041', '1_042', '1_085', '1_086', '1_087', '1_088', '1_089', '1_090', '1_091', '1_092',
                '1_093', '1_094', '1_095', '1_096', '1_097', '1_098', '1_099', '1_100'],
    'walkers_b': ['1_043', '1_044', '1_045', '1_046', '1_047', '1_048', '1_049', '1_050', '1_051', '1_052',
                '1_053', '1_054', '1_055', '1_056', '1_057', '1_058', '1_059', '1_060', '1_061', '1_062',
                '1_063', '1_064', '1_065', '1_066', '1_067', '1_068', '1_069', '1_070', '1_071', '1_072',
                '1_073', '1_074', '1_075', '1_076', '1_077', '1_078', '1_079', '1_080', '1_081', '1_082',
                '1_083', '1_084', '2_060', '2_061', '2_062', '2_063', '2_064', '2_065', '2_066', '2_067',
                '2_068', '2_069', '2_070', '2_071', '2_072', '2_073', '2_074', '2_075', '2_076', '2_077',
                '2_078'],
    'walkers_c': ['2_001', '2_002', '2_003', '2_004', '2_005', '2_006', '2_007', '2_008', '2_009', '2_010',
                '2_011', '2_012', '2_013', '2_014', '2_015', '2_016', '2_017', '2_018', '2_019', '2_020',
                '2_021', '2_022', '2_023', '2_024', '2_025', '2_026', '2_027', '2_028', '2_029', '2_030',
                '2_031', '2_032', '2_033', '2_034', '2_035', '2_036', '2_037', '2_038', '2_039', '2_040',
                '2_041', '2_042', '2_043', '2_044', '2_045', '2_046', '2_047', '2_048', '2_049', '2_050',
                '2_051', '2_052', '2_053', '2_054', '2_055', '2_056', '2_057', '2_058', '2_059']}

DIVISION_BY_FOUR = {
    'walkers_a': ['1_001', '1_002', '1_003', '1_004', '1_005', '1_006', '1_007', '1_008', '1_009', '1_010',
                '1_011', '1_012', '1_013', '1_014', '1_015', '1_016', '1_017', '1_018', '1_019', '1_020',
                '1_021', '1_022', '1_023', '1_024', '1_025', '1_026', '1_027', '1_028', '1_029', '1_030',
                '1_031', '1_032', '1_033', '1_034', '1_035', '1_036', '1_037', '1_038', '1_039', '1_040',
                '1_041', '1_042', '1_094', '1_095', '1_096', '1_097', '1_098', '1_099', '1_100'],
    'walkers_b': ['1_043', '1_044', '1_045', '1_046', '1_047', '1_048', '1_049', '1_050', '1_051', '1_052',
                '1_053', '1_054', '1_055', '1_056', '1_057', '1_058', '1_059', '1_060', '1_061', '1_062',
                '1_063', '1_064', '1_065', '1_066', '1_067', '1_068', '1_069', '1_070', '1_071', '1_072',
                '1_073', '1_074', '1_075', '1_076', '1_077', '1_078', '1_079', '1_080', '1_081', '1_082',
                '1_083', '1_084', '1_085', '1_086', '1_087', '1_088', '1_089', '1_090', '1_091', '1_092',
                '1_093'],
    'walkers_c': ['2_001', '2_002', '2_003', '2_004', '2_005', '2_006', '2_007', '2_008', '2_009', '2_010',
                '2_011', '2_012', '2_013', '2_014', '2_015', '2_016', '2_017', '2_018', '2_019', '2_020',
                '2_021', '2_022', '2_023', '2_024', '2_025', '2_026', '2_027', '2_028', '2_029', '2_030',
                '2_031', '2_032', '2_033', '2_034', '2_072', '2_073', '2_074', '2_075', '2_076', '2_077',
                '2_078'],
    'walkers_d': ['2_035', '2_036', '2_037', '2_038', '2_039', '2_040', '2_041', '2_042', '2_043', '2_044',
                '2_045', '2_046', '2_047', '2_048', '2_049', '2_050', '2_051', '2_052', '2_053', '2_054',
                '2_055', '2_056', '2_057', '2_058', '2_059', '2_060', '2_061', '2_062', '2_063', '2_064',
                '2_065', '2_066', '2_067', '2_068', '2_069', '2_070', '2_071']}

DIVISION_BY_FIVE = {
    'walkers_a': ['1_001', '1_002', '1_003', '1_004', '1_005', '1_006', '1_007', '1_008', '1_009', '1_010',
                '1_011', '1_012', '1_013', '1_014', '1_015', '1_016', '1_017', '1_018', '1_019', '1_020',
                '1_021', '1_022', '1_023', '1_024', '1_025', '1_026', '1_027', '1_028', '1_029', '1_030',
                '1_031', '1_032', '1_033', '1_034', '1_035', '1_036', '1_037', '1_038', '1_039', '1_040',
                '1_041', '1_042'],
    'walkers_b': ['1_043', '1_044', '1_045', '1_046', '1_047', '1_048', '1_049', '1_050', '1_051', '1_052',
                '1_053', '1_054', '1_055', '1_056', '1_057', '1_058', '1_059', '1_060', '1_061', '1_062',
                '1_063', '1_064', '1_065', '1_066', '1_067', '1_068', '1_069', '1_070', '1_071', '1_072',
                '1_073', '1_074', '1_075', '1_076', '1_077', '1_078', '1_079', '1_080', '1_081', '1_082',
                '1_083', '1_084'],
    'walkers_c': ['1_085', '1_086', '1_087', '1_088', '1_089', '1_090', '1_091', '1_092', '1_093', '1_094',
                '1_095', '1_096', '1_097', '1_098', '1_099', '1_100', '2_059', '2_060', '2_061', '2_062',
                '2_063', '2_064', '2_065', '2_066', '2_067', '2_068', '2_069', '2_070', '2_071', '2_072',
                '2_073', '2_074', '2_075', '2_076', '2_077', '2_078'],
    'walkers_d': ['2_035', '2_036', '2_037', '2_038', '2_039', '2_040', '2_041', '2_042', '2_043', '2_044',
                '2_045', '2_046', '2_047', '2_048', '2_049', '2_050', '2_051', '2_052', '2_053', '2_054',
                '2_055', '2_056', '2_057', '2_058'],
    'walkers_e': ['2_001', '2_002', '2_003', '2_004', '2_005', '2_006', '2_007', '2_008', '2_009', '2_010',
                '2_011', '2_012', '2_013', '2_014', '2_015', '2_016', '2_017', '2_018', '2_019', '2_020',
                '2_021', '2_022', '2_023', '2_024', '2_025', '2_026', '2_027', '2_028', '2_029', '2_030',
                '2_031', '2_032', '2_033', '2_034']}


HOUSE_INSPECTION_STATE_TITLES = {'draft':'Draft',
                                 'initial_inspection':'Initial Inspection',
                                 'secondary_inspection':'Secondary Inspection',
                                 'closed':'Closed'}

HOME_INSPECTION_STATE_TITLES = {'failed_final':'Failed Secondary Inspection',
                                'failed_initial':'Failed Initial Inspection',
                                'passed':'Passed',
                                'pending':'Pending',
                                'remedied':'Remedied'}

# TEST_DIVISION_BY_THREE = {'walkers_a': ['1_001', '1_002'],
#                           'walkers_b': ['1_003', '1_004'],
#                           'walkers_c': ['1_005']}
#
# TEST_DIVISION_BY_FOUR = {'walkers_a': ['1_001', '1_002'],
#                          'walkers_b': ['1_003'],
#                          'walkers_c': ['1_004'],
#                          'walkers_d':['1_005']}
#
# TEST_DIVISION_BY_FIVE = {'walkers_a':['1_003'],
#                           'walkers_b':['1_002'],
#                           'walkers_c':['1_003'],
#                           'walkers_d':['1_004'],
#                           'walkers_e':['1_005'],}
#
# DIVISION_BY_THREE = TEST_DIVISION_BY_THREE
# DIVISION_BY_FOUR = TEST_DIVISION_BY_FOUR
# DIVISION_BY_FIVE = TEST_DIVISION_BY_FIVE

LOT_DIVISION_DICT = {3: DIVISION_BY_THREE,
                     4: DIVISION_BY_FOUR,
                     5: DIVISION_BY_FIVE}

IHOAHOUSEINSPECTION_FIELDSETS = ['roof',
                                 'gutters',
                                 'exterior_paint',
                                 'decks',
                                 'entry_way',
                                 'paved_surfaces',
                                 'landscaping',
                                 'general_maintenance']

IHOAHOUSEINSPECTION_FIELDSET_TITLES_DICT = {'roof':'Roof',
                                            'gutters':'Gutters',
                                            'exterior_paint':'Exterior Paint',
                                            'decks':'Decks',
                                            'entry_way':'Entry Way',
                                            'paved_surfaces':'Paved Surfaces',
                                            'landscaping':'Landscaping',
                                            'general_maintenance':'General Maintenance'}

REQUIRED_ACTION_DICT = {'roof': {'clean': 'August 31',
                                 'repair': 'August 31',
                                 'replace': 'June'},
                        'gutters': {'clean': 'August 31',
                                    'repair': 'August 31',
                                    'replace': 'June'},
                        'exterior_paint': {'clean': 'August 31',
                                           'repair': 'August 31',
                                           'replace': 'June'},
                        'decks': {'clean': 'July 31',
                                  'repair': 'August 31',
                                  'replace': 'June'},
                        'entry_way': {'clean': 'July 31',
                                      'repair': 'August 31',
                                      'replace': 'June'},
                        'paved_surfaces': {'clean': 'July 31',
                                           'repair': 'August 31',
                                           'replace': 'June'},
                        'landscaping': {'clean': 'July 31',
                                        'repair': 'August 31',
                                        'replace': 'June'},
                        'general_maintenance': {'clean': 'July 31',
                                                'repair': 'August 31',
                                                'replace': 'June'}}

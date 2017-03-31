import logging
from collections import defaultdict
from operator import itemgetter
from five import grok
from plone import api
from plone.api.exc import MissingParameterError
from plone.protect.utils import addTokenToUrl

from Products.CMFCore.utils import getToolByName

from docent.hoa.houses.content.hoa_neighborhood import IHOANeighborhood
from docent.hoa.houses.content.hoa_house_inspection import IHOAHouseInspection
from docent.hoa.houses.content.hoa_annual_inspection import IHOAAnnualInspection

grok.templatedir('templates')

class WalkerAssignments(grok.View):
    grok.context(IHOANeighborhood)
    grok.require("zope2.View")
    grok.template("walker_assignments")
    grok.name("walker-assignments")

    def update(self):
        """
        get email html structure for all home owners and set them as view attribute
        """
        context = self.context
        context_path = '/'.join(context.getPhysicalPath())
        catalog = getToolByName(context, 'portal_catalog')

        current_inspection_brains = context.portal_catalog.searchResults(
                                               object_provides=IHOAAnnualInspection.__identifier__,
                                               sort_on="created",
                                               sort_order="descending")

        current_inspection_state = ''
        current_inspection = ''
        if len(current_inspection_brains) >= 1:
            current_inspection_brain = current_inspection_brains[0]
            current_inspection_state = current_inspection_brain.review_state
            current_inspection = current_inspection_brain.Title

        home_inspection_state = ''
        if current_inspection_state == 'initial_inspection':
            home_inspection_state = 'pending'
        elif current_inspection_state == 'secondary_inspection':
            home_inspection_state = 'failed_initial'

        house_inspection_brains = []
        if home_inspection_state:
            house_inspection_brains = catalog(path={'query': context_path, 'depth': 2},
                                              object_provides=IHOAHouseInspection.__identifier__,
                                              review_state=home_inspection_state)

        street_dict = defaultdict(list)
        for hi_brain in house_inspection_brains:
            hi_obj = hi_brain.getObject()
            #import pdb;pdb.set_trace()
            if hi_obj.id == '1_008':
                print 'hi_obj.id: 1_008'
            hi_home_obj = hi_obj.aq_parent
            street = getattr(hi_home_obj, 'street_number', '')
            address = getattr(hi_home_obj, 'street_address', '')
            street_address = '%s %s' % (street, address)
            home_listing_dict = {'url':'%s/@@home-inspection' % hi_home_obj.absolute_url(),
                                 'div':getattr(hi_home_obj, 'div', ''),
                                 'lot':getattr(hi_home_obj, 'lot', ''),
                                 'address':street_address,
                                 'map':''}
            # home_listing_tuple = (hi_home_obj.absolute_url(),
            #                       getattr(hi_home_obj, 'div', ''),
            #                       getattr(hi_home_obj, 'lot', ''),
            #                       street_address,
            #                       '')
            # street_dict[address].add(home_listing_tuple)
            street_dict[address].append(home_listing_dict)

        streets = sorted(street_dict.keys())
        #import pdb;pdb.set_trace()
        for street in streets:
            street_dict[street] = sorted(street_dict[street], key=itemgetter('address'))

        self.current_inspection = current_inspection
        self.streets = streets
        self.street_dict = street_dict


    def getTableRowStructure(self, home_listing_dict):
        table_row_structure = ''
        table_row_structure += '<td><a class="inspect-button" href="%s">Inspect</a></td>' % home_listing_dict.get('url')
        table_row_structure += '<td>%s</td>' % home_listing_dict.get('div')
        table_row_structure += '<td>%s</td>' % home_listing_dict.get('lot')
        table_row_structure += '<td>%s</td>' % home_listing_dict.get('address')
        table_row_structure += '<td>%s</td>' % home_listing_dict.get('map')

        return table_row_structure
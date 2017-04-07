import logging
from datetime import date
from collections import Counter
from plone import api
from plone.dexterity.content import Container
from plone.directives import form
from plone.indexer import indexer
from plone.namedfile.field import NamedBlobImage
from plone.supermodel.directives import fieldset
from Products.CMFCore.utils import getToolByName
from zope import schema
from zope.interface import provider, invariant, Invalid
from zope.schema.interfaces import IContextAwareDefaultFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from z3c.form.browser.radio import RadioFieldWidget

from docent.hoa.houses.content.hoa_house import IHOAHouse
from docent.hoa.houses.content.hoa_house_inspection import IHOAHouseInspection
from docent.hoa.houses.registry import IHOAHomeLookupRegistry
from docent.hoa.houses.app_config import HOME_ROLE_TO_ATTRIBUTE_LOOKUP_DICT, LOT_DIVISION_DICT, WALKERS_GROUP_IDS
from docent.hoa.houses.registry import (addHomeToLookupRegistry,
                                        removeHomeFromLookupRegistry,
                                        clearAllHomesForMember,
                                        addCurrentHomeRoles)

from docent.hoa.houses import _

logger = logging.getLogger("Plone")

group_numbers_vocab = SimpleVocabulary([SimpleTerm(value=3, title=_(u'3')),
                                  SimpleTerm(value=4, title=_(u'4')),
                                  SimpleTerm(value=5, title=_(u'5')), ])

def computeTitle():
    date_obj = date.today()
    date_str = date_obj.strftime('%Y')

    return u'Annual Inspection %s' % date_str

class DoubleMemberInGroup(Invalid):
    __doc__ = _(u"You can't have the same member listed twice in a weed walk group.")


class MinimumGroups(Invalid):
    __doc__ = _(u"Groups A, B, and C must have week walkers assigned.")


class IHOAAnnualInspection(form.Schema):
    """
    """

    form.mode(title='hidden')
    title = schema.TextLine(
        title=_(u"Title"),
        required=False,
        defaultFactory=computeTitle,
    )

    form.mode(house_inspection_title='hidden')
    house_inspection_title = schema.TextLine(
        title=_(u"House Inspection Title"),
        required=False,
    )

    start_date = schema.Date(
        title=_(u"Start Date"),
        description=_(u""),
    )

    end_date = schema.Date(
        title=_(u"End Date"),
        description=_(u""),
    )

    form.widget(pic_req=RadioFieldWidget)
    pic_req = schema.Choice(
        title=_(u'Picture Rqd if Failed?'),
        description=_(u''),
        source=SimpleVocabulary([SimpleTerm(value=True,
                                            title=u"Yes"),
                                 SimpleTerm(value=False,
                                            title=U"No")])
    )

    # number_of_groups = schema.Choice(
    #     title=_(u"Number of Groups"),
    #     description=_(u""),
    #     vocabulary=group_numbers_vocab,
    #     required=True,
    # )

    fieldset('team_a',
        label=u'Team A',
        description=u'',
        fields=['group_a_member_one',
                'group_a_member_two', ]
    )

    group_a_member_one = schema.Choice(
        title=_(u"Group A Member One"),
        description=_(u""),
        vocabulary=u'docent.hoa.walkers',
        required=False,
    )

    group_a_member_two = schema.Choice(
        title=_(u"Group A Member Two"),
        description=_(u""),
        vocabulary=u'docent.hoa.walkers',
        required=False,
    )

    fieldset('team_b',
        label=u'Team B',
        description=u'',
        fields=['group_b_member_one',
                'group_b_member_two', ]
    )

    group_b_member_one = schema.Choice(
        title=_(u"Group B Member One"),
        description=_(u""),
        vocabulary=u'docent.hoa.walkers',
        required=False,
    )

    group_b_member_two = schema.Choice(
        title=_(u"Group B Member Two"),
        description=_(u""),
        vocabulary=u'docent.hoa.walkers',
        required=False,
    )

    fieldset('team_c',
        label=u'Team C',
        description=u'',
        fields=['group_c_member_one',
                'group_c_member_two', ]
    )

    group_c_member_one = schema.Choice(
        title=_(u"Group C Member One"),
        description=_(u""),
        vocabulary=u'docent.hoa.walkers',
        required=False,
    )

    group_c_member_two = schema.Choice(
        title=_(u"Group C Member Two"),
        description=_(u""),
        vocabulary=u'docent.hoa.walkers',
        required=False,
    )

    fieldset('team_d',
        label=u'Team D',
        description=u'',
        fields=['group_d_member_one',
                'group_d_member_two', ]
    )

    group_d_member_one = schema.Choice(
        title=_(u"Group D Member One"),
        description=_(u""),
        vocabulary=u'docent.hoa.walkers',
        required=False,
    )

    group_d_member_two = schema.Choice(
        title=_(u"Group D Member Two"),
        description=_(u""),
        vocabulary=u'docent.hoa.walkers',
        required=False,
    )

    fieldset('team_e',
        label=u'Team E',
        description=u'',
        fields=['group_e_member_one',
                'group_e_member_two', ]
    )

    group_e_member_one = schema.Choice(
        title=_(u"Group E Member One"),
        description=_(u""),
        vocabulary=u'docent.hoa.walkers',
        required=False,
    )

    group_e_member_two = schema.Choice(
        title=_(u"Group E Member Two"),
        description=_(u""),
        vocabulary=u'docent.hoa.walkers',
        required=False,
    )

    # @invariant
    # def minimumThreeGroups(data):
    #     assigned_members = 0
    #     group_a_member_one = getattr(data, 'group_a_member_one', None)
    #     if group_a_member_one:
    #         assigned_members += 1
    #     group_a_member_two = getattr(data, 'group_a_member_two', None)
    #     if group_a_member_two:
    #         assigned_members += 1
    #     group_b_member_one = getattr(data, 'group_b_member_one', None)
    #     if group_b_member_one:
    #         assigned_members += 1
    #     group_b_member_two = getattr(data, 'group_b_member_two', None)
    #     if group_b_member_two:
    #         assigned_members += 1
    #     group_c_member_one = getattr(data, 'group_c_member_one', None)
    #     if group_c_member_one:
    #         assigned_members += 1
    #     group_c_member_two = getattr(data, 'group_c_member_two', None)
    #     if group_c_member_two:
    #         assigned_members += 1
    #
    #     if group_a_member_one == group_a_member_two:
    #         raise DoubleMemberInGroup(_(u"You can't have the same member twice in Group A."))
    #
    #     if group_b_member_one == group_b_member_two:
    #         raise DoubleMemberInGroup(_(u"You can't have the same member twice in Group B."))
    #
    #     if group_c_member_one == group_c_member_two:
    #         raise DoubleMemberInGroup(_(u"You can't have the same member twice in Group C."))
    #
    #     if assigned_members != 6:
    #         raise MinimumGroups()

    # @invariant
    # def validateGroups(data):
    #     assigned_members = []
    #     for m_id in ['group_a_member_one'
    #                  'group_a_member_two',
    #                  'group_b_member_one',
    #                  'group_b_member_two',
    #                  'group_c_member_one',
    #                  'group_c_member_two',
    #                  'group_d_member_one',
    #                  'group_d_member_two',
    #                  'group_e_member_one',
    #                  'group_e_member_two']:
    #         a_value = getattr(data, m_id, None)
    #         if a_value:
    #             assigned_members.append(a_value)
    #
    #     sorted_dict = Counter(assigned_members)
    #     import pdb;pdb.set_trace()
    #     for k, v in sorted_dict.iteritems():
    #         if v >= 2:
    #             member_data = api.user.get(userid=k)
    #             fullname = member_data.getProperty('fullname')
    #             portal = api.portal.get()
    #             api.portal.show_message(message="%s has been assigned to multiple groups." % fullname,
    #                                     request=portal.REQUEST,
    #                                     type='warning')






class HOAAnnualInspection(Container):
    """
    """

    def after_object_added_processor(self, context, event):
        self.generate_house_inspection_title()
        self.add_walkers_to_groups()
        context_state = api.content.get_state(obj=self)
        if context_state not in ['draft', 'closed']:
            self.assign_security()

    def after_edit_processor(self):
        self.add_walkers_to_groups()
        context_state = api.content.get_state(obj=self)
        if context_state not in ['draft', 'closed']:
            self.assign_security()

    def after_transition_processor(self):
        context_state = api.content.get_state(obj=self)
        if context_state == 'initial_inspection':
            self.propagate_house_inspections()
            self.assign_security()

    def add_walkers_to_groups(self):
        for g_id in WALKERS_GROUP_IDS:
            current_members = api.user.get_users(groupname=g_id)
            for a_member in current_members:
                api.group.remove_user(groupname=g_id, user=a_member)

        group_a_member_one = getattr(self, 'group_a_member_one', None)
        group_a_member_two = getattr(self, 'group_a_member_two', None)
        group_b_member_one = getattr(self, 'group_b_member_one', None)
        group_b_member_two = getattr(self, 'group_b_member_two', None)
        group_c_member_one = getattr(self, 'group_c_member_one', None)
        group_c_member_two = getattr(self, 'group_c_member_two', None)
        group_d_member_one = getattr(self, 'group_d_member_one', None)
        group_d_member_two = getattr(self, 'group_d_member_two', None)
        group_e_member_one = getattr(self, 'group_e_member_one', None)
        group_e_member_two = getattr(self, 'group_e_member_two', None)

        if group_a_member_one:
            api.group.add_user(groupname='walkers_a', username=group_a_member_one)
        if group_a_member_two:
            api.group.add_user(groupname='walkers_a', username=group_a_member_two)
        if group_b_member_one:
            api.group.add_user(groupname='walkers_b', username=group_b_member_one)
        if group_b_member_two:
            api.group.add_user(groupname='walkers_b', username=group_b_member_two)
        if group_c_member_one:
            api.group.add_user(groupname='walkers_c', username=group_c_member_one)
        if group_c_member_two:
            api.group.add_user(groupname='walkers_c', username=group_c_member_two)
        if group_d_member_one:
            api.group.add_user(groupname='walkers_d', username=group_d_member_one)
        if group_d_member_two:
            api.group.add_user(groupname='walkers_d', username=group_d_member_two)
        if group_e_member_one:
            api.group.add_user(groupname='walkers_e', username=group_e_member_one)
        if group_e_member_two:
            api.group.add_user(groupname='walkers_e', username=group_e_member_two)


    def getNumberOfGroups(self):
        context = self
        group_a_member_one = getattr(self, 'group_a_member_one', None)
        group_a_member_two = getattr(self, 'group_a_member_two', None)
        group_b_member_one = getattr(self, 'group_b_member_one', None)
        group_b_member_two = getattr(self, 'group_b_member_two', None)
        group_c_member_one = getattr(self, 'group_c_member_one', None)
        group_c_member_two = getattr(self, 'group_c_member_two', None)
        group_d_member_one = getattr(self, 'group_d_member_one', None)
        group_d_member_two = getattr(self, 'group_d_member_two', None)
        group_e_member_one = getattr(self, 'group_e_member_one', None)
        group_e_member_two = getattr(self, 'group_e_member_two', None)

        number_of_groups = 0
        if group_a_member_one or group_a_member_two:
            number_of_groups += 1
        if group_b_member_one or group_b_member_one:
            number_of_groups += 1
        if group_c_member_one or group_c_member_two:
            number_of_groups += 1
        if group_d_member_one or group_d_member_two:
            number_of_groups += 1
        if group_e_member_one or group_e_member_two:
            number_of_groups += 1

        return number_of_groups


    def assign_security(self):
        context = self
        parent_container = context.aq_parent
        if parent_container.portal_type != "hoa_neighborhood":
            #woah something went wrong
            return
        #number_of_groups = getattr(context, 'number_of_groups', 3)
        number_of_groups = context.getNumberOfGroups()
        lot_division_dict = LOT_DIVISION_DICT.get(number_of_groups)
        for walker_group_id in lot_division_dict:
            homes_assigned_by_id = lot_division_dict.get(walker_group_id)
            for home_id in homes_assigned_by_id:
                home_obj = parent_container.get(home_id)
                if home_obj:
                    #clear previous group roles
                    for wg_id in WALKERS_GROUP_IDS:
                        api.group.revoke_roles(groupname=wg_id,
                                               roles=['Reader'],
                                               obj=home_obj)
                    #home_obj.manage_delLocalRoles(WALKERS_GROUP_IDS)
                    #set new role
                    api.group.grant_roles(groupname=walker_group_id,
                                          roles=['Reader'],
                                          obj=home_obj)
                    home_obj.reindexObjectSecurity()
                    home_inspections = home_obj.listFolderContents(contentFilter={"portal_type":"hoa_house_inspection",
                                                                         "sort_on":"created",
                                                                         "sort_order":"ascending"})
                    for home_insp in home_inspections:
                        for wg_id in WALKERS_GROUP_IDS:
                            api.group.revoke_roles(groupname=wg_id,
                                                   roles=['Editor', 'Reviewer'],
                                                   obj=home_insp)
                            home_insp.reindexObjectSecurity()

                    house_inspection_title = getattr(context, 'house_inspection_title', '')
                    current_hi = getattr(home_obj, house_inspection_title, None)
                    if current_hi:
                        api.group.grant_roles(groupname=walker_group_id,
                                              roles=['Editor', 'Reviewer'],
                                              obj=current_hi)
                        current_hi.reindexObjectSecurity()


    def generate_house_inspection_title(self):
        today = date.today()
        setattr(self, 'house_inspection_title', today.strftime('%Y'))

    def propagate_house_inspections(self):
        context = self
        parent_container = context.aq_parent
        pc_path = '/'.join(parent_container.getPhysicalPath())
        catalog = getToolByName(parent_container, 'portal_catalog')
        house_brains = catalog(path={'query': pc_path, 'depth': 1},
                               object_provides=IHOAHouse.__identifier__,)
        house_inspection_title = getattr(self, 'house_inspection_title', '')
        if not house_inspection_title:
            today = date.today()
            house_inspection_title = today.strftime('%Y')

        added_inspections = 0
        for house_brain in house_brains:
            house_obj = house_brain.getObject()
            house_obj_title = getattr(house_obj, 'title', 'unknown house')
            if house_inspection_title not in house_obj:
                api.content.create(container=house_obj,
                                   type='hoa_house_inspection',
                                   id=house_inspection_title,
                                   title=house_obj_title,
                                   safe_id=True)
                added_inspections += 1

        api.portal.show_message(message=u"%s houses prepared for annual inspection." % added_inspections,
                                request=context.REQUEST,
                                type='info')

    def verifyFirstInspectionComplete(self):
        context = self
        parent_container = context.aq_parent
        parent_container_path = '/'.join(parent_container.getPhysicalPath())
        current_inspection_brains = context.portal_catalog.searchResults(
                   path={'query': parent_container_path, 'depth': 3},
                   object_provides=IHOAHouseInspection.__identifier__,
                   review_state='pending')

        if current_inspection_brains:
            house_inspection_title = getattr(context, 'house_inspection_title', '')
            current_inspections = []
            [current_inspections.append(i) for i in current_inspection_brains if i.getId() == house_inspection_title]
            pending_inspections = len(current_inspections)
            portal_msg = ""
            if pending_inspections > 20:
                portal_msg += "There are %s homes remaining to inspect." % pending_inspections
            else:
                portal_msg += "The following homes have not been inspected: "
                portal_msg += '<a href="%s">%s</a>' %(current_inspection_brains[0].getURL(), current_inspection_brains[0].Title)
                for ci_brain in current_inspection_brains[1:]:
                    portal_msg += ', <a href="%s">%s</a>' % (ci_brain.getURL(), ci_brain.Title)

            api.portal.show_message(message=portal_msg,
                                    request=context.REQUEST,
                                    type='info')
            return False

        return True

    def verifySecondInspectionComplete(self):
        context = self
        parent_container = context.aq_parent
        parent_container_path = '/'.join(parent_container.getPhysicalPath())
        current_inspection_brains = context.portal_catalog.searchResults(
                   path={'query': parent_container_path, 'depth': 3},
                   object_provides=IHOAHouseInspection.__identifier__,
                   review_state='failed_initial')
        if current_inspection_brains:
            house_inspection_title = getattr(context, 'house_inspection_title', '')
            current_inspections = []
            [current_inspections.append(i) for i in current_inspection_brains if i.getId() == house_inspection_title]
            pending_inspections = len(current_inspections)
            pending_inspections = len(current_inspection_brains)
            portal_msg = ""
            if pending_inspections > 20:
                portal_msg += "There are %s homes remaining to inspect." % pending_inspections
            else:
                portal_msg += "The following homes have not been inspected: "
                portal_msg += '<a href="%s">%s</a>' %(current_inspection_brains[0].getURL(), current_inspection_brains[0].Title)
                for ci_brain in current_inspection_brains[1:]:
                    portal_msg += ', <a href="%s">%s</a>' % (ci_brain.getURL(), ci_brain.Title)

            api.portal.show_message(message=portal_msg,
                                    request=context.REQUEST,
                                    type='info')
            return False

        return True
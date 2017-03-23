# -*- coding: utf-8 -*-
from zope.component import adapter
from plone import api
from Products.CMFCore.interfaces import IMemberData
from docent.hoa.houses.content.hoa_house import IHOAHouse

from docent.hoa.houses.app_config import PROPERTY_ROLE_DICT, PROPERTY_ROLE_TO_HOME_ATTRIBUTE_LOOKUP_DICT

import logging
logger = logging.getLogger("Plone")


def after_edit_processor(context, event):
    logger.info('after_edit_processor')
    if hasattr(context, 'after_edit_processor'):
        context.after_edit_processor()

def after_transition_processor(context, event):
    logger.info('after_transition_processor')
    if hasattr(context, 'after_transition_processor'):
        context.after_transition_processor()

def after_creation_processor(context, event):
    logger.info('after_creation_processor')
    if hasattr(context, 'after_creation_processor'):
        context.after_creation_processor(context, event)

def after_object_added_processor(context, event):
    logger.info('after_object_added_processor')
    if hasattr(context, 'after_object_added_processor'):
        context.after_object_added_processor(context, event)


#@adapter(IPrincipalCreatedEvent)
def onPrincipalCreation(context, event):
    """
    assign member to house
    """
    #event.principal, event.principal.getUserId()
    logger.info('onPrincipalCreation')
    

#@adapter(IPrincipalDeletedEvent)
def onPrincipalDeletion(context, event):
    """
    find member house and remove member from home
    """
    logger.info('onPrincipalDeletion')

#@adapter(IPropertiesUpdatedEvent)
def onPrincipalUpdate(event):
    """
    find member house and update member
    """
    logger.info('HOA.HOUSES: starting event: onPrincipalUpdate')
    # if hasattr(event, 'context'):
    #     context = event.context
    #     if hasattr(context, 'member'):
    #         member_data = context.member
    #         if IMemberData.providedBy(member_data):
    #             #check primary group
    #             primary_role = member_data.getProperty('property_role')
    #             if primary_role:
    #                 member_groups = api.group.get_groups(user=member_data)
    #                 group_ids = []
    #                 [group_ids.append(group_data.getId()) for group_data in member_groups]
    #                 if primary_role not in group_ids:
    #                     default_group_ids = PROPERTY_ROLE_DICT.keys()
    #                     g_id = default_group_ids.pop(primary_role)
    #                     #add member to group
    #                     api.group.add_user(groupname=g_id, user=member_data)
    #                     #remove member from other groups
    #                     for remaining_g_id in default_group_ids:
    #                         api.group.remove_user(groupname=remaining_g_id, user=member_data)
    #
    #             home_uuid = member_data.getProperty('hoa_home_uuid')
    #             member_id = member_data.getId()
    #             if home_uuid:
    #                 hoa_house = api.content.get(UID=home_uuid)
    #                 if IHOAHouse.providedBy(hoa_house):
    #                     fields_to_check = PROPERTY_ROLE_TO_HOME_ATTRIBUTE_LOOKUP_DICT.get(primary_role)
    #                     if fields_to_check:
    #                         member_configured = False
    #                         fields_configured = []
    #                         for f_t_c in fields_to_check:
    #                             set_member = getattr(hoa_house, f_t_c, '')
    #                             if set_member:
    #                                 fields_configured.append(f_t_c)
    #                                 if set_member == member_id:
    #                                     member_configured = True
    #
    #                         if not member_configured:
    #                             if len(fields_configured) == len(fields_to_check):
    #                                 #we can't do anything...
    #                                 fullname = member_data.getProperty('fullname')
    #                                 api.portal.show_message(type='warning',
    #                                                         message='%s cannot be added to home: %s as there are '
    #                                                                 'currently the maximum members set at that '
    #                                                                 'location. Please update the member '
    #                                                                 'information at the home' % (fullname,
    #                                                                                              hoa_house.title))
    #                             else:
    #                                 if len(fields_configured) == 1:
    #                                     field_configured = fields_configured[0]
    #                                     fields_to_check.pop(field_configured)
    #                                     remaining_field = fields_to_check[0]
    #                                     setattr(hoa_house, remaining_field, member_id)
    #                                 elif not fields_configured:
    #                                     field_to_set = fields_to_check[0]
    #                                     setattr(hoa_house, field_to_set, member_id)
    #
    #


# -*- coding: utf-8 -*-
from plone.dexterity.events import EditBegunEvent
from plone.dexterity.interfaces import IDexterityEditForm
from plone.dexterity.interfaces import IDexterityFTI

from plone.z3cform import layout

from zope.component import getUtility
from zope.event import notify
from zope.interface import classImplements
from plone import api
from plone.dexterity.browser import edit
from plone.z3cform.fieldsets.utils import remove
from zope.event import notify
from zope.interface import invariant, Invalid
from z3c.form import interfaces
from z3c.form import field
from z3c.form.browser.radio import RadioFieldWidget
from z3c.form.interfaces import ActionExecutionError, WidgetActionExecutionError
import z3c.form
from plone.formwidget.namedfile.widget import NamedImageWidget
from plone.formwidget.namedfile.widget import NamedImageFieldWidget
from plone.directives import form

from docent.hoa.houses import _
from docent.hoa.houses.browser.house_inspection_form import getAnnualInspection

from docent.hoa.houses.content.hoa_house_inspection import IHOAHouseInspection, IHOAHouseReWalkInspection
from docent.hoa.houses.app_config import IHOAHOUSEINSPECTION_FIELDSETS


# inspection_keys_to_fieldset_dict = {'flowerpots_text': 'flowerpots',
#                                     'paint_text': 'paint',
#                                     'sidewalk_drive_text': 'sidewalk_drive',
#                                     'steps_text': 'steps',
#                                     'decks_patio_text': 'decks_patio',
#                                     'general_maintenance_text': 'general_maintenance'}

inspection_keys_to_fieldset_dict = {'roof_action_required':'roof',
                                    'gutters_action_required':'gutters',
                                    'exterior_paint_action_required':'exterior_paint',
                                    'decks_action_required':'decks',
                                    'entry_way_action_required':'entry_way',
                                    'paved_surfaces_action_required':'paved_surfaces',
                                    'landscaping_action_required':'landscaping',
                                    'general_maintenance_action_required':'general_maintenance'}

class IEmptySchema(form.Schema):
    """
    Empty Schema
    """

class HouseInspectionEditForm(edit.DefaultEditForm):

    description = _(u'For each inspection criteria, if the home fails, select the tab and enter a brief explanation. '
                    u'If a picture is required, take a picture and upload. <i><u>Do Not click "Done" until you have '
                    u'completed the inspection of the house</u></i> as this immediately saves and closes the inspection. '
                    u'<b>Once your inspection is completed, click "Done".</b> You will be brought to a page that summarizes '
                    u'your findings with an opportunity to make changes before the inspection is saved.')

    def updateActions(self):
        super(HouseInspectionEditForm, self).updateActions()
        save_action = self.actions.get('save') or None
        if save_action:
            save_action.title = u'Done'


    def updateWidgets(self):
        context = self.context
        current_state = api.content.get_state(obj=context)
        groups = self.groups

        if current_state in ['failed_final', 'remedied']:
            for group in groups:
                fieldset_key = group.__name__
                group.fields['%s_rewalk_image' % fieldset_key].mode = None
                group.fields['%s_rewalk_text' % fieldset_key].mode = None
                group.fields['%s_cond_remains' % fieldset_key].mode = None
                group.fields['%s_cond_remains' % fieldset_key].widgetFactory = RadioFieldWidget
                group.fields['%s_text' % fieldset_key].mode = interfaces.DISPLAY_MODE
                group.fields['%s_action_required' % fieldset_key].mode = interfaces.DISPLAY_MODE
                group.fields['%s_image' % fieldset_key].mode = interfaces.DISPLAY_MODE
                group.fields['%s_image' % fieldset_key].width = 128
                group.fields['%s_image' % fieldset_key].height = 96

            for_show = []
            fieldset_dict = {}
            [fieldset_dict.update({group.__name__:group}) for group in groups]

            for key in inspection_keys_to_fieldset_dict.keys():
                if getattr(context, key):
                    for_show.append(key)

            new_groups = []
            for skey in for_show:
                fieldset_key = inspection_keys_to_fieldset_dict.get(skey)
                s_group = fieldset_dict.get(fieldset_key)
                new_groups.append(s_group)

            self.groups = new_groups

        super(HouseInspectionEditForm, self).updateWidgets()

    # @z3c.form.button.buttonAndHandler(_(u'Save'))
    # def handleApply(self, action):
    #     data, errors = self.extractData()
    #     context = self.context
    #     context_state = api.content.get_state(obj=context)
    #     if context_state in ['failed_final', 'remedied']:
    #         for fieldset_id in IHOAHOUSEINSPECTION_FIELDSETS:
    #             if hasattr(data, '%s_cond_remains' % fieldset_id):
    #                 initial_text = getattr(data, '%s_text' % fieldset_id) or None
    #                 cond_remains = getattr(data, '%s_cond_remains' % fieldset_id)
    #                 if cond_remains is True:
    #                     continue
    #                 if initial_text is not None and cond_remains is None:
    #                     error_keys = fieldset_id.split('_')
    #                     error_str = ' '.join(error_keys)
    #                     #raise Invalid(_(u"You must verify the condition remains for %s." % error_str))
    #                     #api.portal.show_message(message="Did you verify the condition for %s?" % error_str.title())
    #                     raise  ActionExecutionError(Invalid(_(u"You must verify the condition remains "
    #                                                           u"for %s." % error_str.title())))
    #
    #     if errors:
    #         self.status = self.formErrorsMessage
    #         return

    @property
    def fti(self):
        return getUtility(IDexterityFTI, name=self.portal_type)

    @property
    def label(self):
        type_name = self.fti.Title()
        return _(u"${name} - Failures", mapping={'name': type_name})

DefaultEditView = layout.wrap_form(HouseInspectionEditForm)
classImplements(DefaultEditView, IDexterityEditForm)

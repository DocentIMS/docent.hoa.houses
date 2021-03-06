import logging
from datetime import date, datetime
from plone import api
from plone.dexterity.content import Container
from plone.directives import form
from plone.indexer import indexer
from plone.namedfile.field import NamedBlobImage
from plone.supermodel.directives import fieldset
from zope import schema

from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from z3c.form.browser.radio import RadioFieldWidget

from zope.interface import provider, invariant, Invalid
from zope.schema.interfaces import IContextAwareDefaultFactory

from docent.hoa.houses.app_config import IHOAHOUSEINSPECTION_FIELDSETS

from docent.hoa.houses.registry import IHOAHomeLookupRegistry
from docent.hoa.houses.app_config import HOME_ROLE_TO_ATTRIBUTE_LOOKUP_DICT
from docent.hoa.houses.registry import (addHomeToLookupRegistry,
                                        removeHomeFromLookupRegistry,
                                        clearAllHomesForMember,
                                        addCurrentHomeRoles)

from docent.hoa.houses import _

logger = logging.getLogger("Plone")

def getAnnualInspection():
    portal = api.portal.get()
    from docent.hoa.houses.content.hoa_annual_inspection import IHOAAnnualInspection
    annual_inspection_brains = portal.portal_catalog.searchResults(
                                               object_provides=IHOAAnnualInspection.__identifier__,
                                               sort_on="created",
                                               sort_order="descending")
    annual_inspection_brain = None
    if annual_inspection_brains:
        annual_inspection_brain = annual_inspection_brains[0]

    return annual_inspection_brain

def computeTitle():
    today = date.today()
    house_inspection_title = today.strftime(u'%Y-%m')
    return u'House Inspection %s' % house_inspection_title,


REQUIRED_ACTION_VOCABULARY = SimpleVocabulary(
    [SimpleTerm(value='clean', title=_(u'Clean - 30 Days')),
     SimpleTerm(value='repair', title=_(u'Repair - 60 Days')),
     SimpleTerm(value='replace', title=_(u'Replace - 12 Months'))]
    )


class IHOAHouseInspection(form.Schema):
    """
    """
    fieldset('roof',
        label=u'Roof',
        description=u'',
        fields=['title',
                'inspection_datetime',
                'passed_datetime',
                'inspected_by_first',
                'inspected_by_second',
                'roof_action_required',
                'roof_text',
                'roof_cond_remains',
                'roof_rewalk_text',
                'roof_image',
                'roof_rewalk_image']
    )

    form.mode(title='hidden')
    title = schema.TextLine(
        title=_(u"Title"),
    )

    form.mode(inspection_datetime='hidden')
    inspection_datetime = schema.Datetime(
        title=_(u'First Inspection Datetime'),
        description=_(u''),
        required=False,
    )

    form.mode(passed_datetime='hidden')
    passed_datetime = schema.Datetime(
        title=_(u'Secondary Inspection Datetime'),
        description=_(u''),
        required=False,
    )

    form.mode(inspected_by_first='hidden')
    inspected_by_first = schema.TextLine(
        title=_(u"Primary Inspection By"),
        required=False,
    )

    form.mode(inspected_by_second='hidden')
    inspected_by_second = schema.TextLine(
        title=_(u"Secondary Inspection By"),
        required=False,
    )

    roof_action_required = schema.Choice(
        title=_(u'Roof Required Action'),
        description=_(u''),
        vocabulary=REQUIRED_ACTION_VOCABULARY,
        required=False,
    )

    roof_text = schema.Text(
        title=_(u"Roof Issue"),
        description=_(u"Comments included in letter and email. 50 character limit"),
        required=False,
        max_length=50,
    )

    form.mode(roof_cond_remains='hidden')
    form.widget(roof_cond_remains=RadioFieldWidget)
    roof_cond_remains = schema.Choice(
        title=_(u'Roof Condition Remains?'),
        description=_(u''),
        source=SimpleVocabulary([SimpleTerm(value=True,
                                            title=u"Yes"),
                                 SimpleTerm(value=False,
                                            title=U"No")]),
        required=False,
    )

    form.mode(roof_rewalk_text='hidden')
    roof_rewalk_text = schema.Text(
        title=_(u"Roof Issue"),
        description=_(u"Comments included in letter and email. 50 character limit"),
        required=False,
        max_length=50,
    )

    roof_image = NamedBlobImage(
        title=_(u"Roof Photo"),
        description=_(u""),
        required=False,
    )

    form.mode(roof_rewalk_image='hidden')
    roof_rewalk_image = NamedBlobImage(
        title=_(u"Roof Re-walk Photo"),
        description=_(u""),
        required=False,
    )

    fieldset('gutters',
        label=u'Gutters',
        description=u'',
        fields=['gutters_action_required',
                'gutters_text',
                'gutters_cond_remains',
                'gutters_rewalk_text',
                'gutters_image',
                'gutters_rewalk_image']
    )

    gutters_action_required = schema.Choice(
        title=_(u'Gutters Required Action'),
        description=_(u''),
        vocabulary=REQUIRED_ACTION_VOCABULARY,
        required=False,
    )

    gutters_text = schema.Text(
        title=_(u"Gutters Issue"),
        description=_(u"Comments included in letter and email. 50 character limit"),
        required=False,
        max_length=50,
    )

    form.mode(gutters_cond_remains='hidden')
    form.widget(gutters_cond_remains=RadioFieldWidget)
    gutters_cond_remains = schema.Choice(
        title=_(u'Gutter Condition Remains?'),
        description=_(u''),
        source=SimpleVocabulary([SimpleTerm(value=True,
                                            title=u"Yes"),
                                 SimpleTerm(value=False,
                                            title=U"No")]),
        required=False,
    )

    form.mode(gutters_rewalk_text='hidden')
    gutters_rewalk_text = schema.Text(
        title=_(u"Gutters Issue"),
        description=_(u"Comments included in letter and email. 50 character limit"),
        required=False,
        max_length=50,
    )

    gutters_image = NamedBlobImage(
        title=_(u"Gutters Photo"),
        description=_(u""),
        required=False,
    )

    form.mode(gutters_rewalk_image='hidden')
    gutters_rewalk_image = NamedBlobImage(
        title=_(u"Gutters Re-walk Photo"),
        description=_(u""),
        required=False,
    )

    fieldset('exterior_paint',
        label=u'Exterior Paint',
        description=u'',
        fields=['exterior_paint_action_required',
                'exterior_paint_text',
                'exterior_paint_cond_remains',
                'exterior_paint_rewalk_text',
                'exterior_paint_image',
                'exterior_paint_rewalk_image']
    )

    exterior_paint_action_required = schema.Choice(
        title=_(u'Exterior Paint Required Action'),
        description=_(u''),
        vocabulary=REQUIRED_ACTION_VOCABULARY,
        required=False,
    )

    exterior_paint_text = schema.Text(
        title=_(u"Exterior Paint Issue"),
        description=_(u"Comments included in letter and email. 50 character limit"),
        required=False,
        max_length=50,
    )

    form.mode(exterior_paint_cond_remains='hidden')
    form.widget(exterior_paint_cond_remains=RadioFieldWidget)
    exterior_paint_cond_remains = schema.Choice(
        title=_(u'Exterior Paint Condition Remains?'),
        description=_(u''),
        source=SimpleVocabulary([SimpleTerm(value=True,
                                            title=u"Yes"),
                                 SimpleTerm(value=False,
                                            title=U"No")]),
        required=False,
    )

    form.mode(exterior_paint_rewalk_text='hidden')
    exterior_paint_rewalk_text = schema.Text(
        title=_(u"Exterior Paint Issue"),
        description=_(u"Comments included in letter and email. 50 character limit"),
        required=False,
        max_length=50,
    )

    exterior_paint_image = NamedBlobImage(
        title=_(u"Exterior Paint Photo"),
        description=_(u""),
        required=False,
    )

    form.mode(exterior_paint_rewalk_image='hidden')
    exterior_paint_rewalk_image = NamedBlobImage(
        title=_(u"Exterior Paint Re-walk Photo"),
        description=_(u""),
        required=False,
    )

    fieldset('decks',
        label=u'Decks',
        description=u'',
        fields=['decks_action_required',
                'decks_text',
                'decks_cond_remains',
                'decks_rewalk_text',
                'decks_image',
                'decks_rewalk_image']
    )

    decks_action_required = schema.Choice(
        title=_(u'Decks Required Action'),
        description=_(u''),
        vocabulary=REQUIRED_ACTION_VOCABULARY,
        required=False,
    )

    decks_text = schema.Text(
        title=_(u"Decks Issue"),
        description=_(u"Comments included in letter and email. 50 character limit"),
        required=False,
        max_length=50,
    )

    form.mode(decks_cond_remains='hidden')
    form.widget(decks_cond_remains=RadioFieldWidget)
    decks_cond_remains = schema.Choice(
        title=_(u'Decks Condition Remains?'),
        description=_(u''),
        source=SimpleVocabulary([SimpleTerm(value=True,
                                            title=u"Yes"),
                                 SimpleTerm(value=False,
                                            title=U"No")]),
        required=False,
    )

    form.mode(decks_rewalk_text='hidden')
    decks_rewalk_text = schema.Text(
        title=_(u"Decks Issue"),
        description=_(u"Comments included in letter and email. 50 character limit"),
        required=False,
        max_length=50,
    )

    decks_image = NamedBlobImage(
        title=_(u"Decks Photo"),
        description=_(u""),
        required=False,
    )

    form.mode(decks_rewalk_image='hidden')
    decks_rewalk_image = NamedBlobImage(
        title=_(u"Decks Re-walk Photo"),
        description=_(u""),
        required=False,
    )

    fieldset('entry_way',
        label=u'Entry Way',
        description=u'',
        fields=['entry_way_action_required',
                'entry_way_text',
                'entry_way_cond_remains',
                'entry_way_rewalk_text',
                'entry_way_image',
                'entry_way_rewalk_image']
    )

    entry_way_action_required = schema.Choice(
        title=_(u'Entry Way Required Action'),
        description=_(u''),
        vocabulary=REQUIRED_ACTION_VOCABULARY,
        required=False,
    )

    entry_way_text = schema.Text(
        title=_(u"Entry Way Issue"),
        description=_(u"Comments included in letter and email. 50 character limit"),
        required=False,
        max_length=50,
    )

    form.mode(entry_way_cond_remains='hidden')
    form.widget(entry_way_cond_remains=RadioFieldWidget)
    entry_way_cond_remains = schema.Choice(
        title=_(u'Entry Way Condition Remains?'),
        description=_(u''),
        source=SimpleVocabulary([SimpleTerm(value=True,
                                            title=u"Yes"),
                                 SimpleTerm(value=False,
                                            title=U"No")]),
        required=False,
    )

    form.mode(entry_way_rewalk_text='hidden')
    entry_way_rewalk_text = schema.Text(
        title=_(u"Entry Way Issue"),
        description=_(u"Comments included in letter and email. 50 character limit"),
        required=False,
        max_length=50,
    )

    entry_way_image = NamedBlobImage(
        title=_(u"Entry Way Photo"),
        description=_(u""),
        required=False,
    )

    form.mode(entry_way_rewalk_image='hidden')
    entry_way_rewalk_image = NamedBlobImage(
        title=_(u"Entry Way Re-walk Photo"),
        description=_(u""),
        required=False,
    )

    fieldset('paved_surfaces',
        label=u'Paved Surfaces',
        description=u'',
        fields=['paved_surfaces_action_required',
                'paved_surfaces_text',
                'paved_surfaces_cond_remains',
                'paved_surfaces_rewalk_text',
                'paved_surfaces_image',
                'paved_surfaces_rewalk_image']
    )

    paved_surfaces_action_required = schema.Choice(
        title=_(u'Paved Surfaces Required Action'),
        description=_(u''),
        vocabulary=REQUIRED_ACTION_VOCABULARY,
        required=False,
    )

    paved_surfaces_text = schema.Text(
        title=_(u"Paved Surfaces Issue"),
        description=_(u"Comments included in letter and email. 50 character limit"),
        required=False,
        max_length=50,
    )

    form.mode(paved_surfaces_cond_remains='hidden')
    form.widget(paved_surfaces_cond_remains=RadioFieldWidget)
    paved_surfaces_cond_remains = schema.Choice(
        title=_(u'Paved Surfaces Condition Remains?'),
        description=_(u''),
        source=SimpleVocabulary([SimpleTerm(value=True,
                                            title=u"Yes"),
                                 SimpleTerm(value=False,
                                            title=U"No")]),
        required=False,
    )

    form.mode(paved_surfaces_rewalk_text='hidden')
    paved_surfaces_rewalk_text = schema.Text(
        title=_(u"Paved Surfaces Issue"),
        description=_(u"Comments included in letter and email. 50 character limit"),
        required=False,
        max_length=50,
    )

    paved_surfaces_image = NamedBlobImage(
        title=_(u"Paved Surfaces Photo"),
        description=_(u""),
        required=False,
    )

    form.mode(paved_surfaces_rewalk_image='hidden')
    paved_surfaces_rewalk_image = NamedBlobImage(
        title=_(u"Paved Surfaces Re-walk Photo"),
        description=_(u""),
        required=False,
    )

    fieldset('landscaping',
        label=u'Landscaping',
        description=u'',
        fields=['landscaping_action_required',
                'landscaping_text',
                'landscaping_cond_remains',
                'landscaping_rewalk_text',
                'landscaping_image',
                'landscaping_rewalk_image']
    )

    landscaping_action_required = schema.Choice(
        title=_(u'Landscaping Required Action'),
        description=_(u''),
        vocabulary=REQUIRED_ACTION_VOCABULARY,
        required=False,
    )

    landscaping_text = schema.Text(
        title=_(u"Landscaping Issue"),
        description=_(u"Comments included in letter and email. 50 character limit"),
        required=False,
        max_length=50,
    )

    form.mode(landscaping_cond_remains='hidden')
    form.widget(landscaping_cond_remains=RadioFieldWidget)
    landscaping_cond_remains = schema.Choice(
        title=_(u'Landscaping Condition Remains?'),
        description=_(u''),
        source=SimpleVocabulary([SimpleTerm(value=True,
                                            title=u"Yes"),
                                 SimpleTerm(value=False,
                                            title=U"No")]),
        required=False,
    )

    form.mode(landscaping_rewalk_text='hidden')
    landscaping_rewalk_text = schema.Text(
        title=_(u"Landscaping Issue"),
        description=_(u"Comments included in letter and email. 50 character limit"),
        required=False,
        max_length=50,
    )

    landscaping_image = NamedBlobImage(
        title=_(u"Landscaping Photo"),
        description=_(u""),
        required=False,
    )

    form.mode(landscaping_rewalk_image='hidden')
    landscaping_rewalk_image = NamedBlobImage(
        title=_(u"Landscaping Re-walk Photo"),
        description=_(u""),
        required=False,
    )

    fieldset('general_maintenance',
        label=u'General Maintenance',
        description=u'',
        fields=['general_maintenance_action_required',
                'general_maintenance_text',
                'general_maintenance_cond_remains',
                'general_maintenance_rewalk_text',
                'general_maintenance_image',
                'general_maintenance_rewalk_image']
    )

    general_maintenance_action_required = schema.Choice(
        title=_(u'General Maintenance Required Action'),
        description=_(u''),
        vocabulary=REQUIRED_ACTION_VOCABULARY,
        required=False,
    )

    general_maintenance_text = schema.Text(
        title=_(u"General Maintenance Issue"),
        description=_(u"Comments included in letter and email. 50 character limit"),
        required=False,
        max_length=50,
    )

    form.mode(general_maintenance_cond_remains='hidden')
    form.widget(general_maintenance_cond_remains=RadioFieldWidget)
    general_maintenance_cond_remains = schema.Choice(
        title=_(u'General Maintenance Condition Remains?'),
        description=_(u''),
        source=SimpleVocabulary([SimpleTerm(value=True,
                                            title=u"Yes"),
                                 SimpleTerm(value=False,
                                            title=U"No")]),
        required=False,
    )

    form.mode(general_maintenance_rewalk_text='hidden')
    general_maintenance_rewalk_text = schema.Text(
        title=_(u"General Maintenance Issue"),
        description=_(u"Comments included in letter and email. 50 character limit"),
        required=False,
        max_length=50,
    )

    general_maintenance_image = NamedBlobImage(
        title=_(u"General Maintenance Photo"),
        description=_(u""),
        required=False,
    )

    form.mode(general_maintenance_rewalk_image='hidden')
    general_maintenance_rewalk_image = NamedBlobImage(
        title=_(u"General Maintenance Re-walk Photo"),
        description=_(u""),
        required=False,
    )

    @invariant
    def confirmAction(data):
        context = data.__context__

        context_state = api.content.get_state(obj=context)
        for fieldset_id in IHOAHOUSEINSPECTION_FIELDSETS:
            if hasattr(data, '%s_text' % fieldset_id):
                if getattr(data, '%s_text' % fieldset_id):
                    action_required = getattr(data, '%s_action_required' % fieldset_id)
                    if not action_required:
                        error_keys = fieldset_id.split('_')
                        error_str = ' '.join(error_keys)
                        raise Invalid(_(u"You must provide a required action for %s." % error_str))
            if hasattr(data, '%s_action_required' % fieldset_id):
                if getattr(data, '%s_action_required' % fieldset_id):
                    failure_text = getattr(data, '%s_text' % fieldset_id)
                    if not failure_text:
                        error_keys = fieldset_id.split('_')
                        error_str = ' '.join(error_keys)
                        raise Invalid(_(u"You must provide a description of the issue if action is required for: %s." % error_str))

    @invariant
    def conditionPerists(data):
        context = data.__context__
        context_state = api.content.get_state(obj=context)
        if context_state in ['failed_final', 'remedied']:
            for fieldset_id in IHOAHOUSEINSPECTION_FIELDSETS:
                if hasattr(data, '%s_cond_remains' % fieldset_id):
                    if getattr(data, '%s_cond_remains' % fieldset_id):
                        rewalk_txt = getattr(data, '%s_rewalk_text' % fieldset_id)
                        rewalk_image = getattr(data, '%s_rewalk_image' % fieldset_id)
                        if not rewalk_txt:
                            error_keys = fieldset_id.split('_')
                            error_str = ' '.join(error_keys)
                            raise Invalid(_(u"You must provide an a reason the condition persists for %s." % error_str))
                        if not rewalk_image:
                            error_keys = fieldset_id.split('_')
                            error_str = ' '.join(error_keys)
                            raise Invalid(_(u"You must provide an a photo of the condition for %s." % error_str))

    @invariant
    def verifyCondition(data):
        context = data.__context__
        data_dict = data._Data_data___
        context_state = api.content.get_state(obj=context)
        if context_state in ['failed_final', 'remedied']:
            for fieldset_id in IHOAHOUSEINSPECTION_FIELDSETS:
                if '%s_cond_remains' % fieldset_id in data_dict:
                    initial_text = data_dict.get('%s_text' % fieldset_id) or None
                    cond_remains = data_dict.get('%s_cond_remains' % fieldset_id)
                    if cond_remains is True:
                        continue
                    if cond_remains is False:
                        continue
                    error_keys = fieldset_id.split('_')
                    error_str = ' '.join(error_keys)
                    raise Invalid(_(u"You must verify the condition remains for %s." % error_str))
                    #
                    #  if initial_text is not None and cond_remains is None:
                    #     error_keys = fieldset_id.split('_')
                    #     error_str = ' '.join(error_keys)
                    #     #raise Invalid(_(u"You must verify the condition remains for %s." % error_str))
                    #     api.portal.show_message(message="Did you verify the condition for %s?" % error_str.title())


    @invariant
    def imagesRequired(data):
        context = data.__context__
        context_state = api.content.get_state(obj=context)

        for fieldset_id in IHOAHOUSEINSPECTION_FIELDSETS:
            if context_state == 'failed_initial':
                if getattr(data, '%s_text' % fieldset_id):
                    image = getattr(data, '%s_image' % fieldset_id)
                    if not image:
                        error_keys = fieldset_id.split('_')
                        error_str = ' '.join(error_keys)
                        raise Invalid(_(u"You must provide an image for %s." % error_str))
            if context_state == 'failed_final':
                if getattr(data, '%s_rewalk_text' % fieldset_id):
                    image = getattr(data, '%s_rewalk_image' % fieldset_id)
                    if not image:
                        error_keys = fieldset_id.split('_')
                        error_str = ' '.join(error_keys)
                        raise Invalid(_(u"You must provide an image for %s." % error_str))


class IHOAHouseReWalkInspection(form.Schema):
    """
    """
    fieldset('roof',
        label=u'Roof',
        description=u'',
        fields=['title',
                'inspection_datetime',
                'passed_datetime',
                'inspected_by_first',
                'inspected_by_second',
                'roof_cond_remains',
                'roof_action_required',
                'roof_text',
                'roof_rewalk_text',
                'roof_image',
                'roof_rewalk_image']
    )

    form.mode(title='hidden')
    title = schema.TextLine(
        title=_(u"Title"),
    )

    form.mode(inspection_datetime='hidden')
    inspection_datetime = schema.Datetime(
        title=_(u'First Inspection Datetime'),
        description=_(u''),
        required=False,
    )

    form.mode(passed_datetime='hidden')
    passed_datetime = schema.Datetime(
        title=_(u'Secondary Inspection Datetime'),
        description=_(u''),
        required=False,
    )

    form.mode(inspected_by_first='hidden')
    inspected_by_first = schema.TextLine(
        title=_(u"Primary Inspection By"),
        required=False,
    )

    form.mode(inspected_by_second='hidden')
    inspected_by_second = schema.TextLine(
        title=_(u"Secondary Inspection By"),
        required=False,
    )

    form.widget(roof_cond_remains=RadioFieldWidget)
    roof_cond_remains = schema.Choice(
        title=_(u'Roof Condition Remains?'),
        description=_(u''),
        source=SimpleVocabulary([SimpleTerm(value=True,
                                            title=u"Yes"),
                                 SimpleTerm(value=False,
                                            title=U"No")]),
        required=False,
    )

    form.mode(roof_action_required='display')
    roof_action_required = schema.Choice(
        title=_(u'Roof Required Action'),
        description=_(u''),
        vocabulary=REQUIRED_ACTION_VOCABULARY,
        required=False,
    )

    form.mode(roof_text='display')
    roof_text = schema.Text(
        title=_(u"Roof Issue"),
        description=_(u"Comments included in letter and email. 50 character limit"),
        required=False,
        max_length=50,
    )

    roof_rewalk_text = schema.Text(
        title=_(u"Roof Reinspect Issue"),
        description=_(u"Comments included in letter and email. 50 character limit"),
        required=False,
        max_length=50,
    )

    form.mode(roof_image='display')
    roof_image = NamedBlobImage(
        title=_(u"Roof Photo"),
        description=_(u""),
        required=False,
    )

    roof_rewalk_image = NamedBlobImage(
        title=_(u"Roof Re-walk Photo"),
        description=_(u""),
        required=False,
    )

    fieldset('gutters',
        label=u'Gutters',
        description=u'',
        fields=['gutters_cond_remains',
                'gutters_action_required',
                'gutters_text',
                'gutters_rewalk_text',
                'gutters_image',
                'gutters_rewalk_image']
    )

    form.widget(gutters_cond_remains=RadioFieldWidget)
    gutters_cond_remains = schema.Choice(
        title=_(u'Gutter Condition Remains?'),
        description=_(u''),
        source=SimpleVocabulary([SimpleTerm(value=True,
                                            title=u"Yes"),
                                 SimpleTerm(value=False,
                                            title=U"No")]),
        required=False,
    )

    form.mode(gutters_action_required='display')
    gutters_action_required = schema.Choice(
        title=_(u'Gutters Required Action'),
        description=_(u''),
        vocabulary=REQUIRED_ACTION_VOCABULARY,
        required=False,
    )

    form.mode(gutters_text='display')
    gutters_text = schema.Text(
        title=_(u"Gutters Issue"),
        description=_(u"Comments included in letter and email. 50 character limit"),
        required=False,
        max_length=50,
    )

    gutters_rewalk_text = schema.Text(
        title=_(u"Gutters Reinspect Issue"),
        description=_(u"Comments included in letter and email. 50 character limit"),
        required=False,
        max_length=50,
    )

    form.mode(gutters_image='display')
    gutters_image = NamedBlobImage(
        title=_(u"Gutters Photo"),
        description=_(u""),
        required=False,
    )

    gutters_rewalk_image = NamedBlobImage(
        title=_(u"Gutters Re-walk Photo"),
        description=_(u""),
        required=False,
    )

    fieldset('exterior_paint',
        label=u'Exterior Paint',
        description=u'',
        fields=['exterior_paint_cond_remains',
                'exterior_paint_action_required',
                'exterior_paint_text',
                'exterior_paint_rewalk_text',
                'exterior_paint_image',
                'exterior_paint_rewalk_image']
    )

    form.widget(exterior_paint_cond_remains=RadioFieldWidget)
    exterior_paint_cond_remains = schema.Choice(
        title=_(u'Exterior Paint Condition Remains?'),
        description=_(u''),
        source=SimpleVocabulary([SimpleTerm(value=True,
                                            title=u"Yes"),
                                 SimpleTerm(value=False,
                                            title=U"No")]),
        required=False,
    )

    form.mode(exterior_paint_action_required='display')
    exterior_paint_action_required = schema.Choice(
        title=_(u'Exterior Paint Required Action'),
        description=_(u''),
        vocabulary=REQUIRED_ACTION_VOCABULARY,
        required=False,
    )

    form.mode(exterior_paint_text='display')
    exterior_paint_text = schema.Text(
        title=_(u"Exterior Paint Issue"),
        description=_(u"Comments included in letter and email. 50 character limit"),
        required=False,
        max_length=50,
    )

    exterior_paint_rewalk_text = schema.Text(
        title=_(u"Exterior Paint Reinspect Issue"),
        description=_(u"Comments included in letter and email. 50 character limit"),
        required=False,
        max_length=50,
    )

    form.mode(exterior_paint_image='display')
    exterior_paint_image = NamedBlobImage(
        title=_(u"Exterior Paint Photo"),
        description=_(u""),
        required=False,
    )

    exterior_paint_rewalk_image = NamedBlobImage(
        title=_(u"Exterior Paint Re-walk Photo"),
        description=_(u""),
        required=False,
    )

    fieldset('decks',
        label=u'Decks',
        description=u'',
        fields=['decks_cond_remains',
                'decks_action_required',
                'decks_text',
                'decks_rewalk_text',
                'decks_image',
                'decks_rewalk_image']
    )

    form.widget(decks_cond_remains=RadioFieldWidget)
    decks_cond_remains = schema.Choice(
        title=_(u'Decks Condition Remains?'),
        description=_(u''),
        source=SimpleVocabulary([SimpleTerm(value=True,
                                            title=u"Yes"),
                                 SimpleTerm(value=False,
                                            title=U"No")]),
        required=False,
    )

    form.mode(decks_action_required='display')
    decks_action_required = schema.Choice(
        title=_(u'Decks Required Action'),
        description=_(u''),
        vocabulary=REQUIRED_ACTION_VOCABULARY,
        required=False,
    )

    form.mode(decks_text='display')
    decks_text = schema.Text(
        title=_(u"Decks Issue"),
        description=_(u"Comments included in letter and email. 50 character limit"),
        required=False,
        max_length=50,
    )

    decks_rewalk_text = schema.Text(
        title=_(u"Decks Reinspect Issue"),
        description=_(u"Comments included in letter and email. 50 character limit"),
        required=False,
        max_length=50,
    )

    form.mode(decks_image='display')
    decks_image = NamedBlobImage(
        title=_(u"Decks Photo"),
        description=_(u""),
        required=False,
    )

    decks_rewalk_image = NamedBlobImage(
        title=_(u"Decks Re-walk Photo"),
        description=_(u""),
        required=False,
    )

    fieldset('entry_way',
        label=u'Entry Way',
        description=u'',
        fields=['entry_way_cond_remains',
                'entry_way_action_required',
                'entry_way_text',
                'entry_way_rewalk_text',
                'entry_way_image',
                'entry_way_rewalk_image']
    )

    form.widget(entry_way_cond_remains=RadioFieldWidget)
    entry_way_cond_remains = schema.Choice(
        title=_(u'Entry Way Condition Remains?'),
        description=_(u''),
        source=SimpleVocabulary([SimpleTerm(value=True,
                                            title=u"Yes"),
                                 SimpleTerm(value=False,
                                            title=U"No")]),
        required=False,
    )

    form.mode(entry_way_action_required='display')
    entry_way_action_required = schema.Choice(
        title=_(u'Entry Way Required Action'),
        description=_(u''),
        vocabulary=REQUIRED_ACTION_VOCABULARY,
        required=False,
    )

    form.mode(entry_way_text='display')
    entry_way_text = schema.Text(
        title=_(u"Entry Way Issue"),
        description=_(u"Comments included in letter and email. 50 character limit"),
        required=False,
        max_length=50,
    )

    entry_way_rewalk_text = schema.Text(
        title=_(u"Entry Way Reinspect Issue"),
        description=_(u"Comments included in letter and email. 50 character limit"),
        required=False,
        max_length=50,
    )

    form.mode(entry_way_image='display')
    entry_way_image = NamedBlobImage(
        title=_(u"Entry Way Photo"),
        description=_(u""),
        required=False,
    )

    entry_way_rewalk_image = NamedBlobImage(
        title=_(u"Entry Way Re-walk Photo"),
        description=_(u""),
        required=False,
    )

    fieldset('paved_surfaces',
        label=u'Paved Surfaces',
        description=u'',
        fields=['paved_surfaces_cond_remains',
                'paved_surfaces_action_required',
                'paved_surfaces_text',
                'paved_surfaces_rewalk_text',
                'paved_surfaces_image',
                'paved_surfaces_rewalk_image']
    )

    form.widget(paved_surfaces_cond_remains=RadioFieldWidget)
    paved_surfaces_cond_remains = schema.Choice(
        title=_(u'Paved Surfaces Condition Remains?'),
        description=_(u''),
        source=SimpleVocabulary([SimpleTerm(value=True,
                                            title=u"Yes"),
                                 SimpleTerm(value=False,
                                            title=U"No")]),
        required=False,
    )

    form.mode(paved_surfaces_action_required='display')
    paved_surfaces_action_required = schema.Choice(
        title=_(u'Paved Surfaces Required Action'),
        description=_(u''),
        vocabulary=REQUIRED_ACTION_VOCABULARY,
        required=False,
    )

    form.mode(paved_surfaces_text='display')
    paved_surfaces_text = schema.Text(
        title=_(u"Paved Surfaces Issue"),
        description=_(u"Comments included in letter and email. 50 character limit"),
        required=False,
        max_length=50,
    )

    paved_surfaces_rewalk_text = schema.Text(
        title=_(u"Paved Surfaces Reinspect Issue"),
        description=_(u"Comments included in letter and email. 50 character limit"),
        required=False,
        max_length=50,
    )

    form.mode(paved_surfaces_image='display')
    paved_surfaces_image = NamedBlobImage(
        title=_(u"Paved Surfaces Photo"),
        description=_(u""),
        required=False,
    )

    paved_surfaces_rewalk_image = NamedBlobImage(
        title=_(u"Paved Surfaces Re-walk Photo"),
        description=_(u""),
        required=False,
    )

    fieldset('landscaping',
        label=u'Landscaping',
        description=u'',
        fields=['landscaping_cond_remains',
                'landscaping_action_required',
                'landscaping_text',
                'landscaping_rewalk_text',
                'landscaping_image',
                'landscaping_rewalk_image']
    )

    form.widget(landscaping_cond_remains=RadioFieldWidget)
    landscaping_cond_remains = schema.Choice(
        title=_(u'Landscaping Condition Remains?'),
        description=_(u''),
        source=SimpleVocabulary([SimpleTerm(value=True,
                                            title=u"Yes"),
                                 SimpleTerm(value=False,
                                            title=U"No")]),
        required=False,
    )

    form.mode(landscaping_action_required='display')
    landscaping_action_required = schema.Choice(
        title=_(u'Landscaping Required Action'),
        description=_(u''),
        vocabulary=REQUIRED_ACTION_VOCABULARY,
        required=False,
    )

    form.mode(landscaping_text='display')
    landscaping_text = schema.Text(
        title=_(u"Landscaping Issue"),
        description=_(u"Comments included in letter and email. 50 character limit"),
        required=False,
        max_length=50,
    )

    landscaping_rewalk_text = schema.Text(
        title=_(u"Landscaping Reinspect Issue"),
        description=_(u"Comments included in letter and email. 50 character limit"),
        required=False,
        max_length=50,
    )

    form.mode(landscaping_image='display')
    landscaping_image = NamedBlobImage(
        title=_(u"Landscaping Photo"),
        description=_(u""),
        required=False,
    )

    landscaping_rewalk_image = NamedBlobImage(
        title=_(u"Landscaping Re-walk Photo"),
        description=_(u""),
        required=False,
    )

    fieldset('general_maintenance',
        label=u'General Maintenance',
        description=u'',
        fields=['general_maintenance_cond_remains',
                'general_maintenance_action_required',
                'general_maintenance_text',
                'general_maintenance_rewalk_text',
                'general_maintenance_image',
                'general_maintenance_rewalk_image']
    )

    form.widget(general_maintenance_cond_remains=RadioFieldWidget)
    general_maintenance_cond_remains = schema.Choice(
        title=_(u'General Maintenance Condition Remains?'),
        description=_(u''),
        source=SimpleVocabulary([SimpleTerm(value=True,
                                            title=u"Yes"),
                                 SimpleTerm(value=False,
                                            title=U"No")]),
        required=False,
    )

    form.mode(general_maintenance_action_required='display')
    general_maintenance_action_required = schema.Choice(
        title=_(u'General Maintenance Required Action'),
        description=_(u''),
        vocabulary=REQUIRED_ACTION_VOCABULARY,
        required=False,
    )

    form.mode(general_maintenance_text='display')
    general_maintenance_text = schema.Text(
        title=_(u"General Maintenance Issue"),
        description=_(u""),
        required=False,
        max_length=50,
    )

    general_maintenance_rewalk_text = schema.Text(
        title=_(u"General Maintenance Reinspect Issue"),
        description=_(u"Comments included in letter and email. 50 character limit"),
        required=False,
        max_length=50,
    )

    form.mode(general_maintenance_image='display')
    general_maintenance_image = NamedBlobImage(
        title=_(u"General Maintenance Photo"),
        description=_(u""),
        required=False,
    )

    general_maintenance_rewalk_image = NamedBlobImage(
        title=_(u"General Maintenance Re-walk Photo"),
        description=_(u""),
        required=False,
    )

    form.mode(redirect_assignments='hidden')
    redirect_assignments = schema.TextLine(title=_(u"Redirect Assignments"),
                                           required=False)

    @invariant
    def confirmAction(data):
        context = data.__context__
        context_state = api.content.get_state(obj=context)
        for fieldset_id in IHOAHOUSEINSPECTION_FIELDSETS:
            if hasattr(data, '%s_text' % fieldset_id):
                if getattr(data, '%s_text' % fieldset_id):
                    action_required = getattr(data, '%s_action_required' % fieldset_id)
                    if not action_required:
                        error_keys = fieldset_id.split('_')
                        error_str = ' '.join(error_keys)
                        raise Invalid(_(u"You must provide a required action for %s." % error_str))
            if hasattr(data, '%s_action_required' % fieldset_id):
                if getattr(data, '%s_action_required' % fieldset_id):
                    failure_text = getattr(data, '%s_text' % fieldset_id)
                    if not failure_text:
                        error_keys = fieldset_id.split('_')
                        error_str = ' '.join(error_keys)
                        raise Invalid(_(u"You must provide a description of the issue if action is required for: %s." % error_str))

    @invariant
    def conditionPerists(data):
        context = data.__context__
        context_state = api.content.get_state(obj=context)
        if context_state in ['failed_final', 'remedied']:
            for fieldset_id in IHOAHOUSEINSPECTION_FIELDSETS:
                if hasattr(data, '%s_cond_remains' % fieldset_id):
                    if getattr(data, '%s_cond_remains' % fieldset_id):
                        rewalk_txt = getattr(data, '%s_rewalk_text' % fieldset_id)
                        rewalk_image = getattr(data, '%s_rewalk_image' % fieldset_id)
                        if not rewalk_txt:
                            error_keys = fieldset_id.split('_')
                            error_str = ' '.join(error_keys)
                            raise Invalid(_(u"You must provide an a reason the condition persists for %s." % error_str))
                        if not rewalk_image:
                            error_keys = fieldset_id.split('_')
                            error_str = ' '.join(error_keys)
                            raise Invalid(_(u"You must provide an a photo of the condition for %s." % error_str))

    @invariant
    def verifyCondition(data):
        context = data.__context__
        context_state = api.content.get_state(obj=context)
        if context_state in ['failed_final', 'remedied']:
            for fieldset_id in IHOAHOUSEINSPECTION_FIELDSETS:
                if hasattr(data, '%s_cond_remains' % fieldset_id):
                    initial_text = getattr(data, '%s_text' % fieldset_id)
                    if initial_text and not getattr(data, '%s_cond_remains' % fieldset_id):
                        error_keys = fieldset_id.split('_')
                        error_str = ' '.join(error_keys)
                        raise Invalid(_(u"You must provide an image for %s." % error_str))

    @invariant
    def imagesRequired(data):
        context = data.__context__
        context_state = api.content.get_state(obj=context)

        for fieldset_id in IHOAHOUSEINSPECTION_FIELDSETS:
            if context_state == 'failed_initial':
                if getattr(data, '%s_text' % fieldset_id):
                    image = getattr(data, '%s_image' % fieldset_id)
                    if not image:
                        error_keys = fieldset_id.split('_')
                        error_str = ' '.join(error_keys)
                        raise Invalid(_(u"You must provide an image for %s." % error_str))
            if context_state == 'failed_final':
                if getattr(data, '%s_rewalk_text' % fieldset_id):
                    image = getattr(data, '%s_rewalk_image' % fieldset_id)
                    if not image:
                        error_keys = fieldset_id.split('_')
                        error_str = ' '.join(error_keys)
                        raise Invalid(_(u"You must provide an image for %s." % error_str))


class HOAHouseInspection(Container):
    """
    """

    def after_transition_processor(self, event):
        context_state = api.content.get_state(obj=self)
        now = datetime.now()
        if hasattr(event, 'transition'):
            transition = event.transition
            if transition:
                if transition.title == 'Retract':
                    portal = api.portal.get()
                    hoa_neighborhoods = api.content.find(context=portal, portal_type='hoa_neighborhood')
                    if not hoa_neighborhoods:
                        api.portal.show_message(message="Could not locate your neighborhood. Please contact an administrator.",
                                                request=self.REQUEST,
                                                type='warn')
                    elif len(hoa_neighborhoods) > 1:
                        api.portal.show_message(message="Found too many neighborhoods! Please contact an administrator.",
                                                request=self.REQUEST,
                                                type='warn')
                    else:
                        hoa_neighborhood_brain = hoa_neighborhoods[0]
                        setattr(self, 'redirect_assignments', hoa_neighborhood_brain.UID)
                        #needs logic to determine what to delete (ie first vs second)
                        annual_inspection_brain = getAnnualInspection()
                        inspection_state = annual_inspection_brain.review_state
                        if inspection_state == 'initial_inspection' or inspection_state == 'Initial Inspection':
                            #remove values of this initial inspection
                            setattr(self, 'inspection_datetime', None)
                            setattr(self, 'passed_datetime', None)
                            setattr(self, 'inspected_by_first', u'')
                            setattr(self, 'roof_action_required', '')
                            setattr(self, 'roof_text', u'')
                            setattr(self, 'roof_image', None)
                            setattr(self, 'gutters_action_required', '')
                            setattr(self, 'gutters_text', u'')
                            setattr(self, 'gutters_image', None)
                            setattr(self, 'exterior_paint_action_required', '')
                            setattr(self, 'exterior_paint_text', u'')
                            setattr(self, 'exterior_paint_image', None)
                            setattr(self, 'decks_action_required', '')
                            setattr(self, 'decks_text', u'')
                            setattr(self, 'decks_image', None)
                            setattr(self, 'entry_way_action_required', '')
                            setattr(self, 'entry_way_text', u'')
                            setattr(self, 'entry_way_image', None)
                            setattr(self, 'paved_surfaces_action_required', '')
                            setattr(self, 'paved_surfaces_text', u'')
                            setattr(self, 'paved_surfaces_image', None)
                            setattr(self, 'landscaping_action_required', '')
                            setattr(self, 'landscaping_text', u'')
                            setattr(self, 'landscaping_image', None)
                            setattr(self, 'general_maintenance_action_required', '')
                            setattr(self, 'general_maintenance_text', u'')
                            setattr(self, 'general_maintenance_image', None)
                        elif inspection_state == 'secondary_inspection' or inspection_state == 'Secondary Inspection':
                            setattr(self, 'landscaping_cond_remains', '')
                            setattr(self, 'landscaping_rewalk_text', u'')
                            setattr(self, 'landscaping_rewalk_image', None)
                            setattr(self, 'general_maintenance_cond_remains', '')
                            setattr(self, 'general_maintenance_rewalk_text', u'')
                            setattr(self, 'general_maintenance_rewalk_image', None)
                            setattr(self, 'paved_surfaces_cond_remains', '')
                            setattr(self, 'paved_surfaces_rewalk_text', u'')
                            setattr(self, 'paved_surfaces_rewalk_image', None)
                            setattr(self, 'entry_way_cond_remains', '')
                            setattr(self, 'entry_way_rewalk_text', u'')
                            setattr(self, 'entry_way_rewalk_image', None)
                            setattr(self, 'decks_cond_remains', '')
                            setattr(self, 'decks_rewalk_text', u'')
                            setattr(self, 'decks_rewalk_image', None)
                            setattr(self, 'exterior_paint_cond_remains', '')
                            setattr(self, 'exterior_paint_rewalk_text', u'')
                            setattr(self, 'exterior_paint_rewalk_image', None)
                            setattr(self, 'gutters_cond_remains', '')
                            setattr(self, 'gutters_rewalk_text', u'')
                            setattr(self, 'gutters_rewalk_image', None)
                            setattr(self, 'roof_cond_remains', '')
                            setattr(self, 'roof_rewalk_text', u'')
                            setattr(self, 'roof_rewalk_image', None)
                            setattr(self, 'inspected_by_second', u'')

                        return

        if context_state == 'passed':
            setattr(self, 'passed_datetime', now)

        setattr(self, 'inspection_datetime', now)
        setattr(self, 'redirect_assignments', '')
        annual_inspection_brain = getAnnualInspection()
        ai_obj = annual_inspection_brain.getObject()
        ai_obj.checkLastInspection()

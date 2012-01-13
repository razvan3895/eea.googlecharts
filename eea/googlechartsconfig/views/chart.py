# -*- coding: utf-8 -*-
""" GoogleCharts View
"""
__author__ = """European Environment Agency (EEA)"""
__docformat__ = 'plaintext'
__credits__ = """contributions: Zoltan Szabo"""

import json

from zope.interface import implements
from zope.component import queryAdapter, getUtility, getMultiAdapter
from zope.schema.interfaces import IVocabularyFactory

from StringIO import StringIO

from eea.daviz.interfaces import IDavizConfig

from eea.daviz.views.view import ViewForm

class View(ViewForm):
    """ GoogleChartsView
    """
    label = 'GoogleCharts'
    view_name = "googlechart.googlecharts"
    section = "Charts"

    def get_charts(self):
        mutator = queryAdapter(self.context, IDavizConfig)
        config = ''
        for view in mutator.views:
            if (view.get('chartsconfig')):
                config = view.get('chartsconfig')
        return json.load(StringIO(config))['charts']

    @property
    def get_columns(self):
        vocab = getUtility(IVocabularyFactory, 
                               name="eea.daviz.vocabularies.FacetsVocabulary")
        terms = [[term.token, term.title] for term in vocab(self.context)]
        return json.dumps(dict(terms));

    def get_rows(self):
        result = getMultiAdapter((self.context, self.request), name="daviz-relateditems.json")()
        return result;
import pytz
from datetime import datetime, timedelta
from jira.commons.constants import Constants
from jira.model.issue_base import IssueBase

tz = pytz.timezone('America/Lima')


class Story(IssueBase):
    def __init__(self):
        super().__init__()
        self.feature_key = ''
        self.story_points = 0
        self.comments = []
        self.jira_tasks = []
        self.label_folio_id = ''
        self.label_source_id = ''
        self.label_process_id = ''
        self.desc_folio_id = ''
        self.desc_source_id = ''
        self.desc_tds_id = ''
        self.desc_bui_local_id = ''
        self.desc_pgyc_id = ''

    def __add_attr_dictamen(self):
        data_text = self.description
        # Extraemos el Folio, Id Fuente y TDS
        start_index = data_text.find(Constants.CRITERIA_TO_FIND_TABLE) + len(Constants.CRITERIA_TO_FIND_TABLE)
        data_dictamen = data_text[start_index:len(data_text) - 1]
        arr_row = data_dictamen.split(Constants.CRITERIA_TO_FIND_TABLE)
        if len(arr_row) >= 1:
            row_first = arr_row[0]
            arr_cell = row_first.split(Constants.PIPE_ID)

            if len(arr_cell) >= 3:
                self.desc_folio_id = arr_cell[0]
                self.desc_source_id = arr_cell[1]
                self.desc_tds_id = arr_cell[2]
        # Extraemos la BUI Local y el PGyC
        bui_start_index = data_text.find(Constants.CRITERIA_TO_FIND_GS) + len(Constants.CRITERIA_TO_FIND_GS)
        data_bui = data_text[bui_start_index: len(data_text) - 1]
        bui_end_index = data_bui.find(Constants.SLASH_ID)
        self.desc_bui_local_id = data_bui[0:bui_end_index]
        # Extraemos el PGyC
        pgyc_start_index = data_bui.find(Constants.CRITERIA_TO_FIND_GS) + len(Constants.CRITERIA_TO_FIND_GS)
        data_pgyc = data_bui[pgyc_start_index:len(data_bui) - 1]
        pgyc_end_index = data_pgyc.find(Constants.SLASH_ID)
        self.desc_pgyc_id = data_pgyc[0:pgyc_end_index]

    def convert_json_story(self, json_jira):

        fields = json_jira["fields"]
        changelog = json_jira["changelog"]
        histories = changelog.get('histories')

        self.feature_key = fields.get("customfield_10004")

        if fields.get('customfield_10002') is not None:
            self.story_points = fields.get('customfield_10002')
        labels = fields["labels"]
        for label in labels:
            if label[0:2] == 'F-':
                self.label_folio_id = label[2:len(label)]
            elif label[0:3] == 'ID-':
                self.label_source_id = label[3:len(label)]
            elif label[0:2] == 'P-':
                self.label_process_id = label[2:len(label)]
        self.labels = ', '.join(labels)
        self._add_attr_basic(json_jira)
        self._get_attr_from_histories(histories)

        # self.__add_attr_dictamen() -- Por ahora se comenta este código
        return self

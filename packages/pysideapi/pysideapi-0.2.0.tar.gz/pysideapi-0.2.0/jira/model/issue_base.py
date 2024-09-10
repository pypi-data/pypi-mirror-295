from datetime import datetime, timedelta

import pytz

from jira.commons.constants import Constants
from jira.model.issue_status import IssueStatus

tz = pytz.timezone('America/Lima')


class IssueBase:
    def __init__(self):
        self.id = ''
        self.key = ''
        self.title = ''
        self.description = ''
        self.issue_type_id = ''
        self.issue_type_name = ''
        self.assignee_name = ''
        self.assignee_email = ''
        self.creator_name = ''
        self.creator_email = ''
        self.sprint_estimate = ''
        self.status_id = ''
        self.status_name = ''
        self.create_date = ''
        self.update_date = ''
        self.historical_status_change = []
        self.labels = ''
        self.jira_project_id = ''
        self.jira_project_key = ''
        self.jira_project_name = ''
        self.team_backlog_id = ''
        self.team_backlog_name = ''
        self.created_team_backlog_id = ''
        self.created_team_backlog_name = ''

    def _add_attr_basic(self, json_jira):
        self.id = json_jira["id"]
        self.key = json_jira["key"]
        fields = json_jira["fields"]
        # changelog = json_jira["changelog"]
        # histories = changelog.get('histories')
        self.title = fields.get("summary")
        self.description = fields.get("description")
        self.issue_type_id = fields.get('issuetype').get('id')
        self.issue_type_name = fields.get('issuetype').get('name')
        self.assignee_name = fields.get("assignee").get("name") if fields.get("assignee") is not None else None
        self.assignee_email = fields.get("assignee").get("emailAddress") if fields.get("assignee") is not None else None
        self.creator_name = fields.get("creator").get("name") if fields.get("creator") is not None else None
        self.creator_email = fields.get("creator").get("emailAddress") if fields.get("creator") is not None else None
        if fields.get('customfield_10272') is not None:
            self.sprint_estimate = fields.get('customfield_10272').get('value')
        if fields.get("status") is not None:
            self.status_id = fields.get("status").get("id")
            self.status_name = fields.get("status").get("name")
        created_date = datetime.strptime(fields.get('created'), '%Y-%m-%dT%H:%M:%S.%f%z')
        created_date = created_date.astimezone(tz)
        created_date = created_date.strftime("%Y-%m-%d %H:%M:%S")
        self.create_date = created_date
        update_date = datetime.strptime(fields.get('updated'), '%Y-%m-%dT%H:%M:%S.%f%z')
        update_date = update_date.astimezone(tz)
        update_date = update_date.strftime("%Y-%m-%d %H:%M:%S")
        self.update_date = update_date
        self.jira_project_id = fields.get('project').get('id')
        self.jira_project_key = fields.get('project').get('key')
        self.jira_project_name = fields.get('project').get('name')
        self.team_backlog_id = ', '.join(fields.get('customfield_13300'))
        # self.labels = fields["labels"]

    def _get_attr_from_histories(self, json_histories):
        # Inclyendo HUT New por Default
        today = datetime.today().astimezone(tz)
        minor_team_backlog_date = today + timedelta(days=1)

        issue_new = IssueStatus()
        issue_new.from_status_id = ''
        issue_new.from_status_name = ''
        issue_new.to_status_id = '10173'
        issue_new.to_status_name = 'New'
        issue_new.status_change_date = self.create_date
        issue_new.modifier_name = self.creator_name
        issue_new.modifier_email = self.creator_email
        issue_new.issue_key = self.key
        self.historical_status_change.append(issue_new)
        # Incluyendo todos los cambios del changelog
        for story in json_histories:
            items = story.get('items')
            for item in items:
                if item.get('field') == 'status':
                    issue_status = IssueStatus()
                    finish = datetime.strptime(story.get('created'), '%Y-%m-%dT%H:%M:%S.%f%z')
                    finish = finish.astimezone(tz)
                    finish = finish.strftime("%Y-%m-%d %H:%M:%S")
                    issue_status.from_status_id = item.get('from')
                    issue_status.from_status_name = item.get('fromString')
                    issue_status.to_status_id = item.get('to')
                    issue_status.to_status_name = item.get('toString')
                    issue_status.status_change_date = finish
                    issue_status.modifier_name = story.get("author").get("displayName")
                    issue_status.modifier_email = story.get("author").get("emailAddress")
                    issue_status.issue_key = self.key
                    self.historical_status_change.append(issue_status)
                if item.get('field') == 'Team Backlog':
                    finish = datetime.strptime(story.get('created'), '%Y-%m-%dT%H:%M:%S.%f%z')
                    finish = finish.astimezone(tz)
                    if finish < minor_team_backlog_date:
                        self.created_team_backlog_id = item.get('from')
                        from_string = item.get('fromString')
                        start_index = from_string.find(Constants.CRITERIA_TO_FIND_START_TEAM_BACKLOG)
                        end_index = from_string.find(Constants.CRITERIA_TO_FIND_END_TEAM_BACKLOG)
                        self.created_team_backlog_name = from_string[start_index:end_index]
                        minor_team_backlog_date = finish
                    if self.team_backlog_id == item.get('to') and self.team_backlog_name == '':
                        to_string = item.get('toString')
                        start_index = to_string.find(Constants.CRITERIA_TO_FIND_START_TEAM_BACKLOG)
                        end_index = to_string.find(Constants.CRITERIA_TO_FIND_END_TEAM_BACKLOG)
                        self.team_backlog_name = to_string[start_index:end_index]
        if self.created_team_backlog_id == "":
            self.created_team_backlog_id = self.team_backlog_id
            self.created_team_backlog_name = self.team_backlog_name


import requests
import config
from .Milestone import Milestone
from factories.IssueFactory import IssueFactory
from .Tag import Tag
from dateutil.parser import parse


class Project(object):

    def __init__(self, _id=None, _json={}):
        if _id:
            _json = requests.get(
                "{}/api/v3/projects/{}".format(
                    config.HOST, _id),
                headers={"PRIVATE-TOKEN": config.PRIVATE_TOKEN}).json()
        self.id = _json['id']
        self.description = _json['description']
        self.default_branch = _json['default_branch']
        self.public = _json['public']
        self.visibility_level = _json['visibility_level']
        self.ssh_url_to_repo = _json['ssh_url_to_repo']
        self.http_url_to_repo = _json['http_url_to_repo']
        self.web_url = _json['web_url']
        self.tag_list = _json['tag_list']
        # self.owner = _json['owner']
        self.name = _json['name']
        self.name_with_namespace = _json['name_with_namespace']
        self.path = _json['path']
        self.path_with_namespace = _json['path_with_namespace']
        self.issues_enabled = _json['issues_enabled']
        self.open_issues_count = _json['open_issues_count']
        self.merge_requests_enabled = _json['merge_requests_enabled']
        self.builds_enabled = _json['builds_enabled']
        self.wiki_enabled = _json['wiki_enabled']
        self.snippets_enabled = _json['snippets_enabled']
        self.container_registry_enabled = _json['container_registry_enabled']
        self.created_at = parse(_json['created_at'])
        self.last_activity_at = parse(_json['last_activity_at'])
        self.creator_id = _json['creator_id']
        self.archived = _json['archived']
        self.avatar_url = _json['avatar_url']
        self.shared_runners_enabled = _json['shared_runners_enabled']
        self.forks_count = _json['forks_count']
        self.star_count = _json['star_count']
        # self.runners_token = _json['runners_token']
        self.public_builds = _json['public_builds']

        self.milestones = []
        self.issues = []
        self.tags = []

    @classmethod
    def findAll(cls):
        _jsons = requests.get("{}/api/v3/projects".format(config.HOST),
                              headers={"PRIVATE-TOKEN": config.PRIVATE_TOKEN}).json()
        return [Project(_json=_json) for _json in _jsons]

    def findAllMilestones(self):
        page = 1
        per_page = 100
        if not self.milestones:
            while True:
                milestones = [Milestone(self, _json=_json)
                              for _json in requests.get("{}/api/v3/projects/{}/milestones?page={}&per_page={}".format(config.HOST, self.id, page, per_page), headers={"PRIVATE-TOKEN": config.PRIVATE_TOKEN}).json()
                              ]
                if not milestones:
                    break
                self.milestones += milestones
                if len(milestones) < per_page:
                    break
                page += 1
        return self.milestones

    def findAllTags(self):
        page = 1
        per_page = 100
        if not self.tags:
            while True:
                tags = [Tag(self, _json=_json)
                        for _json in requests.get("{}/api/v3/projects/{}/repository/tags?page={}&per_page={}".format(config.HOST, self.id, page, per_page), headers={"PRIVATE-TOKEN": config.PRIVATE_TOKEN}).json()
                        ]
                if not tags:
                    break
                self.tags += tags
                if len(tags) < per_page:
                    break
                page += 1
        return self.tags

    def findAllIssues(self):
        page = 1
        per_page = 100
        if not self.issues:
            while True:
                issues = [IssueFactory.factory(self, _json=json_issue)
                          for json_issue in requests.get("{}/api/v3/projects/{}/issues?page={}&per_page={}".format(config.HOST, self.id, page, per_page), headers={"PRIVATE-TOKEN": config.PRIVATE_TOKEN}).json()
                          ]
                if not issues:
                    break
                self.issues += issues
                if len(issues) < per_page:
                    break
                page += 1
        return self.issues

    def getId(self):
        return self.id

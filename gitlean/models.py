import json
from dateutil.parser import parse


class GitlabHook:

    def __init__(self, request):
        self.params = json.loads(request.body.decode('utf-8'))
        if self.params['object_kind'] == 'issue':
            self._update_issue()
        elif self.params['object_kind'] == 'note':
            self._update_note()

    def _update_issue(self):
        from . import controllers
        project = controllers.ProjectController(_id=self.params['object_attributes']['project_id']).find()
        issue = controllers.IssueController(project, _id=self.params['object_attributes']['id']).flushAndUpdate()
        return issue

    def _update_note(self):
        from . import controllers
        project = controllers.ProjectController(_id=self.params['project_id']).find()
        if "issue" in self.params:
            issue = controllers.IssueController(project, _id=self.params['issue']['id']).find()
            note = controllers.NoteController(issue, _id=self.params['object_attributes']['id']).flushAndUpdate()
        return note


class Commit:

    def __init__(self, project, _json={}):
        self.project = project
        self.sha = _json['id']
        self.committed_date = None
        if 'committed_date' in _json:
            self.committed_date = _json['committed_date']
        self.message = _json['message']
        self.author_email = _json['author_email']
        self.author_name = _json['author_name']
        self.authored_date = None
        if 'authored_date' in _json:
            self.authored_date = _json['authored_date']
        self.status = None
        if 'status' in _json:
            self.status = _json['status']
        self.created_at = _json['created_at']
        self.title = _json['title']
        self.short_id = _json['short_id']
        self.parent_ids = []
        if 'parent_ids' in _json:
            self.parent_ids = _json['parent_ids']

    def getParents(self):
        from .controllers import CommitController
        return [CommitController(self.project, _id).find() for _id in self.parent_ids]


class Issue:

    def __init__(self, project, _json={}):
        self.project = project
        self.id = _json['id']
        self.project_id = _json['project_id']
        self.author_id = _json['author']['id']

        self.assignee_id = 0
        if _json['assignee']:
            self.assignee_id = _json['assignee']['id']

        self.milestone_id = 0
        if _json['milestone']:
            self.milestone_id = _json['milestone']['id']

        self.description = _json['description']
        self.state = _json['state']
        self.iid = _json['iid']
        self.labels = _json['labels']
        self.title = _json['title']
        self.updated_at = _json['updated_at']
        self.created_at = _json['created_at']
        self.due_date = 0
        if 'due_date' in _json:
            self.due_date = _json['due_date']
        self.notes = []

    @property
    def findAllNotes(self):
        from .controllers import NoteController
        if not self.notes:
            self.notes = sorted(NoteController(self).findAll(), key=lambda x: x.created_at)
        return self.notes


class Milestone:

    def __init__(self, project, _json={}):
        self.project = project
        self.id = _json['id']
        self.iid = _json['iid']
        self.title = _json['title']
        self.description = _json['description']
        self.due_date = _json['due_date']
        if self.due_date:
            self.due_date = parse(self.due_date)
        self.state = _json['state']
        self.updated_at = _json['updated_at']
        self.created_at = _json['created_at']
        self.issues = []

    def findAllIssues(self):
        from .controllers import IssueController
        if not self.issues:
            self.issues = IssueController(self.project).findAll(milestone=self)
        return self.issues


class Note:

    def __init__(self, issue, _json={}):
        self.id = _json['id']
        self.body = _json['body']
# self.created_at = 0
# if 'created_at' in _json:
        self.created_at = parse(_json['created_at'])
        self.author_id = _json['author']['id']
        self.issue = issue


class Project(object):

    def __init__(self, _json={}):
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
        self.commits = []

    @property
    def findAllMilestones(self):
        from .controllers import MilestoneController
        if not self.milestones:
            self.milestones = MilestoneController(self).findAll()
        return self.milestones

    @property
    def findAllTags(self):
        from .controllers import TagController
        if not self.tags:
            self.tags = TagController(self).findAll()
        return self.tags

    @property
    def findAllIssues(self):
        from .controllers import IssueController
        if not self.issues:
            self.issues = IssueController(self).findAll()
        return self.issues

    @property
    def findAllCommits(self):
        from .controllers import CommitController
        if not self.commits:
            self.commits = CommitController(self).findAll()
        return self.commits


class Tag:

    def __init__(self, project, _json={}):
        self.name = _json['name']
        self.commit_id = _json['commit']['id']
        self.release = _json['release']
        self.message = _json['message']

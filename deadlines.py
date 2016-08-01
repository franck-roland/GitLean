from gitlean import config
import csv
from datetime import datetime
from gitlean.controllers import ProjectController


def writerow(csvwriter, row):
    csvwriter.writerow(row)

if __name__ == '__main__':
    with open('milestones.csv', 'w') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=';')
        for project in ProjectController().findAll():
            if project.name in config.PROJECTS:
                issues = project.findAllIssues()
                milestones = project.findAllMilestones()
                tags = project.findAllTags()
                commits = project.findAllCommits()
                for issue in issues:
                    print(len(issue.findAllNotes()))

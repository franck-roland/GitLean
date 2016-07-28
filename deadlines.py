import config
import csv
from datetime import datetime
from controllers.ProjectController import ProjectController


def writerow(csvwriter, row):
    csvwriter.writerow(row)

if __name__ == '__main__':
    with open('milestones.csv', 'w') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=';')
        for project in ProjectController.findAll():
            if project.name in config.PROJECTS:
                issues = project.findAllIssues()
                milestones = project.findAllMilestones()
                for issue in issues:
                    print(issue)
                    for note in issue.findAllNotes():
                        print(note)

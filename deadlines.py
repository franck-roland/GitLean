import config
import csv
from datetime import datetime
from models.Project import Project


def writerow(csvwriter, row):
    csvwriter.writerow(row)

if __name__ == '__main__':
    with open('milestones.csv', 'w') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=';')
        for project in Project.findAll():
            if project['name'] in config.PROJECTS:
                project = Project(_id=project['id'])
                milestones = project.findAllMilestones()
                issues = project.findAllIssues()
                for milestone in milestones:
                    issues = milestone.findAllIssues()
                    writerow(csvwriter, ['Title', 'Description', 'State', 'Due Date'])
                    writerow(csvwriter, [milestone.title, milestone.description, milestone.state, milestone.due_date])
                    if len(issues):
                        writerow(csvwriter, ['Issue number', 'Issue Title', 'Description', 'State', 'Since'])
                    for issue in issues:
                        if issue.kanban_state and issue.findAllTransitionNotes() and issue.state == 'opened':
                            notes = issue.findAllTransitionNotes()
                            diff = (datetime.now(issue.notes[-1].created_at.tzinfo) - issue.notes[-1].created_at)
                            writerow(csvwriter, ['=HYPERLINK("' + project.web_url + '/issues/' + str(issue.iid) + '","#' + str(issue.iid) + '")', issue.title, issue.description, issue.kanban_state, str(diff)])
                            print(issue.title + '; ' + issue.kanban_state + '; ' + str(diff))

                tags = project.findAllTags()
                for tag in tags:
                    print(tag.name + ' commit ' + str(tag.commit))

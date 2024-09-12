#!/usr/bin/python
# coding=utf-8
import argparse
import sqlite3
import os
from atlassian import Jira
import sys

# Default values.
JIRA_CLOSED = ['Closed', 'Resolved']
JIRA_TYPE = "Task"
JIRA_LABELS = []

# Check if we are running this on windows platform
IS_WINDOWS = sys.platform.startswith('win')

# Console Colors
if IS_WINDOWS:
    # Windows deserves coloring too :D
    G = '\033[92m'  # green
    Y = '\033[93m'  # yellow
    B = '\033[94m'  # blue
    R = '\033[91m'  # red
    W = '\033[0m'   # white
    try:
        import win_unicode_console, colorama
        win_unicode_console.enable()
        colorama.init()
    except:
        G = Y = B = R = W = G = Y = B = R = W = ''
else:
    G = '\033[92m'  # green
    Y = '\033[93m'  # yellow
    B = '\033[94m'  # blue
    R = '\033[91m'  # red
    W = '\033[0m'   # white


def db_install(sqli_db):
    if not (os.path.isfile('./' + sqli_db)):
        db = sqlite3.connect(sqli_db)
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE jira(identifier TEXT PRIMARY KEY, jira_key TEXT)''')
        db.commit()
        db.close()
    else:
        pass


def upsert_new_identifier(identifier, jira_key):
    try:
        # Update if it exists
        cursor.execute('''UPDATE jira SET jira_key=? WHERE identifier=?''', (jira_key, identifier))
        # Insert or ignore if already exists
        cursor.execute('''INSERT OR IGNORE INTO jira(identifier, jira_key) VALUES(?,?)''', (identifier, jira_key))
        db.commit()
    except Exception as e:
        print(e)


def is_identifier_in_db(identifier):
    try:
        cursor.execute('''SELECT * from jira where identifier = ?''', (identifier,))
        if cursor.fetchall():
            return True
        else:
            return False
    except Exception as e:
        return False


def get_jira_key_by_identifier(identifier):
    try:
        cursor.execute('''SELECT jira_key FROM jira where identifier = ?''', (identifier,))
        all_rows = cursor.fetchall()
        for row in all_rows:
            return row[0]
    except Exception as e:
        print(e)
    return ""


def update_jira_db(id, jira_key):
    try:
        cursor.execute('''UPDATE jira SET jira_key = ? WHERE id = ? ''', (jira_key, id))
        db.commit()
    except Exception as e:
        print("We could not connect to {} due to following error: {}".format(jira_key, e))

def has_existing_task_stateless(identifier, jira_closed, stateless_field_name):
    if stateless_field_name:
        # If stateless_field_name is provided, use it to check for existing tasks in Jira.
        # Use JQL to search for issues with the custom field matching the local identifier and open status.
        statuses = ",".join(['"' + status + '"' for status in jira_closed])
        jql = f'"{stateless_field_name}" = "{identifier}" AND status not in ({statuses})'

        issues = jira.search_issues(jql)

        if issues:
            # Issue with the same local identifier exists and not closed.
            return True

    return False


def has_existing_task_local_db(identifier, jira_closed):
    # Check the local database
    if is_identifier_in_db(identifier):
        jira_key = get_jira_key_by_identifier(identifier)
        status = jira.get_issue_status(jira_key)
        # If task exists but is closed, return False.
        if status in jira_closed:
            return False
        else:
            return True

    return False


# Checks if we already have an existing Jira task so we'll know if we want to update or create a new one.
def has_existing_task(identifier, jira_closed, stateless_field_name):
    # Check if stateless_field_name is provided.
    if stateless_field_name:
        return has_existing_task_stateless(identifier, jira_closed, stateless_field_name)
    else:
        return has_existing_task_local_db(identifier, jira_closed)


# Upsert a jira issue (wrapper for insert or update actions).
def upsert_jira(identifier, project, summary, skip_existing, jira_closed, attachments, itype, description, labels, priority, stateless_field_name):
    if has_existing_task(identifier, jira_closed, stateless_field_name):
        if skip_existing:
            print('Issue already exists and open. Skipping.')
            return False
        jira_key = get_jira_key_by_identifier(identifier)
        update_jira(jira_key, attachments)
    else:
        new_jira = create_new_jira(project, itype, summary, description, labels, attachments, priority, identifier, stateless_field_name)
        jira_key = new_jira['key']
        upsert_new_identifier(identifier, jira_key)
        print(f'Created new Jira ticket: {jira_key}. jTrack id: {identifier}')


# Create a new Jira issue.
def create_new_jira(project, itype, summary, description, labels, attachments, priority, local_identifier, stateless_field_name):
    fields = {
        'project': {'key': project},
        'issuetype': {
            "name": itype
        },
        'summary': summary,
        'labels': labels
    }

    # Add custom field for local identifier
    if stateless_field_name and local_identifier:
        fields[stateless_field_name] = local_identifier

    # Add priority
    if priority is not None:
        fields['priority'] = {'name': priority}

    # Add description.
    if description is not None:
        fields['description'] = description

    new_task = jira.issue_create(fields=fields)

    jira_key = new_task['id']

    # Add the report as an attachment
    if attachments is not None:
        for attachment in attachments:
            jira.add_attachment(jira_key, attachment)

    return new_task


# Currently onlyl support attachment addition.
# @todo Extend to support description.
def update_jira(jira_key, attachments):
    if attachments is not None:
        for attachment in attachments:
            jira.add_attachment(jira_key, attachment)
    else:
        print('No attachment provided. Nothing to updated.')


def attachment_arg(paths):
    # from os.path import exists
    paths = str(paths).split(',')
    for path in paths:
        if not os.path.isfile(path):
            raise ValueError  # or TypeError, or `argparse.ArgumentTypeError
    return paths


def banner():
    print("""%s                                        
  ,--.,--------.                     ,--.     
  `--''--.  .--',--.--. ,--,--. ,---.|  |,-.  
  ,--.   |  |   |  .--'' ,-.  || .--'|     /  
  |  |   |  |   |  |   \ '-'  |\ `--.|  \  \  
.-'  /   `--'   `--'    `--`--' `---'`--'`--' 
'---'%s%s

              # Coded By Rotem Reiss - @2RS3C
    """ % (B, W, B))


def main(identifier, project, summary, **kwargs):
    global db
    global cursor
    global jira

    # Every tool needs a banner.
    if kwargs.get('quiet', False) is False:
        banner()

    # Jira Connection Details
    JIRA_URL = os.environ.get('JIRA_URL')
    JIRA_USER = os.environ.get('JIRA_USER')
    JIRA_PASSWORD = os.environ.get('JIRA_PASSWORD')

    jira = Jira(
        url=JIRA_URL,
        username=JIRA_USER,
        password=JIRA_PASSWORD)

    stateless_field_name = kwargs.get('stateless_field_name')

    if not stateless_field_name:
        # Init DB.
        sqli_db = "jtrack.db"
        db_install(sqli_db)
        db = sqlite3.connect(sqli_db)
        cursor = db.cursor()

    # Initialize default values.
    skip_existing = kwargs.get('skip_existing', True)
    jira_closed = kwargs.get('jira_closed', JIRA_CLOSED)
    attachments = kwargs.get('attach', None)
    itype = kwargs.get('itype', JIRA_TYPE)
    description = kwargs.get('desc', None)
    labels = kwargs.get('labels', JIRA_LABELS)
    priority = kwargs.get('priority', None)
    stateless_field_name = kwargs.get('stateless_field_name')
    upsert_jira(
        identifier,
        project,
        summary,
        skip_existing,
        jira_closed,
        attachments,
        itype,
        description,
        labels,
        priority,
        stateless_field_name
    )

    if not stateless_field_name:
        db.close()


def interactive():
    parser = argparse.ArgumentParser(description='Creates a Jira task.')

    # Add the arguments
    parser.add_argument('-i', '--identifier', help='A system identifier for the issue.', dest='identifier',
                        required=True)
    parser.add_argument('-p', '--project', help='The project\'s name on Jira (e.g. EXAMPLE).', dest='project',
                        required=True)
    parser.add_argument('-s', '--summary', help='Value for the summary field.', dest='summary', required=True)
    parser.add_argument('-d', '--description', help='Value for the description field.', dest='desc')
    parser.add_argument('-pr', '--priority', help='Value for the priority field.', dest='priority')
    parser.add_argument('-a', '--attachment', help='One or more file paths seperated by comma to be attached', type=attachment_arg,
                        dest='attach')
    parser.add_argument('-l', '--labels', nargs='*', help='Jira labels to add to new issues.', dest='labels',
                        default=JIRA_LABELS,
                        type=str)
    parser.add_argument('-j', '--jira-closed-status', nargs='*', help='Jira statuses that are considered to be closed.',
                        dest='jira_closed',
                        default=JIRA_CLOSED,
                        type=str)
    parser.add_argument('-t', '--jira-type', help='Jira issue type for new tasks.', dest='itype', default=JIRA_TYPE,
                        required=False)
    parser.add_argument('-se', '--skip-existing', help='Do nothing if Jira already exists and open.',
                        action='store_true',
                        dest='skip_existing')
    parser.add_argument('-sfn', '--stateless-field-name', help='Name of the Jira custom field for holding the local identifier.', dest='stateless_field_name')
    parser.add_argument('-q', '--quiet', help='Do not print the banner.', action='store_true', dest='quiet')
    args = parser.parse_args()

    main(args.identifier,
         args.project,
         args.summary,
         desc=args.desc,
         priority=args.priority,
         attach=args.attach,
         labels=args.labels,
         jira_closed=args.jira_closed,
         itype=args.itype,
         skip_existing=args.skip_existing,
         quiet=args.quiet,
         stateless_field_name=args.stateless_field_name
         )


if __name__ == "__main__":
    interactive()

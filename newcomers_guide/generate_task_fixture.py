import json
from newcomers_guide import process_files


def generate_task_fixture(files):
    header = ('export const buildTasksFixture = (): Store => {\n'
              '    return {\n'
              '        taskMap: ')

    footer = ('\n'
              '    }\n'
              '}')

    result = process_files.process_all_files(files)

    return header + json.dumps(result) + footer

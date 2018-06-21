import json
from newcomers_guide import process_files


def generate_task_fixture(files):
    header = ('export const buildTasksFixture = (): Store => {\n'
              '    return {\n'
              '        taskMap: ')

    footer = ('\n'
              '    }\n'
              '}')

    result = process_files.process_all_task_files(files)

    return header + json.dumps(result, ensure_ascii=True, sort_keys=True, indent=4) + footer

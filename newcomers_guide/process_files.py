from newcomers_guide import parse_file_path, data_cleanup, task_builder


def process_all_task_files(file_specs):
    builders = {}
    for spec in file_specs:
        path = spec[0]
        description = clean_text(spec[1])
        parsed_path = parse_file_path.parse_file_path(path)
        task_id = parsed_path.id

        if parsed_path.type == 'tasks':
            if task_id in builders:
                add_to_existing_builder(builders[task_id], parsed_path, description)
            else:
                builders[task_id] = create_builder(parsed_path, description)

    return make_task_map(builders)


def clean_text(text):
    text = data_cleanup.clean_up_newlines(text)
    text = data_cleanup.clean_up_links(text)
    return text


def create_builder(parsed_path, description):
    task_id = parsed_path.id
    locale = parsed_path.locale
    builder = task_builder.TaskBuilder()
    builder.set_id(task_id)
    builder.set_title_in_locale(locale, parsed_path.title)
    builder.set_description_in_locale(locale, description)
    return builder


def add_to_existing_builder(builder, parsed_path, description):
    locale = parsed_path.locale
    builder.set_title_in_locale(locale, parsed_path.title)
    builder.set_description_in_locale(locale, description)


def make_task_map(builders):
    tasks = {}
    for key in builders:
        tasks[key] = builders[key].to_task()
    return tasks

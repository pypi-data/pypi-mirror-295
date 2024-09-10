from os.path import join
import os
import sys
import json
from ara_cli.output_suppressor import suppress_stdout


def check_validity(condition, error_message):
    if not condition:
        print(error_message)
        sys.exit(1)


def create_action(args):
    from ara_cli.artefact_creator import ArtefactCreator
    from ara_cli.classifier_validator import is_valid_classifier
    from ara_cli.filename_validator import is_valid_filename
    from ara_cli.template_manager import SpecificationBreakdownAspects

    check_validity(is_valid_classifier(args.classifier), "Invalid classifier provided. Please provide a valid classifier.")
    check_validity(is_valid_filename(args.parameter), "Invalid filename provided. Please provide a valid filename.")

    aspect = args.aspect if hasattr(args, "aspect") else None
    if args.parameter and args.classifier and aspect:
        sba = SpecificationBreakdownAspects()
        try:
            sba.create(args.parameter, args.classifier, aspect)
            return
        except ValueError as ve:
            print(f"Error: {ve}")
            sys.exit(1)

    parent_classifier = args.parent_classifier if hasattr(args, "parent_classifier") else None
    parent_name = args.parent_name if hasattr(args, "parent_name") else None
    if parent_classifier and parent_name:
        check_validity(is_valid_classifier(parent_classifier), "Invalid parent classifier provided. Please provide a valid classifier")
        check_validity(is_valid_filename(parent_name), "Invalid filename provided for parent. Please provide a valid filename.")

    template_path = join(os.path.dirname(__file__), 'templates')
    artefact_creator = ArtefactCreator()
    artefact_creator.run(args.parameter, args.classifier, template_path, parent_classifier, parent_name)


def delete_action(args):
    from ara_cli.artefact_deleter import ArtefactDeleter

    artefact_deleter = ArtefactDeleter()
    artefact_deleter.delete(args.parameter, args.classifier)


def rename_action(args):
    from ara_cli.artefact_renamer import ArtefactRenamer
    from ara_cli.classifier_validator import is_valid_classifier
    from ara_cli.filename_validator import is_valid_filename

    check_validity(is_valid_filename(args.parameter), "Invalid filename provided. Please provide a valid filename.")
    check_validity(is_valid_classifier(args.classifier), "Invalid classifier provided. Please provide a valid classifier.")
    check_validity(is_valid_filename(args.aspect), "Invalid new filename provided. Please provide a valid filename.")

    artefact_renamer = ArtefactRenamer()
    artefact_renamer.rename(args.parameter, args.aspect, args.classifier)


def list_action(args):
    from ara_cli.artefact_lister import ArtefactLister

    artefact_lister = ArtefactLister()
    if (args.tags):
        artefact_lister.list_files(tags=args.tags)
        return
    artefact_lister.list_files()


def get_tags_action(args):
    from ara_cli.tag_extractor import TagExtractor

    tag_extractor = TagExtractor()
    tags = tag_extractor.extract_tags()

    if args.json:
        output = json.dumps({"tags": tags})
        print(output)
        return

    output = "\n".join(f"- {tag}" for tag in tags)
    print(output)


def prompt_action(args):
    from ara_cli.prompt_handler import initialize_prompt_templates, load_selected_prompt_templates
    from ara_cli.prompt_handler import create_and_send_custom_prompt
    from ara_cli.prompt_extractor import extract_and_save_prompt_results
    from ara_cli.update_config_prompt import update_artefact_config_prompt_files
    from ara_cli.prompt_rag import search_and_add_relevant_files_to_prompt_givens
    from ara_cli.prompt_chat import initialize_prompt_chat_mode
    from ara_cli.classifier_validator import is_valid_classifier
    from ara_cli.filename_validator import is_valid_filename

    check_validity(is_valid_classifier(args.classifier), "Invalid classifier provided. Please provide a valid classifier.")
    check_validity(is_valid_filename(args.parameter), "Invalid filename provided. Please provide a valid filename.")

    classifier = args.classifier
    param = args.parameter
    init = args.steps

    if (init == 'init'):
        initialize_prompt_templates(classifier, param)
    if (init == 'init-rag'):
        initialize_prompt_templates(classifier, param)
        search_and_add_relevant_files_to_prompt_givens(classifier, param)
    if (init == 'load'):
        load_selected_prompt_templates(classifier, param)
    if (init == 'send'):
        create_and_send_custom_prompt(classifier, param)
    if (init == 'load-and-send'):
        load_selected_prompt_templates(classifier, param)
        create_and_send_custom_prompt(classifier, param)
    if (init == 'extract'):
        extract_and_save_prompt_results(classifier, param)
        print(f"automatic update after extract")
        update_artefact_config_prompt_files(classifier, param, automatic_update=True)
    if (init == 'chat'):
        chat_name = args.chat_name
        reset = args.reset
        output_mode = args.output_mode
        append_strings = args.append
        initialize_prompt_chat_mode(classifier, param, chat_name, reset=reset, output_mode=output_mode, append_strings=append_strings)
    if (init == 'update'):
        update_artefact_config_prompt_files(classifier, param, automatic_update=True)


def chat_action(args):
    from ara_cli.chat import Chat

    reset = args.reset
    output_mode = args.output_mode
    append_strings = args.append

    chat_name = "chat"
    if args.chat_name:
        chat_name = args.chat_name
    cwd = os.getcwd()
    chat_file_path = join(cwd, chat_name)
    with suppress_stdout(output_mode):
        chat = Chat(chat_file_path, reset=reset)

    if append_strings:
        chat.append_strings(append_strings)

    if output_mode:
        chat.start_non_interactive()
        return
    chat.start()


def template_action(args):
    from ara_cli.classifier import Classifier
    from ara_cli.template_manager import TemplatePathManager

    check_validity(Classifier.is_valid_classifier(args.classifier), "Invalid classifier provided. Please provide a valid classifier.")
    check_validity(Classifier.is_valid_classifier(args.classifier), "Invalid classifier provided. Please provide a valid classifier.")

    template_manager = TemplatePathManager()
    content = template_manager.get_template_content(args.classifier)

    print(content)


def fetch_templates_action(args):
    import shutil
    from ara_cli.ara_config import ConfigManager
    from ara_cli.template_manager import TemplatePathManager

    config = ConfigManager().get_config()
    prompt_templates_dir = config.local_prompt_templates_dir
    template_base_path = TemplatePathManager.get_template_base_path()
    global_prompt_templates_path = join(template_base_path, "prompt-modules")

    subdirs = ["commands", "rules", "intentions", "recipes"]

    os.makedirs(join(prompt_templates_dir, "global-prompt-modules"), exist_ok=True)
    for subdir in subdirs:
        target_dir = join(prompt_templates_dir, "global-prompt-modules", subdir)
        source_dir = join(global_prompt_templates_path, subdir)
        os.makedirs(target_dir, exist_ok=True)
        for item in os.listdir(source_dir):
            source = join(source_dir, item)
            target = join(target_dir, item)
            shutil.copy2(source, target)

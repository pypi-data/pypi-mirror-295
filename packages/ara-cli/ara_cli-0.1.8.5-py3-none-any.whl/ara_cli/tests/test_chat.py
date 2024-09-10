import pytest
import os
import tempfile
import mock
import glob
import cmd2
from unittest.mock import patch, MagicMock
from ara_cli.chat import Chat

# dependencies for mocking purposes
from ara_cli.template_manager import TemplatePathManager
from ara_cli.ara_config import ConfigManager


@pytest.fixture
def temp_chat_file():
    """Fixture to create a temporary chat file."""
    temp_file = tempfile.NamedTemporaryFile(delete=True, mode='w+', encoding='utf-8')
    yield temp_file
    temp_file.close()


@pytest.fixture
def temp_load_file():
    """Fixture to create a temporary file to load."""
    temp_file = tempfile.NamedTemporaryFile(delete=True, mode='w+', encoding='utf-8')
    temp_file.write("This is the content to load.")
    temp_file.flush()
    yield temp_file
    temp_file.close()


def test_handle_existing_chat_no_reset(temp_chat_file):
    with mock.patch('builtins.input', return_value='n'):
        chat = Chat(temp_chat_file.name, reset=None)
        assert chat.chat_name == temp_chat_file.name


def test_handle_existing_chat_with_reset(temp_chat_file):
    with mock.patch('builtins.input', return_value='y'):
        chat = Chat(temp_chat_file.name, reset=None)
        with open(temp_chat_file.name, 'r', encoding='utf-8') as file:
            content = file.read()
        assert content.strip() == "# ara prompt:"


def test_handle_existing_chat_reset_flag(temp_chat_file):
    chat = Chat(temp_chat_file.name, reset=True)
    with open(temp_chat_file.name, 'r', encoding='utf-8') as file:
        content = file.read()
    assert content.strip() == "# ara prompt:"


@pytest.mark.parametrize("chat_name, expected_file_name", [
    ("test", "test_chat.md"),
    ("test.md", "test.md"),
    ("test_chat", "test_chat.md"),
    ("test_chat.md", "test_chat.md"),
    ("another_test", "another_test_chat.md"),
    ("another_test.md", "another_test.md")
])
def test_initialize_new_chat(chat_name, expected_file_name):
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_chat_file_path = os.path.join(temp_dir, "temp_chat_file.md")
        chat_instance = Chat(temp_chat_file_path, reset=False)
        created_chat_file = chat_instance.initialize_new_chat(os.path.join(temp_dir, chat_name))

        assert created_chat_file.endswith(expected_file_name)
        assert os.path.exists(created_chat_file)

        with open(created_chat_file, 'r', encoding='utf-8') as file:
            content = file.read()

        assert content == chat_instance.default_chat_content


@pytest.mark.parametrize("chat_name, existing_files, expected", [
    ("test_chat", ["test_chat"], "test_chat"),
    ("test_chat", ["test_chat.md"], "test_chat.md"),
    ("test_chat", ["test_chat_chat.md"], "test_chat_chat.md"),
    ("new_chat", [], "new_chat_chat.md"),
])
def test_setup_chat(monkeypatch, chat_name, existing_files, expected):
    def mock_exists(path):
        return path in existing_files

    monkeypatch.setattr(os.path, 'exists', mock_exists)
    monkeypatch.setattr(Chat, 'handle_existing_chat', lambda self, chat_file, reset=None: chat_file)
    monkeypatch.setattr(Chat, 'initialize_new_chat', lambda self, chat_name: f"{chat_name}_chat.md")

    chat_instance = Chat(chat_name)
    result = chat_instance.setup_chat(chat_name)
    assert result == expected


@pytest.mark.parametrize("lines, expected", [
    (["This is a line.", "Another line here.", "Yet another line."], None),
    (["This is a line.", "# ara prompt:", "Another line here."], "# ara prompt:"),
    (["This is a line.", "# ara prompt:", "Another line here.", "# ara response:"], "# ara response:"),
    (["This is a line.", "  # ara prompt:  ", "Another line here.", "  # ara response:   "], "# ara response:"),
    (["# ara prompt:", "# ara response:"], "# ara response:"),
    (["# ara response:", "# ara prompt:", "# ara prompt:", "# ara response:"], "# ara response:"),
    ([], None)
])
def test_get_last_role_marker(lines, expected):
    assert Chat.get_last_role_marker(lines=lines) == expected


def test_start_non_interactive(temp_chat_file, capsys):
    content = "This is a test chat content.\nAnother line of chat."
    temp_chat_file.write(content)
    temp_chat_file.flush()

    chat = Chat(temp_chat_file.name, reset=False)
    chat.start_non_interactive()

    captured = capsys.readouterr()

    assert content + "\n" in captured.out


def test_start(temp_chat_file):
    initial_dir = os.getcwd()
    chat = Chat(temp_chat_file.name, reset=False)

    with patch('ara_cli.chat.Chat.cmdloop') as mock_cmdloop:
        chat.start()
        mock_cmdloop.assert_called_once()

    assert os.getcwd() == os.path.dirname(temp_chat_file.name)

    os.chdir(initial_dir)


@pytest.mark.parametrize("initial_content, expected_content", [
    (["This is a line.\n", "Another line here.\n", "Yet another line.\n"],
     ["This is a line.\n", "Another line here.\n", "Yet another line.\n", "\n", "# ara prompt:"]),

    (["This is a line.\n", "# ara prompt:\n", "Another line here.\n"],
     ["This is a line.\n", "# ara prompt:\n", "Another line here.\n"]),

    (["This is a line.\n", "# ara prompt:\n", "Another line here.\n", "# ara response:\n"],
     ["This is a line.\n", "# ara prompt:\n", "Another line here.\n", "# ara response:\n", "\n", "# ara prompt:"]),

    (["This is a line.\n", "  # ara prompt:  \n", "Another line here.\n", "  # ara response:   \n"],
     ["This is a line.\n", "  # ara prompt:  \n", "Another line here.\n", "  # ara response:   \n", "\n", "# ara prompt:"]),

    (["# ara prompt:\n", "# ara response:\n"],
     ["# ara prompt:\n", "# ara response:\n", "\n", "# ara prompt:"]),

    (["# ara response:\n", "# ara prompt:\n", "# ara prompt:\n", "# ara response:\n"],
     ["# ara response:\n", "# ara prompt:\n", "# ara prompt:\n", "# ara response:\n", "\n", "# ara prompt:"]),
])
def test_add_prompt_tag_if_needed(temp_chat_file, initial_content, expected_content):
    temp_chat_file.writelines(initial_content)
    temp_chat_file.flush()

    Chat(temp_chat_file.name, reset=False).add_prompt_tag_if_needed(temp_chat_file.name)

    with open(temp_chat_file.name, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    assert lines == expected_content


@pytest.mark.parametrize("lines, expected", [
    (["\n", "   ", "# ara prompt:", "Another line here.", "  \n"], "Another line here."),
    (["This is a line.", "Another line here.", "  \n", "\n"], "Another line here."),
    (["\n", "  \n", "  \n"], ""),
    (["This is a line.", "Another line here.", "# ara response:", "  \n"], "# ara response:"),
])
def test_get_last_non_empty_line(lines, expected, temp_chat_file):
    temp_chat_file.writelines(line + '\n' for line in lines)
    temp_chat_file.flush()

    with open(temp_chat_file.name, 'r', encoding='utf-8') as file:
        assert Chat.get_last_non_empty_line(Chat, file) == expected


@pytest.mark.parametrize("chat_history, last_line_in_file, expected_written_content", [
    (["Message 1", "Message 2"], "Some other line", "\n# ara response:\n"),
    (["Message 1", "Message 2"], "# ara response:", ""),
])
def test_send_message(temp_chat_file, chat_history, last_line_in_file, expected_written_content):
    chat = Chat(temp_chat_file.name, reset=False)
    chat.chat_history = chat_history

    mock_chunks = [MagicMock(content="response_part_1"), MagicMock(content="response_part_2")]
    with patch('ara_cli.chat.send_prompt', return_value=mock_chunks):
        with patch.object(chat, 'get_last_non_empty_line', return_value=last_line_in_file):
            chat.send_message()

    with open(temp_chat_file.name, 'r', encoding='utf-8') as file:
        lines = file.read()

    assert expected_written_content in lines
    assert "response_part_1" in lines
    assert "response_part_2" in lines


@pytest.mark.parametrize("role, message, initial_content, expected_content", [
    ("ara prompt", "This is a new prompt message.",
     ["Existing content.\n"],
     ["Existing content.\n", "\n", "# ara prompt:\nThis is a new prompt message.\n"]),

    ("ara response", "This is a new response message.",
     ["# ara prompt:\nThis is a prompt.\n"],
     ["# ara prompt:\nThis is a prompt.\n", "\n", "# ara response:\nThis is a new response message.\n"]),

    ("ara prompt", "This is another prompt.",
     ["# ara response:\nThis is a response.\n"],
     ["# ara response:\nThis is a response.\n", "\n", "# ara prompt:\nThis is another prompt.\n"]),

    ("ara response", "Another response here.",
     ["# ara prompt:\nPrompt here.\n", "# ara response:\nFirst response.\n"],
     ["# ara prompt:\nPrompt here.\n", "# ara response:\nFirst response.\n", "\n", "# ara response:\nAnother response here.\n"]),

    ("ara prompt", "Final prompt message.",
     ["# ara prompt:\nInitial prompt.\n", "# ara response:\nResponse here.\n"],
     ["# ara prompt:\nInitial prompt.\n", "# ara response:\nResponse here.\n", "\n", "# ara prompt:\nFinal prompt message.\n"])
])
def test_save_message(temp_chat_file, role, message, initial_content, expected_content):
    temp_chat_file.writelines(initial_content)
    temp_chat_file.flush()

    chat_instance = Chat(temp_chat_file.name, reset=False)
    chat_instance.save_message(role, message)

    with open(temp_chat_file.name, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    assert ''.join(lines) == ''.join(expected_content)


@pytest.mark.parametrize("initial_content, expected_content, expected_chat_history", [
    (["# ara prompt:\nPrompt message.\n", "# ara response:\nResponse message.\n"],
     ["# ara prompt:\nPrompt message.\n"],
     ["# ara prompt:\nPrompt message.\n"]),
    (["# ara prompt:\nPrompt message 1.\n", "# ara response:\nResponse message 1.\n", "# ara prompt:\nPrompt message 2.\n", "# ara response:\nResponse message 2.\n"],
     ["# ara prompt:\nPrompt message 1.\n", "# ara response:\nResponse message 1.\n", "# ara prompt:\nPrompt message 2.\n"],
     ["# ara prompt:\nPrompt message 1.\n", "# ara response:\nResponse message 1.\n", "# ara prompt:\nPrompt message 2.\n"]),
    (["# ara prompt:\nOnly prompt message.\n"],
     ["# ara prompt:\nOnly prompt message.\n"],
     ["# ara prompt:\nOnly prompt message.\n"]),
    (["# ara prompt:\nPrompt message.\n", "# ara response:\nResponse message.\n", "# ara prompt:\nAnother prompt message.\n"],
     ["# ara prompt:\nPrompt message.\n", "# ara response:\nResponse message.\n", "# ara prompt:\nAnother prompt message.\n"],
     ["# ara prompt:\nPrompt message.\n", "# ara response:\nResponse message.\n", "# ara prompt:\nAnother prompt message.\n"]),
])
def test_resend_message(temp_chat_file, initial_content, expected_content, expected_chat_history):
    temp_chat_file.writelines(initial_content)
    temp_chat_file.flush()

    chat = Chat(temp_chat_file.name, reset=False)

    with patch.object(chat, 'send_message') as mock_send_message:
        chat.resend_message()

    with open(temp_chat_file.name, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    assert ''.join(lines) == ''.join(expected_content)
    assert ''.join(chat.chat_history) == ''.join(expected_chat_history)
    mock_send_message.assert_called_once()


def test_resend_message_empty(temp_chat_file):
    temp_chat_file.writelines([])
    temp_chat_file.flush()

    chat = Chat(temp_chat_file.name, reset=False)

    with patch.object(chat, 'send_message') as mock_send_message:
        chat.resend_message()

    with open(temp_chat_file.name, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    assert ''.join(lines) == ''
    assert ''.join(chat.chat_history) == ''
    mock_send_message.assert_not_called()


@pytest.mark.parametrize("strings, expected_content", [
    (["Line 1", "Line 2", "Line 3"], "Line 1\nLine 2\nLine 3\n"),
    (["Single line"], "Single line\n"),
    (["First line", "", "Third line"], "First line\n\nThird line\n"),
    ([], "\n"),
])
def test_append_strings(temp_chat_file, strings, expected_content):
    chat_instance = Chat(temp_chat_file.name, reset=False)
    chat_instance.append_strings(strings)

    with open(temp_chat_file.name, 'r', encoding='utf-8') as file:
        content = file.read()

    assert content == expected_content


def test_load_file(temp_chat_file):
    chat = Chat(temp_chat_file.name, reset=False)

    with tempfile.NamedTemporaryFile(delete=True, mode='w+', encoding='utf-8') as temp_load_file:
        temp_load_file.write("This is the content to load.")
        temp_load_file.flush()

        assert chat.load_file(temp_load_file.name)
        with open(chat.chat_name, 'r', encoding='utf-8') as file:
            content = file.read()
        assert "This is the content to load." in content

        chat.create_empty_chat_file(chat.chat_name)

        prefix = "Prefix:\n"
        suffix = "\nSuffix."
        assert chat.load_file(temp_load_file.name, prefix=prefix, suffix=suffix)
        with open(chat.chat_name, 'r', encoding='utf-8') as file:
            content = file.read()
        assert "Prefix:\nThis is the content to load.\nSuffix." in content


def test_load_file_not_found(temp_chat_file):
    chat = Chat(temp_chat_file.name, reset=False)

    assert not chat.load_file("non_existent_file.txt")


@pytest.mark.parametrize("directory, pattern, file_type, existing_files, user_input, expected_output, expected_loaded_file", [
    ("prompt.data", "*.rules.md", "rules", ["rules1.md"], "", "Loaded rules from rules1.md", "rules1.md"),
    ("prompt.data", "*.rules.md", "rules", ["rules1.md", "rules2.md"], "1", "Loaded rules from rules1.md", "rules1.md"),
    ("prompt.data", "*.rules.md", "rules", ["rules1.md", "rules2.md"], "2", "Loaded rules from rules2.md", "rules2.md"),
    ("prompt.data", "*.rules.md", "rules", ["rules1.md", "rules2.md"], "3", "Invalid choice. Aborting load.", None),
    ("prompt.data", "*.rules.md", "rules", ["rules1.md", "rules2.md"], "invalid", "Invalid input. Aborting load.", None),  # Added case for ValueError
    ("prompt.data", "*.rules.md", "rules", [], "", "No rules file found.", None),
])
def test_load_helper(monkeypatch, capsys, temp_chat_file, directory, pattern, file_type, existing_files, user_input, expected_output, expected_loaded_file):
    def mock_glob(file_pattern):
        return existing_files

    def mock_input(prompt):
        return user_input

    def mock_load_file(self, file_path, prefix="", suffix=""):
        return True

    monkeypatch.setattr(glob, 'glob', mock_glob)
    monkeypatch.setattr('builtins.input', mock_input)
    monkeypatch.setattr(Chat, 'load_file', mock_load_file)
    monkeypatch.setattr(Chat, 'add_prompt_tag_if_needed', lambda self, chat_file: None)

    chat = Chat(temp_chat_file.name, reset=False)
    chat._load_helper(directory, pattern, file_type)

    captured = capsys.readouterr()
    assert expected_output in captured.out

    if expected_loaded_file:
        assert expected_loaded_file in captured.out


def test_help_menu_with_aliases(temp_chat_file, capsys):
    chat = Chat(temp_chat_file.name, reset=False)

    chat._help_menu(verbose=False)
    captured = capsys.readouterr()

    assert "Aliases" in captured.out
    assert "q -> quit" in captured.out
    assert "h -> help" in captured.out
    assert "s -> SEND" in captured.out


def test_do_quit(temp_chat_file, capsys):
    chat = Chat(temp_chat_file.name, reset=False)

    with patch('cmd2.Cmd.do_quit', return_value=True) as mock_do_quit:
        chat.do_quit("")
        mock_do_quit.assert_called_once()

    captured = capsys.readouterr()
    assert "Chat ended" in captured.out


def test_onecmd_plus_hooks(temp_chat_file):
    chat = Chat(temp_chat_file.name, reset=False)

    command = "dummy command"

    with patch.object(chat, 'full_input', create=True):
        with patch.object(cmd2.Cmd, 'onecmd_plus_hooks', return_value=True) as mock_super_onecmd_plus_hooks:
            result = chat.onecmd_plus_hooks(command)

    mock_super_onecmd_plus_hooks.assert_called_once_with(command)
    assert result is True


def test_default(temp_chat_file):
    chat = Chat(temp_chat_file.name, reset=False)
    chat.full_input = "sample input"
    chat.default(chat.full_input)
    assert chat.message_buffer == ["sample input"]


@pytest.mark.parametrize("file_name, matching_files, expected_output, expected_loaded_file", [
    ("test_file.txt", ["test_file.txt"], "Loaded contents of file test_file.txt", "test_file.txt"),
    ("test_file.txt", ["test_file_1.txt", "test_file_2.txt"], "Loaded contents of file test_file_1.txt", "test_file_1.txt"),
    ("non_existent_file.txt", [], "No files matching pattern non_existent_file.txt found.", None),
])
def test_do_LOAD(monkeypatch, capsys, temp_chat_file, file_name, matching_files, expected_output, expected_loaded_file):
    def mock_glob(file_pattern):
        return matching_files

    def mock_load_file(self, file_path, prefix="", suffix=""):
        return True

    monkeypatch.setattr(glob, 'glob', mock_glob)
    monkeypatch.setattr(Chat, 'load_file', mock_load_file)
    monkeypatch.setattr(Chat, 'add_prompt_tag_if_needed', lambda self, chat_file: None)

    chat = Chat(temp_chat_file.name, reset=False)
    chat.do_LOAD(file_name)

    captured = capsys.readouterr()
    assert expected_output in captured.out

    if expected_loaded_file:
        assert expected_loaded_file in captured.out


def test_do_LOAD_interactive(monkeypatch, capsys, temp_chat_file, temp_load_file):
    def mock_glob(file_pattern):
        return [temp_load_file.name]

    def mock_input(prompt):
        return temp_load_file.name

    monkeypatch.setattr(glob, 'glob', mock_glob)
    monkeypatch.setattr('builtins.input', mock_input)
    monkeypatch.setattr(Chat, 'add_prompt_tag_if_needed', lambda self, chat_file: None)

    chat = Chat(temp_chat_file.name, reset=False)
    chat.do_LOAD("")

    captured = capsys.readouterr()
    assert f"Loaded contents of file {temp_load_file.name}" in captured.out


@pytest.mark.parametrize("text, line, begidx, endidx, matching_files", [
    ("file", "LOAD file", 5, 9, ["file1.md", "file2.txt"]),
    ("path/to/file", "LOAD path/to/file", 5, 18, ["path/to/file1.md", "path/to/file2.txt"]),
    ("nonexistent", "LOAD nonexistent", 5, 16, []),
])
def test_complete_LOAD(monkeypatch, temp_chat_file, text, line, begidx, endidx, matching_files):
    def mock_glob(pattern):
        return matching_files

    monkeypatch.setattr(glob, 'glob', mock_glob)

    chat = Chat(temp_chat_file.name, reset=False)
    completions = chat.complete_LOAD(text, line, begidx, endidx)

    assert completions == matching_files


@pytest.mark.parametrize("input_chat_name, expected_chat_name", [
    ("", "What should be the new chat name? "),
    ("new_chat", "new_chat_chat.md"),
    ("new_chat.md", "new_chat.md"),
])
def test_do_new(monkeypatch, temp_chat_file, input_chat_name, expected_chat_name):
    def mock_input(prompt):
        return "input_chat_name"
    
    monkeypatch.setattr('builtins.input', mock_input)

    chat = Chat(temp_chat_file.name, reset=False)
    
    with patch.object(Chat, '__init__', return_value=None) as mock_init:
        chat.do_NEW(input_chat_name)
        if input_chat_name == "":
            mock_init.assert_called_with(os.path.join(os.path.dirname(temp_chat_file.name), "input_chat_name"))
        else:
            mock_init.assert_called_with(os.path.join(os.path.dirname(temp_chat_file.name), input_chat_name))


def test_do_RERUN(temp_chat_file):
    initial_content = [
        "# ara prompt:\nPrompt message.\n",
        "# ara response:\nResponse message.\n"
    ]
    temp_chat_file.writelines(initial_content)
    temp_chat_file.flush()

    chat = Chat(temp_chat_file.name, reset=False)

    with patch.object(chat, 'resend_message') as mock_resend_message:
        chat.do_RERUN("")
        mock_resend_message.assert_called_once()


def test_do_CLEAR(temp_chat_file, capsys):
    initial_content = "Initial content in the chat file."
    temp_chat_file.write(initial_content)
    temp_chat_file.flush()

    chat = Chat(temp_chat_file.name, reset=False)

    with patch('builtins.input', return_value='y'):
        chat.do_CLEAR(None)

    captured = capsys.readouterr()

    with open(temp_chat_file.name, 'r', encoding='utf-8') as file:
        content = file.read()

    assert content.strip() == "# ara prompt:"
    assert "Cleared content of" in captured.out


def test_do_CLEAR_abort(temp_chat_file, capsys):
    initial_content = "Initial content in the chat file."
    temp_chat_file.write(initial_content)
    temp_chat_file.flush()

    chat = Chat(temp_chat_file.name, reset=False)

    with patch('builtins.input', return_value='n'):
        chat.do_CLEAR(None)

    captured = capsys.readouterr()

    with open(temp_chat_file.name, 'r', encoding='utf-8') as file:
        content = file.read()

    assert content.strip() == initial_content
    assert "Cleared content of" not in captured.out


@pytest.mark.parametrize("rules_name, expected_directory, expected_pattern", [
    ("", "prompt.data", "*.rules.md"),
    ("global/test_rule", "mocked_global_directory/prompt-modules/rules/", "test_rule"),
    ("local_rule", "mocked_local_directory/custom-prompt-modules/rules", "local_rule")
])
def test_do_LOAD_RULES(monkeypatch, temp_chat_file, rules_name, expected_directory, expected_pattern):
    chat = Chat(temp_chat_file.name, reset=False)

    with patch.object(chat, '_load_template_helper') as mock_load_template_helper:
        chat.do_LOAD_RULES(rules_name)
        mock_load_template_helper.assert_called_once_with(rules_name, "rules", "*.rules.md")


@pytest.mark.parametrize("intention_name, expected_directory, expected_pattern", [
    ("", "prompt.data", "*.intention.md"),
    ("global/test_intention", "mocked_global_directory/prompt-modules/intentions/", "test_intention"),
    ("local_intention", "mocked_local_directory/custom-prompt-modules/intentions", "local_intention")
])
def test_do_LOAD_INTENTION(monkeypatch, temp_chat_file, intention_name, expected_directory, expected_pattern):
    chat = Chat(temp_chat_file.name, reset=False)

    with patch.object(chat, '_load_template_helper') as mock_load_template_helper:
        chat.do_LOAD_INTENTION(intention_name)
        mock_load_template_helper.assert_called_once_with(intention_name, "intention", "*.intention.md")


@pytest.mark.parametrize("commands_name, expected_directory, expected_pattern", [
    ("", "prompt.data", "*.commands.md"),
    ("global/test_command", "mocked_global_directory/prompt-modules/commands/", "test_command"),
    ("local_command", "mocked_local_directory/custom-prompt-modules/commands", "local_command")
])
def test_do_LOAD_COMMANDS(monkeypatch, temp_chat_file, commands_name, expected_directory, expected_pattern):
    chat = Chat(temp_chat_file.name, reset=False)

    with patch.object(chat, '_load_template_helper') as mock_load_template_helper:
        chat.do_LOAD_COMMANDS(commands_name)
        mock_load_template_helper.assert_called_once_with(commands_name, "commands", "*.commands.md")


@pytest.mark.parametrize("template_name, template_type, default_pattern, expected_directory, expected_pattern", [
    ("", "commands", "*.commands.md", "prompt.data", "*.commands.md"),
    ("global/test_command", "commands", "*.commands.md", "mocked_template_base_path/prompt-modules/commands/", "test_command"),
    ("local_command", "commands", "*.commands.md", "mocked_local_templates_path/custom-prompt-modules/commands", "local_command"),

    ("", "rules", "*.rules.md", "prompt.data", "*.rules.md"),
    ("global/test_rule", "rules", "*.rules.md", "mocked_template_base_path/prompt-modules/rules/", "test_rule"),
    ("local_rule", "rules", "*.rules.md", "mocked_local_templates_path/custom-prompt-modules/rules", "local_rule"),

    ("", "intention", "*.intentions.md", "prompt.data", "*.intentions.md"),
    ("global/test_intention", "intention", "*.intentions.md", "mocked_template_base_path/prompt-modules/intentions/", "test_intention"),
    ("local_intention", "intention", "*.intentions.md", "mocked_local_templates_path/custom-prompt-modules/intentions", "local_intention")
])
def test_load_template_helper(monkeypatch, temp_chat_file, template_name, template_type, default_pattern, expected_directory, expected_pattern):
    chat = Chat(temp_chat_file.name, reset=False)

    mock_template_base_path = "mocked_template_base_path"
    mock_local_templates_path = "mocked_local_templates_path"

    monkeypatch.setattr(TemplatePathManager, 'get_template_base_path', lambda: mock_template_base_path)
    monkeypatch.setattr(ConfigManager, 'get_config', lambda: MagicMock(local_prompt_templates_dir=mock_local_templates_path))

    with patch.object(chat, '_load_helper') as mock_load_helper:
        chat._load_template_helper(template_name, template_type, default_pattern)

        mock_load_helper.assert_called_once_with(expected_directory, expected_pattern, template_type)


def test_do_EXTRACT(temp_chat_file, capsys):
    chat = Chat(temp_chat_file.name, reset=False)

    with patch('ara_cli.prompt_extractor.extract_responses') as mock_extract_responses:
        chat.do_EXTRACT("")
        mock_extract_responses.assert_called_once_with(temp_chat_file.name, True)

    captured = capsys.readouterr()
    assert "End of extraction" in captured.out


def test_do_SEND(temp_chat_file):
    chat = Chat(temp_chat_file.name, reset=False)
    chat.message_buffer = ["Message part 1", "Message part 2"]

    with patch.object(chat, 'save_message') as mock_save_message:
        with patch.object(chat, 'send_message') as mock_send_message:
            chat.do_SEND(None)
            mock_save_message.assert_called_once_with(Chat.ROLE_PROMPT, "Message part 1\nMessage part 2")
            mock_send_message.assert_called_once()

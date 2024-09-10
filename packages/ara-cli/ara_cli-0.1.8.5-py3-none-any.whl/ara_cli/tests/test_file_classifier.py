import pytest
from unittest.mock import MagicMock, patch, mock_open
from ara_cli.file_classifier import FileClassifier


@pytest.fixture
def mock_file_system():
    return MagicMock()


def test_file_classifier_init(mock_file_system):
    classifier = FileClassifier(mock_file_system)
    assert classifier.file_system == mock_file_system


def test_read_file_content(mock_file_system):
    classifier = FileClassifier(mock_file_system)

    test_file_path = "test_file.txt"
    test_file_content = "This is a test file."

    with patch("builtins.open", mock_open(read_data=test_file_content)) as mock_file:
        content = classifier.read_file_content(test_file_path)
        mock_file.assert_called_once_with(test_file_path, 'r', encoding='utf-8')
        assert content == test_file_content


def test_is_binary_file(mock_file_system):

    classifier = FileClassifier(mock_file_system)

    test_binary_file_path = "test_binary_file.bin"
    test_text_file_path = "test_text_file.txt"
    binary_content = b'\x00\x01\x02\x03\x04\x80\x81\x82\x83'
    text_content = "This is a text file."

    # Test binary file
    with patch("builtins.open", mock_open(read_data=binary_content)) as mock_file:
        result = classifier.is_binary_file(test_binary_file_path)
        mock_file.assert_called_once_with(test_binary_file_path, 'rb')
        assert result is True

    # Test text file
    with patch("builtins.open", mock_open(read_data=text_content.encode('utf-8'))) as mock_file:
        result = classifier.is_binary_file(test_text_file_path)
        mock_file.assert_called_once_with(test_text_file_path, 'rb')
        assert result is False

    # Test exception handling
    with patch("builtins.open", side_effect=Exception("Unexpected error")):
        result = classifier.is_binary_file(test_binary_file_path)
        assert result is False


def test_print_classified_files(mock_file_system):
    classifier = FileClassifier(mock_file_system)
    files_by_classifier = {
        'python': ['test1.py', 'test2.py'],
        'text': ['test1.txt', 'test2.txt'],
        'binary': []
    }

    with patch("builtins.print") as mock_print:
        classifier.print_classified_files(files_by_classifier)
        mock_print.assert_any_call("Python files:")
        mock_print.assert_any_call("  - test1.py")
        mock_print.assert_any_call("  - test2.py")

        mock_print.assert_any_call("Text files:")
        mock_print.assert_any_call("  - test1.txt")
        mock_print.assert_any_call("  - test2.txt")

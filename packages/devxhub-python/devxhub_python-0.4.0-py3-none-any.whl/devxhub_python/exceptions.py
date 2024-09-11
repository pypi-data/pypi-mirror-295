"""All exceptions used in the devxhub_python code base are defined here."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from jinja2 import TemplateError


class devxhub_pythonException(Exception):
    """
    Base exception class.

    All devxhub_python-specific exceptions should subclass this class.
    """


class NonTemplatedInputDirException(devxhub_pythonException):
    """
    Exception for when a project's input dir is not templated.

    The name of the input directory should always contain a string that is
    rendered to something else, so that input_dir != output_dir.
    """


class UnknownTemplateDirException(devxhub_pythonException):
    """
    Exception for ambiguous project template directory.

    Raised when devxhub_python cannot determine which directory is the project
    template, e.g. more than one dir appears to be a template dir.
    """

    # unused locally


class MissingProjectDir(devxhub_pythonException):
    """
    Exception for missing generated project directory.

    Raised during cleanup when remove_repo() can't find a generated project
    directory inside of a repo.
    """

    # unused locally


class ConfigDoesNotExistException(devxhub_pythonException):
    """
    Exception for missing config file.

    Raised when get_config() is passed a path to a config file, but no file
    is found at that path.
    """


class InvalidConfiguration(devxhub_pythonException):
    """
    Exception for invalid configuration file.

    Raised if the global configuration file is not valid YAML or is
    badly constructed.
    """


class UnknownRepoType(devxhub_pythonException):
    """
    Exception for unknown repo types.

    Raised if a repo's type cannot be determined.
    """


class VCSNotInstalled(devxhub_pythonException):
    """
    Exception when version control is unavailable.

    Raised if the version control system (git or hg) is not installed.
    """


class ContextDecodingException(devxhub_pythonException):
    """
    Exception for failed JSON decoding.

    Raised when a project's JSON context file can not be decoded.
    """


class OutputDirExistsException(devxhub_pythonException):
    """
    Exception for existing output directory.

    Raised when the output directory of the project exists already.
    """


class EmptyDirNameException(devxhub_pythonException):
    """
    Exception for a empty directory name.

    Raised when the directory name provided is empty.
    """


class InvalidModeException(devxhub_pythonException):
    """
    Exception for incompatible modes.

    Raised when devxhub_python is called with both `no_input==True` and
    `replay==True` at the same time.
    """


class FailedHookException(devxhub_pythonException):
    """
    Exception for hook failures.

    Raised when a hook script fails.
    """


class UndefinedVariableInTemplate(devxhub_pythonException):
    """
    Exception for out-of-scope variables.

    Raised when a template uses a variable which is not defined in the
    context.
    """

    def __init__(
        self, message: str, error: TemplateError, context: dict[str, Any]
    ) -> None:
        """Exception for out-of-scope variables."""
        self.message = message
        self.error = error
        self.context = context

    def __str__(self) -> str:
        """Text representation of UndefinedVariableInTemplate."""
        return (
            f"{self.message}. "
            f"Error message: {self.error.message}. "
            f"Context: {self.context}"
        )


class UnknownExtension(devxhub_pythonException):
    """
    Exception for un-importable extension.

    Raised when an environment is unable to import a required extension.
    """


class RepositoryNotFound(devxhub_pythonException):
    """
    Exception for missing repo.

    Raised when the specified devxhub_python repository doesn't exist.
    """


class RepositoryCloneFailed(devxhub_pythonException):
    """
    Exception for un-cloneable repo.

    Raised when a devxhub_python template can't be cloned.
    """


class InvalidZipRepository(devxhub_pythonException):
    """
    Exception for bad zip repo.

    Raised when the specified devxhub_python repository isn't a valid
    Zip archive.
    """

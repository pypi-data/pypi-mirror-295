# Copyright 2023 Inductor, Inc.
"""Functionality for general LLM program execution tasks."""

import collections
import contextlib
import contextvars
import io
import sys
import traceback
from typing import Any, Callable, Dict, Iterator, List, NamedTuple, Optional, Set, TextIO, TypeVar, Union

from inductor.backend_client import wire_model
from inductor.data_model import data_model


# The following module-private variables are used to store information
# about the current LLM program execution. Context variables are used to
# enable running multiple LLM program executions in parallel using
# multiple threads. While an LLM program itself may use multiple threads,
# those nested threads can not interact with the LLM program's execution
# (e.g., by calling inductor.log()).
#
# Whether the logger decorator (inductor.logger) is enabled. This is set to
# False when running tests to prevent the logger from sending duplicate data to
# the backend, in the case that the LLM program being tested uses the logger
# decorator.
logger_decorator_enabled = True
# Stores a list of logged values for the current LLM program execution.
logged_values = contextvars.ContextVar("logged_values", default=None)
# Dictionary of hyperparameter values for the current LLM program execution.
hparams = {}
# Dictionary of default hyperparameter values that have been used in the
# current LLM program execution.
_default_hparams: Optional[Dict[str, Set[wire_model.HparamType]]] = None


@contextlib.contextmanager
def set_hparams(
    hparams_to_set: wire_model.HparamsType,
    primary_execution: bool = True):
    """Set execution.hparams to the given hparams within this context manager.
    
    Set the execution.hparams module-level variable to the given
    hyperparameters. On exit, set `execution.hparams` to its original value
    (i.e., the value it had before entering this context manager).

    Args:
        hparams_to_set: A dictionary mapping hyperparameter names to values.
        primary_execution: Whether the current LLM program execution is the
            primary execution. (This flag is relevant to live executions
            which may or may not be a primary execution. See
            `inductor.execution.live_execution._primary_execution` for
            details. A test suite run is always considered a primary
            execution.) If False, the current hyperparameters will not be
            overwritten.
    """
    if primary_execution:
        global hparams
        original_hparams = hparams
        try:
            hparams = hparams_to_set
            yield
        finally:
            hparams = original_hparams
    else:
        yield


@contextlib.contextmanager
def capture_default_hparams() -> Iterator[
    Dict[str, Set[wire_model.HparamType]]]:
    """Capture default hyperparameters used in the current LLM program.

    Initialize the `_default_hparams` module-private variable to an empty
    default dictionary. On exit, set `_default_hparams` to its original value.

    Yields:
        A dictionary mapping hyperparameter names to sets of default hparam
            values that have been used in the current LLM program execution.
    """
    global _default_hparams
    original_default_hparams = _default_hparams
    try:
        _default_hparams = collections.defaultdict(set)
        yield _default_hparams
    finally:
        _default_hparams = original_default_hparams


def hparam(
    name: str,
    default_value: wire_model.HparamType) -> wire_model.HparamType:
    """Return the value of the hyperparameter having the given name.

    Args:
        name: Name of hyperparameter value to be returned.
        default_value: Value that will be returned if a value has not
            been specified for the given name.
    """
    if name in hparams:
        return hparams[name]
    else:
        if _default_hparams is not None:
            _default_hparams[name].add(default_value)
        return default_value


def _log(
    value: Any, *, after_complete: bool, description: Optional[str] = None):
    """Log a value and associate it with the current LLM program execution.

    Args:
        value: The value to be logged.
        after_complete: Whether the value was logged after the LLM
            program execution completed.
        description: An optional human-readable description of the logged
            value.
    """
    logged_values_list = logged_values.get()
    if logged_values_list is None:
        # We can not distinguish between the below two cases described in the
        # printed message, so we print the same message for both cases.
        print(
            f"[WARNING] inductor.log call failed with "
            f"{{\"value\": {value}, \"name\": {description}}}.\n"
            "Cannot call inductor.log outside of a function "
            "decorated with @inductor.logger, unless you are running "
            "a test suite. This log call will be ignored. "
            "Also note that invoking inductor.log from a thread different "
            "from the one that initialized the logger (via the decorator or "
            "the CLI tool) is currently unsupported. If you require support "
            "for this, please contact Inductor support to submit a feature "
            "request.")
    else:
        logged_values_list.append(
            wire_model.LoggedValue(
                value=data_model.deepcopy_or_str(value),
                description=description,
                after_complete=after_complete))


def log(value: Any, *, name: Optional[str] = None):
    """Log a value and associate it with the current LLM program execution.

    Args:
        value: The value to be logged.
        name: An optional human-readable name for the logged value.
    
    Raises:
        RuntimeError: If the LLM program execution was not initiated via the
            Inductor CLI, and the LLM program is not decorated with
            @inductor.logger.
    """
    _log(value, description=name, after_complete=False)


# Type variable for IteratorWrapper objects.
_T_IteratorWrapper = TypeVar(  # pylint: disable=invalid-name
    "_T_IteratorWrapper", bound="IteratorWrapper")


class IteratorWrapper:
    """Iterator wrapper.

    Wraps an iterator and captures values yielded by the iterator. When the
    iterator is exhausted or an error (raised by the underlying iterator)
    occurs during iteration, the wrapper calls a given `stop_signal_handler`
    function. The IteratorWrapper instance is passed to the
    `stop_signal_handler` function as the keyword argument `output`. The stop
    signal handler function can also be passed additional keyword arguments
    via the `stop_signal_handler_kwargs` argument.
    """
    def __init__(
        self,
        iterator: Iterator,
        *,
        stop_signal_handler: Callable,
        stop_signal_handler_kwargs: Optional[Dict[str, Any]] = None,
        iterator_wrapper_error_message: str):
        """Create an IteratorWrapper.
        
        Args:
            iterator: The iterator to wrap.
            stop_signal_handler: Function to call when the iterator is
                exhausted or an error (raised by the underlying iterator)
                occurs during iteration. This function is required to accept
                the keyword argument `output`, which will be this
                `IteratorWrapper` instance (which is of type
                `IteratorWrapper`). If `stop_signal_handler_kwargs` is not
                None, any keyword arguments passed via 
                `stop_signal_handler_kwargs` will also be passed to
                `stop_signal_handler` when it is called.
            stop_signal_handler_kwargs: Keyword arguments to pass to
                `stop_signal_handler` when it is called. If
                `stop_signal_handler_kwargs` includes the key "output",
                an error will be raised as this key is reserved.
            iterator_wrapper_error_message: Error message to print if an error
                occurs within this `IteratorWrapper` instance as part of
                capturing values yielded by the iterator, or if an error
                occurs within the `stop_signal_handler` function. The actual
                error that occurred will be printed after this message.
        
        Raises:
            ValueError: If `stop_signal_handler_kwargs` includes the key
                "output".
        """
        self._iterator = iterator

        self._completed_values = []
        self._skip_stop_signal_handler = False
        self._stop_signal_occurred = False
        self._iteration_error = None

        self._stop_signal_handler = stop_signal_handler
        if stop_signal_handler_kwargs is None:
            stop_signal_handler_kwargs = {}
        self._stop_signal_handler_kwargs = stop_signal_handler_kwargs.copy()
        if "output" in self._stop_signal_handler_kwargs:
            raise ValueError(
                "The key 'output' is reserved and cannot be "
                "passed in `stop_signal_handler_kwargs`.")
        self._stop_signal_handler_kwargs["output"] = self

        self._iterator_wrapper_error_message = iterator_wrapper_error_message

    def __iter__(self) -> _T_IteratorWrapper:
        return self

    def __next__(self) -> Any:
        """Get the next value from the iterator.

        Before returning the next value from the iterator, append a deep copy
        of the value or a string representation of the value to the list of
        completed values. (See `data_model.deepcopy_or_str` for details.)
        If the iterator is exhausted or an error occurs during iteration, call
        the `stop_signal_handler` function. Print the
        `iterator_wrapper_error_message` if an error occurs within this
        `IteratorWrapper` instance as part of capturing values yielded by the
        iterator, or if an error occurs within the `stop_signal_handler`
        function.

        Returns:
            The next value from the iterator.

        Raises:
            StopIteration: If the iterator is exhausted.
        """
        try:
            value = next(self._iterator)
        except StopIteration as stop_signal:
            self._stop_signal_occurred = True
            raise stop_signal
        except Exception as error:  # pylint: disable=broad-except
            self._iteration_error = error
            raise error
        finally:
            if not self._skip_stop_signal_handler:
                try:
                    if (self._stop_signal_occurred or
                        self._iteration_error is not None):
                        if all(
                            isinstance(value, str)
                            for value in self._completed_values
                        ):
                            self._completed_values = "".join(
                                self._completed_values)

                        self._stop_signal_handler(
                            **self._stop_signal_handler_kwargs)

                        self._skip_stop_signal_handler = True
                    else:
                        self._completed_values.append(
                            data_model.deepcopy_or_str(value))  # pylint: disable=used-before-assignment

                except Exception as wrapper_error:  # pylint: disable=broad-except
                    self._skip_stop_signal_handler = True
                    traceback.print_exc()
                    print(self._iterator_wrapper_error_message)
                    print(wrapper_error)

        return value

    def __getattr__(self, name: str) -> Any:
        """Forward unknown attributes to the iterator.
        
        This allows the iterator wrapper to be used as if it were the
        underlying iterator.

        Args:
            name: Name of attribute to get.

        Returns:
            The requested attribute.
        """
        return getattr(self._iterator, name)

    def _get_completed_values(self) -> Union[List[Any], str]:
        """Get the values that were yielded by the iterator.

        If all of the values are strings, the values are joined into a single
        string.

        Returns:
            The values that were yielded by the iterator.
        """
        completed_values = self._completed_values
        if not isinstance(completed_values, str) and all(
            isinstance(value, str)
            for value in completed_values
        ):
            completed_values = "".join(completed_values)
        return completed_values


class _CaptureStdoutStderrYield(NamedTuple):
    """Yield type for the `capture_stdout_stderr` context manager.
    
    See `capture_stdout_stderr` context manager's docstring
    (below) for descriptions of fields.
    """
    stdout: io.StringIO
    stderr: io.StringIO
    suppressed: io.StringIO


@contextlib.contextmanager
def capture_stdout_stderr(
    suppress: bool = False
) -> Iterator[_CaptureStdoutStderrYield]:
    """Capture stdout and stderr.
    
    On exit, restore the original stdout and stderr and close the yielded
    StringIO buffers (i.e., the yielded buffers' contents will be discarded
    when context manager exits).
    
    Args:
        suppress: Whether to suppress stdout and stderr. If True, the
            contents of stdout and stderr will be suppressed after being
            captured. If False, stdout and stderr will behave as normal,
            but their contents will still be captured.

    Yields:
        Named tuple with the following fields:
            stdout: StringIO buffer capturing stdout.
            stderr: StringIO buffer capturing stderr.
            suppressed: StringIO buffer capturing any suppressed output,
                which could be any combination of stdout and stderr output.
    """
    class Tee(io.StringIO):
        """A StringIO buffer that optionally writes to a file in addition to
        capturing the written string."""
        def __init__(self, file: Optional[TextIO]):
            """Override the constructor to store the file to which to write."""
            self.file = file
            super().__init__()

        def write(self, s: str):
            """Override the write method to write to the file (as merited)
            in addition to capturing the written string."""
            if self.file is not None:
                self.file.write(s)
            return super().write(s)

    suppressed_capture = io.StringIO()
    stdout_capture = Tee(sys.stdout if not suppress else suppressed_capture)
    stderr_capture = Tee(sys.stderr if not suppress else suppressed_capture)

    # Save the original stdout and stderr.
    original_stdout = sys.stdout
    original_stderr = sys.stderr
    # Redirect stdout and stderr to the Tee objects.
    sys.stdout = stdout_capture
    sys.stderr = stderr_capture
    try:
        yield _CaptureStdoutStderrYield(
            stdout_capture, stderr_capture, suppressed_capture)
    finally:
        # Restore the original stdout and stderr.
        sys.stdout = original_stdout
        sys.stderr = original_stderr
        # Close the StringIO buffers.
        stdout_capture.close()
        stderr_capture.close()


@contextlib.contextmanager
def capture_logged_values():
    """Capture values logged via log() calls.
    
    If logging has not already been initialized, initialize logging by setting
    the logged values context variable (`_logged_values`) to an empty list,
    and, on exit, set `_logged_values` to `None`.
    If logging has already been initialized, do nothing.
    In either case, yield the list of logged values.

    The purpose of this context manager is to manage the state of the
    logged values context variable, which should only be initialized
    once per LLM program execution.

    Yields:
        The list of logged values.
    """
    init_logged_values = logged_values.get()
    initializing_logged_values = init_logged_values is None
    try:
        if initializing_logged_values:
            logged_values.set([])
        yield logged_values.get()
    finally:
        if initializing_logged_values:
            logged_values.set(None)

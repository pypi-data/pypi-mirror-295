from typing import Callable, Dict, List, Optional, Tuple, Union

from .models import LLMLog, Log
from .parser import XMLParser
from .prompts import create_fix_xml_prompt


class SafeXMLParser:
    """
    A class to handle XML parsing with a correction mechanism using LLM models and logging.

    This class provides multiple attempts to parse an XML string with optional correction
    using a Large Language Model (LLM) if parsing fails. It logs each attempt, including
    details about the input, output, any errors, and the correction prompts.

    Attributes:
    ----------
    _default_llm_model : Optional[Callable]
        The LLM model used to correct the XML if parsing fails on the first attempt.
    _default_nb_attempts : int
        The number of parsing attempts before raising an exception.
    _logs : List[Log]
        A list of logs recording each parsing attempt.

    Methods:
    -------
    safe_parse(text_to_parse: str, nb_attempts: Optional[int] = None,
               llm_model: Optional[Callable] = None,
               correctness_prompt_maker: Callable = create_fix_xml_prompt) -> Dict[str, Union[Dict, str]]:
        Safely parses the XML string, with multiple attempts and optional LLM correction.

    logs(timestamp: bool = True) -> List[Dict[str, str]]:
        Returns the logs of parsing attempts, with or without a timestamp.
    """

    def __init__(
        self,
        default_llm_model: Optional[Callable] = None,
        default_nb_attempts: int = 1,
    ) -> None:
        """
        Initializes the SafeXMLParser with optional LLM correction and the number of attempts.

        Args:
        -----
        default_llm_model : Optional[Callable]
            The LLM model used to correct XML if parsing fails. Default is None.
        default_nb_attempts : int
            The number of parsing attempts allowed before raising an exception. Default is 1.
        """
        self._default_llm_model = default_llm_model
        self._default_nb_attempts = default_nb_attempts
        self._logs: List[Log] = []

    def _log_attempt(
        self,
        input_text: str,
        output: Optional[str] = None,
        error: Optional[str] = None,
        correctness_prompt: Optional[str] = None,
        correctness_output: Optional[str] = None,
    ) -> None:
        """
        Logs each parsing attempt, including input, output, errors, and corrections.

        If the LLM correction is applied, the correctness prompt and output are also logged.

        Args:
        -----
        input_text : str
            The input text that was being parsed.
        output : Optional[str]
            The result of the parsing attempt, if successful. Default is None.
        error : Optional[str]
            The error message if parsing fails. Default is None.
        correctness_prompt : Optional[str]
            The prompt sent to the LLM model for XML correction. Default is None.
        correctness_output : Optional[str]
            The corrected output from the LLM model. Default is None.
        """
        if correctness_prompt and correctness_output:
            self._logs.append(
                LLMLog(
                    input=repr(input_text),
                    output=repr(output) if output else "N/A",
                    error=repr(error) if error else "N/A",
                    correctness_prompt=correctness_prompt,
                    correctness_output=correctness_output,
                )
            )
        else:
            self._logs.append(
                Log(
                    input=repr(input_text),
                    output=repr(output) if output else "N/A",
                    error=repr(error) if error else "N/A",
                )
            )

    @staticmethod
    def _check_safe_parse_input(
        nb_attempts: Optional[int] = None,
        llm_model: Optional[Callable] = None,
    ) -> None:
        """
        Ensures that if multiple attempts are specified, an LLM model is provided for correction.

        Args:
        -----
        nb_attempts : Optional[int]
            The number of parsing attempts.
        llm_model : Optional[Callable]
            The LLM model used to correct XML between attempts.

        Raises:
        ------
        ValueError:
            If `nb_attempts` is greater than 1 but no `llm_model` is provided.
        """
        if nb_attempts and not llm_model:
            raise ValueError(
                "You must provide an 'llm_model' if you specify multiple 'nb_attempts'."
            )

    def safe_parse(
        self,
        text_to_parse: str,
        nb_attempts: Optional[int] = None,
        llm_model: Optional[Callable] = None,
        correctness_prompt_maker: Callable = create_fix_xml_prompt,
    ) -> Dict[str, Union[Dict, str]]:
        """
        Safely parses the XML string with multiple attempts and optional LLM correction.

        This method tries to parse the XML string using `XMLParser`. If parsing fails,
        it applies an LLM model (if provided) to correct the XML and attempts to parse again.
        The process repeats up to `nb_attempts`.

        Args:
        -----
        text_to_parse : str
            The XML string to be parsed.
        nb_attempts : Optional[int]
            Number of parsing attempts before failure. Defaults to the class setting.
        llm_model : Optional[Callable]
            A function to correct the XML between attempts. Defaults to the class setting.
        correctness_prompt_maker : Callable
            A function that generates prompts for LLM correction. Defaults to `create_fix_xml_prompt`.

        Raises:
        ------
        Exception:
            Raised if all parsing attempts fail.

        Returns:
        -------
        dict:
            A dictionary representation of the parsed XML.
        """
        self._check_safe_parse_input(
            nb_attempts=nb_attempts,
            llm_model=llm_model,
        )
        llm_model = llm_model if llm_model else self._default_llm_model
        nb_attempts = nb_attempts if nb_attempts else self._default_nb_attempts

        self._logs = []  # Clear logs for the new parse session

        attempts = 0

        while attempts < nb_attempts:
            try:
                # Try to parse the text
                output = XMLParser.parse(text_to_parse)

                # Log successful parsing
                self._log_attempt(
                    input_text=text_to_parse,
                    output=repr(output),
                )
                return output
            except Exception as exc:
                # Log the error and apply the LLM model if available
                self._log_attempt(text_to_parse, error=str(exc))
                if llm_model:
                    (
                        correctness_prompt,
                        correctness_output,
                    ) = self._process_xml(
                        text_to_parse, llm_model, correctness_prompt_maker
                    )
                    self._log_attempt(
                        input_text=text_to_parse,
                        error=str(exc),
                        correctness_prompt=correctness_prompt,
                        correctness_output=correctness_output,
                    )
                    text_to_parse = correctness_output
                    attempts += 1
                else:
                    attempts = nb_attempts  # Stop further attempts if no LLM model

        # If all attempts fail, raise an exception and log it
        final_error = f"Parsing failed after {nb_attempts} attempts"
        self._log_attempt(text_to_parse, error=final_error)
        raise Exception(final_error)

    def _process_xml(
        self,
        xml_to_process: str,
        llm_model: Callable,
        correctness_prompt_maker: Callable,
    ) -> Tuple[str, str]:
        """
        Generates an LLM correction prompt and processes the XML with the provided LLM model.

        Args:
        -----
        xml_to_process : str
            The XML string that needs correction.
        llm_model : Callable
            The LLM model used to correct the XML.
        correctness_prompt_maker : Callable
            A function to create the correctness prompt.

        Returns:
        -------
        tuple:
            The correctness prompt and the corrected output.
        """
        correctness_prompt = correctness_prompt_maker(xml_to_process)
        corrected_output = llm_model(correctness_prompt)

        return (
            correctness_prompt,
            corrected_output,
        )

    @property
    def logs(self, timestamp: bool = True) -> List[Dict[str, str]]:
        """
        Retrieves logs of all parsing attempts, with or without timestamps.

        Args:
        -----
        timestamp : bool
            Whether to include timestamps in the logs. Default is True.

        Returns:
        -------
        list:
            A list of dictionaries containing the logs of parsing attempts.
        """
        exclude = {"timestamp"} if not timestamp else {}
        return [log.model_dump(exclude=exclude) for log in self._logs]

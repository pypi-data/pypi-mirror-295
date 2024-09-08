import json
import re
from pathlib import Path
from typing import Any

from django.conf import settings

from .translator import Translator


class TransformTemplateContext:
    def __init__(
        self,
        template_dir: str | Path,
        user_or_account: Any,
        kwargs_map: dict[str, dict[str, Any]] = {},
    ):
        """
        Initialize the TransformContext.

        :param json_file_path: Path to the JSON file.
        :param translate: Function to translate text.
        :param user_or_account: User or account object containing language preferences.
        :param kwargs_map: Dictionary containing key-value pairs for formatting.
        """
        self.kwargs_map = kwargs_map
        self.translate = Translator(
            target_language=user_or_account.language
        ).get_translation
        self.user_or_account = user_or_account
        self.template_dir = template_dir.strip("/")
        self.template_root = Path(settings.ROOT_DIR) / "templates"
        self.data = self.read_json(self.template_info_path)

    @property
    def template_file_path(self) -> Path:
        return self.template_root / self.template_dir / "index.html"

    @property
    def template(self) -> str:
        """template name

        Returns:
            str: _description_
        """
        return self.template_dir + "/index.html"

    @property
    def template_info_path(self) -> Path:
        return self.template_root / self.template_dir / "info.json"

    def read_json(self, file_path: str) -> dict[str, Any]:
        """
        Read JSON data from a file.

        :param file_path: Path to the JSON file.
        :return: Parsed JSON data as a dictionary.
        """
        with open(file_path) as file:
            return json.load(file)

    def extract_patterns(self, input_string: str) -> dict[str, str]:
        """
        Extract key-value patterns from the input string.

        :param input_string: String containing the patterns in the format {key: value}.
        :return: Dictionary containing extracted key-value pairs.
        """
        # Define the regex pattern to match {<key>:<value>}
        pattern = r"\{([^{}:]+):([^{}]+)\}"

        # Find all matches in the input string
        matches = re.findall(pattern, input_string)

        # Create a dictionary from the matches
        result = {key.strip(): value.strip() for key, value in matches}
        return result

    @staticmethod
    def replace_placeholders(input_string: str, replacements: dict[str, str]) -> str:
        """
        Replace placeholders in the input string with values from the replacements dictionary.

        :param input_string: String containing placeholders in the format {variable_key: value}.
        :param replacements: Dictionary containing replacement values for each variable_key.
        :return: String with placeholders replaced by corresponding values.
        """
        # Define the pattern to match the placeholders {variable_key: value} and ignore those without a colon
        pattern = r"\{([^{}:]+):([^{}]+)\}"

        # Function to replace each match with the corresponding value from the replacements dictionary
        def replacer(match):
            variable_key = match.group(1).strip()  # Extract and strip the variable_key
            # Get the replacement value from the dictionary or use the original value if key not found
            return replacements.get(variable_key, match.group(0))

        # Use re.sub with the replacer function to replace all valid placeholders
        return re.sub(pattern, replacer, input_string)

    def process_string(self, value: str, key: str) -> str:
        """
        Process a string by translating and formatting it.

        :param value: String to be processed.
        :param key: Key associated with the string in the JSON data.
        :return: Translated and formatted string.
        """
        # Translate the value
        translated_value = self.translate(
            value, target_language=self.user_or_account.language
        )
        # Format the string using the corresponding kwargs_map
        formatted_value = translated_value.format_map(self.kwargs_map.get(key, {}))
        return formatted_value

    def process_dict(self, value: dict[str, Any], key: str) -> str:
        """
        Process a dictionary containing plainText and meta keys.

        :param value: Dictionary to be processed.
        :param key: Key associated with the dictionary in the JSON data.
        :return: Processed string with translated and formatted content.
        """
        plain_text = value["plainText"]
        # Translate the value
        translated_value: str = self.translate(
            plain_text, target_language=self.user_or_account.language
        )
        meta = value.get("meta", {})
        final_text: str = self.process_meta(translated_value, meta, key)

        try:
            # Format the string using the corresponding kwargs_map
            formatted_value = final_text.format_map(self.kwargs_map.get(key, {}))
        except KeyError as err:
            raise KeyError(
                f"no data for {str(err)} in kwargs_map['{key}']: meta: {meta}, final_text: {final_text}"
            ) from err
        return formatted_value

    @staticmethod
    def custom_format_map(template: str, replacements: dict[str, str]) -> str:
        """
        Custom format function that replaces placeholders in the format
        [key] with values from the replacements dictionary.

        :param template: The template string containing placeholders in the format [key].
        :param replacements: A dictionary containing replacement values for each key.
        :return: The formatted string with placeholders replaced by corresponding values.
        """
        # Define the pattern to match placeholders in the format [key]
        pattern = r"\[([^\[\]]+)\]"

        # Function to replace each match with the corresponding value from the replacements dictionary
        def replacer(match):
            key = match.group(1)  # Extract the key from the match
            return replacements.get(
                key, match.group(0)
            )  # Return the replacement value or the original placeholder

        # Use re.sub with the replacer function to replace all placeholders
        return re.sub(pattern, replacer, template)

    def process_meta(
        self, plain_text: str, meta: dict[str, dict[str, dict[str, str]]], key: str
    ) -> str:
        """
        Process meta information to replace placeholders with HTML tags.

        :param plain_text: Translated plain text string.
        :param meta: Meta information containing HTML tag and attributes.
        :param key: Key associated with the meta data.
        :return: String with placeholders replaced by HTML tags.
        """
        mapping = {
            _key: self.custom_format_map(
                value, replacements=self.kwargs_map.get(key, {})
            )
            for _key, value in self.extract_patterns(plain_text).items()
        }
        html_mapping = dict()
        for tag_variable, attributes in meta.items():
            tag, variable = tag_variable.split(":")
            # Format each attribute in the meta dictionary
            for attr, val in attributes["attr"].items():
                try:
                    attributes["attr"][attr] = val.format_map(
                        self.kwargs_map.get(key, {})
                    )
                except KeyError as e:
                    raise KeyError(f"No {str(e)} in kwargs_map['{key}']") from e
            variable = variable.strip()
            attributes_str = " ".join(
                [f'{k}="{v}"' for k, v in attributes["attr"].items()]
            )
            if variable in mapping:
                html_mapping[variable] = (
                    f"<{tag} {attributes_str}>" + "{" + variable + "}" + f"</{tag}>"
                ).format_map({variable: mapping[variable]})
        return self.replace_placeholders(
            input_string=plain_text, replacements=html_mapping
        )

    def get_context(self, **kwargs) -> dict[str, Any]:
        """
        Transform the JSON data by processing strings and dictionaries.

        :return: Dictionary containing transformed JSON data.
        """
        # Process the json_data
        result = {}
        for key, value in self.data.items():
            if isinstance(value, str):
                # Process the string value
                result[key] = self.process_string(value, key)
            elif isinstance(value, dict):
                # Handle plainText and meta structure
                result[key] = self.process_dict(value, key)
            else:
                raise ValueError(f"Value must either be a string or a dict: {value}")
        return {**result, **kwargs}

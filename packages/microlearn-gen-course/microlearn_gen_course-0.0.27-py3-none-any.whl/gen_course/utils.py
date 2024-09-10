import json
import logging
import re
import json_repair


def extract_json_from_text(text):
    """
    Extracts JSON content from a given text.

    Args:
    text (str): Text from which JSON content needs to be extracted.

    Returns:
    dict: Json content extracted from the text.
    """
    logger = logging.getLogger(__name__)
    json_pattern = re.compile(r'((\[[^\}]{3,})?\{s*[^\}\{]{3,}?:.*\}([^\{]+\])?)', re.DOTALL)
    match = json_pattern.search(text)

    if match:
        json_str = match.group(0)
        try:
            json_data = json_repair.loads(json_str)
            return json_data
        except json.JSONDecodeError:
            try:
                logger.warning("JSON is not valid. Trying to repair it.")
                json_reparied = json_repair.loads(json_str)
                logger.info(f"JSON repaired successfully:\n\n=====================\nOriginal JSON:\n{json_str}\n\nRepaired JSON:\n{json_reparied}\n=====================")
                return json_reparied
            except json.JSONDecodeError as e:
                raise e
    else:
        raise


def remove_html(html_string):
    """
    Function that removes HTML tags from a string.

    Args:
        html_string: str

    Returns:
        str: String without HTML tags
    """
    clean = re.compile('<.*?>')
    return re.sub(clean, '', html_string)


def remove_markdown(text):
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    text = re.sub(r'__(.*?)__', r'\1', text)

    text = re.sub(r'\*(.*?)\*', r'\1', text)
    text = re.sub(r'_(.*?)_', r'\1', text)

    text = re.sub(r'`(.*?)`', r'\1', text)
    text = re.sub(r'```[\s\S]+?```', '', text)

    text = re.sub(r'^\s*#(#+)\s+', '', text, flags=re.MULTILINE)
    return text
import re
from bs4 import BeautifulSoup
import nltk

# Download necessary NLTK data
nltk.download("punkt")
nltk.download("averaged_perceptron_tagger")


def clean_text(text):
    """
    Cleans the input text by removing unwanted symbols like `**`, `-`, and `##`,
    but preserves URLs and specific punctuations.
    """
    # Remove unwanted patterns like `-`, `**`, and `##`, but preserve URLs and specific punctuation
    text = re.sub(r"(\*\*|##|-)", "", text)  # Remove `**`, `##`, `-`

    # Preserve links (URLs) while removing other unwanted characters
    def preserve_links(match):
        return match.group(0)

    # Keep URLs intact and remove unwanted characters
    cleaned_text = re.sub(
        r"((http|https)://\S+)|[^!?()\[\]{}.\-\w\s$:]",  # Allow URLs, specific punctuations
        lambda match: preserve_links(match) if match.group(1) else "",
        text,
    )
    return cleaned_text


def format_text(dynamic_text):
    """
    Formats the dynamic input text into structured HTML by processing
    headings, lists, links, and paragraphs.
    """
    # Clean the input text first
    dynamic_text = clean_text(dynamic_text)

    # Create a BeautifulSoup object to construct HTML
    soup = BeautifulSoup("", "html.parser")

    # Split the input text into lines
    lines = dynamic_text.strip().split("\n")

    # Initialize variables
    current_heading = None
    ul_tag = None

    for line in lines:
        line = line.strip()

        if not line:
            continue

        # Handle headings (Markdown style: #, ##, ###)
        if re.match(r"^### (.+)$", line):  # H3 Heading
            current_heading = soup.new_tag("h3")
            current_heading.string = re.match(r"^### (.+)$", line).group(1)
            soup.append(current_heading)
            ul_tag = None
            continue
        elif re.match(r"^## (.+)$", line):  # H2 Heading
            current_heading = soup.new_tag("h2")
            current_heading.string = re.match(r"^## (.+)$", line).group(1)
            soup.append(current_heading)
            ul_tag = None
            continue
        elif re.match(r"^# (.+)$", line):  # H1 Heading
            current_heading = soup.new_tag("h1")
            current_heading.string = re.match(r"^# (.+)$", line).group(1)
            soup.append(current_heading)
            ul_tag = None
            continue

        # Handle lists (Markdown style: - item)
        if re.match(r"^\s*- (.+)$", line):  # List item
            if not ul_tag:
                ul_tag = soup.new_tag("ul")
                soup.append(ul_tag)
            li_tag = soup.new_tag("li")
            li_tag.string = re.match(r"^\s*- (.+)$", line).group(1)
            ul_tag.append(li_tag)
            continue
        elif ul_tag:
            # Close the list after items are added
            ul_tag = None

        # Convert links in the format [text](url) to <a> tags within paragraphs
        line = re.sub(
            r"\[(.+?)\]\((http[s]?://\S+)\)",
            r'<a href="\2" target="_blank">\1</a>',
            line,
        )

        # Add regular paragraphs if no special format is detected
        p_tag = soup.new_tag("p")
        p_tag.append(
            BeautifulSoup(line, "html.parser")
        )  # Support inline HTML tags like <a>
        soup.append(p_tag)

    return str(soup)

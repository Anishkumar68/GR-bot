import re
import nltk
from bs4 import BeautifulSoup

# Download necessary NLTK data
nltk.download("punkt")
nltk.download("averaged_perceptron_tagger")


def clean_text(text):
    # Preserve links while cleaning the rest of the text
    def preserve_links(match):
        return match.group(0)

    # Remove unwanted patterns like "-**" except in URLs, $ sign, and colon
    cleaned_text = re.sub(
        r"((http|https)://\S+)|[^!?()\[\]{}.\-\w\s$:]",  # Allow $ sign and colon
        lambda match: preserve_links(match) if match.group(1) else "",
        text,
    )
    return cleaned_text


def format_text(dynamic_text):
    # Clean the text
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

        # Convert headings
        if re.match(r"^### (.+)$", line):
            if current_heading:
                soup.append(current_heading)
            current_heading = soup.new_tag("h3")
            current_heading.string = re.match(r"^### (.+)$", line).group(1)
            soup.append(current_heading)
            ul_tag = None
            continue
        elif re.match(r"^## (.+)$", line):
            if current_heading:
                soup.append(current_heading)
            current_heading = soup.new_tag("h2")
            current_heading.string = re.match(r"^## (.+)$", line).group(1)
            soup.append(current_heading)
            ul_tag = None
            continue
        elif re.match(r"^# (.+)$", line):
            if current_heading:
                soup.append(current_heading)
            current_heading = soup.new_tag("h1")
            current_heading.string = re.match(r"^# (.+)$", line).group(1)
            soup.append(current_heading)
            ul_tag = None
            continue

        # Convert lists
        if re.match(r"^\s*- (.+)$", line):
            if not ul_tag:
                ul_tag = soup.new_tag("ul")
            li_tag = soup.new_tag("li")
            li_tag.string = re.match(r"^\s*- (.+)$", line).group(1)
            ul_tag.append(li_tag)
            continue
        elif ul_tag:
            soup.append(ul_tag)
            ul_tag = None

        # Convert links to anchor tags
        if re.search(r"\[(.+?)\]\((http[s]?://\S+)\)", line):
            link_text = re.search(r"\[(.+?)\]\((http[s]?://\S+)\)", line).group(1)
            link_url = re.search(r"\[(.+?)\]\((http[s]?://\S+)\)", line).group(2)
            a_tag = soup.new_tag("a", href=link_url, target="_blank")
            a_tag.string = link_text
            soup.append(a_tag)
            continue

        # Preserve line breaks
        if re.search(r"<br>", line):
            line = re.sub(r"<br>", "\n", line)

        # General information (preserve text as is)
        p_tag = soup.new_tag("p")
        p_tag.string = line
        soup.append(p_tag)

    # Append the last heading if exists
    if current_heading:
        soup.append(current_heading)

    return str(soup)

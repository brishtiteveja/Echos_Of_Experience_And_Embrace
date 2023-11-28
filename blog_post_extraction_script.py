
import xml.etree.ElementTree as ET
import re
from html.parser import HTMLParser

# HTML Parser class to strip HTML tags
class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.text = []

    def handle_data(self, d):
        self.text.append(d)

    def get_data(self):
        return ''.join(self.text)

# Function to strip HTML tags
def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

# Function to check if the text has at least a certain number of sentences
def has_minimum_sentences(text, min_sentences=2):
    sentences = re.split(r'[.!?]+\s+|\.$', text)
    return len(sentences) >= min_sentences

# Function to clean text by removing excessive whitespace and non-textual content
def clean_text(text):
    lines = text.split('\n')
    cleaned_lines = [line.strip() for line in lines if line.strip() and not line.strip().startswith('<')]
    return ' '.join(cleaned_lines)

# Load the XML file
file_path = './data/experienceampembrace.wordpress.2023-11-28.000.xml' # Replace with the path to your XML file
tree = ET.parse(file_path)
root = tree.getroot()
channel = root.find('channel')
posts = channel.findall('item')

# Namespace for 'content:encoded'
namespace = {'content': 'http://purl.org/rss/1.0/modules/content/'}
namespace_wp = {'wp': 'http://wordpress.org/export/1.2/'}

# Extracting and cleaning data
extracted_data_final = []
def parse():
    for post in posts:
        post_id = post.find('wp:post_id', namespace_wp).text if post.find('wp:post_id', namespace_wp) is not None else 'No ID'
        title = post.find('title').text if post.find('title') is not None else 'No Title'
        pub_date = post.find('pubDate').text if post.find('pubDate') is not None else 'No Date'
        content_encoded = post.find('content:encoded', namespace)
        content = content_encoded.text if content_encoded is not None else None
        if content is not None and has_minimum_sentences(content):
            categories = [category.text for category in post.findall('category') if 'domain' in category.attrib and category.attrib['domain'] == 'category']
            tags = [tag.text for tag in post.findall('category') if 'domain' in tag.attrib and tag.attrib['domain'] == 'post_tag']
            categories_tags = ', '.join(categories + tags)
            cleaned_content = clean_text(strip_tags(content))
            if cleaned_content:  # Only include if the cleaned content is not empty
                extracted_data_final.append((post_id, title, pub_date, categories_tags, cleaned_content))

def save():
    # Save the cleaned and final data to a text file
    output_file_path_final = 'extracted_blog_posts_final.txt'
    with open(output_file_path_final, 'w') as file:
        for post_id, title, pub_date, categories_tags, content in extracted_data_final:
            file.write(f"Post ID: {post_id}\nTitle: {title}\nPublished Date: {pub_date}\nCategories & Tags: {categories_tags}\nContent:\n{content}\n\n---\n\n")
            
def main():
    parse()
    save()

if __name__ == '__main__':
    main()
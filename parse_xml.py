# Re-importing the necessary library and re-running the extraction process due to code execution state reset
import xml.etree.ElementTree as ET

# Re-loading the file and parsing it
file_path_reuploaded = './data/experienceampembrace.wordpress.2023-11-28.000.xml'
tree = ET.parse(file_path_reuploaded)
root = tree.getroot()
channel = root.find('channel')
posts = channel.findall('item')

# Namespace for 'content:encoded'
namespace = {'content': 'http://purl.org/rss/1.0/modules/content/'}
extracted_data_new = []

def parse():
    nc = 0
    nci = []
    for pi, post in enumerate(posts):  # Analyzing the first 100 posts
        title = post.find('title').text if post.find('title') is not None else 'No Title'
        pub_date = post.find('pubDate').text if post.find('pubDate') is not None else 'No Date'
        content_encoded = post.find('content:encoded', namespace)
        content = content_encoded.text if content_encoded is not None else 'No Content'
        if content != 'No Content':
            extracted_data_new.append((title, pub_date, content))
            if content is not None:
                print(f"Post ID #{pi}")
                print("-------------------------------------------------")
                print(title)
                print(pub_date)
                print(content)
                print("\n\n")
                nc += 1
                nci.append(pi)

    print(f"Total number of non-empty posts: {nc}")
    print(nci)

def main():
    parse()
    # Checking the first few extracted posts with the new method
    extracted_data_new[:100]

if __name__ == '__main__':
    main()
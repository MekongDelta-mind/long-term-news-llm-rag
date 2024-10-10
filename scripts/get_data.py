import feedparser
import json
import os
import xml.etree.ElementTree as ET


# If the RSS feed format would be same , then the input to the method would be an element of the python dict `feed`. 
# So input to this method would be an element which is of the type `dict`.
def extract_turbo_content(entry_element):
    """
    Extracts turbo:content from the raw XML
    """
    try:
        if entry_element:  
            content = entry_element.get('turbo_content')  
        return content if content else None

    except (AttributeError, KeyError, TypeError) as e:
        # AttributeError: If entry_element doesn't support dictionary operations
        # KeyError: If 'turbo_content' doesn't exist
        # TypeError: If entry_element is not of the expected type
        print(f"Error extracting turbo content: {str(e)}")


def parse_rss_to_json(feed_url, output_file_path):
    # Parse the RSS feed
    feed = feedparser.parse(feed_url)

    # Structure the feed data into JSON format
    rss_feed = {
        "meta": {
            "title": feed.feed.title,
            "link": feed.feed.link,
            "description": feed.feed.description,
            "language": feed.feed.language
        },
        "items": []
    }

    # Loop through each item in the feed and add it to the JSON
    for entry in feed.entries:
        # Extract turbo content if available
        turbo_content = extract_turbo_content(entry)
 
        item = {
            "title": entry.title,
            "link": entry.link,
            "pubDate": entry.published,
            "author": entry.author if "author" in entry else None,
            "category": entry.get("category", None),
            "description": entry.description,
            "content": turbo_content,  # Here we add the content field from turbo:content
            "enclosure": {
                "url": entry.enclosures[0].href,
                "type": entry.enclosures[0].type
            } if entry.enclosures else None
        }
        rss_feed["items"].append(item)

    # Convert the structured feed data to JSON string
    rss_feed_json = json.dumps(rss_feed, indent=4)

    # Create the directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

    # Save the JSON string to a file
    with open(output_file_path, 'w') as json_file:
        json_file.write(rss_feed_json)

    print(f"RSS feed data saved to {output_file_path}")

if __name__ == "__main__":
    # RSS feed URL and output file path
    feed_url = 'https://pythoninvest.com/rss-feed-612566707351.xml'  # Fin news RSS
    output_file_path = '../data/input_news_feed.json' # folder relative to the current notebook
    
    # Parse and save the RSS feed to a JSON file
    parse_rss_to_json(feed_url, output_file_path)

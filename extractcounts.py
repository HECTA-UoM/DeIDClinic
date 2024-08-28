import os
from collections import defaultdict
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

# Define the directory containing the XML files
xml_directory = 'dataset/training-PHI-Gold-Set1'

# Function to extract entities from a single XML file using BeautifulSoup
def extract_entities_from_xml(xml_file):
    try:
        with open(xml_file, 'r', encoding='utf-8') as file:
            content = file.read()

        # Parse the XML content using BeautifulSoup
        soup = BeautifulSoup(content, 'lxml-xml')
        entity_counts = defaultdict(int)  # Dictionary to store the counts of each entity type
        unique_entities = defaultdict(set)  # Dictionary to store unique entities for each type

        # Define the tags corresponding to different entity types
        entity_tags = ['ID', 'PHI', 'CONTACT','NAME', 'PROFESSION', 'LOCATION', 'AGE', 'DATE']  # Add other tags if necessary

        # Loop through each tag and extract the entities
        for tag in entity_tags:
            tags = soup.find_all(tag)
            entity_counts[tag] += len(tags)  # Count the occurrences of each entity type
            for entity_tag in tags:
                text = entity_tag.get('text')
                if text:
                    unique_entities[tag].add(text)  # Add the entity to the set of unique entities
                    # Check for special case where entity text is "ON"
                    if text == "ON":
                        print(f"Special case 'ON' found in {xml_file} within {tag} tag.")

        return entity_counts, unique_entities  # Return the counts and unique entities
    except Exception as e:
        # Handle exceptions and print error messages
        print(f"Error parsing XML file {xml_file}: {e}")
        return defaultdict(int), defaultdict(set)

# Initialize dictionaries to store total counts and unique entities across all files
total_entity_counts = defaultdict(int)
total_unique_entities = defaultdict(set)

# Process each XML file in the directory
for filename in os.listdir(xml_directory):
    if filename.endswith('.xml'):
        file_path = os.path.join(xml_directory, filename)
        print(f"Processing file: {file_path}")
        entity_counts, unique_entities = extract_entities_from_xml(file_path)

        # Update total counts and unique entities with data from the current file
        for tag, count in entity_counts.items():
            total_entity_counts[tag] += count
        for tag, entities in unique_entities.items():
            total_unique_entities[tag].update(entities)

# Print the total counts of each entity type
print("Total counts of each entity type:")
for tag, count in total_entity_counts.items():
    print(f"{tag}: {count}")

# Print unique values and their counts for each entity type
print("\nUnique values and their counts for each entity type:")
for tag, entities in total_unique_entities.items():
    print(f"{tag} ({len(entities)} unique values):")
    # Uncomment the below lines to print each unique entity
    # for entity in entities:
    #     print(f"  - {entity}")

# Optionally, write unique values to a text file
with open('unique_entities.txt', 'w', encoding='utf-8') as f:
    for tag, entities in total_unique_entities.items():
        f.write(f"{tag} ({len(entities)} unique values):\n")
        for entity in entities:
            f.write(f"  - {entity}\n")
        f.write("\n")

# Prepare data for plotting
entities = list(total_entity_counts.keys())
value_counts = [total_entity_counts[entity] for entity in entities]
unique_counts = [len(total_unique_entities[entity]) for entity in entities]

# Plotting the bar graph to compare value counts and unique counts for each entity type
x = range(len(entities))
width = 0.4

fig, ax = plt.subplots()
bar1 = ax.bar(x, value_counts, width, label='Value Count')
bar2 = ax.bar([p + width for p in x], unique_counts, width, label='Unique Count')

# Adding labels and title to the plot
ax.set_xlabel('Entity')
ax.set_ylabel('Count')
ax.set_title('Value Counts vs Unique Counts for Each Entity')
ax.set_xticks([p + width / 2 for p in x])
ax.set_xticklabels(entities, rotation=45, ha='right')
ax.legend()

# Adding value labels on top of the bars
for bar in bar1:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2.0, yval, int(yval), va='bottom')  # va: vertical alignment

for bar in bar2:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2.0, yval, int(yval), va='bottom')  # va: vertical alignment

# Ensure the plot layout is tight and display the plot
plt.tight_layout()
plt.show()

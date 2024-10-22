import xmltodict
import pandas as pd
import os

# Path for input XML and output XML
INPUT_XML_FILE = 'D:/Python/firewall_rules.xml'
OUTPUT_XML_FILE = 'D:/Python/updated_firewall_rules.xml'
CSV_FILE = 'D:/Python/updates.csv'

def load_xml(xml_file):
    try:
        with open(xml_file) as f:
            xml_data = xmltodict.parse(f.read())
        print(f"Successfully loaded XML: {xml_file}")
        return xml_data
    except Exception as e:
        print(f"Error loading XML file: {xml_file}\n{e}")
        return None
    
def save_xml(data, xml_file):
    try:
        abs_path = os.path.abspath(xml_file)
        print(f"Saving updated XML at: {abs_path}")
        with open(xml_file, 'w') as f:
            f.write(xmltodict.unparse(data, pretty=True))
        print(f"XML successfully saved at: {abs_path}")
    except Exception as e:
        print(f"Error saving XML file: {xml_file}\n{e}")

def load_csv(csv_file):
    try:
        updates = pd.read_csv(csv_file, encoding='utf-8-sig', header=0)
        print(f"Successfully loaded CSV: {csv_file}")
        return updates
    except Exception as e:
        print(f"Error loading CSV file: {csv_file}\n{e}")
        return None

def update_rules(rules, updates):
    if not rules or updates is None:
        print("No rules or updates to process.")
        return
    for update in updates.itertuples(index=False):
        id_or_name = update.id_or_name
        new_source = update.new_source
        new_destination = update.new_destination

        for rule in rules:
            if rule.get('id') == id_or_name or rule.get('name') == id_or_name:
                # Update the source and destination
                if 'source' in rule and 'ipAddress' in rule['source']:
                    print(f"Updating source for rule {id_or_name}")
                    rule['source']['ipAddress'] = new_source
                if 'destination' in rule and 'ipAddress' in rule['destination']:
                    print(f"Updating destination for rule {id_or_name}")
                    rule['destination']['ipAddress'] = new_destination

def main():
    # Load the XML data
    xml_data = load_xml(INPUT_XML_FILE)
    
    if xml_data is None or 'firewall' not in xml_data or 'firewallRules' not in xml_data['firewall']:
        print("Error: Invalid XML structure or 'firewallRules' not found in XML.")
        return

    rules = xml_data['firewall']['firewallRules'].get('firewallRule', [])
    print(f"Loaded {len(rules)} firewall rules.")

    # Load the updates from the CSV file
    updates = load_csv(CSV_FILE)

    # Update the rules based on the CSV
    update_rules(rules, updates)

    # Save the updated XML data
    save_xml(xml_data, OUTPUT_XML_FILE)
    

if __name__ == '__main__':
    main()

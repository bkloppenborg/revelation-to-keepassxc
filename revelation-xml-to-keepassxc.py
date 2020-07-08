# revelation-xml-to-keepassxc.py - A python script to convert Revelation
# XML export data to KeePassXC-compatable CSV format while preserving data
# and structure.
#
# Copyright (C) 2020 Brian Kloppenborg
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import argparse
from argparse import RawTextHelpFormatter
import xml.etree.ElementTree as ET
import csv

# Reads a Revelation XML file and creates a KeePassXC compatable
# CSV file for import

def make_output(folders, title, username, password, url, notes, last_modified, created):
    """Generates and populates a dictionary containing KeePassXC fields:
    * group
    * title
    * username
    * password
    * URL
    * notes
    * last modified
    * created
    """

    group = '/'.join(folders)
    tmp = {'group': group,
           'title': title,
           'username': username,
           'password': password,
           'url': url,
           'notes': notes,
           'last_modified': last_modified,
           'created': created}
    return tmp

def parse_common(entry):
    """Parses the name, description, notes, and updated fields from
    a Revelation XML Entry"""

    f_name          = entry.find('name').text
    f_description   = entry.find('description').text
    f_notes         = entry.find('notes').text
    f_last_modified = entry.find('updated').text

    name = f_name
    notes = ""
    last_modified = f_last_modified
    if f_description is not None:
        notes += "Description: " + f_description + "\n"

    if f_notes is not None:
        notes = "Notes: " + f_notes + "\n"

    return name, notes, last_modified

def map_fields(entry, field_ids):
    """Extracts the text values in the fields with the specified
    field_ids. Returns the text values as a list in the same order
    as field_ids."""

    output = []

    fields = entry.findall('field')
    for field in fields:
        f_id = field.get('id')

        if f_id in field_ids:
            text = field.text
            if text != None:
                output.append(text)
            else:
                output.append("")
        else:
            output.append("")

    return output

def parse_generic(entry, folders):
    """Parses a Revelation entry of 'generic' type (i.e. <entry
    type="generic">). Returns a dictionary with KeePassXC compatable fields"""

    name, notes, last_modified = parse_common(entry)
    field_ids = ['generic-hostname', 'generic-username', 'generic-password']
    hostname, username, password = map_fields(entry, field_ids)

    return make_output(folders, name, username, password, hostname, notes, last_modified, "")

def parse_creditcard(entry, folders):
    """Parses a Revelation entry of 'creditcard' type (i.e. <entry
    type="creditcard">). Returns a dictionary with KeePassXC compatable fields"""

    name, notes, last_modified = parse_common(entry)
    field_ids = ['creditcard-cardtype', 'creditcard-cardnumber', 'creditcard-expirydate',
                 'creditcard-ccv', 'generic-pin']
    c_type, c_num, c_exp, c_ccv, pin = map_fields(entry, field_ids)

    notes += "Type:   " + c_type + "\n"
    notes += "Number: " + c_num  + "\n"
    notes += "Type:   " + c_exp  + "\n"
    notes += "Type:   " + c_ccv  + "\n"

    username = ""
    hostname = ""
    return make_output(folders, name, username, pin, hostname, notes, last_modified, "")

def parse_cryptokey(entry, folders):
    """Parses a Revelation entry of 'cryptokey' type (i.e. <entry
    type="cryptokey">). Returns a dictionary with KeePassXC compatable fields"""

    name, notes, last_modified = parse_common(entry)

    field_ids = ['generic-hostname', 'generic-certificate',
                 'generic-keyfile', 'generic-password']
    hostname, cert, key, password = map_fields(entry, field_ids)

    notes += "Cert: " + cert + "\n"
    notes += "Key:  " + key  + "\n"

    username = ""

    return make_output(folders, name, username, password, hostname, notes, last_modified, "")

def parse_database(entry, folders):
    """Parses a Revelation entry of 'database' type (i.e. <entry
    type="database">). Returns a dictionary with KeePassXC compatable fields"""

    name, notes, last_modified = parse_common(entry)

    field_ids = ['generic-hostname', 'generic-username',
                 'generic-password', 'generic-database']
    hostname, username, password, database = map_fields(entry, field_ids)

    notes += "Database: " + database + "\n"

    return make_output(folders, name, username, password, hostname, notes, last_modified, "")

def parse_door(entry, folders):
    """Parses a Revelation entry of 'door' type (i.e. <entry
    type="door">). Returns a dictionary with KeePassXC compatable fields"""

    name, notes, last_modified = parse_common(entry)

    field_ids = ['generic-location', 'generic-code']
    location, code = map_fields(entry, field_ids)

    return make_output(folders, name, location, code, "", notes, last_modified, "")

def parse_email(entry, folders):
    """Parses a Revelation entry of 'email' type (i.e. <entry
    type="email">). Returns a dictionary with KeePassXC compatable fields"""

    name, notes, last_modified = parse_common(entry)
    field_ids = ['generic-email', 'generic-hostname',
                 'generic-username', 'generic-password']
    email, hostname, username, password = map_fields(entry, field_ids)

    return make_output(folders, name, username, password, hostname, notes, last_modified, "")

def parse_ftp(entry, folders):
    """Parses a Revelation entry of 'ftp' type (i.e. <entry
    type="ftp">). Returns a dictionary with KeePassXC compatable fields"""

    name, notes, last_modified = parse_common(entry)
    field_ids = ['generic-hostname', 'generic-port',
                 'generic-username', 'generic-password']
    host, port, username, password = map_fields(entry, field_ids)

    hostname = host + ":" + port
    return make_output(folders, name, username, password, hostname, notes, last_modified, "")

def parse_phone(entry, folders):
    """Parses a Revelation entry of 'phone' type (i.e. <entry
    type="phone">). Returns a dictionary with KeePassXC compatable fields"""

    name, notes, last_modified = parse_common(entry)
    field_ids = ['phone-phonenumber', 'generic-pin']
    number, pin = map_fields(entry, field_ids)

    return make_output(folders,  name, number, pin, "", notes, last_modified, "")

def parse_shell(entry, folders):
    """Parses a Revelation entry of 'shell' type (i.e. <entry
    type="shell">). Returns a dictionary with KeePassXC compatable fields"""

    name, notes, last_modified = parse_common(entry)
    field_ids = ['generic-hostname', 'generic-domain',
                 'generic-username', 'generic-password']
    hostname, domain, username, password = map_fields(entry, field_ids)

    hostname += '.' + domain

    return make_output(folders, name, username, password, hostname, notes, last_modified, "")

def parse_remote_desktop(entry, folders):
    """Parses a Revelation entry of 'remotedesktop' type (i.e. <entry
    type="remotedesktop">). Returns a dictionary with KeePassXC compatable fields"""

    name, notes, last_modified = parse_common(entry)
    field_ids = ['generic-hostname', 'generic-port',
                 'generic-username', 'generic-password']
    hostname, port, username, password = map_fields(entry, field_ids)

    hostname += ':' + port

    return make_output(folders, name, username, password, hostname, notes, last_modified, "")

def parse_vnc(entry, folders):
    """Parses a Revelation entry of 'vnc' type (i.e. <entry
    type="vnc">). Returns a dictionary with KeePassXC compatable fields"""

    name, notes, last_modified = parse_common(entry)
    field_ids = ['generic-hostname', 'generic-port',
                 'generic-username', 'generic-password']
    hostname, port, username, password = map_fields(entry, field_ids)

    hostname += ':' + port

    return make_output(folders, name, username, password, hostname, notes, last_modified, "")
    
def parse_website(entry, folders):
    """Parses a Revelation entry of the 'website' type (i.e. 
    <entry type="website">. Returns a dictionary with KeePassXC compatable fields."""

    name, notes, last_modified = parse_common(entry)
    field_ids = ['generic-url', 'generic-username', 
                 'generic-email', 'generic-password']
    url, username, email, password = map_fields(entry, field_ids) 
    
    notes += "\n" + email
    
    return make_output(folders, name, username, password, url, notes, last_modified, "")

def parse_child(root, folders):
    """Recursively parses and extracts KeePassXC compatable fields
    from the specified Revelation XML entry."""

    e_type = root.attrib.get('type')

    output = None
    if e_type == "folder":
        pass
        # extract the name, then recurse
        name = root.find('name').text
        folders.append(name)

        output = []
        for child in root:
            temp = parse_child(child, folders)
            output.extend(temp)

        # remove the folder name as we're done in this "directory"
        folders.pop()
    else:
        if e_type == "generic":
            output = parse_generic(root, folders)
        elif e_type == "creditcard":
            output = parse_creditcard(root, folders)
        elif e_type == "cryptokey":
            output = parse_cryptokey(root, folders)
        elif e_type == "database":
            output = parse_database(root, folders)
        elif e_type == "door":
            output = parse_door(root, folders)
        elif e_type == "email":
            output = parse_email(root, folders)
        elif e_type == "ftp":
            output = parse_ftp(root, folders)
        elif e_type == "phone":
            output = parse_phone(root, folders)
        elif e_type == "shell":
            output = parse_shell(root, folders)
        elif e_type == "remotedesktop":
            output = parse_remote_desktop(root, folders)
        elif e_type == "vnc":
            output = parse_vnc(root, folders)
        elif e_type == "website":
            output = parse_website(root, folders)

        # package the output into a list
        output = [output]

    return output


def main():

    description = ("revelation-xml-to-keepassxc.py.  Copyright (C) 2020 Brian Kloppenborg. \n\n"
                   "This program comes with ABSOLUTELY NO WARRANTY. This is free software. \n"
                   "You are welcome to redistribute it under certain conditions; \n"
                   "see LICENSE for further information."
                   )

    parser = argparse.ArgumentParser(description=description, formatter_class=RawTextHelpFormatter)
    parser.add_argument('revelation_xml', metavar='xml', type=str,
                        help="Exported Revelation XML file")
    parser.add_argument('output_csv', metavar='csv', type=str,
                        help="Output CSV file")

    args = parser.parse_args()


    tree = ET.parse(args.revelation_xml) # password 'demo'
    root = tree.getroot()

    folder = []
    output = []
    for child in root:
        temp = parse_child(child, folder)
        output.extend(temp)

    # filter out None from the list
    output = list(filter(None, output))

    if len(output) == 0:
        print("No data were imported")
        return 0

    keys = output[0].keys()
    with open(args.output_csv, 'wb') as outfile:
        writer = csv.DictWriter(outfile, keys)
        writer.writeheader()
        writer.writerows(output)

if __name__ == "__main__":
    main()

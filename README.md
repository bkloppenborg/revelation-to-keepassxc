Revelation XML to KeePassXC Converter
=====

This tool converts Revelation XML exports to a CSV file for import into 
KeePassXC while preserving Revelation content and organizational structure.

![Revelation Input Database](/screenshots/revelation-demo-database.png)
![KeePassXC Import](/screenshots/keepass-resulting-import.png)

# Instructions

1. Open the Revelation password database.
2. Choose `File -> Export`. Save the file as a XML file
3. Accept the "Save to Insecure File" dialog.
4. Run the python script in this repository to convert the Revelation Output XML
   file to a KeePassXC-compatable CSV file using a command similar to the following:
   `python revelation-xml-to-keepassxc.py REVELATION_XML_FILE DESIRED_OUTPUT_FILE`
   for example:
   `python revelation-xml-to-keepassxc.py passwords.xml passwords.csv`
5. Import the resulting file into KeePassXC using the "Import CSV" function.
   Be sure to click the "First Record Has Field Names" button and map the
   column layout as shown below.
   
![KeePassXC Field Mapping](/screenshots/keepassxc-map-fields.png) 
   
# Demo

Want to see how this works on your own system before exporting your Revelation
database? Try out the functionality on the included demo database.

Open the `demo-database/revelation-test-db` file in Revelation and try out
the instructions above.
   
# Donations

If you found this script helpful, please consider donating.

All donations go to Brian Kloppenborg, the original project author and current maintainer.

[![](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=X6XHVCPMRQEL4)

[![](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=2KTUU3STLNN3G&item_name=Revelation%20XML%20To%20KeePassXC%20Script&currency_code=USD)

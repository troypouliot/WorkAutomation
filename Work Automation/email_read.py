import os
from outlook_msg import Message
import re

files_dir = r'C:\New folder\covid count'

files_dir = os.path.abspath(files_dir)

skipRegex = re.compile(r'(no new case)', flags=re.I)
casesRegex = re.compile(r'(\w+)(?= (new )?confirm)')
for root, subdirs, files in os.walk(files_dir):

    for filename in files:
        if filename.endswith('.msg'):
            file_path = os.path.join(root, filename)
            with open(file_path) as msg_file:
                msg = Message(msg_file)

            # Contents are the plaintext body of the email
            contents = msg.body

            if not skipRegex.findall(contents):
                mo = casesRegex.search(contents)
                if casesRegex.search(contents):
                    print(file_path)
                    print(mo)





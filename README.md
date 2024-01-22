﻿# DownloadProtectedGoogleDocs
Use Selenium to automate downloading Google Docs protected documents.

Note: 
- Chrome must have a default profile with a logged in Google account.
- Every Chrome instances must be closed before running the script.
- Must set default download location
- Headless doesn't work

Process:
- Disable Javascript and go to /mobilebasic version of the document to copy the content
- Paste them into a new Google Docs document
- Download it as a .docx file

# fastcode

A Python Library for simplifying the use of repetitive code in my Python projects.

## Installation
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install.

```bash
pip install fastcode
```

## Usage
For now, I have two functions there all displayed with their parameters and requirements by using typing Library.
 
The first one is IMAP, which is used to read emails and download their attachments in a created folder in the download_folder path.


```python
import fastcode

# Read email
imap(imap_port: int,
    imap_server: str,
    email_account: str,
    password: str,
    mailbox: str = 'inbox',
    search_criteria: str = 'ALL',
    download_folder: Optional[str] = None
    ) -> None
```

The Second one is SMTP, which is used to send emails.

```python
import fastcode

# Send email
smtp(to_emails:List[str], 
         smtp_port:int, 
         smtp_server:str, 
         sender_email:str, 
         sender_password:str, 
         subject:str,
         body:str,
         body_type:str,
         attachments: Optional[Dict[str,str]] = None,
         cc_emails:Optional[List[str]] = []
         ) -> None
```
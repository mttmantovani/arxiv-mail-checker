# arXiv mail checker

Check emails from the [arXiv mailing list](https://arxiv.org/help/subscribe) and return hits to a list of keywords or authors. 

## Requirements
* `python>=3.6`;
* A subscription to [email alerts](https://arxiv.org/help/subscribe) from arXiv.


## Usage
```
usage: arxivmailchecker.py [-h] [--login-file LOGIN_FILE] [--user USER]
                           [--imap IMAP] [--port PORT] [--folder FOLDER]
                           [--keywords-file KEYWORDS_FILE]
                           [--authors-file AUTHORS_FILE]
                           [--keywords KEYWORDS [KEYWORDS ...]]
                           [--authors AUTHORS [AUTHORS ...]]
                           [--output [OUTPUT]]

arXiv mailing list checker.

optional arguments:
  -h, --help            show this help message and exit
  --login-file LOGIN_FILE
                        File storing email login credentials (default:
                        login.txt)
  --user USER           Email address
  --imap IMAP           IMAP server address
  --port PORT           Port (default: 993)
  --folder FOLDER       Folder to look for emails (default: Inbox)
  --keywords-file KEYWORDS_FILE
                        Text file storing keywords to be searched (default:
                        keywords.txt)
  --authors-file AUTHORS_FILE
                        Text file storing authors to be searched (default:
                        authors.txt)
  --keywords KEYWORDS [KEYWORDS ...]
                        Space-separated keywords to search
  --authors AUTHORS [AUTHORS ...]
                        Space-separated authors to search
  --output [OUTPUT], -o [OUTPUT]
                        Specifies output file.
```
* The file `login.txt` contains credentials to access the email account (i.e., email address, IMAP server address and password). Example:

	```
	$ cat logins.txt
	user@example.com
	imap.example.com
	password
	```

	The port is 993 by default but can be passed through `--port`. If `login.txt` cannot be parsed, `--user` and `--imap` options are used, and if they are not set they are input from command line.
	
* `--folder` specify the mailbox folder in which to look for emails coming from no-reply@arxiv.org. Default is `Inbox`.
* `--keywords-file` and `--authors-file` specify text files with lists of keywords and authors to look for in the emails. Examples:

	```
	$ cat keywords.txt
	superconducting qubit
	quantum dot
	quantum-dot
	cavity
	
	$ cat authors.txt
	Doe
	Bar
	Foo
	```
	Instead of the files, keywords and authors can be supplied through `--keywords` and `--authors`:
	
	```
	$ python arxivmailchecker.py --keywords cavity 'quantum dot' 'superconducting qubit' --authors Doe Foo Bar 'Monty Python' 
	```

* Output is printed to `stdout` by default. The `--output, -o` flag specifies an output file.

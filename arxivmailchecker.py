# coding: utf-8

import argparse
import click
import datetime
import getpass
import imaplib
import os
import sys
import textwrap


class Checker(object):
    """ A class for the Checker. """
    def __init__(self, args):
        """ Initialize checker through command-line args."""
        try:
            with open(args.login_file) as f:
                self.user, self.imap_server, self.passwd = f.read().splitlines()
        except:
            print(f'Could not parse {args.login_file}. Falling back to command line.')
            self.user = click.prompt('Email', type=str) if args.user is None else args.user
            self.imap = click.prompt('IMAP server address', type=str) if args.imap is None else args.imap
            self.passwd = getpass.getpass(prompt='Insert password: ')

        self.port = args.port
        self.folder = args.folder
        self.data = []
        self.hits = []
        self.output = args.output

        try:
            with open(args.keywords_file) as f:
                self.keywords = f.read().splitlines()
        except:
            print(f'Could not parse {args.keywords_file}. Using command-line keywords.')
            self.keywords = args.keywords

        try:
            with open(args.authors_file) as f:
                self.authors = f.read().splitlines()
        except:
            print(f'Could not parse {args.authors_file}. Using command-line authors.')
            self.authors = args.authors  

            
    def connect(self):
        """ Connect to email account. """
        mail = imaplib.IMAP4_SSL(self.imap_server, self.port)
        result, status = mail.login(self.user, self.passwd)
        print(status[0].decode('utf8'))
        self.mail = mail


    def fetch(self):
        """ Fetch raw emails from arXiv. """
        self.mail.select(self.folder)
        result, data = self.mail.search(None, '(FROM "no-reply@arXiv.org")')
        ids = data[0]
        self.id_list = ids.split()
        print(f'Found {len(self.id_list)} email(s) from arXiv.\n')


    def split_body(self, email):
        """ Split a raw email in parts each containing a preprint. """
        sep = '\r\n------------------------------------------------------------------------------\r\n\\\\\r\n'
       
        result, data = self.mail.fetch(email, "(RFC822)")
        raw_email = data[0][1] 
        raw_email_string = raw_email.decode('utf-8')
        preprints = raw_email_string.split(sep)[1:]

        return preprints


    def populate(self):
        """ Parse raw string for each preprint in each email and populates a dictionary. """
        for email in self.id_list:
            preprints = self.split_body(email)
            
            for preprint in preprints:
                chunks = preprint.split(r'\\')
                metadata = chunks[0]
                abstract = ' '.join(chunks[1].split()) if len(chunks)>2 else ''
                url = chunks[2] if len(chunks)>2 else chunks[1]
        
                lines = metadata.split('\r\n')

                for idx, line in enumerate(lines):
                    if line.startswith('arXiv:'):
                        arxiv_id = line.strip().replace('arXiv:', '')
                        url = 'https://arxiv.org/abs/' + arxiv_id
                    if line.startswith('Title:'):
                        title = join_lines(lines, idx, ' ')
                    if line.startswith('Authors:'):
                        author = join_lines(lines, idx, ' ')
                    if line.startswith('Categories:'):
                        category = join_lines(lines, idx, ' ') 
        
                self.data.append({'arXiv Id': arxiv_id,
                                  'Title': title.replace('Title: ', ''), 
                                  'Authors': author.replace('Authors: ', ''),
                                  'Categories': category.replace('Categories: ', ''),
                                  'Abstract': abstract.replace('\n', ' ').replace('  ', ' ') if len(chunks)>2 else '',
                                  'URL': url})


    def search(self):
        """ Search keywords and authors in the dictionary. """
        for preprint in self.data:
            if (any(keyword in preprint['Title'].lower() for keyword in self.keywords) or 
                any(keyword in preprint['Abstract'].lower() for keyword in self.keywords) or
                any(author in preprint['Authors'] for author in self.authors)):
                self.hits.append(preprint)
        print(f'Found {len(self.hits)} hit(s) in {len(self.data)} preprints.\n')
        

    def print_results(self):
        """ Print search results to stdout or to file. """
        string = ''
        for hit in self.hits:
            string += '\n'.join([': '.join([str(k), str(v)]) for k, v in hit.items()])
            string += '\n\n'+79*'='+'\n\n'

        # Wrap long lines
        wrapper = textwrap.TextWrapper(width=79, break_on_hyphens=False)
        string = '\n'.join(['\n'.join(wrapper.wrap(text=line)) for line in string.split('\n')])


        if self.output is sys.stdout:
            print(string)
            print(f'\nFound {len(self.hits)} hit(s) in {len(self.data)} preprints.')
        else: 
            now = datetime.datetime.now()
            with open(self.output.name, 'w+') as f:
                f.write(f'Generated by arxivmailchecker on {now.strftime("%Y-%m-%d %H:%M:%S")}\n\n')
                f.write(f'Found {len(self.hits)} hits among {len(self.data)} preprints.\n\n'+79*'='+'\n\n')
                f.write(string)
            print(f'Results saved to {self.output.name}.')


def join_lines(lines, idx, delimiter):
    """ Helper function to join title/author fields which occupy more than one line in the raw email. """
    j = 1
    while lines[idx+j].startswith(delimiter):
        j += 1
    field = ' '.join([lines[idx+i] for i in range(j)])
    field = ' '.join(field.split())   

    return field
    

def main():
    parser = argparse.ArgumentParser(description='arXiv mailing list checker.')
    parser.add_argument('--login-file', default='login.txt',
            help='File storing email login credentials (default: login.txt)')
    parser.add_argument('--user', default=None, help='Email address')
    parser.add_argument('--imap', default=None, help='IMAP server address')
    parser.add_argument('--port', default=993, type=int, help='Port (default: 993)')
    parser.add_argument('--folder', default='Inbox', 
            help='Folder to look for emails (default: Inbox)')
    parser.add_argument('--keywords-file', default='keywords.txt', 
        help='Text file storing keywords to be searched (default: keywords.txt)')
    parser.add_argument('--authors-file', default='authors.txt', 
        help='Text file storing authors to be searched (default: authors.txt)')
    parser.add_argument('--keywords', nargs='+', default=[], 
                        help='Space-separated keywords to search')
    parser.add_argument('--authors', nargs='+', default=[], 
                        help='Space-separated authors to search')
    parser.add_argument('--output', '-o', nargs='?', type=argparse.FileType('w'),
                        default=sys.stdout,
                        help='Specifies output file.')
    args = parser.parse_args()


    checker = Checker(args)
    checker.connect()
    checker.fetch()
    checker.populate()
    checker.search()
    checker.print_results()


if __name__=='__main__':
    main()
    


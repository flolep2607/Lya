#!/usr/bin/python
# coding: utf-8

import argparse
import commands
from email.mime.text import MIMEText
from subprocess import Popen, PIPE

def main():
    configuration = {
        'from': 'mail@example.com',
        'to': 'mail@example.com',
        'subject': '[kalliope]',
        'body': 'toto'
    }


    parser = argparse.ArgumentParser()

    parser.add_argument("-f", "--fromemail", help="From email address")
    parser.add_argument("-t", "--to", help="To email address")
    parser.add_argument("-s", "--subject", help="Email subject")
    parser.add_argument("-b", "--body", help="Email body, used if -c is not present")
    parser.add_argument("-c", "--command", help="Command to generate text body")
    parser.add_argument("-v", "--verbose", help="Verbose mode", action="store_true")

    args = parser.parse_args()

    if args.fromemail:
        configuration["from"] = args.fromemail
    if args.to:
        configuration["to"] = args.to
    if args.subject:
        configuration["subject"] = args.subject

    if args.command:
        status, output = commands.getstatusoutput(args.command)
        configuration["body"] = output
    elif args.body:
        configuration["body"] = args.body

    send_mail(configuration)

def send_mail(configuration):
    msg = MIMEText(configuration['body'])
    msg["From"] = configuration['from']
    msg["To"] = configuration['to']
    msg["Subject"] = configuration['subject']

    p = Popen(["/usr/sbin/sendmail", "-t", "-oi"], stdin=PIPE)
    p.communicate(msg.as_string())

if __name__ == "__main__":
    main()

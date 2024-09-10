
from typing import Dict, TypedDict
import sendgrid
from sendgrid.helpers import mail
import re
import base64
import io
import os
import zipfile as zf
import openpyxl as xl
from utilita import excel, date_fns
import mimetypes

class SingleEmail(TypedDict):
    """Define email address and friendly name

    Params:
        email (str): test@example.com
        name (str): John Doe
        reply_to (str): support@example.com
    """
    email: str
    name: str
    reply_to: str

class RecipientsEmail(TypedDict):
    """Define the recipients for an email.

    You cannot have a single email be in multiple lines eg: john@example.com cannot be in cc
    and bcc.
    
    Params:
        to (str): test1@example.com, test2@example.com, test3@example.com
        cc (str): test4@example.com
        bcc (str): test5@example.com, test6@example.com        
        """
    to: str
    cc: str
    bcc: str

class ReplyToEmail(TypedDict):
    """Define email address and friendly name

    Params:
        email (str): support@example.com
    """
    email: str

class SendgridHelper:
    def __init__(self, sendgrid_api_key: str=None, from_email: SingleEmail=None, reply_to_email: ReplyToEmail=None):
        """ Creates a new SendgridHelper Instance

        Args:
            sendgrid_api_key (str): Sendgrid API key from the website

            from_email (dict): dict in the form of {"email": 'noreply@email.com', 'name': 'John Doe', 'reply_to': 'support@email.com'}. replyto is optional.

            reply_to_email (dict): dict in the form of {"email": 'support_group@email.com', 'name': 'John Doe'}. For setting an alternate reply address.
        """

        if not isinstance(from_email, dict) or from_email.get('email') is None:
            raise ValueError('from email must be defined.')
        
        if from_email.get('reply_to') is not None:
            reply_to_email: SingleEmail = {"email": from_email.get("reply_to")}

        if isinstance(reply_to_email, dict) and reply_to_email.get('email') is None:
            raise ValueError('reply-to email must be defined if its defined.')

        self.from_email: SingleEmail = from_email
        self.reply_to: SingleEmail = reply_to_email
        self.sendgrid_api_key = sendgrid_api_key

        assert not [x for x in (sendgrid_api_key, from_email) if x is None], f"Must have a sendgrid_api_key and from_email"

    def config_email(self, subject: str, recipients: RecipientsEmail, body: str):
        """Configure basic settings of the email.

        Args:
        subject (str): Subject line

        recipients (dict): dict of the email recipients in the form of: \
            :python:`{"to": "example1, example2", "cc": "example3", "bcc": "example4, example5"}`. \
                Each line is optional. Separate emails by commas. The same email cannot exist \
                in multiple lines.

        body (str): HTML of the body of the email.
        """


        e = """Configure basic settings of the email.

        Params:
            subject (str): Subject line

            recipients (dict): dict of the email recipients in the form of: {"to": "example1, example2", "cc": "example3", "bcc": "example4, example5"}. Each line is optional. Separate emails by commas. The same email cannot exist in multiple lines.

            body (str): HTML of the body of the email.        
        """
        self.client = sendgrid.SendGridAPIClient(api_key = self.sendgrid_api_key)
        self.msg = sendgrid.helpers.mail.Mail()
        self.msg.from_email = sendgrid.helpers.mail.Email(self.from_email.get('email'), self.from_email.get('name'))

        if self.reply_to is not None:
            self.msg.reply_to = sendgrid.helpers.mail.reply_to.ReplyTo(
                email=self.reply_to.get('email'), name=self.reply_to.get('name')
                )

        
        self.p = sendgrid.helpers.mail.Personalization()
        self.p.subject = subject
        self.recipients = recipients

        if isinstance(self.recipients, Dict):
            to_emails = get_email_address_list(self.recipients.get('to'))
            for e in to_emails:
                self.p.add_to(sendgrid.helpers.mail.Email(e))

            cc_emails = get_email_address_list(self.recipients.get('cc', []))
            for e in cc_emails:
                self.p.add_cc(sendgrid.helpers.mail.Email(e))

            bcc_emails = get_email_address_list(self.recipients.get('bcc', []))
            for e in bcc_emails:
                self.p.add_bcc(sendgrid.helpers.mail.Email(e))

        else:
            to_emails = get_email_address_list(self.recipients)
            for d in to_emails:
                self.p.add_to(sendgrid.helpers.mail.Email(d))


        self.msg.add_personalization(self.p)

        self.msg.add_content(
            sendgrid.helpers.mail.Content(
                'text/html',
                body
            )
        )

    def send_email(self):
        """Attemps to send the email"""
        try:
            response = self.client.client.mail.send.post(request_body = self.msg.get())
            return response
        except Exception() as e:
            return e


    def attach_df_as_csv(self, file_obj, df_filename=None, compressed=True):
        """Attach a pandas dataframe as a csv file

        Params:
            file_obj: dict in the format of {"df": [dataframe], "zip_filename": "[filename as string]"}
                {"df": unmapped_df, "zip_filename": f"uber_unmappable_transactions for {date}"}

            df_filename:

            compressed=True: compress the file as a zip file.
        """
        df = file_obj.get("df")
        zip_filename=file_obj.get("zip_filename")
        
        assert not [x for x in (df, zip_filename) if x is None], "df==None and zip_filename==None must not be true."
        
        zip_filename = zip_filename.replace('.zip','')

        if df_filename is None: df_filename = zip_filename
        df_filename = df_filename.replace('.csv','')

        zip_bytes = df_to_zipfile_bytes(df, df_filename+".csv")
        zip_bytes.seek(0)
        report_bytes = zip_bytes.read()

        self.msg.add_attachment(
            attachment_from_bytes(
            file_name = zip_filename+".zip",
            file_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            file_bytes = report_bytes
            )
        )


    def attach_single_df_as_csv(self, df, df_filename, compressed=False) -> None:
        """Attach a pandas dataframe as a csv file

        Params:
            df: dataframe object

            df_filename: what to name the file. 

            compressed=True: compress the file as a zip file. If True, the compressed file name is the same as the df filename.

        Returns:
            Nothing, as it gets added to the object.
        """
        
        if compressed==True:
            zip_filename = df_filename.replace('.zip','')
            df_filename = df_filename.replace('.csv','')

            zip_bytes = df_to_zipfile_bytes(df=df, df_filename=df_filename+'.csv')
            zip_bytes.seek(0)
            report_bytes = zip_bytes.read()
            
            attach_filename = df_filename+'.zip'
            attach_mime_type = 'application/zip'

        else:
            csv_bytes = df_to_csv_bytes(df=df)
            attach_filename = df_filename+'.csv'
            attach_mime_type = 'text/csv'
            report_bytes = csv_bytes.read()

        self.msg.add_attachment(
            attachment_from_bytes(
            file_name = attach_filename,
            file_type = attach_mime_type,
            file_bytes = report_bytes
            )
        )
    
    def attach_excel_file_from_path(self, excel_path):
        """Attaches an excel file from the filesystem.
        
        This is a deprecated function. Please use attach_file_from_path() instead.

        Params:
            excel_path (str): file from filesystem.
        """
        self.attach_file_from_path(excel_path)

    def attach_excel_file_from_bytes(self, excel_bytes, file_name):
        self.msg.add_attachment(
            attachment_from_bytes(
                file_name = file_name,
                file_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                file_bytes = excel_bytes
            )
        )

    def attach_openpyxl_workbook_from_bytes(self, wb: object, file_name: str):
        """Attaches an openpyxl workbook object into the email.
        
        Params:
            wb (openpyxl.workbook.workbook.Workbook): Workbook file.

            file_name (str): The actual file name to show in the email.   
        """
        report_bytes = io.BytesIO()
        wb.save(report_bytes)
        report_bytes.seek(0)
        self.attach_excel_file_from_bytes(report_bytes.read(), file_name=file_name)

    def attach_file_from_path(self, file_path: str) -> None:
        """Attaches a file from the filesystem.
        
        Params:
            file_path (str): full or relative filepath of the file
        """
        file_name = os.path.basename(p=file_path)

        with open(file=file_path, mode='rb') as f:
            data: bytes = base64.b64encode(f.read())

        mime_type, _ = mimetypes.guess_type(file_path)

        a = mail.Attachment()
        a.disposition = mail.Disposition(disposition='attachment')
        a.file_type = mail.FileType(file_type=mime_type)
        a.file_name = mail.FileName(file_name=file_name)
        a.file_content = mail.FileContent(file_content=data.decode('utf-8'))

        self.msg.add_attachment(a)


def get_email_address_list(address_string):
    if isinstance(address_string, str):
        address_string = re.split(r',|;', address_string)

    return [x.strip() for x in address_string]

def attachment_from_bytes(file_name, file_type, file_bytes):
    a = mail.Attachment()
    a.disposition = mail.Disposition('attachment')
    a.file_type = mail.FileType(file_type)
    a.file_name = mail.FileName(file_name)
    data_64 = str(base64.b64encode(file_bytes).decode('utf-8'))
    a.file_content = mail.FileContent(data_64)
    return a

def df_to_zipfile_bytes(df, df_filename):
    file_obj = io.BytesIO()
    x = zf.ZipFile(file=file_obj, mode='w', compression=zf.ZIP_DEFLATED, compresslevel=5) #winrar "normal" compression
    x.writestr(zinfo_or_arcname=df_filename ,data=df.to_csv(index=False)) #filename of the 
    x.close()

    return file_obj

def df_to_csv_bytes(df):
    file_obj = io.BytesIO(initial_bytes=df.to_csv(index=False).encode('utf-8'))
    file_obj.seek(0)

    return file_obj
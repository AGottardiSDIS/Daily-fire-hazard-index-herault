import win32com.client as win32

outlook = win32.Dispatch('outlook.application')
mail = outlook.CreateItem(0)
mail.To = 'agottardi@sdis34.fr'
mail.Subject = 'Message subject'
mail.Body = 'Message body'

# To attach a file to the email (optional):
'''attachment  = "Path to the attachment"
mail.Attachments.Add(attachment)
'''
mail.Send()

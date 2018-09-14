
# -*- coding: cp1252 -*-
"""
Created on Fri Sep 14 13:32:28 2018

@author: carlos
"""

import smtplib
#toaddrs = ["cgrs27@gmail.com","jleonel78@uasd.edu.do"]
def enviar_correo(toaddrs,msg):
    
    fromaddr = 'analisisuasd2015@gmail.com'
   
    msg = msg[14:]
    fecha = msg.split(" ")[2]
    asunto = "evento publicado el "+fecha
 
    
    email = """From: %s 
    To: %s 
    MIME-Version: 1.0 
    Content-type: text/html 
    Subject: %s 
    
    %s
    """ % (fromaddr, toaddrs, asunto, msg) 
    
    # Datos
    password = 'sismologia1948'
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(fromaddr,password)
    server.sendmail(fromaddr, toaddrs, email)
    server.quit()
    
    

#enviar_correo(toaddrs,asunto,msg)
import RPi.GPIO as GPIO
import smtplib as smtp
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time, datetime as dt


msg = EmailMessage()
msg['from'] = 'from@gmail.com'
msg['to'] =   'to@gmail.com'
msg['subject'] = 'rBox ready and online {}'.format(dt.datetime.now().strftime("%a, %d%b%y %X"))
msg.set_content('The rBox facility is running and connected - waiting for visitors.')

sndMail = False

# Set up email sending
if (sndMail):
    server = smtp.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("from@gmail.com", "frompwd")
    server.send_message(msg)
    server.quit()

GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
PIR_PIN = 23
RLY_PIN = 24
GPIO.setup(PIR_PIN,  GPIO.IN)
GPIO.setup(RLY_PIN, GPIO.OUT)

def rAlert():
    
    if not (sndMail) : return

    try:
        server = smtp.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login("from@gmail.com", "frompwd")

        msg = EmailMessage()
        msg['from'] = 'from@gmail.com'
        msg['to'] =   'to@gmail.com'
        msg['subject'] = 'rBox Visitor Alert {}'.format(dt.datetime.now().strftime("%a, %d%b%y %X"))
        msg.set_content('The rBox facility has detained one or more visitors. Please empty rBox and re-prime if needed!')
        server.send_message(msg)
        server.quit()
        print("Alert sent : {}".format(msg))
    except Exception as e:
        server.quit()
        print(e)
try:
    print("PIR Module Test (CTRL+C to exit)")
    time.sleep(2)
    print ("Ready")
    while True:
        if(GPIO.input(PIR_PIN)):
            print("Motion detected! {}".format(dt.datetime.now().strftime("%A, %d%b%y at %X")))
            time.sleep(5)
            GPIO.output(RLY_PIN, 1)

            rAlert()

            time.sleep(.7) # sleep brief wink while door comes down
            GPIO.output(RLY_PIN, 0)
            
        time.sleep(.25)
        GPIO.output(RLY_PIN, 0)
except KeyboardInterrupt:
    print("Quit")
    GPIO.cleanup()

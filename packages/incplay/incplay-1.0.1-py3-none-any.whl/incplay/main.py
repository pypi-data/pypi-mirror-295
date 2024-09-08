#! /bin/python3
import argparse
from requests import get
import onvif
import cv2
print("-h to help")
parser = argparse.ArgumentParser(description='')
parser.add_argument("--ip", default=None, help="ip адрес устройства")
parser.add_argument("--u", default='admin', help="Имя пользователя (default = admin)")
parser.add_argument("--p", default='12345', help="пароль (default = 12345)")
args = parser.parse_args()
error=False

if args.ip:
    ip=args.ip
    
else:
    error = True
if args.u:
    user=args.u
else:
    user='admin'
if args.p:
    passwd=args.p
else:
    passwd='12345'

if error == False :


    my=onvif.ONVIFCamera(ip,80,user,passwd)
    media_service = my.create_media_service()
    profiles = media_service.GetProfiles()
    token = profiles[0].token
    mycam = media_service.create_type('GetStreamUri')
    mycam.ProfileToken = token
    mycam.StreamSetup = {'Stream': 'RTP-Unicast', 'Transport': {'Protocol': 'RTSP'}}
    ms = media_service.GetStreamUri(mycam)

    if ms['Uri']:
        uri=ms['Uri']
        uri =uri[7:]
        uri=f"rtsp://{user}:{passwd}@{uri}"
        cam=cv2.VideoCapture(uri)
        while True:
            ret, frame = cam.read()
            cv2.imshow('Camera', frame)
            if cv2.waitKey(1) == ord('q'):
                break
        cam.release()
        
        cv2.destroyAllWindows()



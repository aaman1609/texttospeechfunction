import logging

import azure.functions as func
import speech_recognition as sr
from os import path
import json

def main(req: func.HttpRequest) -> func.HttpResponse:
    try :
    
        logging.info('Python HTTP trigger function processed a request.')

        AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "file.wav")
        with open(AUDIO_FILE, "wb") as vid:
            video_stream = req.files['audio-file'].read()
            vid.write(video_stream)

        # use the audio file as the audio source
        r = sr.Recognizer()
        with sr.AudioFile(AUDIO_FILE) as source:
            audio = r.record(source)  # read the entire audio file
    
        sphinx =""
        logging.info('trying sphinx')
        # recognize speech using Sphinx
        try:
            sphinx = ("Sphinx(local  + Free) thinks you said " + r.recognize_sphinx(audio))
            logging.info(sphinx)
        except sr.UnknownValueError:
            sphinx = ("Sphinx could not understand audio")
        except sr.RequestError as e:
            sphinx = ("Sphinx error; {0}".format(e))
        except Exception as  e:
             sphinx = ("Some other error occoured {0}".format(e))


        gsr = ""
        # recognize speech using Google Speech Recognition
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            gsr = ("Google Speech Recognition(Internet + Free) thinks you said " + r.recognize_google(audio))
            logging.info(gsr)
        except sr.UnknownValueError:
            gsr = ("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            gsr = ("Could not request results from Google Speech Recognition service; {0}".format(e))
        except Exception as  e:
             gsr = ("Some other error occoured {0}".format(e))

        gcs = ""

        # recognize speech using Google Cloud Speech
        GOOGLE_CLOUD_SPEECH_CREDENTIALS = {
                  "type": "service_account",
                  "project_id": "react-password-mngr",
                  "private_key_id": "966eaa923db7046d7d7784d88910119198ceaed0",
                  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDHbYyTXTYg4/VG\nl6bZf2FxNOc+pyaqeqNOwZYunQt5k03xYZ0aHP2Tpdk39Dtp//HN3P3zqoxskHlt\neDB78yOqp8Rzsk4LR9wWWO4l2zxUBoCJPM97ygs9MwA6RGl4SFgAtQS7l7DshfZt\nUBXD5q+pAcBRFdBxQngnx42ZagSYTIB6gbaQSrkPCrj4dScXzvzDYnXB5hcDYUiv\nblZuKOFzGY7GQ7r9531ABvt+p04by+L/4BIX4zET6A0buPpKGeG33WvQNBNGO30Q\nqyVa0MLnSLqvTtDtPwGY6/kGqlE+rtU33geyumy4IgIR8ehEi+9Or2dglQ9KSoZ3\n9q6z7DGjAgMBAAECggEAA37Qt0croF6eeULwh7YLLS1yMs+XMTxpCa5W8DDhzJsK\nWLAPTYUzOe1EO2N/zxckqSkLF8Q7ey5PvTLIFsQSMfbdeJxSxdvX6FmyrYiELCzY\n/+QdoYZ5tUmO4svkKq7fQVPq5fwoplygDxZs6zwV2W57F8YRcIrBCbbJApFbIe2I\nE1H9V418iiN/PxY8ZYctyw4g/AfbK30Qng72n9bZh84gd6sQGPy0XI1Tb4QHDcAo\ntsXUwQvyPSggX7PHF73hF2YntAIr73M9WK6w8hLLOjmmd1V7mUqT8+coWEr4KYEY\nQ2Kby0Rx/myzWFj3WUHLP9DwgPzEB3cm1anskoFXsQKBgQDqKmtoUCR6YH81Dh8Q\nzNbTWUqZ0hS/M8+rcWivZJ9htfqjrm5L7j4DmUKnTdb0Ancd2zMONAu/cWZfoH1O\nYNJ9v+vq0qfDEHz6LuelPWZNgm9BYmUeyEE7MVFvHRjRj8wvABaddeZDYV4w1ZSf\nb0XLjBPz3L33WORWtPDmp8FsBQKBgQDaBe6i5Lzh53E0l9edGxLCi9Z51vdomP0D\nNq/FUR7P0y/Lo+Ygc8X/r5pItg843e1Bl7POgOGOzrOOUXLp+bP2xqKDCLgoB5Ja\nyH88yYb+J+KuH5uiEvlWaxIWvP/Kdf86ZE6BvZe0zvVYW1kLH5sDdQHmFcIQ6IS6\nDgizTKs/hwKBgFGmoPUqnM2fQDv7xJFTG8VuaTjhrCJPqqYZUWt3JqwnjFHuzL7l\nP/J5SmiUF9PV2Dss58yYEVCb9hp6F7dww3TdqyGieqTl5u5F1LglhLqaNLkT2ja1\nlSlStRaNis3n2ka5PSmCptvv46wbjUtavXeQTJTH7+WDtXsWdLm43RURAoGAW0dM\nh6pYYgPx42EHBmGFUyoUm2IipwoWM7g7ktLJoZz7T7jI6iFObiPo5jRC3z4azPFk\neDqBNLbZeeYjxE2kyNaUx2NpJmk1Hwj+LEb7W4D7aIcXM53aAhJFuntaZDtOpfXE\n4JCt6ScUlO95siyDS8k7CEdnvoh6uSKTBe49bBUCgYEA0sD0gSzXHdIknZzJa4dv\nqa+6RXvKvjgqiyRuPtB/vdQEqtnNk9843X0JiuWaUz0gCTtz9kNvAsOU/3nmDH61\n0bK3ipfKyCqoTpHQYH2U3O05Yv5/1+W7zlHECct3H9XaFzvzxe2NbJR9v1TxIrDB\nkrsw3MaklXIvetKj8EhwI78=\n-----END PRIVATE KEY-----\n",
                  "client_email": "kotakpoc@react-password-mngr.iam.gserviceaccount.com",
                  "client_id": "105535306148553976277",
                  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                  "token_uri": "https://oauth2.googleapis.com/token",
                  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/kotakpoc%40react-password-mngr.iam.gserviceaccount.com",
                  "universe_domain": "googleapis.com"
                }
        GCS_CRED = path.join(path.dirname(path.realpath(__file__)), "GCS.json")

        with open(GCS_CRED, 'w') as f:
            json.dump(GOOGLE_CLOUD_SPEECH_CREDENTIALS, f)
       

        logging.info(GOOGLE_CLOUD_SPEECH_CREDENTIALS)
        try:
            gcs = ("Google Cloud Speech(Internet + Paid) thinks you said " + r.recognize_google_cloud(audio, credentials_json=GCS_CRED))
            logging.info(gcs)
        except sr.UnknownValueError:
            gcs = ("Google Cloud Speech could not understand audio")
        except sr.RequestError as e:
            gcs = ("Could not request results from Google Cloud Speech service; {0}".format(e))
        except Exception as  e:
             gcs = ("Some other error occoured {0}".format(e))

        

        whisper =""
        # recognize speech using whisper
        try:
            whisper =("Whisper by OpenAI(local + Free) thinks you said " + r.recognize_whisper(audio, language="english"))
            logging.info(whisper)
        except sr.UnknownValueError:
            whisper =("Whisper by OpenAI could not understand audio")
        except sr.RequestError as e:
            whisper =("Could not request results from Whisper")
        except Exception as  e:
             whisper = ("Some other error occoured {0}".format(e))

        logging.info(sphinx)
        logging.info(gsr)
        logging.info(gcs)
        logging.info(whisper)
    
        abc = { "sphinx" :sphinx,
           "gsr" :gsr,
           "gcs" :gcs,
           "whisper" :whisper,
           "status_code": "200",
           "error_message": "Success"}
        logging.info(abc)
        return func.HttpResponse(json.dumps(abc))
    except Exception as e:
        abc = { "error_message" :"Some error occured",
           "status_code" :500}
        logging.info(abc)
        logging.info(e)
        logging.info("Some error occured")
        return func.HttpResponse(json.dumps(abc))
        

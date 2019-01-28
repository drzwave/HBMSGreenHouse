from firebase import firebase
import uuid
import time

class Thundercloud:

   def __init__(self):

      self.addr     = 'https://'-- Firebase Database Name --'.firebaseio.com/'
      self.firebase = firebase.FirebaseApplication(self.addr, None)

   def getSession(self, deviceId):

      timestamp = int(time.time() * 1000)
      guid = str(uuid.uuid1())

      url = 'thunderboard/{}/sessions'.format(deviceId)
      self.firebase.put(url, timestamp, guid)

      
      d = {
            "startTime" : timestamp,
            "endTime" : timestamp,
            "shortURL": '',
            "contactInfo" : {
                 "fullName":"First and last name",
                 "phoneNumber":"12345678",
                 "emailAddress":"name@example.com",
                 "title":"",
                 "deviceName": 'Thunderboard #{}'.format(deviceId)
             },
             "temperatureUnits" : 0,
             "measurementUnits" : 0,
         }

      url = 'sessions'
      self.firebase.put(url, guid, d)

      return guid

   def putEnvironmentData(self, guid, data):

      timestamp = int(time.time() * 1000)
      url = 'sessions/{}/environment/data'.format(guid)
      self.firebase.put(url, timestamp, data)

      url = 'sessions/{}'.format(guid)
      self.firebase.put(url, 'endTime', timestamp)



if __name__ == '__main__':

   fb = Thundercloud()
   guid = fb.getSession(37372)

   data = {
      "temperature" : 0 ,
      "humidity" : 0 ,
      "ambientLight" : 0,
      "uvIndex" : 0
   }

   for i in range(3):
      fb.putEnvironmentData(guid, data)
      time.sleep(1)

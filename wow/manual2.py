#!/usr/bin/python

import os
import time
import subprocess

time.sleep(7)
subprocess.Popen(['/usr/bin/play','-q','/usr/share/sounds/ubuntu/notifications/Mallet.ogg'])
subprocess.Popen(['notify-send','--icon=face-smile', '--urgency=critical', 'Sebastien', 'Hello'])
time.sleep(15)
subprocess.Popen(['/usr/bin/play','-q','/usr/share/sounds/ubuntu/notifications/Mallet.ogg'])
subprocess.Popen(['notify-send','--icon=face-smile', '--urgency=critical', 'Sebastien', "Are you available? It's urgent."])
time.sleep(10)
subprocess.Popen(['/usr/bin/play','-q','/usr/share/sounds/ubuntu/notifications/Mallet.ogg'])
subprocess.Popen(['notify-send','--icon=face-smile', '--urgency=critical', 'Sebastien', "The hotel needs your signature for 300 extra attendees before we start. Can you sign it now, we start in an hour?"])

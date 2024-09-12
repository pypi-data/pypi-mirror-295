### window-recorder
Background window recorder

Installation:
`pip install python-window-recorder`

```
from window-recorder import Recorder
from time import sleep

recorder = Recorder('New Tab - Google Chrome')
print('Starting recording')
recorder.start(folder='recordings', filename='test')
sleep(3)
print('Stopping recording')
recorder.stop()
> Video saved as test_2024-06-29 19-08-11.mp4
```
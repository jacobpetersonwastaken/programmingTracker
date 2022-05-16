# Hours programmed tracker using Pixela and Arduino
A little script that tracks IDE's and logs the hours programmed in 
combination with an Arduino connected button to post those to Pixe.la.

* This is my first public script and is far from perfect.
* Frankensteined another script that was already running for my Arduino into this one.
* Yes I know its spaghetti code. But I have to start somewhere.


##  Get started
1. Set up [Pixe.la](https://pixe.la/) and follow their documentation.
2. Add the program.exe strings that you want to track in the programTracker.py trackPrograms list.
3. Under Arduino.py select the COM port your Arduino is plugged into.
4. Choose 4 different media clips:
   1. I have two buttons connected to my Arduino, 1st for when code is working to flip a button in celebration that plays [Its working](https://www.youtube.com/watch?v=SlSylJRwtCk). Second is to upload data to Pixela. The first MEDIA_1_FILE_PATH is for the is working celebration.
   2. MEDIA_2_FILE_PATH is for the days programming log was successfully posted to Pixela.
   3. MEDIA_3_FILE_PATH is for when post failed to Pixela.
   4. MEDIA_4_FILE_PATH is for when the file has been saved successfully. To keep performance better I slowed down the while loops and so it can take ~30 seconds to save.
5. Get programming!

###Notes
To avoid upload overlap for those late night coding sessions
I chose to have the program log anything from 0AM to 4AM on the previous day. 
Also if there are a couple of days that don't get posted, when you finally do post
the time will just get summed and posted on the first day missed.

Send me a message on twitter [@melockchain](https://twitter.com/melockchain) for any comments on how I can improve it or feature ideas.
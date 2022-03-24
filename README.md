# pic-to-rgb
I wanna be able to make a desmos graph using dots of an image, and to get the colours, I use this script.

## Instructions
- Run convert.py
- Specify file to use (by path, currently only supports jpg/png) and dimensions (in form '<width> <height>' of resulting colours)
- Copy output from 'out.txt' and paste into the browser console while on the desmos graph
- In the 'Dim' folder, adjust 'W' and 'H' to the width and height you set in the script earlier
- Also in the 'Dim' folder, adjust 'S' to change the size of the dots until you are satisfied
- Done

## Other Links
The graph I use: https://www.desmos.com/calculator/fthcivyxha

## Notes
- The desmos limit for a list is 10000, trying anything bigger will give you an error specifically saying that
- Using the 'rgb' function in desmos in an array seems to further limit the size to about ~2000 (1500 is fine, 2500 is too much)
  - This does not mean better resolutions cannot be achieved, this just means you'd need more than one colour variable list, probably also more than one list of points
- The console commands require 'C' to remain in cell 1, do not move it without also updating code
- I recommend not clicking on any cell with a long list as desmos will get laggy
- Save the graph frequently, it may freeze on you while changing - restarting due to a freeze may work better if you do it from an entirely new tab
  
## Future Changes?? 
- Automatically update desmos resolution
- Try more lists of points and colours 
  - Detect how many it needs when running a script and act accordingly

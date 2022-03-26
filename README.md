# pic-to-rgb
I wanna be able to make a Desmos graph of a picture using dots, and to get the colours, I use this script.

## Instructions (for Desmos)
1) Run `convert.py`
2) Specify file to use (by path, currently only supports jpg/png) and desired dimensions in pixel/dot count
- Alternatively, run it from the command line with something like `py convert.py <path> <width> <height>` (e.g. `py convert.py samples/test.jpg 50 40`)
3) Copy output from `out.txt` and paste into the browser console (Ctrl+Shift+J) while on the desmos graph
- Adjust the value of S on the graph to change the size of the dots until you are satisfied
- Done!

## Other Links
Latest Desmos graph link: https://www.desmos.com/calculator/3wzqhr9vmi

## Desmos Notes
- The Desmos limit for a list is 10000, trying anything bigger will give you an error specifically saying that
- Using `rgb()` in Desmos in an array seems to further limit the size to under 2500 (2200 is fine, 2500 is too much)
- The console commands require the first folder and the top 7 equations in it to remain where they are - if adding anything, do it below the "Dimensions" folder
- I recommend not clicking on any cell with a long list nor opening the "Dimensions" folder unless needed, as Desmos will get laggy
- Save the graph frequently, it may freeze on you while changing - restarting due to a freeze may work better if you do it from an entirely new tab
  
## Future Changes?? 
- Be able to change output type to make a cross-stitch pattern
- Increase max new resolution again
- Take average of nearby pixels when zooming in instead of the exact value

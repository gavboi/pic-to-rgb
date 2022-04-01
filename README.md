# pic-to-rgb
I wanna be able to make a Desmos graph of a picture using dots, and to get the colours, I use this script. I added a few other output formats too, because why not.

## Instructions
1) Run `convert.py`
2) Specify file to use (by path, currently only supports jpg/png), then desired dimensions in pixel/dot count (width then height), and desired output format
- Alternatively, run it from the command line with something like `py convert.py <path> <width> <height> <format>` (e.g. `py convert.py samples/test.jpg 50 40 desmos`)
### (for Desmos)
3) Copy output from `out.txt` and paste into the browser console (Ctrl+Shift+J) while on the desmos graph
4) Adjust the value of S on the graph to change the size of the dots until you are satisfied
5) Done!
### (for HTML)
3) Open `out.html`
4) Done!

## Other Links
Latest Desmos graph link: https://www.desmos.com/calculator/3wzqhr9vmi

## Desmos Notes
- The Desmos limit for a list is 10000, trying anything bigger will give you an error specifically saying that
- Using `rgb()` in Desmos in an array seems to further limit the size to under 2500 (2200 is fine, 2500 is too much)
- The console commands require the first folder and the top 7 equations in it to remain where they are - if adding anything, do it below the "Dimensions" folder
- I recommend not clicking on any cell with a long list nor opening the "Dimensions" folder unless needed, as Desmos will get laggy
- Save the graph frequently, it may freeze on you while changing - restarting due to a freeze may work better if you do it from an entirely new tab

## HTML Notes
- Zooming in will make the pixels/cells less square
- Printing the page currently does not keep the pixel/cell colours, eventually if you are able to do that it will probably be another output format option added sometime in the future
  
## Future Changes?? 
- Be able to change output type to make a cross-stitch pattern/excel sheet
- Restrict colour palette
- Some kind of proper GUI
- Increase Desmos max new resolution again
- Properly re-sample instead of picking individual pixels

# GPX Merger
A simple script to merge multiple GPX files into one large GPX file.  Forked from https://github.com/locked-fg/gpxmerger. 
  
## Use Case
A walking or biking track log is captured on my Apple Watch en route to officiating at STC soccer.  The matches play out and I capture another log as I return home.  In my [@Summitt Dweller · I Like to Hike](https://hikes.summittdweller.com/) logs I'd like to see just one "round trip".  Using this app to "merge" the two tracks works nicely!  

## Usage 
```python3 /Users/mark/GitHub/gpxmerger.py /Users/mark/Downloads```
All of the `.gpx` files found in the specified directory are merged into a single track written as `merged.gpx` into the same specified directory.


---
# Original `README.md` Follows

## Use Case
During holidays, one or more tracks are created for each tour / day.
In the end a single GPX Track is required for example to use in Lightroom 
in order for easy geo tagging or to get an overall map of all tracks.

Thus, a single GPX Track should be created from multiple GPX files.
  
## Usage 
```python gpxmerger.py "C:\Users\[...]\Track_1.gpx" "C:\Users\[...]\Track_2.gpx"```
The merged track is written as `merged.gpx` into the directory of the first GPX file.
 
In Windows, create a desktop link / shortcut with:
- Target: ```[path to]\python.exe gpxmerger.py```
- Execute in: ```[path to gpxmerger.py directory]```
- select multiple GPX files and drag & drop them to the link - the ```merged.gpx``` is created next to the selected tracks. 

Logging output is written to Console and into ```gpxmerger.log``` in the directory of the ```gpxmerger.py```.
# Document offset detection

## How does it work

1. Loads .png images from *input_images*

2. Performs canny edge detection

3. Detects horizontal lines
   
   - Only lines with 30deg offset from a straight line
   
   - For a group of similar lines at the same location pick outs the most confident one 

4. Calculates the mode value of the offset of all lines from a straight line

5. Depeding on threshold (0.5 deg), rotates the image

6. The rotated image is saved in *output*

# Todo

- [x] Line detection  
- [x] Slope detection 
- [x] Straightening documents  
- [x] Nice output (img with lines/result)  
- [x] multiple input > output  
- [x] Figure out angle threshold when a document shouldnt be rotated  
- [ ] Handle cases where the document is oriented vertically
  - [ ] Just add a 'vertical mode' , to which we swap if more vlines than hlines are detected

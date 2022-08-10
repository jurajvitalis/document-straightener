# Document offset detection

## How to run it

1. Put .png of the document you want to rotate in *input_images*

2. Run python main.py

```bash
python main.py
```

## How does it work

1. Loads .png images from *input_images* folder

2. Performs canny edge detection

3. Detects horizontal lines
   
   - Considers only lines with 30deg offset from a straight line
   
   - For a group of similar lines at the same location pick outs the most confident one 

4. Calculates the mode value of the offset of all lines from a straight line

5. Depeding on threshold (0.5 deg), rotates the image

6. Plots the result

7. The rotated image is saved in *output* folder

# Built with

- Python 3.9.12

- opencv 4.6.0

- numpy 1.23.1

- matplotlib 3.5.2

- All dependencies in *conda_environment.yml*

# Todo

- [x] Line detection
- [x] Slope detection
- [x] Straightening documents
- [x] Nice output (img with lines/result)
- [x] multiple input > output
- [x] Figure out angle threshold when a document shouldnt be rotated
- [ ] Handle cases where the document is oriented vertically
  - [ ] Add a 'vertical mode' , to which we swap if more vlines than hlines are detected

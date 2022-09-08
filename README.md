# Document offset detection

![Screenshot](/assets/showcase.png)

A script I developed in collaboration with my PwC colleagues. We had a lot of invoices and similarly structured documents that were to be annotated and later used in NLP models. A large portion of the documents were crooked, they needed to be straightened. This script solved the problem.

## How to use the script

1. Put .png of the document you want to rotate in *input_images*

2. ```bash
   python main.py
   ```

3. The straightened documents are stored in *output*

## How does the script work

1. Loads .png images from *input_images* folder

2. Performs canny edge detection

3. Detects horizontal lines
   
   - Considers only lines with 30deg offset from a straight line
   
   - For a group of similar lines at the same location pick outs the most confident one 

4. Calculates the mode value of the offset of all lines from a straight line

5. Depeding on the threshold (0.5 deg), rotates the image

6. Plots the result

7. Saves the straightened images in *output* folder

# Built with

- Python 3.9.12

- opencv 4.6.0

- numpy 1.23.1

- matplotlib 3.5.2

- All dependencies in *conda_environment.yml*

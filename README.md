# Morphing-opencv
A project I made last year using opencv modules. It consists in displaying a picture of a man that would be half-human, half-cat, using 2 pictures of a human and a cat. The initial project was to create intermediate views between 2 views of a same building, which explains the additional functions that are not used in the code.

The main file for running the code is morphing.py

## How to interact with the code

1. Change the path to the images in the code to fit your path (normally, you only have to change the user name)
2. Run the code
3. The image of the man appears : click on a pixel that you want to warp into the corresponding pixel of the cat image
4. Press on any keyboard
5. Click on the corresponding output pixel on the cat image
6. Press on any keyboard
7. Repeat steps 2 to 5 until the 28 pairs of points have been chosen
8. The first image of the transformation is shown : it is the man before the morphing
9. Each time you press on a keyboard, you see the next step of the morphing
10. You can escape the morphing by pressing esc.
11. On the last image, you have the photo of the cat.

In the repository, you will find a video retracing the steps of the transformation in an example run I had made.

You will find a pdf report as well. It was my grade report and explains the steps I went through to create this algorithm, knowing that I spent the greatest part of this project trying to create intermediate views betweeen two views of a building, which is explained in the first part of the report.

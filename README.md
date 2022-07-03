# RTX-in-python
Here's a script rendering a scene with spheres and light sources.
You can download the zip file, uncompress it and run the script with python3 with math, numpy, and multiprocessing installed.

Each render is really slow, especially the big render. It's recommended not to touch the window during a render.

It is possible to change the starting scene by changing the string at line 7.
There are 2 scenes I made (Objects1.txt and Objects2.txt) but you can make new ones with the template :
"x, y, z, radius, r, g, b,Sp" for a sphere with x, y and z its coordinates and r, g and b its color
"x, y, z, r, g, b,Src" for a light source with the same names.

PS : Don't mind the jank colors when the sum goes over 100%.

(to do : fix jank color sum, add light reflexion with vectorial product)

# I am remaking this in C++ and it works much better.

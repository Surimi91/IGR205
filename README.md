# Reaction Diffusion execution

Open the terminal (with Homebrew previously installed)
$ brew install sfml

With $ pip install, make sure to have all the libraries for the python part to run. The code should have this structure  \
<img width="120" alt="Capture d’écran 2024-06-27 à 12 24 45" src="https://github.com/Surimi91/IGR205/assets/123871877/2ed95d46-24fd-40e0-ab29-cb592b11b712">

- `src` contains the C++ code for pattern generation
- `py` contains the Python scripts for image processing
- `bin` contains folders with media (one image folder per video), data (CSV grids of pixels), and the executable obtained after compiling `main.cpp`


Run `grid.py` to generate the grid corresponding to the image (read the code for more details, but basically, it's the appropriate grid for Reaction-Diffusion).  
We obtain `grid.csv`.

- Now we will generate the maze pattern using the RD simulator.  
  (Before compilation, make sure to change the paths in the Makefile to match the location of SFML on your Mac)


$ make    # to get the correct executable
$ ./bin/app

This will produce output.csv (the pixel grid displayed after execution).
It's a binary pixel grid (0 for white, 1 for black).



  # Creating and moving the maze

  Now we operate through ipynb notebooks\
  - exampleNotebook is used as a pre-executed notebook to see each step clearly
  - Then main.ipynb contains several example that be executed to see results\\

Note: Those notebooks are focused on the process of creating coherent frames, thus do not return complete gif. That's why you can find some example of our results down here:

<div style="display: flex; justify-content: space-around;">
    <img src="https://github.com/Surimi91/IGR205/assets/125984433/f85710d6-f2fe-4a84-86ea-9f20377d9c5e" alt="result1" width="45%">
    <img src="https://github.com/Surimi91/IGR205/assets/125984433/32f8f882-8a05-4c7d-b347-c6e74469b43c" alt="citron1" width="45%">
</div>


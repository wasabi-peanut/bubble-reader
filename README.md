# bubble-reader
reads bubble sheets

It's intended for use for FRC scouting, but it works for whatever bubbly needs you have.

This project is inspired by PyImageSearch's bubble sheet reader, but this version is much more practical. It uses QR code-style markers to denote the location of columns, and supports two columns per sheet. paper.png is the type of sheet that this program was designed to read. The code in this repository is specialized for robot scouting for the 2019 FRC Game Destination: Deep Space. It reads scouting sheets and also reads QR codes generated by an app made to track robot cycle times. 

This code was hacked together. It works, but it's not very readable or reusable.

Dependencies:

imutils

scikit-image

numpy

opencv 3 (not 4)

pyzbar (must have zbar installed on machine)

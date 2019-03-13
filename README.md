# bubble-reader
reads bubble sheets

It's intended for use for FRC scouting, but it works for whatever bubbly needs you have.

This project is inspired by PyImageSearch's bubble sheet reader, but this version is much more practical. It uses QR code-style markers to denote the location of columns, and supports two columns per sheet. paper.png is the sheet that this program was designed to read.

Dependencies:

imutils

skimage

numpy

opencv 3 (not 4)

pyzbar (must have zbar installed on machine)

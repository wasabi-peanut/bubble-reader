# bubble-reader
reads bubble sheets

It is based on pyimagesearch's bubble sheet code. It has a few notable imporvements, which make it better-suited to be used as a data entry tool.
- adaptive thresholding makes it work much better in low-light and shadowy conditions.
- verifies that each bubble is counted only once via contour hierarchy analysis
- better contour filtering

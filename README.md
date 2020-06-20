# Cartoon Image Styling in Python

**Cartoon Styling Image with Python**

Bik Nandy &amp; Griffin Danninger

June 12, 2019

**Abstract: The goal of this project is to turn an image into its cartoon style in Python. We tested multiple color palette reduction and border detection/threshold methods in order to simplify an image so that it can be represented as a small number of colors and black outlines. We found that a k-means color clustering algorithm implementation with a k value of 15 paired with adaptive thresholding to determine borders works best and included it as our final algorithm for the application.**

### I. Introduction

As multiple new mobile applications are released involving manipulating camera images through filters, such as Snapchat and Instagram, we thought it would be exciting to try and recreate one of these photo manipulations and investigate methods to turn an image into its cartoon style. This task can be decomposed into 2 components: simplifying the color palette and identifying edges and borders to darken.

The first approach to color palette simplification is bit manipulation of the red, green, and blue values of the original image. Bit manipulation is done by setting a number of the least significant bits to zero which reduces the number of colors in the image itself. This makes the resulting image appear more cartoon-like.

The next approach to color palette simplification is rounding the individual RGB color values. This method is similar to bit manipulation as dividing the RGB values by a specified factor, rounding these values, and refactoring also reduces the number of colors in the image leading to a more cartoon-like image.

In order to improve the smoothness of results achieved when rounding an RGB color value, a modal filter can be applied. The modal filter isolates and generalizes colors in order to create an image that is closer to one color without gradients, much like a cartoon image.

The final method of color palette reduction involves utilizing an image version of the k-means machine learning clustering algorithm. The k-means clustering algorithm works by setting initial centroid values and assigning pixel values to clusters based on these centroid values. Then the algorithm switches between doing this and picking new centroids based on the current clusters. The data is assigned to a centroid using the following formula:

```
argmin (dist(c,x))
```

Here, _c_ is the full collection of centroids and the distance metric is either Minkowski or Euclidean (p=2).

The centroids are found from the following formula:

![](RackMultipart20200620-4-kdbwj2_html_92f07c00ddffd118.png)

_Si_ is the set of data point assignments for each _ith_ cluster.

These approaches are then combined with some form of edge and border detection that creates outlines and texture in only black in order to imitate the outlines of each region and give the image a true cartoon-like style.

Laplacian of the Gaussian edge detection is an intuitive first step in detecting edges in the image. This is performed by convolving the laplacian operator with a gaussian filter, convolving the resulting filter with the image, and detecting zero crossings. This would theoretically isolate edges that could be emphasized in a final cartoon style image.

Another method for identifying areas that could be set to black in the final image is the use of Otsu&#39;s method thresholding. This method analyzes the histogram of an image in order to select a threshold that minimizes the intra-class variance of the two resulting classes, or equivalently, maximizes the inter-class variance. The mathematical details of Otsu&#39;s method are discussed further in the _ **Methods** _.

Finally, adaptive thresholding provides a locally focused way to identify possible borders for the image. This is performed by convolving the image with a gaussian filter, and then subtracting an offset value and setting pixels greater than this filter to white and less than the filter values to black. This results in a localized thresholding because each pixel&#39;s threshold value is determined only by the value of their gaussian filtered neighborhood. The specifics of our implementation are discussed in detail in the _**Methods**_ section

### II. Methods

**\*See** _**VI. References**_ **for required python packages\***

**.py files created for application:**

- **adaptiveThresh.py**
- **cartoonstyle.py**
- **clusterColor.py**
- **color.py**
- **edgeDetectLoG.py**
- **kmean.py**

**Cartoonstyle.py**

This python file is where our main function for the application is housed. The _cartoonStyle_ function calls adaptiveThresh to perform adaptive thresholding on the input image, and clusterColor to create the limited palette color version of the image. Then, the minimum value of these two images is used for each pixel of the results. This results in the black outlines from the adaptive thresholding being visible in the final image, and otherwise the colors are less than or equal to the pure white of the rest of the threshold output. To call _cartoonStyle_ on an image, enter the command &quot;python cartoonStyle \&lt;filename\&gt;&quot; with the file in the same folder.

The file also contains a function named _cartoonStyleGrid_ which we used for our testing and results. This function calls the highest level functions from all the other files and creates a grid of different combinations between color palette simplification and edge/border detection so we can easily evaluate all possible options.

**Color.py**

This file provides a handful of methods to simplify the color palette of an image. The first function, _RGBfactor_, extracts the red, green, and blue values of an input image, divides each value of the elements in the array in each color by a specific factor, and the rounds each value to the nearest whole number. The numpy package is used in this case to do all of these array manipulations. Then, in order to apply a modal filter to these values in the function _colorModalFilter_, we map the RGB colors to an individual, 2D grayscale space, then apply a 2D modal filter to this. We found that this was more simple than trying to develop a specific modal filter for RGB images considering we had already reduced the number of colors of colors to a small subset. We then switched from the greyscale modal back to the RGB space through a reverse map and refactored the result. To target high frequency noise, we apply our modal filter on a circular area of radius 5. This size is not adaptive to the size of the image because larger discontinuities in color can be helpful for allowing some texture in certain areas of the image. We also added a function called _bitManipulateColor_ that provides a similar but more direct color simplification. This function isolates the red, green, and blue values as numpy arrays and removes the least significant bit for each color. It does this by right shifting then left shifting each binary value in order to get rid of the least significant bit.

**kmean.py**

This file includes multiple helper functions for the k-means clustering algorithm performed in _**clusterColor.py**_. The distance function is implemented and parameterized such that any value of p for a Minkowski distance can be used. We tested this alternative distance metric after reading &quot;Choice of distance metrics for RGB color image analysis&quot; [1] and identifying that Minkowski with p = 5 was one of the higher performing metrics for color segmentation of RGB images. However, we have selected Euclidean distance (p = 2) as we saw little aesthetic improvement in our results when using a Minkowski distance metric with p = 5.

**clusterColor.py**

_clusterColors_ takes an input image and reads it into an image dataset. Then this dataset is manipulated into a compatible format in order for the algorithm to run on it. Using functions from the _kmean.py_, the initial centroids are set randomly from the dataset and the algorithm is trained to find initial clusters. The training is done in the _train\_kmean_ function where data is assigned to clusters and then a check for empty clusters is ran. If an empty cluster is found then an element from the longest cluster is popped to fill the empty cluster and then centers are recalculated based on these new clusters. The train function ends training when the centers converge or the iteration limit of 30 is reached; otherwise, the iteration number increases and the function is run again. The image is then reconstructed and returned.

**adaptiveThresh.py**

This file implements Otsu&#39;s Method [2] for thresholding and localized adaptive thresholding for the detection of edges to be set to black in the final image. For both methods, the image is first converted to grayscale for faster analysis.

For Otsu&#39;s method, the goal of minimizing intra-class variance is performed as the equivalent maximizing of the inter-class variance. To achieve for each possible threshold, two weights are computed.

_Where L = number of histogram bins, t is the threshold, and p(n) is the probability of pixel value n_

Then, the class means are computed such that

Finally the inter-class variance is computed as specified below, and the threshold t with the maximum inter-class variance is selected. Values below the threshold are set to black, and values above are set to white. This result is returned as a greyscale image.

Adaptive thresholding is implemented through convolution with a gaussian filter and the subtraction of an offset value to determine the threshold at each point in the image. First, a window size for the gaussian filter is determined based on the size of the image using the equation below. This allows the adaptive thresholding to perform in a similar style on similar images of different resolutions

Then, the threshold values for each pixel are determined by convolving the image with the gaussian filter using reflection to fill empty edge values, and an offset of 10 is subtracted. Pixel values above their threshold are set to 255, and the remainder are set to 0. This filter is returned as a greyscale image.

**edgeDetectLoG.py**

This file implements Laplacian of the Gaussian edge detection with a sigma of 3 for the gaussian filter. It first converts the image to grayscale and convolves it with the laplacian of the gaussian filter. It then identifies zero crossings and sets these to 0, otherwise the pixel is set to 255. This filter is returned as a grayscale image.

### III. Results

In addition to the images shown below, a few more results with the original and cartoon styled images are included in our submission.

**Image 1: Lena3.bmp**

Original Image

![](RackMultipart20200620-4-kdbwj2_html_862c7cc4a01e0448.png)

Styled Image Combinations (attached as **lena3\_grid.bmp** )

![](RackMultipart20200620-4-kdbwj2_html_d0aa40c943c6ad17.gif)

Final Result

![](RackMultipart20200620-4-kdbwj2_html_67a5927975ab0835.jpg)

**Image 2: windows.jpeg**

Original Image

![](RackMultipart20200620-4-kdbwj2_html_7497f93afa0c05c8.png)

Styled Image Combinations (attached as **windows\_grid.bmp** )

![](RackMultipart20200620-4-kdbwj2_html_f2095e738bb50815.gif)

Final Image

![](RackMultipart20200620-4-kdbwj2_html_2df002f889dfd859.jpg)

**Image 3: windows\_explosion.bmp**

Original Image

![](RackMultipart20200620-4-kdbwj2_html_5bdc95bbe593d9f6.jpg)

Styled Image Combination is attached as **windows\_explosion\_grid.bmp** _(See zip folder)_

Follows same grid categories as other examples

Final Image

![](RackMultipart20200620-4-kdbwj2_html_14235fb89a71aa77.jpg)

**Image 4: beach.jpeg**

Original Image

![](RackMultipart20200620-4-kdbwj2_html_3a8e90905a97c315.jpg)

Styled Image Combination (attached as **beach\_grid.bmp** )

![](RackMultipart20200620-4-kdbwj2_html_80b925b07c821460.gif)

Final Image

![](RackMultipart20200620-4-kdbwj2_html_dbbd8f3672023844.jpg)

**Image 5: bik.jpg**

Original

![](RackMultipart20200620-4-kdbwj2_html_ac16db348ddef95a.jpg)

Styled Image Combination (attached as bik\_grid\_offset10.bmp)

Final Result (Euclidian, Minkowski)

![](RackMultipart20200620-4-kdbwj2_html_2f3967c39d6d28b1.jpg) ![](RackMultipart20200620-4-kdbwj2_html_f64556e9a379d4d9.jpg)

### IV. Discussion and Conclusion

Of the different approaches, a k-means clustering of colors with a k-value of 15 and an iteration limit of 30 paired with adaptive thresholding proved to result in the most successful &quot;cartoon-like&quot; image out of all the different combinations of image stylings. This is because it properly reduces the color palette without significant artifacting and preserves the image subject, while also emphasizing borders between object regions.

Our initial interest in using 2nd order Laplacian edge detection was quickly found to be misguided. This can be seen in the first row of each output figure. While it does identify the important edges, it also recognizes far too many finer edges. When the size of the gaussian filter used was increased, the remaining edges were no longer close enough to the original image to be effectively overlayed.

Because Otsu&#39;s method is designed with bimodal histogram distributions in mind, it works a lot better on images that have inherently higher contrast and fully reach the colorspace&#39;s low end of the dynamic range. One example of this working well is the second row of the output from **lena3.bmp** , where a small amount of the image that was already fairly dark has been blacked out. However, this method fails on brighter images like **windows.jpeg** , as large patches of the grass and sky in the image that are not initially extremely dark are set to black. Because of this issue, we believed a method that only took into consideration the local neighborhood while thresholding would perform better.

Finally, we implemented adaptive thresholding to achieve our ideal results. Adaptive thresholding allows us to threshold the image in such a way that only the local neighborhood of a pixel is taken into account when determining if it should be thresholded. This results in clean outlines of most objects and effective texturing of patterned regions. The improved outlining can be seen in the third row of the combination output for **windows.jpeg** , and its usefulness for texturization of solid color regions can be seen in the third row of the combination output for **lena3.bmp** , in her hat. This works most effectively when combined with color palette reduction techniques as it results in the most comic-like outline.

Our first color palette reduction technique we tested was bit manipulation. It provided interesting initial results at first. However, since bit manipulation completely sets the least significant bit to 0, it does not account for which final color the pixel is actually closest too. We solved this problem by implementing a factoring and rounding method that achieves the same level of color simplification with more pixels being assigned to closer color values. We also modal filtered these values which resulted in smoothly colored images. One issue with these solutions is that it can occasionally result in strong artifacting if there is a slight hue in certain regions of an image. This is especially prominent in the image **beach.jpeg** , where the sand is discolored as red and yellow regions. A similar but less extreme example of this is the appearance of purple regions in the sky of **windows.jpeg** , which has no purple colors in the actual image. While it did have good vibrant results in many cases, the downside of such artifacts caused us to pursue other methods.

Our next color reduction technique was the k-means clustering algorithm. This technique proved to be the most successful as clustering the colors resulted in the most accurate representation of the original colors and provides the least artifacting. We found through inspection that a k value of 15 provided the best results, as having significantly fewer centroids (such as k=7) resulted in some strong discoloration, while larger k values (such as k = 30) resulted in too realistic of an image. We also tested an alternative distance metric, the Minkowski distance with p=5 that has been previously evaluated to be more effective in image color clustering [1]. However, as seen in the final results for **bik.jpg** , there is little aesthetic difference between the two. Because we preferred the style of the euclidean result, we chose this distance metric for our final implementation.

In conclusion, we found that a k value of 15 utilizing a k-means clustering algorithm on the image paired with adaptive thresholding allowed us to recreate the original image to its cartoon likeness. A definite shortcoming of our algorithm is that it is not intelligent enough to adapt to different styles of images. For example, our _**Image 3**_came out as a much more accurate comic representation of the original than say _**Image 5**_ as our k-means clustering machine learning algorithm does not adapt to different styles of images. Also, it seemed that our algorithm did not work as well with lower resolution images as there are less pixels involved. Some different ways we could have completed this application was by using bilateral filtering which is an edge-preserving, and noise-reducing smoothing filter that could help with coloring. Also, a more developed machine learning algorithm could be implemented to detect the type, style, setting, and/or format of an image better to adapt the cartoon styling process.

### V. References

[1] Sanda Mahama, Dossa, and Gouton (2016). &quot;[Choice of distance metrics for RGB color image analysis](https://www.ingentaconnect.com/content/ist/ei/2016/00002016/00000020/art00036?crawler=true)&quot;. _Society for Imaging Science and Technology_.

[2] Nobuyuki Otsu (1979). &quot;[A Threshold Selection Method from Gray-level Histograms](https://ieeexplore.ieee.org/document/4310076)&quot;. _IEEE Trans. Sys., Man., Cyber._ **9** (1): 62-66.

import numpy as np
import scipy
import scipy.ndimage as ndimage
import matplotlib.pyplot as plt
from skimage import io
from skimage import color
from scipy import ndimage as ndi
from skimage import feature
from PIL import Image

varFile = 'scipiart.jpg'
img = color.rgb2gray(io.imread(varFile, as_grey=True))
plt.imshow(img, cmap=plt.get_cmap('gray'))
plt.show()
# Note the 0 sigma for the last axis, we don't wan't to blurr the color
# planes together!
img = ndimage.gaussian_filter(img, sigma=(5, 6), order=0)
plt.imshow(img, cmap=plt.get_cmap('gray'))
plt.show()
print img.shape
img = img.astype('float32')
print "check1"
dx = ndimage.sobel(img, 0)  # horizontal derivative
print "check2"
dy = ndimage.sobel(img, 1)  # vertical derivative
mag = np.hypot(dx, dy)  # magnitude
print mag;
mag *= 255.0 / np.max(mag)  # normalize (Q&D)
plt.imshow(img, cmap=plt.get_cmap('gray'))
plt.show()
scipy.misc.imsave('sobel.jpg', mag)

im = io.imread('sobel.jpg')
# Compute the Canny filter for two values of sigma
edges = np.uint8(feature.canny(im, sigma=1) * 255)


print edges.shape

newArr = [];

for y in range(edges.shape[1]):
    for x in range(edges.shape[0]):
        if(edges[x][y] == 255):
            tempVar = str(x)+","+str(y)
            newArr.append(tempVar)


plt.imshow(edges)

plt.show()
scipy.misc.imsave('canny.jpg', edges)

kernel_finalSharpen = np.array([[1., 1., 1.],
                                [1., 2., 1.],
                                [1., 1., 1.]])

kernel_finalBlur = np.array([[1., 1., 1.],
                            [1., 0., 1.],
                            [1., 1., 1.]])

shape = img.shape
supershape = (shape[0] + 2, shape[1] + 2)
supermatrix = np.zeros(supershape, dtype=np.float)
supermatrix[1:-1, 1:-1] = img



def neighbors(r, c, supermatrix):
    imageSlicing = supermatrix[r-1:r+2, c-1:c+2]
    print imageSlicing.shape
    return imageSlicing


def convolution(imageMatrix, kernelSharpen,kernelBlur, arrayPos, supermatrix):
    returnVal=imageMatrix
    for y in range(imageMatrix.shape[1]):
        for x in range(imageMatrix.shape[0]):
            returnStr=str(x) + "," + str(y)
            if returnStr in arrayPos:
                if imageMatrix[x][y].shape == kernelSharpen.shape:
                    imageSlice=neighbors(x, y, supermatrix)
                    print "ImageSlice.shape: ",imageSlice.shape
                    print "ReturnStr: ",returnStr
                    imageSlicerAsArray = np.squeeze(np.asarray(imageSlice))
                    kernelAsArray = np.squeeze(np.asarray(kernelSharpen))
                    matrixProd = imageSlicerAsArray*kernelAsArray
                    print "Matrix Product.sum(): ", matrixProd.sum()
                    print "Kernel.sum(): ", kernelSharpen.sum()
                    summation = matrixProd.sum()/kernelSharpen.sum()
                    returnVal[x][y] = summation
                    side_blur_right = str(x+1) + "," + str(y)
                    side_blur_left = str(x-1) + "," + str(y)
                    if side_blur_left not in arrayPos:
                        if imageMatrix[x-1][y].shape == kernelBlur.shape:
                            imageSliceLeft = neighbors(x-1,y,supermatrix)
                            imageSlicerAsArray = np.squeeze(np.asarray(imageSliceLeft))
                            kernelAsArray = np.squeeze(np.asarray(kernelBlur))
                            matrixProd = imageSlicerAsArray*kernelAsArray
                            sum_left = matrixProd.sum()/kernelBlur.sum()
                            returnVal[x+1][y] = sum_left
                    if side_blur_right not in arrayPos:
                        if imageMatrix[x+1][y].shape == kernelBlur.shape:
                            imageSliceRight = neighbors(x+1,y,supermatrix)
                            imageSlicerAsArray = np.squeeze(np.asarray(imageSliceRight))
                            kernelAsArray = np.squeeze(np.asarray(kernelBlur))
                            matrixProd = imageSlicerAsArray*kernelAsArray
                            sum_right = matrixProd.sum()/kernelBlur.sum()
                            returnVal[x+1][y] = sum_right

    return returnVal



# Note the 0 sigma for the last axis, we don't wan't to blurr the color
# planes together!
img2 = io.imread(varFile)
plt.imshow(img2)
plt.title('finally')
plt.show()
img2 = ndimage.gaussian_filter(img2, sigma=(4, 5, 0), order=0)
#img2 = ndimage.gaussian_filter(img2, sigma=1 , order=0)
#plt.imshow(img2)
#plt.show()
returnVal1=convolution(img2, kernel_finalSharpen, kernel_finalBlur, newArr, supermatrix)
returnVal1 = ndimage.gaussian_filter(returnVal1, sigma=(5,6,0), order=0)
plt.imshow(returnVal1)
plt.title('finalone')
plt.show()
scipy.misc.imsave('completed_output.jpg', returnVal1)


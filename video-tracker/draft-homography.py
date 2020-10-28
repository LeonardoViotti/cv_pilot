
#------------------------------------------------------------------------------
# Draft homography 

# https://towardsdatascience.com/a-social-distancing-detector-using-a-tensorflow-object-detection-model-python-and-opencv-4450a431238


def compute_perspective_transform(corner_points,width,height,image):
	""" Compute the transformation matrix
	@ corner_points : 4 corner points selected from the image
	@ height, width : size of the image
	return : transformation matrix and the transformed image
	"""
	# Create an array out of the 4 corner points
	corner_points_array = np.float32(corner_points)
	# Create an array with the parameters (the dimensions) required to build the matrix
	img_params = np.float32([[0,0],[width,0],[0,height],[width,height]])
	# Compute and return the transformation matrix
	matrix = cv2.getPerspectiveTransform(corner_points_array,img_params) 
	img_transformed = cv2.warpPerspective(image,matrix,(width,height))
	return matrix,img_transformed

# p0, p1, p2, p3 = (231, 34), (13, 137), (413, 330), (477, 81)
# mt, img_plane = compute_perspective_transform([p0, p3, p1, p2],  img_0.shape[0],  img_0.shape[1], img_0)


# Order has to be top-left, top-right, bottom-left, bottom-right
p0, p1, p2, p3 = (231, 34), (477, 81), (13, 137), (413, 330)
# drawCentroid(img_0, p4)
# stable_show(img_0)

mt, img_plane = compute_perspective_transform([p0, p1, p2, p3],  img_0.shape[0],  img_0.shape[1], img_0)
stable_show(img_plane)





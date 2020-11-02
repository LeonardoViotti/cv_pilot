
# Maybe centroids are not the best option?
#   - Try a buffer? This won't work until I have movments defined
#   - Try Bbox?

# Find all intersectinos between all trajectories
# Plot trajectories and intersection




# Test function
A = np.array([[1,4],[2,5],[3,6]])
B = np.array([[1,4],[3,6],[7,8]])


# https://stackoverflow.com/questions/8317022/get-intersecting-rows-across-two-2d-numpy-arrays
def matching_rows(A,B):
  matches=[i for i in range(B.shape[0]) if np.any(np.all(A==B[i],axis=1))]
  if len(matches)==0:
    return B[matches]
  return np.unique(B[matches],axis=0)

matching_rows(A,B)

# Find two trajectories I know match
#   - Test drawing each trajectory separeately

# Separate trajectories. I think this can vary from each run but usually the first trejctory is the van and the 9th is a pedestrian
t_car = ct_tracked[0:1]
t_ped = ct_tracked[9:10]

# Combine them again
conflict_ts = np.vstack((t_car,t_ped))


# Find matches
matching_rows(t_car[0],t_ped[0])



# Draw trajectories and intersection
img_0_conflict = img_0.copy()
draw_trajectories(img_0_conflict, conflict_ts)
stable_show(img_0_conflict)
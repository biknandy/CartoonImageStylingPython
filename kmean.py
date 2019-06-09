import random

# DONE: Select the first k points from your data set as starting centers.
def init_centers_first_k(data_set, k):
    """
    Initialize centers as first k data points in the data_set.

    Args:
        data_set: a list of data points, each data point is a dictionary:
            {'country': 'country_name',
             'vals': [x_1, ..., x_n]}
        k: the number of mean/clusters.

    Returns:
        centers: a list of k elements: centers initialized using first k data points in your data_set.
                 Each center is a list of numerical values. i.e., 'vals' of a data point.
    """
    centers = []
    for i in range(k):
        centers.append(data_set[i]['vals'])
    return centers


# DONE: Select k points randomly from your data set as starting centers.
def init_centers_random(data_set, k):
    """
    Initialize centers by selecting k random data points in the data_set.

    Args:
        data_set: a list of data points, each data point is a dictionary:
            {'country': 'country_name',
             'vals': [x_1, ..., x_n]}
        k: the number of mean/clusters.

    Returns:
        centers: a list of k elements: centers initialized using random k data points in your data_set.
                 Each center is a list of numerical values. i.e., 'vals' of a data point.
    """
    centers = random.sample(range(len(data_set)-1),k)
    for i in range(len(centers)):
        centers[i] = data_set[centers[i]]['vals']
    return centers


# DONE: compute the euclidean distance from a data point to the center of a cluster
def dist(vals, center):
    """
    Helper function: compute the euclidean distance from a data point to the center of a cluster

    Args:
        vals: a list of numbers (i.e. 'vals' of a data_point)
        center: a list of numbers, the center of a cluster.

    Returns:
         d: the euclidean distance from a data point to the center of a cluster
    """
    d = 0
    for i in range(len(vals)):
        d+= (vals[i]-center[i])**2
    d = d**0.5
    return d


# DONE: return the index of the nearest cluster
def get_nearest_center(vals, centers):
    """
    Assign a data point to the cluster associated with the nearest of the k center points.
    Return the index of the assigned cluster.

    Args:
        vals: a list of numbers (i.e. 'vals' of a data point)
        centers: a list of center points.

    Returns:
        c_idx: a number, the index of the center of the nearest cluster, to which the given data point is assigned to.
    """
    c_idx = 0
    fdist = -1
    for i,c in enumerate(centers):
        tdist = dist(vals,c)
        if tdist<fdist or fdist<0:
            fdist = tdist
            c_idx = i
    return c_idx


# DONE: compute element-wise addition of two vectors.
def vect_add(x, y):
    """
    Helper function for recalculate_centers: compute the element-wise addition of two lists.
    Args:
        x: a list of numerical values
        y: a list of numerical values

    Returns:
        s: a list: result of element-wise addition of x and y.
    """
    if y == []:
        return x
    s = []
    for i in range(len(x)):
        s.append(x[i]+y[i])
    return s


# DONE: averaging n vectors.
def vect_avg(s, n):
    """
    Helper function for recalculate_centers: Averaging n lists.
    Args:
        s: a list of numerical values: the element-wise addition over n lists.
        n: a number, number of lists

    Returns:
        s: a list of numerical values: the averaging result of n lists.
    """
    avg = []
    #sum vectors in s
    for v in s:
        avg = vect_add(v['vals'],avg)
    #divide elementwise by n
    for i in range(len(avg)):
        avg[i] = avg[i]/(1.0*n)
    return avg


# DONE: return the updated centers.
def recalculate_centers(clusters):
    """
    Re-calculate the centers as the mean vector of each cluster.
    Args:
         clusters: a list of clusters. Each cluster is a list of data_points assigned to that cluster.

    Returns:
        centers: a list of new centers as the mean vector of each cluster.
    """
    centers = []
    for c in clusters:
        centers.append(vect_avg(c,len(c)))
    return centers


# DONE: run kmean algorithm on data set until convergence or iteration limit.
def train_kmean(data_set, centers, iter_limit):
    """
    Args:
        data_set: a list of data points, each data point is a dictionary of
            {'country': 'country_name',
             'vals': [x_1, ..., x_n]}
        centers: a list of initial centers.
        iter_limit: a number, iteration limit

    Returns:
        centers: a list of updates centers/mean vectors.
        clusters: a list of clusters. Each cluster is a list of data points.
        num_iterations: a number, num of iteration when converged.
    """
    num_iterations = 0
    #centers = init_centers
    while num_iterations<iter_limit:
        #assign
        clusters = [[] for x in range(len(centers))]
        for d in data_set:
            t = get_nearest_center(d['vals'], centers)
            clusters[t].append(d)
        #check for empty clusters
        for i in range(len(clusters)):
            if clusters[i] == []:
                '''
                #pop element from new cluster with 2 or more elements to fill empty cluster
                for j in range(1,len(clusters)):
                    if len(clusters[(i+j)%(len(clusters)-1)]) > 1:
                        clusters[i].append(clusters[(i+j)%(len(clusters)-1)].pop())
                        break
                '''
                #pop element from longest cluster to fill empty cluster
                maxD = 0
                maxI = 0
                for j in range(len(clusters)):
                    if len(clusters[j])>maxD:
                        maxI = j
                        maxD = len(clusters[j])
                clusters[i].append(clusters[j].pop())

        #re-calc
        newCenters = recalculate_centers(clusters)
        #convergence? FIX THIS / UPDATE CENTERS NOT WORKING
        for i,c in enumerate(centers):
            if newCenters[i] != c:
                break
            elif i == len(centers)-1:
                return centers, clusters, num_iterations
        #not converged, increment iterations and loop
        num_iterations += 1
        centers = newCenters
    return centers, clusters, num_iterations


# DONE: helper function: compute within group sum of squares
def within_group_ss(cluster, center):
    """
    For each cluter, compute the sum of squares of euclidean distance
    from each data point in the cluster to the empirical mean of this cluster.
    Please note that the euclidean distance is squared in this function.

    Args:
        cluster: a list of data points.
        center: the center for the given cluster.

    Returns:
        ss: a number, the within cluster sum of squares.
    """
    ss = 0.0
    for i in range(len(cluster)):
        ss += (dist(cluster[i]['vals'],center))**2
    return ss


# DONE: compute sum of within group sum of squares
def sum_of_within_group_ss(clusters, centers):
    """
    For total of k clusters, compute the sum of all k within_group_ss(cluster).

    Args:
        clusters: a list of clusters.
        centers: a list of centers of the given clusters.

    Returns:
        sss: a number, the sum of within cluster sum of squares for all clusters.
    """
    sss = 0.0
    for i in range(len(clusters)):
        sss += within_group_ss(clusters[i],centers[i])
    return sss

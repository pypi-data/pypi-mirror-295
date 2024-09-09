import numpy as np
import tensorflow as tf


@tf.function
def distance_consistency_impl(X_2d, y, n_classes):
    y_sort_ixs = tf.argsort(y)

    X_2d = tf.gather(X_2d, y_sort_ixs)  # re-order, grouped per class
    y_sorted = tf.gather(y, y_sort_ixs)
    uniq, _, sizes = tf.unique_with_counts(y_sorted)
    per_class = tf.split(X_2d, sizes, num=n_classes)

    centroids = tf.convert_to_tensor(
        [tf.reduce_mean(single_class_data, axis=0) for single_class_data in per_class]
    )

    closest_centroid = tf.argmin(
        tf.linalg.norm(tf.expand_dims(X_2d, 1) - centroids, axis=-1), axis=1
    )
    closest_centroid = tf.gather(uniq, closest_centroid)

    return tf.reduce_mean(tf.cast(closest_centroid == y_sorted, tf.float64))


def distance_consistency(X_2d, y):
    n_classes = len(np.unique(y))

    return distance_consistency_impl(X_2d, y, n_classes)

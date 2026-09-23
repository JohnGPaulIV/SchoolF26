"""Pure Python Decision Tree Classifier.

Simple binary decision tree classifier. Splits are based on gini impurity.
API is a subset of the scikit-learn API.

Author: CS445 Instructor and ???
Version:

"""
from collections import namedtuple, Counter
import numpy as np

# -----------------------------------------------------------------------
# Your code should not depend on any external libraries other than numpy.
# You are free to add any private methods you like, but the
# public API must match the provided docstrings below.
# -----------------------------------------------------------------------

# Named tuple is a quick way to create a simple wrapper class...
Split_ = namedtuple(
    "Split",
    [
        "dim",
        "pos",
        "X_left",
        "y_left",
        "counts_left",
        "X_right",
        "y_right",
        "counts_right",
    ],
)


class Split(Split_):
    """
    Represents a possible split point during the decision tree
    creation process.

    Attributes:

        dim (int): the dimension along which to split
        pos (float): the position of the split
        X_left (ndarray): all X entries that are <= to the split position
        y_left (ndarray): labels corresponding to X_left
        counts_left (Counter): label counts
        X_right (ndarray):  all X entries that are > the split position
        y_right (ndarray): labels corresponding to X_right
        counts_right (Counter): label counts
    """

    def __repr__(self):
        result = "Split(dim={}, pos={},\nX_left=\n".format(self.dim, self.pos)
        result += repr(self.X_left) + ",\ny_left="
        result += repr(self.y_left) + ",\ncounts_left="
        result += repr(self.counts_left) + ",\nX_right=\n"
        result += repr(self.X_right) + ",\ny_right="
        result += repr(self.y_right) + ",\ncounts_right="
        result += repr(self.counts_right) + ")"

        return result


def split_generator(X, y, keep_counts=True):
    """
    Utility method for generating all possible splits of a data set
    for the decision tree construction algorithm.

    :param X: Numpy array with shape (num_samples, num_features)
    :param y: Numpy array with length num_samples
    :param keep_counts: Maintain counters (only useful for classification.)
    :return: A generator for Split objects that will yield all
            possible splits of the data
    """

    # Loop over all of the dimensions.
    for dim in range(X.shape[1]):
        counts_left = Counter()
        counts_right = Counter(y)

        # Get the indices in sorted order so we can sort both  data and labels
        ind = np.argsort(X[:, dim])

        # Copy the data and the labels in sorted order
        X_sort = X[ind, :]
        y_sort = y[ind]

        last_split = 0
        # Loop through the midpoints between each point in the
        # current dimension
        for index in range(1, X_sort.shape[0]):
            # don't try to split between equal points.
            if X_sort[index - 1, dim] != X_sort[index, dim]:
                pos = (X_sort[index - 1, dim] + X_sort[index, dim]) / 2.0

                flipped_counts = Counter(y_sort[last_split:index])
                counts_left = counts_left + flipped_counts
                counts_right = counts_right - flipped_counts

                last_split = index
                # Yield a possible split.  Note that the slicing here does
                # not make a copy, so this should be relatively fast.
                yield Split(
                    dim,
                    pos,
                    X_sort[0:index, :],
                    y_sort[0:index],
                    counts_left,
                    X_sort[index::, :],
                    y_sort[index::],
                    counts_right,
                )


class DecisionTreeClassifier:
    """
    A binary decision tree classifier for use with real-valued attributes.

    """

    def __init__(self, max_depth=None):
        """
        Decision tree constructor.

        :param max_depth: limit on the tree depth (minimum is 1), None for no
        limit.
        """
        if max_depth is None:
            self.max_depth = float("inf")
        elif max_depth < 1:
            raise Exception("A decision tree must have a minimum of depth 1")
        else:
            self.max_depth = max_depth
        self.tree = None

    # def fit(self, X: np.ndarray, y):
    #     """
    #     Construct the decision tree using the provided data and labels.

    #     :param X: Numpy array of samples with shape (num_samples,
    # num_features)
    #     :param y: Numpy array of targets with length num_samples
    #     """
    #     self.tree = Node(X, y)
    #     next_node = deque([self.tree])
    #     def build_tree(node: "Node"):
    #         f_idx = DecisionTreeClassifier.__find_best_feature__(node)
    #         if f_idx is None:
    #             return

    #         l_mask = node.X[:, f_idx] == True
    #         r_mask = ~l_mask
    #         l_X = node.X[l_mask]
    #         l_y = node.y[l_mask]
    #         r_X = node.X[r_mask]
    #         r_y = node.y[r_mask]

    #         f_mask = np.ones(node.X.shape[1], dtype=bool)
    #         f_mask[f_idx] = False

    #         l_node = Node(l_X[:, f_mask], l_y)
    #         r_node = Node(r_X[:, f_mask], r_y)

    #         node.left = l_node
    #         node.right = r_node
    #         next_node.append(l_node)
    #         next_node.append(r_node)

    #     while self.get_depth() < self.max_depth:
    #         nxt = next_node.popleft()
    #         step_n = build_tree(nxt)
    #         if step_n is None:
    #             break

    def fit(self, X: np.ndarray, y):
        """
        Construct the decision tree using the provided data and labels.

        :param X: Numpy array of samples with shape (num_samples, num_features)
        :param y: Numpy array of targets with length num_samples
        """
        self.tree = Node(X, y)

        def fit_recursive_helper(root: "Node", curr_depth: int):

            if len(set(root.y)) == 1:
                return

            if self.max_depth is not None and curr_depth >= self.max_depth:
                return

            best = None
            best_score = float("inf")
            for split in split_generator(root.X, root.y):
                score = DecisionTreeClassifier.__split_gini__(split)
                if score < best_score:
                    best_score = score
                    best = split

            if best is None:
                return

            root.left = Node(best.X_left, best.y_left)
            root.right = Node(best.X_right, best.y_right)
            root.split = best

            fit_recursive_helper(root.left, curr_depth + 1)
            fit_recursive_helper(root.right, curr_depth + 1)

        fit_recursive_helper(self.tree, 0)

    def predict(self, X):
        """
        Predict labels for a data set by finding the appropriate leaf node
        for each input and using the majority label at that leaf as the
        prediction.  (The data sets used for grading are selected so that
        there will be no ties.)

        :param X:  Numpy array of samples with shape (num_samples,
        num_features)
        :return: A length num_samples numpy array containing predictions.
        """
        predictions = []
        for x in X:
            node = self.tree
            while not DecisionTreeClassifier.node_is_leaf(node):
                if x[node.split.dim] <= node.split.pos:
                    node = node.left
                else:
                    node = node.right

            predictions.append(DecisionTreeClassifier.__leaf_prediction__(
                node))
        return np.array(predictions)

    def score(self, X, y):
        """
        Calculate the accuracy of the decision tree on the provided data.

        :param X: Numpy array of samples with shape (num_samples, num_features)
        :param y: Numpy array of targets with length num_samples
        :return: A float representing the fraction of correct predictions.
        """
        return np.sum(self.predict(X) == y) / len(y)

    # Trailing underscore indicates properties that are only available after
    # fitting.
    @property
    def feature_importances_(self):
        """Return the feature importances based on the splits made in the tree.

        Feature importances are the weighted and normalized gini gains for
        each feature.

        Below, n is the total number of training samples, n_node is the number
        of samples at the node being split, and n_left and n_right are the
        numbers of samples sent to that node's two children.

        gini gain is the reduction in gini impurity from a split:
            gini_gain = gini_node - (gini_left * n_left/n_node
                                     + gini_right * n_right/n_node)

        weighted: The contribution of each split is weighted by the fraction of
             the training samples that reach that node.
             importances[dim] += (n_node / n) * gini_gain

        normalized: The sum of all feature importances are scaled to sum to 1.
             If the tree contains no splits, all importances should be 0.

        :return: A numpy array with length num_features containing the
                 feature importances for each feature.
        """
        n = len(self.tree.y)
        importances = np.zeros(len(self.tree.X[0]))

        def visit(node: "Node"):
            if DecisionTreeClassifier.node_is_leaf(node):
                return

            split = node.split
            n_left = sum(split.counts_left.values())
            n_right = sum(split.counts_right.values())
            n_node = n_left + n_right

            gini_node = DecisionTreeClassifier.__gini__(Counter(node.y))
            gini_gain = gini_node - (
                DecisionTreeClassifier.__gini__(split.counts_left) * (
                    n_left / n_node
                    )
                + DecisionTreeClassifier.__gini__(split.counts_right) * (
                    n_right / n_node
                    )
                    )

            importances[split.dim] += (n_node / n) * gini_gain

            visit(node.left)
            visit(node.right)
        visit(self.tree)

        total = importances.sum()
        if total == 0:
            return importances
        return importances / total

    def get_depth(self):
        """
        :return: The depth of the decision tree.
        """
        def get_depth_helper(node: "Node"):
            if DecisionTreeClassifier.node_is_leaf(node):
                return 0
            return 1 + max(get_depth_helper(node.left), get_depth_helper(
                node.right
                ))
        return get_depth_helper(self.tree)

    @staticmethod
    def node_is_leaf(node: "Node"):
        return (node.left is None) and (node.right is None)

    @staticmethod
    def __leaf_prediction__(node: "Node"):
        counts = Counter(node.y)
        curr_prediction = None
        curr_count = 0
        for p, c in counts.items():
            if c > curr_count:
                curr_prediction = p
                curr_count = c
        return curr_prediction

    @staticmethod
    def __gini__(counts):
        total = sum(counts.values())
        if total == 0:
            return 0.0
        return 1 - sum((c / total) ** 2 for c in counts.values())

    @staticmethod
    def __split_gini__(split):
        n_left = sum(split.counts_left.values())
        n_right = sum(split.counts_right.values())
        n = n_left + n_right

        return (n_left / n) * DecisionTreeClassifier.__gini__(
            split.counts_left
            ) + \
            (n_right / n) * DecisionTreeClassifier.__gini__(
                split.counts_right
                )

    # @staticmethod
    # def __get_depth_from_node__(root: "Node") -> int:
    #     if (root is None):
    #         return 0

    #     l_depth = DecisionTreeClassifier.__get_depth_from_node__(root.left)
    #     r_depth = DecisionTreeClassifier.__get_depth_from_node__(root.right)

    #     return 1 + max(l_depth, r_depth)

    # @staticmethod
    # def __get_unique_classes__(target_list: np.ndarray) -> set | None:
    #     if target_list is None:
    #         return None
    #     return set(target_list.tolist())

    # @staticmethod
    # def __sort_by_class__(X: np.ndarray, y: np.ndarray) -> dict | None:
    #     if X is None or y is None:
    #         return None

    #     unique_classes = DecisionTreeClassifier.__get_unique_classes__(y)

    #     sorted_X = dict()
    #     for c in unique_classes:
    #         c_mask = y == c
    #         sorted_X[c] = X[c_mask].tolist()

    #     return sorted_X

    # @staticmethod
    # def __get_class_counts__(X: np.ndarray, y: np.ndarray) -> tuple[dict,
    # int] | None:
    #     sorted_by_class = DecisionTreeClassifier.__sort_by_class__(X, y)

    #     if sorted_by_class is None:
    #         return None

    #     total = X.shape[0]
    #     class_counts = dict()

    #     for c, s in sorted_by_class.items():
    #         class_counts[c] = len(s)

    #     return (class_counts, total)

    # @staticmethod
    # def __get_class_info__(X: np.ndarray, y: np.ndarray) -> tuple[dict, int]:
    #     sorted_by_class = DecisionTreeClassifier.__sort_by_class__(X, y)
    #     counts, total = DecisionTreeClassifier.__get_class_counts__(X, y)

    #     for c, s in sorted_by_class.items():
    #         counts[c]["samples"] = s

    #     return (counts, total)

    # @staticmethod
    # def __calculate_gini__(X: np.ndarray, y: np.ndarray) -> float:
    #     gini = 1
    #     class_counts, total = DecisionTreeClassifier.__get_class_counts__(X,
    # y)

    #     if class_counts is not None:
    #         gini = 1 - (np.sum(np.array([
    #             c / total for c in class_counts.values()
    #             ]) ** 2))

    #     return gini

    # @staticmethod
    # def __calculate_weighted_gini__(root: "Node"):
    #     l = root.left
    #     r = root.right

    #     if l is None or r is None:
    #         return DecisionTreeClassifier.__calculate_gini__(root.X, root.y)

    #     num_l_samples = l.X.shape[0]
    #     num_r_samples = r.X.shape[0]
    #     num_root_samples = root.X.shape[0]

    #     l_gini = DecisionTreeClassifier.__calculate_gini__(l.X, l.y)
    #     r_gini = DecisionTreeClassifier.__calculate_gini__(r.X, r.y)

    #     return 1 - (((num_l_samples / num_root_samples) * l_gini) + (
    # (num_r_samples / num_root_samples) * r_gini))

    # @staticmethod
    # def __find_best_feature__(node: "Node"):
    #     feature_pool = [f for f in range(node.X.shape[1])]

    #     if len(feature_pool) == 0 or feature_pool is None:
    #         return None

    #     best_feature = (float("-inf"), -1)
    #     root = Node(node.X, node.y)

    #     for f in feature_pool:
    #         l = node.X[:, f] == True
    #         r = ~l

    #         l_node = Node(root.X[l], root.y[l])
    #         r_node = Node(root.X[r], root.y[r])
    #         root.left = l_node
    #         root.right = r_node

    #         w_gini = DecisionTreeClassifier.__calculate_weighted_gini__(root)
    #         if w_gini > best_feature[0]:
    #             best_feature = (w_gini, f)

    #     return best_feature[1]


class Node:
    """
    It will probably be useful to have a Node class.  In order to use the
    visualization code in draw_trees, the node class must have three
    attributes:

    Attributes:
        left:  A Node object or Null for leaves.
        right - A Node object or Null for leaves.
        split - A Split object representing the split at this node,
                or Null for leaves
    """

    def __init__(self, X: np.ndarray = None, y: np.ndarray = None, split=None):
        self.left: Node | None = None
        self.right: Node | None = None
        self.split: Split = split

        self.X: np.ndarray = X
        self.y: np.ndarray = y

        # Feel free to add any other attributes you like.

    # def maj_class():


def tree_demo():
    import draw_tree as draw_tree

    X = np.array([[0.88, 0.39], [0.49, 0.52], [0.68, 0.26], [0.57, 0.51], [
        0.61, 0.73]])
    y = np.array([1, 0, 0, 0, 1])
    clf = DecisionTreeClassifier()
    clf.fit(X, y)
    draw_tree.draw_tree(X, y, clf)


if __name__ == "__main__":
    tree_demo()

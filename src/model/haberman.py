# http://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html
import numpy as np

from src.lib import sklearnlib, plot, itertver
from src.lib.data import HaberManData, Data


class Haberman:

    my_haber_man_data = HaberManData()
    my_haber_man_data.load_haber_man_data()
    X, y = my_haber_man_data.get_haber_man_data()  # get instances matrix and corresponding label
    Y = np.array(y.transpose())[0]

    def __init__(self):
        pass

    def run_haber_man(self):
        my_sklearn = sklearnlib.Sklearnlib()
        weights, scores, mean_point = my_sklearn.train_and_test(3200, self.X, self.Y, 0.3)
        Data().write_to_csv_file("../resources/haberman/output_weights_haber_man", weights)
        Data().write_score_to_file("../resources/haberman/scores", scores)

        my_itertver = itertver.IteratedTverberg()
        center_point_with_proof = my_itertver.center_point(weights)

        my_plot = plot.Plot()
        my_plot.plot3dpoints(weights, center_point_with_proof[0][0], mean_point)
        print "Center Point with proof: ", center_point_with_proof[0]
        print "Center point: ", center_point_with_proof[0][0]
        print "Proof of center point: ", center_point_with_proof[0][1]
        print "Depth of center point: ", len(center_point_with_proof[0][1])
        return weights, center_point_with_proof[0][0], mean_point

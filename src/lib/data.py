"""
This file process data
"""
import numpy as np
import random
import csv


class Data:
    """
    Class contains general data-set methods
    """

    def __init__(self):
        pass

    def split_to_train_and_test(self, train_x, label_y, percent_train):
        """
        split data matrix into train and set, with percent_train/10 as the percentage
        """
        m, n = np.shape(train_x)
        train_matrix, test_matrix = np.vsplit(train_x, np.array([percent_train*m/10]))
        m_tr, n_tr = np.shape(train_matrix)
        train_class_list = label_y[0:m_tr]
        test_class_list = label_y[m_tr:m]
        return train_matrix.astype(np.float), train_class_list.astype(np.float), test_matrix.astype(np.float), \
               test_class_list.astype(np.float)

    def get_random_index_list(self, length, data_set):
        """
        get part of the train data matrix by index
        """
        m, n = np.shape(data_set)
        return random.sample(range(m), length)

    def write_to_csv_file(self, file_path, content):
        """
         write weights to file
        """
        with open(file_path, "w") as f:
            writer = csv.writer(f)
            writer.writerows(content)

    def write_score_to_file(self, file_path, content):
        """
        write score of weights in file
        """
        with open(file_path, "w") as f:
            f.writelines(["%s\n" % item for item in content])

    def get_disjoint_subset_data(self, num_subset, data_set, label_set):
        """
        get the subset of the train data set with how many "num_subset" equal set we want to have
        """
        return np.array_split(data_set, num_subset), np.array_split(label_set, num_subset)


class HaberManData:
    """
    Class contains methods processing haber man data set.
    """

    haber_man_data = []

    def __init__(self):
        pass

    def load_haber_man_data(self):
        """
        load haber_man data
        """
        fr = open("../resources/haberman/haberman.data")
        for line in fr:
            self.haber_man_data.append(line.split(","))

    def get_haber_man_data(self):
        """
        return haber man data with instances and labels
        """
        temp_list = []
        for lists in self.haber_man_data:
            temp_list.append([int(x) for x in lists])
        x, y = np.hsplit(np.asarray(temp_list), np.array([3, ]))
        return x, y


class SkinData:
    """
    Class contains methods processing skin data set
    """

    skin_data = []

    def __init__(self):
        pass

    def load_skin_data(self):
        """
        load skin data
        """
        fr = open("../resources/skin/skin_nonskin.txt")
        for line in fr:
            self.skin_data.append(line.strip().split("\t"))

    def get_skin_data(self):
        """
        return skin data with instances and labels
        """
        skin_data = np.asarray(self.skin_data)
        np.random.shuffle(skin_data)
        x_, y_ = np.hsplit(skin_data, np.array([3, ]))
        y_ = y_.transpose()[0]
        y_[y_ == '1'] = 0
        y_[y_ == '2'] = 1
        x_ = x_.astype(np.float)
        y_ = y_.astype(np.float)
        return x_, y_


class BankData:
    """
    Class contains methods processing bank data set
    """

    data_line_full, filtered_data, teacher_label, train_class_list, test_class_list, header_line = [], [], [], [], [], \
                                                                                                   []
    data_matrix, test_matrix, train_matrix = np.mat, np.mat, np.mat

    negative_instances, positive_instances = 0, 0

    def __init__(self):
        pass

    def load_bank_data_set(self):
        """
        load bank data
        """
        fr = open("../resources/bank/bank-additional-full.csv")
        self.header_line = next(fr).split(";")
        for line in fr:
            self.data_line_full.append(line.split(";"))

    def filter_bank_data_set(self):
        """
        omit data with both unknown features attributes && with duration attribute column
        """
        lines_omit = 0
        lines_left = 0
        duration_idx = self.header_line.index('"duration"')
        for lists in self.data_line_full:
            if lists.count('"unknown"'):
                lines_omit += 1
            else:
                del lists[duration_idx]
                self.filtered_data.append(lists)
                lines_left += 1

    def convert_bank_category_to_numerical(self, index, attribute):
        """
        convert all value into double
        """

        if index == 1:
            if attribute == '"admin."':
                return 1
            elif attribute == '"blue-collar"':
                return 2
            elif attribute == '"entrepreneur"':
                return 3
            elif attribute == '"housemaid"':
                return 4
            elif attribute == '"management"':
                return 5
            elif attribute == '"retired"':
                return 6
            elif attribute == '"self-employed"':
                return 7
            elif attribute == '"services"':
                return 8
            elif attribute == '"student"':
                return 9
            elif attribute == '"technician"':
                return 10
            elif attribute == '"unemployed"':
                return 11
            else:
                raise NameError('error in converCatToNumerical function, no this job title!')

        elif index == 2:
            if attribute == '"divorced"':
                return 1
            elif attribute == '"married"':
                return 2
            elif attribute == '"single"':
                return 3
            else:
                raise NameError('error in converCatToNumerical function, no this marital status!')

        elif index == 3:
            if attribute == '"basic.4y"':
                return 1
            elif attribute == '"basic.6y"':
                return 2
            elif attribute == '"basic.9y"':
                return 3
            elif attribute == '"high.school"':
                return 4
            elif attribute == '"illiterate"':
                return 5
            elif attribute == '"professional.course"':
                return 6
            elif attribute == '"university.degree"':
                return 7
            else:
                raise NameError('error in converCatToNumerical function, no this education level!')

        elif index == 4:
            if attribute == '"no"':
                return 1
            elif attribute == '"yes"':
                return 2
            else:
                raise NameError('error in converCatToNumerical function, index==4!')

        elif index == 5:
            if attribute == '"no"':
                return 1
            elif attribute == '"yes"':
                return 2
            else:
                raise NameError('error in converCatToNumerical function, index==5!')

        elif index == 6:
            if attribute == '"no"':
                return 1
            elif attribute == '"yes"':
                return 2
            else:
                raise NameError('error in converCatToNumerical function, index==6!')

        elif index == 7:
            if attribute == '"cellular"':
                return 1
            elif attribute == '"telephone"':
                return 2
            else:
                raise NameError('error in converCatToNumerical function, index==7!')

        elif index == 8:
            if attribute == '"jan"':
                return 1
            elif attribute == '"feb"':
                return 2
            elif attribute == '"mar"':
                return 3
            elif attribute == '"apr"':
                return 4
            elif attribute == '"may"':
                return 5
            elif attribute == '"jun"':
                return 6
            elif attribute == '"jul"':
                return 7
            elif attribute == '"aug"':
                return 8
            elif attribute == '"sep"':
                return 9
            elif attribute == '"oct"':
                return 10
            elif attribute == '"nov"':
                return 11
            elif attribute == '"dec"':
                return 12
            else:
                raise NameError('error in converCatToNumerical function, index==8!')

        elif index == 9:
            if attribute == '"mon"':
                return 1
            elif attribute == '"tue"':
                return 2
            elif attribute == '"wed"':
                return 3
            elif attribute == '"thu"':
                return 4
            elif attribute == '"fri"':
                return 5

        elif index == 13:
            if attribute == '"failure"':
                return 1
            elif attribute == '"nonexistent"':
                return 2
            elif attribute == '"success"':
                return 3
            else:
                raise NameError('error in converCatToNumerical function, index==14!')

        else:
            return float(attribute)

    def parse_bank_teacher_label(self, str_in):
        """
        parse teacher label and return
        """
        if str_in == '"no"\n':
            self.negative_instances += 1
            return 0
        else:
            self.positive_instances += 1
            return 1

    def convert_bank_attr_to_matrix(self):
        """
        convert all value into numpy mat
        """
        temp_array = np.zeros((len(self.filtered_data), len(self.header_line)-2), dtype=float)
        # make sure the dataset are random, here is easier to achieve, as the data and label are together at present
        np.random.shuffle(self.filtered_data)
        for idx_list, data_line in enumerate(self.filtered_data):
            self.teacher_label.append(self.parse_bank_teacher_label(data_line.pop()))
            for idx_line, element in enumerate(data_line):
                temp_array[idx_list][idx_line] = self.convert_bank_category_to_numerical(idx_line, element)
        self.data_matrix = np.asmatrix(temp_array)

    def split_to_train_and_test(self, percent_train):
        """
        split the data matrix into training and testing sub-data-set
        """
        m, n = np.shape(self.data_matrix)
        np.random.shuffle(self.data_matrix)
        self.train_matrix, self.test_matrix = np.vsplit(self.data_matrix, np.array([percent_train*m/10]))
        m_tr, n_tr = np.shape(self.train_matrix)
        self.train_class_list = self.teacher_label[0:m_tr]
        self.test_class_list = self.teacher_label[m_tr:m]

    def pre_process_data(self):
        """
        pre process all the data
        """
        self.load_bank_data_set()
        self.filter_bank_data_set()
        self.convert_bank_attr_to_matrix()

    def get_bank_positive_instances_percent(self):
        """
        get the percent of positive instance in bank dataset
        """
        return float(self.positive_instances) / float(self.positive_instances+self.negative_instances)


class ShuttleData:

    shuttle_data_train, shuttle_data_test = [], []

    def __init__(self):
        pass

    def load_shuttle_data(self):
        """
        load skin data
        """
        fr_trn = open("../resources/shuttle/shuttle.trn")
        for line in fr_trn:
            self.shuttle_data_train.append(line.strip().split(' '))

        fr_tst = open("../resources/shuttle/shuttle.tst")
        for line in fr_tst:
            self.shuttle_data_test.append(line.strip().split(' '))

    def get_shuttle_data(self):
        self.load_shuttle_data()
        shuttle_data_trn = np.asarray(self.shuttle_data_train)
        np.random.shuffle(shuttle_data_trn)
        shuttle_trn_data, shuttle_trn_label = np.hsplit(shuttle_data_trn, np.array([9, ]))

        shuttle_trn_label[shuttle_trn_label == '2'] = 0
        shuttle_trn_label[shuttle_trn_label == '3'] = 0
        shuttle_trn_label[shuttle_trn_label == '4'] = 0
        shuttle_trn_label[shuttle_trn_label == '5'] = 0
        shuttle_trn_data = shuttle_trn_data.astype(np.float)
        shuttle_trn_label = shuttle_trn_label.astype(np.float)

        shuttle__tst_data, shuttle_tst_label = np.hsplit(np.asarray(self.shuttle_data_test), np.array([9, ]))
        shuttle_tst_label[shuttle_tst_label == '2'] = 0
        shuttle_tst_label[shuttle_tst_label == '3'] = 0
        shuttle_tst_label[shuttle_tst_label == '4'] = 0
        shuttle_tst_label[shuttle_tst_label == '5'] = 0
        shuttle__tst_data.astype(np.float)
        shuttle_tst_label.astype(np.float)
        shuttle_tst_label = shuttle_tst_label.astype(np.float)
        shuttle__tst_data = shuttle__tst_data.astype(np.float)

        return shuttle_trn_data, shuttle_trn_label, shuttle__tst_data, shuttle_tst_label


class ProteinData:

    """
    Protein data processing class
    """
    protein_instances_list, protein_labels_list = [], []

    def __init__(self):
        pass

    def read_protein_file(self):
        with open("../resources/protein/CASP.csv", "rb") as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',')
            for i, row in enumerate(spamreader):
                if i == 0:
                    print row
                else:
                    self.protein_instances_list.append([float(i) for i in row][:])

    def get_protein_data(self):
        data_matrix = np.asarray(self.protein_instances_list)
        np.random.shuffle(data_matrix)
        y_, x_ = np.hsplit(data_matrix, np.array([1, ]))
        y_ = np.hstack(y_).tolist()
        y_ = [(0 if num < 14 else 1) for num in y_]
        return x_, y_


class TelescopeData:

    telescope_data_list = []

    def __init__(self):
        pass

    def read_telescope_data(self):
        """
        load skin data
        """
        fr = open("../resources/telescope/magic04.data.txt")
        for line in fr:
            line = line.strip().split(',')
            if line[-1] == 'g':
                line[-1] = 0
            if line[-1] == 'h':
                line[-1] = 1
            self.telescope_data_list.append([float(i) for i in line][:])

    def get_telescope_data(self):
        """
        get telescope data and return with data and label
        """
        data_matrix = np.asarray(self.telescope_data_list)
        np.random.shuffle(data_matrix)
        x_, y_ = np.hsplit(data_matrix, np.array([10, ]))
        y_ = np.hstack(y_).tolist()
        return x_, y_


class WiltData:

    wilt_data_list, wilt_test_list = [], []

    def __init__(self):
        pass

    def read_wilt__file(self):

        with open("../resources/wilt/training.csv", "rb") as csv_file_train:
            spam_reader_train = csv.reader(csv_file_train, delimiter=',')
            for i, row in enumerate(spam_reader_train):
                if i == 0:
                    print row
                else:
                    if row[0] == 'w':
                        row[0] = 0
                    else:
                        row[0] = 1
                    self.wilt_data_list.append([float(i) for i in row][:])

        with open("../resources/wilt/testing.csv", "rb") as csv_file_test:
            spamreader = csv.reader(csv_file_test, delimiter=',')
            for i, row in enumerate(spamreader):
                if i == 0:
                    print row
                else:
                    if row[0] == 'w':
                        row[0] = 0
                    else:
                        row[0] = 1
                    self.wilt_test_list.append([float(i) for i in row][:])

    def get_wilt_file(self):
        data_matrix = np.asarray(self.wilt_data_list)
        np.random.shuffle(data_matrix)
        label_matrix = np.asarray(self.wilt_test_list)
        np.random.shuffle(label_matrix)
        y_train, x_train = np.hsplit(data_matrix, np.array([1, ]))
        y_test, x_test = np.hsplit(label_matrix, np.array([1, ]))
        y_train = np.hstack(y_train).tolist()
        y_test = np.hstack(y_test).tolist()
        return x_train, y_train, x_test, y_test

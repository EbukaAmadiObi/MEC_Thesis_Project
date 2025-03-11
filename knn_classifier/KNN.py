import numpy
from sklearn.neighbors import KNeighborsClassifier
import pandas
import pickle
import cmd

def gen_data():
    # Set random seed for reproducibility
    numpy.random.seed(42)

    # Generate 25 data points for Class 0
    class_0_x = numpy.random.normal(loc=2.0, scale=1.0, size=25)  # Feature x
    class_0_y = numpy.random.normal(loc=2.0, scale=1.0, size=25)  # Feature y
    class_0_labels = [0] * 25

    # Generate 25 data points for Class 1
    class_1_x = numpy.random.normal(loc=7.0, scale=1.0, size=25)  # Feature x
    class_1_y = numpy.random.normal(loc=5.0, scale=1.0, size=25)  # Feature y
    class_1_labels = [1] * 25

    # Generate 25 data points for Class 1
    class_2_x = numpy.random.normal(loc=5.0, scale=1.0, size=25)  # Feature x
    class_2_y = numpy.random.normal(loc=7.0, scale=1.0, size=25)  # Feature y
    class_2_labels = [2] * 25

    # Combine the data
    x_values = numpy.concatenate([class_0_x, class_1_x, class_2_x])
    y_values = numpy.concatenate([class_0_y, class_1_y, class_2_y])
    labels = class_0_labels + class_1_labels + class_2_labels

    # Create a DataFrame for easier manipulation
    data = pandas.DataFrame({
        'Feature_X': x_values,
        'Feature_Y': y_values,
        'Class': labels
    })

    data.to_csv('knn_dataset.csv', index=False)

def fit():
    # Read data into csv
    df = pandas.read_csv('knn_dataset.csv')

    # Unpack into lists
    x_values = df.loc[:,"Feature_X"].to_list()
    y_values = df.loc[:,"Feature_Y"].to_list()
    labels = df.loc[:,"Class"].to_list()

    # Reformat data and fit KNN classifier
    data = list(zip(x_values, y_values))
    knn_classifier = KNeighborsClassifier(n_neighbors=1)
    knn_classifier.fit(data, labels)

    # Serialize model and save
    with open("KNN_classifierl.pkl", "wb") as f:
        pickle.dump(knn_classifier, f)


def predict(new_x, new_y):

    loop = True

    while loop:

        with open("KNN_classifierl.pkl", "rb") as f:
            knn_classifier = pickle.load(f)

        # Read data into csv
        df = pandas.read_csv('knn_dataset.csv')

        new_point = [(new_x, new_y)]

        prediction = knn_classifier.predict(new_point)

        return prediction

class KNNCLI(cmd.Cmd):
    prompt = ">> "
    intro = "Welcome to KNN CLI. Type \"help\" for available commands."

    def __init__(self):
        super().__init__()

    def do_predict(self, arg):
        """Predict x and y values"""
        if not arg:
            print("No arguments given, should be in the format predict \"x\", \"y\"")
        else:
            x, y = arg.split(" ")
            print(f"Predicting for values x = {x}, y = {y}")
            prediction = predict(float(x),float(y))
            print(prediction)
if __name__ == '__main__':
    gen_data()
    fit()

    cli = KNNCLI()
    
    cli.cmdloop()

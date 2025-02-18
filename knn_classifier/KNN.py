import numpy
from sklearn.neighbors import KNeighborsClassifier
import pandas
import pickle

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

    data.to_csv('knn_classifier/knn_dataset.csv', index=False)

def fit():
    # Read data into csv
    df = pandas.read_csv('knn_classifier/knn_dataset.csv')

    # Unpack into lists
    x_values = df.loc[:,"Feature_X"].to_list()
    y_values = df.loc[:,"Feature_Y"].to_list()
    labels = df.loc[:,"Class"].to_list()

    # Display the given info
    #matplotlib.pyplot.scatter(x_values,y_values,c=labels)
    #matplotlib.pyplot.show()

    # Reformat data and fit KNN classifier
    data = list(zip(x_values, y_values))
    knn_classifier = KNeighborsClassifier(n_neighbors=1)
    knn_classifier.fit(data, labels)

    # Serialize model and save
    with open("knn_classifier/KNN_classifierl.pkl", "wb") as f:
        pickle.dump(knn_classifier, f)


def predict(new_x, new_y):

    loop = True

    while loop:

        with open("knn_classifier/KNN_classifierl.pkl", "rb") as f:
            knn_classifier = pickle.load(f)

        # Read data into csv
        df = pandas.read_csv('knn_classifier/knn_dataset.csv')

        # Unpack into lists
        x_values = df.loc[:,"Feature_X"].to_list()
        y_values = df.loc[:,"Feature_Y"].to_list()
        labels = df.loc[:,"Class"].to_list()

        new_point = [(new_x, new_y)]

        prediction = knn_classifier.predict(new_point)

        return prediction

        # Plot new point with predicted class
        #matplotlib.pyplot.scatter(numpy.append(x_values,[new_x]), numpy.append(y_values,[new_y]), c=labels + [prediction[0]])
        #matplotlib.pyplot.text(x=new_x-1.7, y=new_y-0.7, s=f"new point, class: {prediction[0]}")
        #matplotlib.pyplot.scatter(new_x, new_y, s=80, facecolors='none', edgecolors='r')
        #matplotlib.pyplot.show()

        if input("\nWould you like to make another prediction? (Y/N) ") == "N":
            loop = False
        print("\n")
if __name__ == '__main__':
    gen_data()
    fit()

    #TODO: all of this needs to be running from within the docker container, not client server interface.
    while True:
        connection, _ = srv.listen()

        while True:
            try:
                srv.send_str(connection, "Welcome! Give your point to classify using KNN [x,y]")
                received_string = srv.recv_str(connection)
                prediction = predict(*[int(char) for char in received_string.split(",")])
                srv.send_str(connection, f"Classifier predicted as class: {prediction}\n")
            except ConnectionResetError as e:
                print(f"{e.errno}: Client Disconnected, ")
                break

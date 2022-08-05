# Import Dependencies
import sklearn
import yaml
from joblib import dump, load
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
# Naive Bayes Approach
from sklearn.naive_bayes import MultinomialNB
# Trees Approach
from sklearn.tree import DecisionTreeClassifier
# Ensemble Approach
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
import seaborn as sn
import matplotlib.pyplot as plt


class DiseasePrediction:
    # Initialize
    def __init__(self, model_name=None):

        # Load Training Data
        self.train_features, self.train_labels, self.train_df = self._load_train_dataset()
        # Load Test Data
        self.test_features, self.test_labels, self.test_df = self._load_test_dataset()
        # Feature Correlation in Training Data
        self._feature_correlation(data_frame=self.train_df, show_fig=False)
        # Model Definition
        self.model_name = model_name
        # Model Save Path
        self.model_save_path = './saved_model/'

    # Function to Load Train Dataset
    def _load_train_dataset(self):
        df_train = pd.read_csv('./dataset/training_data.csv')
        cols = df_train.columns
        cols = cols[:-2]
        train_features = df_train[cols]
        train_labels = df_train['prognosis']

        # Check for data sanity
        assert (len(train_features.iloc[0]) == 132)
        assert (len(train_labels) == train_features.shape[0])
        #print("Length of Training Data: ", df_train.shape)
        #print("Training Features: ", train_features.shape)
        #print("Training Labels: ", train_labels.shape)
        return train_features, train_labels, df_train

    # Function to Load Test Dataset
    def _load_test_dataset(self):
        df_test = pd.read_csv('./dataset/test_data.csv')
        cols = df_test.columns
        cols = cols[:-1]
        test_features = df_test[cols]
        test_labels = df_test['prognosis']

        # Check for data sanity
        assert (len(test_features.iloc[0]) == 132)
        assert (len(test_labels) == test_features.shape[0])
        # print("Length of Test Data: ", df_test.shape)
        # print("Test Features: ", test_features.shape)
        # print("Test Labels: ", test_labels.shape)
        return test_features, test_labels, df_test

    # Features Correlation
    def _feature_correlation(self, data_frame=None, show_fig=False):
        # Get Feature Correlation
        corr = data_frame.corr()
        sn.heatmap(corr, square=True, annot=False, cmap="YlGnBu")
        plt.title("Feature Correlation")
        plt.tight_layout()
        if show_fig:
            plt.show()
        plt.savefig('feature_correlation.png')

    # Dataset Train Validation Split
    def _train_val_split(self):
        X_train, X_val, y_train, y_val = train_test_split(self.train_features, self.train_labels,
                                                          test_size=0.33,
                                                          random_state=101)
        #print("Number of Training Features: {0}\tNumber of Training Labels: {1}".format(len(X_train), len(y_train)))
        #print("Number of Validation Features: {0}\tNumber of Validation Labels: {1}".format(len(X_val), len(y_val)))
        return X_train, y_train, X_val, y_val

    # Model Selection
    def select_model(self):
        if self.model_name == 'mnb':
            self.clf = MultinomialNB()
        elif self.model_name == 'decision_tree':
            self.clf = DecisionTreeClassifier(criterion='entropy')
        elif self.model_name == 'random_forest':
            self.clf = RandomForestClassifier(n_estimators=10)
        elif self.model_name == 'gradient_boost':
            self.clf = GradientBoostingClassifier(n_estimators=150,
                                                  criterion='friedman_mse')
        print('select model is ',self.model_name)
        return self.clf

    # ML Model
    def train_model(self):
        # Get the Data
        X_train, y_train, X_val, y_val = self._train_val_split()
        classifier = self.select_model()
        # Training the Model
        classifier = classifier.fit(X_train, y_train)
        # Trained Model Evaluation on Validation Dataset
        confidence = classifier.score(X_val, y_val)
        # Validation Data Prediction
        y_pred = classifier.predict(X_val)
        # Model Validation Accuracy
        accuracy = accuracy_score(y_val, y_pred)
        # Model Confusion Matrix
        conf_mat = confusion_matrix(y_val, y_pred)
        # Model Classification Report
        clf_report = sklearn.metrics.classification_report(y_val, y_pred)
        # Model Cross Validation Score
        score = cross_val_score(classifier, X_val, y_val, cv=3)
        #print('\nTraining Accuracy: ', confidence)
        #print('\nValidation Prediction: ', y_pred)
        #print('\nValidation Accuracy: ', accuracy)
        #print('\nValidation Confusion Matrix: \n', conf_mat)
        #print('\nCross Validation Score: \n', score)
        #print('\nClassification Report: \n', clf_report)

        # Save Trained Model
        dump(classifier, str(self.model_save_path + self.model_name + ".joblib"))

    # Function to Make Predictions on Test Data
    def make_prediction(self, saved_model_name=None, test_data=None):
        try:
            # Load Trained Model
            clf = load(str(self.model_save_path + saved_model_name + ".joblib"))
        except Exception as e:
            print("Model not found...")

        if test_data is not None:
            result = clf.predict(test_data)
            return result
        else:
            result = clf.predict(self.test_features)
        accuracy = accuracy_score(self.test_labels, result)
        clf_report = sklearn.metrics.classification_report(self.test_labels, result)
        return accuracy, clf_report


if __name__ == "__main__":
    models='mnb','decision_tree','random_forest','gradient_boost'
    max_accuracy=0
    best_model=''
    for i in range(4):
        # Model Currently Training
        current_model_name = models[i]
        # Instantiate the Class
        dp = DiseasePrediction(model_name=current_model_name)
        # Train the Model
        dp.train_model()
        # Get Model Performance on Test Data
        test_accuracy, classification_report = dp.make_prediction(saved_model_name=current_model_name)
        print("Model Test Accuracy: ", test_accuracy)
        #print("Test Data Classification Report: \n", classification_report)
        if(test_accuracy>max_accuracy):
            max_accuracy=test_accuracy
            best_model=current_model_name

    print('\n\n\tthe best model is ',best_model)
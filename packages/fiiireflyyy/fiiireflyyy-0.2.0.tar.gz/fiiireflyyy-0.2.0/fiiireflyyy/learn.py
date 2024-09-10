import os
import pickle
import shutil
import sys
from random import randint

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import to_categorical

from sklearn.inspection import permutation_importance
from matplotlib import transforms
from matplotlib.collections import PathCollection
from matplotlib.legend_handler import HandlerPathCollection, HandlerLine2D
from matplotlib.patches import Ellipse
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from fiiireflyyy import files as ff


def generate_classes(data_dir, destination, targets):
    """
    Generate a specific folder structure for Keras models by isolating classes as different folders.

    :param data_dir:
    :type data_dir: str
    :param destination: Where to generate the classes folders
    :type destination: str
    :param targets: the different classes to use
    :type targets: str
    :return:
    """
    ff.verify_dir(destination)
    files = ff.get_all_files(data_dir)
    
    # Creating directories architecture for keras model
    for target in targets:
        ff.verify_dir(os.path.join(destination, target))
        
        for file in files:
            if target in file:
                shutil.copy2(file, os.path.join(destination, target))


def train_RFC_from_dataset(x_train, y_train, savepath=""):
    """
    Train a Random Forest Classifier model from an already formatted dataset.

        Parameters
        ----------

        savepath: str, optional, default:''
            name of the saved file. If empty, does not save the file.


        Returns
        -------
        out : tuple of size (1, 2).
            The first element is a trained random forest classifier.
            The second is its scores.
    """
    
    clf = RandomForestClassifier(n_estimators=1000)
    clf.fit(x_train.values, y_train.values)
    if savepath:
        pickle.dump(clf, open(savepath, "wb"))
    return clf


def get_top_features_from_trained_RFC(clf, mode='impurity', **kwargs):
    """
    select to top n% feature sorted by highest importance, of a trained Random Forest Classifier model.

        Parameters
        ----------
        clf : RandomForestClassifier
            a trained model

        **kwargs: keyword arguments
            show: bool, optional, default: True
                Whether to show a plot of the model feature importance or not.

            mode: ['impurity', 'permutation'], optional, default: 'impurity'
                Mode to select which feature importance base to use fo the RFC.
                If 'permutation', 'X_test' and 'y_test' must be provided.

            X_test: Dataframe, optional, default: None
                The X testing set for permutation based feature importance.

            y_test: Dataframe, optional, default: None
                The y testing set for permutation based feature importance.


        Returns
        -------
        out : list
            Feature importances of the model.
    """
    options = {"iterations": 10,
               "X_test": None,
               "y_test": None}
    options.update(**kwargs)
    
    importances_over_iterations = []
    mean_importances_over_iterations = []
    if mode == 'impurity':
        for i in range(options["iterations"]):
            mean = np.mean([tree.feature_importances_ for tree in clf.estimators_], axis=0)
            importances_over_iterations.append(mean)
        arrays = [np.array(x) for x in importances_over_iterations]
        mean_importances_over_iterations = [np.mean(k) for k in zip(*arrays)]
    
    elif mode == 'permutation':
        if options["X_test"] is None or options["y_test"] is None:
            raise AttributeError("While using permutation feature importance, X_test and y_test must be provided.")
        mean_importances_over_iterations = permutation_importance(clf,
                                                                  options["X_test"],
                                                                  options["y_test"],
                                                                  n_repeats=options["iterations"],
                                                                  random_state=42).importances_mean
    
    return mean_importances_over_iterations


def fit_pca_deprecated(dataframe: pd.DataFrame, n_components=3):
    """
    fit a Principal Component Analysis and return its instance and dataset.

        Parameters
        ----------
        dataframe: DataFrame
            The data on which the pca instance has to be fitted.
        n_components: int, optional, default: 3
            The number of components for the PCA instance.

        Returns
        -------
        out: tuple of shape (1, 3)
            The first element is the PCA instance. The second
            element is the resulting dataframe. The third is the
            explained variance ratios.
    """
    features = dataframe.columns[:-1]
    x = dataframe.loc[:, features].values
    x = StandardScaler().fit_transform(x)  # normalizing the features
    pca = PCA(n_components=n_components)
    principalComponent = pca.fit_transform(x)
    principal_component_columns = [f"principal component {i + 1}" for i in range(n_components)]
    
    principal_tahyna_Df = pd.DataFrame(data=principalComponent, columns=principal_component_columns)
    
    principal_tahyna_Df["label"] = dataframe["label"]
    
    return pca, principal_tahyna_Df, pca.explained_variance_ratio_


def apply_pca_deprecated(pca, dataframe):
    """
    Transform data using an already fit PCA instance.
        Parameters
        ----------
        pca: PCA instance
            The fitted PCA instance from what the data will
            be transformed.
        dataframe: DataFrame
            The data to transform using an already fitted PCA.
            Must have a 'label' column.

        Returns
        -------
        out: DataFrame
            The transformed data.
    """
    features = dataframe.columns[:-1]
    x = dataframe.loc[:, features].values
    x = StandardScaler().fit_transform(x)  # normalizing the features
    transformed_ds = pca.transform(x)
    transformed_df = pd.DataFrame(data=transformed_ds,
                                  columns=[f"principal component {i + 1}" for i in range(transformed_ds.shape[1])])
    transformed_df['label'] = dataframe['label']
    return transformed_df


def pca_fit_apply(dataframe_fit, dataframe_apply, n_components, label_column):
    """
    Fit a Principal Component Analysis and transform data using the fitted PCA instance.
     returns the transformed data.
        Parameters
        ----------
        dataframe_fit: pd.DataFrame
            DataFrame containing the data that the PCA will be fitted on.
            Must have a 'label' column.
        dataframe_apply: DataFrame
            DataFrame containing the data that the fitted PCA will transform.
            Must have a 'label' column.
        n_components: int
            The nimber of components used for the PCA
        label_column: str
            The name of the column that contains the labels in both dataframes

        Returns
        -------
        out: DataFrame,
            The transformed data.
        out : ratio (list)
            The explained variance ratio for each principal component
    """
    features = dataframe_fit.loc[:, dataframe_fit.columns != label_column].columns
    
    # normalizing the features
    pca_object = PCA(n_components=n_components)
    principal_component_columns = [f"principal component {i + 1}" for i in range(n_components)]
    
    # --- FIT
    x_fit = dataframe_fit.loc[:, features].values
    standard_scaler = StandardScaler().fit(x_fit)
    x_fit = standard_scaler.transform(x_fit)
    principalComponent_fit = pca_object.fit_transform(x_fit)
    pcdf = pd.DataFrame(data=principalComponent_fit
                        , columns=principal_component_columns, )
    pcdf.reset_index(drop=True, inplace=True)
    dataframe_fit.reset_index(drop=True, inplace=True)
    pcdf[label_column] = dataframe_fit[label_column]
    
    # --- APPLY
    x_apply = dataframe_apply.loc[:, features].values  # normalizing the features
    x_apply = standard_scaler.transform(x_apply)
    principalComponent_apply = pca_object.transform(x_apply)
    transformed_df = pd.DataFrame(data=principalComponent_apply,
                                  columns=[f"principal component {i + 1}" for i in
                                           range(principalComponent_apply.shape[1])])
    transformed_df.reset_index(drop=True, inplace=True)
    dataframe_apply.reset_index(drop=True, inplace=True)
    transformed_df[label_column] = dataframe_apply[label_column]
    
    # ---
    ratio = pca_object.explained_variance_ratio_
    ratio = [round(x * 100, 2) for x in ratio]
    
    return transformed_df, ratio
def confidence_ellipse(x, y, ax, n_std=3.0, color='none', **kwargs):
    """
    Create a plot of the covariance confidence ellipse of *x* and *y*.

        Parameters
        ----------
        x, y : array-like, shape (n, )
            Input data.

        ax : matplotlib.axes.Axes
            The axes object to draw the ellipse into.

        n_std : float
            The number of standard deviations to determine the ellipse's radiuses.

        color : str
            color of the ellipsis.

        **kwargs
            Forwarded to `~matplotlib.patches.Ellipse`

        Returns
        -------
        matplotlib.patches.Ellipse
    """
    if x.size != y.size:
        raise ValueError("x and y must be the same size")
    
    cov = np.cov(x, y)
    pearson = cov[0, 1] / np.sqrt(cov[0, 0] * cov[1, 1])
    # Using a special case to obtain the eigenvalues of this
    # two-dimensional dataset.
    ell_radius_x = np.sqrt(1 + pearson)
    ell_radius_y = np.sqrt(1 - pearson)
    ellipse = Ellipse((0, 0), width=ell_radius_x * 2, height=ell_radius_y * 2,
                      color=color, **kwargs)
    
    # Calculating the standard deviation of x from
    # the squareroot of the variance and multiplying
    # with the given number of standard deviations.
    scale_x = np.sqrt(cov[0, 0]) * n_std
    mean_x = np.mean(x)
    
    # calculating the standard deviation of y ...
    scale_y = np.sqrt(cov[1, 1]) * n_std
    mean_y = np.mean(y)
    
    transform = transforms.Affine2D() \
        .rotate_deg(45) \
        .scale(scale_x, scale_y) \
        .translate(mean_x, mean_y)
    
    ellipse.set_transform(transform + ax.transData)
    return ax.add_patch(ellipse)


def plot_pca(dataframe: pd.DataFrame, **kwargs):
    """
    plot the result of PCA.

    Parameters
    ----------
    dataframe: DataFrame
        The data to plot. Must contain a 'label' column.
    n_components: int, optional, default: 2
        Number of principal components. Also, teh dimension
        of the graph. Must be equal to 2 or 3.
    show: bool, optional, default: True
        Whether to show the plot or not.
    save: bool, optional, default: False
        Whether to save the plot or not.
    commentary: str, optional, default: "T=48H"
        Any specification to include in the file name while saving.
    points: bool, optional, default: True
        whether to plot the points or not.
    metrics: bool, optional, default: False
        Whether to plot the metrics or not
    savedir: str, optional, default: ""
        Directory where to save the resulting plot, if not empty.
    title: str, optional, default: ""
        The filename of the resulting plot. If empty,
        an automatic name will be generated.
    ratios: tuple of float, optional, default: ()
        the PCA explained variance ratio
    """
    
    options = {
        'n_components': 2,
        'show': True,
        'commentary': "",
        'points': True,
        'metrics': False,
        'savedir': "",
        'pc_ratios': [],
        'title': "",
        'ratios': (),
        'dpi': 300,
        
    }
    
    options.update(kwargs)
    targets = (list(set(dataframe["label"])))
    colors = ['g', 'b', 'r', 'k', 'sandybrown', 'deeppink', 'gray']
    if len(targets) > len(colors):
        n = len(targets) - len(colors) + 1
        for i in range(n):
            colors.append('#%06X' % randint(0, 0xFFFFFF))
    
    label_params = {'fontsize': 20, "labelpad": 8}
    ticks_params = {'fontsize': 20, }
    if options['n_components'] == 2:
        fig, ax = plt.subplots(1, 1, figsize=(12, 10))
        
        plt.xticks(**ticks_params)
        plt.yticks(**ticks_params)
        xlabel = f'Principal Component-1 ({options["ratios"][0]}%)'
        ylabel = f'Principal Component-2 ({options["ratios"][1]}%)'
        if len(options['pc_ratios']):
            xlabel += f" ({round(options['pc_ratios'][0] * 100, 2)}%)"
            ylabel += f" ({round(options['pc_ratios'][1] * 100, 2)}%)"
        
        plt.xlabel(xlabel, **label_params)
        plt.ylabel(ylabel, **label_params)
        
        for target, color in zip(targets, colors):
            indicesToKeep = dataframe['label'] == target
            x = dataframe.loc[indicesToKeep, 'principal component 1']
            y = dataframe.loc[indicesToKeep, 'principal component 2']
            if options['points']:
                alpha = 1
                if options['metrics']:
                    alpha = .2
                plt.scatter(x, y, c=color, s=10, alpha=alpha, label=target)
            if options['metrics']:
                plt.scatter(np.mean(x), np.mean(y), marker="+", color=color, linewidth=2, s=160)
                confidence_ellipse(x, y, ax, n_std=1.0, color=color, fill=False, linewidth=2)
        
        def update(handle, orig):
            handle.update_from(orig)
            handle.set_alpha(1)
        
        plt.legend(prop={'size': 25}, handler_map={PathCollection: HandlerPathCollection(update_func=update),
                                                   plt.Line2D: HandlerLine2D(update_func=update)})
    elif options['n_components'] == 3:
        plt.figure(figsize=(10, 10))
        ax = plt.axes(projection='3d')
        
        xlabel = f'Principal Component-1 ({options["ratios"][0]}%)'
        ylabel = f'Principal Component-2 ({options["ratios"][1]}%)'
        zlabel = f'Principal Component-3 ({options["ratios"][2]}%)'
        if len(options['pc_ratios']):
            xlabel += f" ({round(options['pc_ratios'][0] * 100, 2)}%)"
            ylabel += f" ({round(options['pc_ratios'][1] * 100, 2)}%)"
            zlabel += f" ({round(options['pc_ratios'][2] * 100, 2)}%)"
        
        ax.set_xlabel(xlabel, **label_params)
        ax.set_ylabel(ylabel, **label_params)
        ax.set_zlabel(zlabel, **label_params)
        for target, color in zip(targets, colors):
            indicesToKeep = dataframe['label'] == target
            x = dataframe.loc[indicesToKeep, 'principal component 1']
            y = dataframe.loc[indicesToKeep, 'principal component 2']
            z = dataframe.loc[indicesToKeep, 'principal component 3']
            ax.scatter3D(x, y, z, c=color, s=10)
        plt.legend(targets, prop={'size': 18})
    
    if options['savedir']:
        if options["title"] == "":
            if options['commentary']:
                options["title"] += options["commentary"]
        
        plt.savefig(os.path.join(options['savedir'], options["title"] + ".png"), dpi=options['dpi'])
    
    if options['show']:
        plt.show()
    plt.close()


def plot_umap(dataframe, **kwargs):
    """
    plot the result of UMAP.

        Parameters
        ----------
        dataframe: DataFrame
            The data to plot. Must contain a 'label' column.

        **kwargs: keyword arguments
            n_components: int, optional, default: 3
                Number of principal components. Also, teh dimension
                of the graph. Must be equal to 2 or 3.
            show: bool, optional, default: True
                Whether to show the plot or not.
            save: bool, optional, default: False
                Whether to save the plot or not.
            commentary: str, optional, default: ""
                Any specification to include in the file name while saving.
            points: bool, optional, default: True
                whether to plot the points or not.
            metrics: bool, optional, default: False
                Whether to plot the metrics or not
            savedir: str, optional, default: ""
                Directory where to save the resulting plot, if not empty.
    """
    options = {"n_components": 3, "show": True, "save": False, "commentary": "", "points": True,
               "metrics": False, "savedir": ""}
    options.update(**kwargs)
    targets = dataframe["label"].unique()
    colors = ['r', 'g', 'b', 'k', 'sandybrown', 'deeppink', 'gray']
    if len(targets) > len(colors):
        n = len(targets) - len(colors) + 1
        for i in range(n):
            colors.append('#%06X' % randint(0, 0xFFFFFF))
    if options["n_components"] == 2:
        fig, ax = plt.subplots(1, 1, figsize=(10, 10))
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=14)
        plt.xlabel(f'PC-1', fontsize=20)
        plt.ylabel(f'PC-2', fontsize=20)
        plt.title(f"Uniform Manifold Approximated Projection", fontsize=20)
        for target, color in zip(targets, colors):
            indicesToKeep = dataframe['label'] == target
            x = dataframe.loc[indicesToKeep, 'dimension 1']
            y = dataframe.loc[indicesToKeep, 'dimension 2']
            if options["points"]:
                alpha = 1
                if options["metrics"]:
                    alpha = .2
                plt.scatter(x, y, c=color, s=10, alpha=alpha, label=target)
            if options["metrics"]:
                plt.scatter(np.mean(x), np.mean(y), marker="+", color=color, linewidth=2, s=160)
                confidence_ellipse(x, y, ax, n_std=1.0, color=color, fill=False, linewidth=2)
        
        def update(handle, orig):
            handle.update_from(orig)
            handle.set_alpha(1)
        
        plt.legend(prop={'size': 15}, handler_map={PathCollection: HandlerPathCollection(update_func=update),
                                                   plt.Line2D: HandlerLine2D(update_func=update)})
    if options["n_components"] == 3:
        plt.figure(figsize=(10, 10))
        ax = plt.axes(projection='3d')
        ax.set_xlabel(f'dimension-1', fontsize=20)
        ax.set_ylabel(f'dimension-2', fontsize=20)
        ax.set_zlabel(f'dimension-3', fontsize=20)
        for target, color in zip(targets, colors):
            indicesToKeep = dataframe['label'] == target
            x = dataframe.loc[indicesToKeep, dataframe.columns[0]]
            y = dataframe.loc[indicesToKeep, dataframe.columns[1]]
            z = dataframe.loc[indicesToKeep, dataframe.columns[2]]
            ax.scatter3D(x, y, z, c=color, s=10, label='bla')
        plt.legend(targets, prop={'size': 15})
        plt.title(f"Uniform Manifold Approximated Projection", fontsize=20)
    
    if options["savedir"]:
        if options["commentary"]:
            plt.savefig(os.path.join(options["savedir"],
                                     f"UMAP n={options['n_components']} t={targets} {options['commentary']}.png"))
        else:
            plt.savefig(os.path.join(options["savedir"], f"UMAP n={options['n_']} t={targets}.png"))
    
    if options["show"]:
        plt.show()
    plt.close()


def test_clf_by_confusion(clf, test_dataset: pd.DataFrame, training_targets: tuple, return_data=False, **kwargs):
    """
    Test an already trained Random forest classifier model,
    resulting in a confusion matrix. The test can be done
    on targets_labels different from the targets_labels used for training
    the model.
        Parameters
        ----------
        clf: RandomForestClassifier
            the trained model.
        test_dataset:  pandas Dataframe.
            Dataframe containing the data used for testing the
            model. The rows are the entries, and the columns are
            the features on which the model has been trained.
            The last column is 'status' containing the labels
            of the targets_labels for each entry.
        training_targets: tuple of str
            the targets on which the model has been trained.
        **kwargs: keyword arguments
            savepath: str, optional, default: ""
                If not empty, path where le result will be saved.
            verbose: Bool, optional. Default: False
                Whether to display more information when computing
                or not.
            show: Bool, optional. Default: True
                Whether to show the resulting confusion matrix or not.
            iterations: int, optional. Default: 10
                Number of iterations the test will be computed.
            commentary: str, optional. Default: ""
                If any specification to add to the file name.
            testing_targets: tuple of str
                the targets on which the model will be tested.
                Can be different from the training targets.
            mode: ['numeric', 'percent'], default 'numeric'
    """
    options = {"verbose": False, "show": True,
               "testing_targets": (),
               "iterations": 10,
               "commentary": "", "savepath": "", "title": ""}
    options.update(**kwargs)
    if not options["testing_targets"]:
        options["testing_targets"] = training_targets
    TRAIN_CORRESPONDENCE = {}
    TEST_CORRESPONDENCE = {}
    train_target_id = 0
    test_target_id = 0
    for t in training_targets:
        if t not in TRAIN_CORRESPONDENCE:
            TRAIN_CORRESPONDENCE[t] = train_target_id
            train_target_id += 1
    for t in options["testing_targets"]:
        if t not in TEST_CORRESPONDENCE:
            TEST_CORRESPONDENCE[t] = test_target_id
            test_target_id += 1
    
    if not TEST_CORRESPONDENCE:
        TEST_CORRESPONDENCE = TRAIN_CORRESPONDENCE.copy()
    
    X = test_dataset.loc[:, ~test_dataset.columns.isin(['label', 'ID'])]
    y = test_dataset["label"]
    
    X.reset_index(drop=True, inplace=True)
    
    if options["verbose"]:
        progress = 0
        sys.stdout.write(f"\rTesting model: {progress}%")
        sys.stdout.flush()
    
    # get predictions and probabilities
    all_matrices = []
    all_probability_matrices = []
    for iters in range(options["iterations"]):
        matrix = np.zeros((len(training_targets), len(options['testing_targets'])))
        probabilities_matrix = np.empty((len(training_targets), len(options['testing_targets'])), dtype=object)
        
        # Initializing the matrix containing the probabilities
        for i in range(len(probabilities_matrix)):
            for j in range(len(probabilities_matrix[i])):
                probabilities_matrix[i][j] = []
        
        # Making predictions and storing the results in predictions[]
        predictions = []
        for i in range(len(X.values)):
            row = X.iloc[i]
            y_pred = clf.predict([row])[0]
            proba_class = clf.predict_proba([row])[0]
            predictions.append((y_pred, proba_class))
        
        #
        targets = []
        for i in y.index:
            targets.append(y.loc[i])
        # Building the confusion matrix
        for i in range(len(targets)):
            y_true = targets[i]
            y_pred = predictions[i][0]
            y_proba = max(predictions[i][1])
            matrix[TRAIN_CORRESPONDENCE[y_pred]][TEST_CORRESPONDENCE[y_true]] += 1
            
            probabilities_matrix[TRAIN_CORRESPONDENCE[y_pred]][TEST_CORRESPONDENCE[y_true]].append(y_proba)
        mean_probabilities = np.zeros((len(training_targets), len(options['testing_targets'])))
        for i in range(len(probabilities_matrix)):
            for j in range(len(probabilities_matrix[i])):
                mean_probabilities[i][j] = np.mean(probabilities_matrix[i][j])
        all_matrices.append(matrix)
        all_probability_matrices.append(mean_probabilities)
    
    mean_probabilities_matrix = np.empty((len(training_targets), len(options['testing_targets'])))
    overall_matrix = np.mean(np.array([i for i in all_matrices]), axis=0)
    overall_probabilities = np.mean(np.array([i for i in all_probability_matrices]), axis=0)
    
    accuracies = np.empty((len(training_targets), len(options['testing_targets']))).tolist()
    cups = np.empty((len(training_targets), len(options['testing_targets']))).tolist()
    
    # averaging the probabilities
    for i in range(len(overall_probabilities)):
        for j in range(len(overall_probabilities[i])):
            mean_probabilities_matrix[i][j] = np.mean(overall_probabilities[i][j])
    
    # mixing count and probabilities for displaying
    if options['mode'] == 'numeric':
        for i in range(len(overall_probabilities)):
            for j in range(len(overall_probabilities[i])):
                np.nan_to_num(overall_matrix[i][j])
                np.nan_to_num(mean_probabilities_matrix[i][j])
                CUP = round(mean_probabilities_matrix[i][j], 3) if int(overall_matrix[i][j]) != 0 else 0
                accuracies[i][j] = int(overall_matrix[i][j])
                cups[i][j] = CUP
    elif options['mode'] == 'percent':
        total_per_column = np.sum(overall_matrix, axis=0)
        
        for i in range(len(overall_probabilities)):
            for j in range(len(overall_probabilities[i])):
                np.nan_to_num(overall_matrix[i][j])
                np.nan_to_num(mean_probabilities_matrix[i][j])
                percent = round(int(overall_matrix[i][j]) / total_per_column[j] * 100, 1) if int(
                    overall_matrix[i][j]) != 0 else "0"
                CUP = round(mean_probabilities_matrix[i][j], 3) if int(overall_matrix[i][j]) != 0 else 0
                overall_matrix[i][j] = percent
                
                accuracies[i][j] = percent
                cups[i][j] = CUP
    
    columns = [x for x in TEST_CORRESPONDENCE.keys()]
    indexes = [x for x in TRAIN_CORRESPONDENCE.keys()]
    df_acc = pd.DataFrame(columns=columns, index=indexes, data=accuracies)
    df_cup = pd.DataFrame(columns=columns, index=indexes, data=cups)
    df_acc.index.name = "Train label"
    df_cup.index.name = "Train label"
    if return_data:
        return df_acc, df_cup, TRAIN_CORRESPONDENCE, TEST_CORRESPONDENCE
        # return overall_matrix, mixed_labels_matrix, TRAIN_CORRESPONDENCE, TEST_CORRESPONDENCE
    
    mixed_labels_matrix = np.empty((len(TRAIN_CORRESPONDENCE.keys()), len(TEST_CORRESPONDENCE.keys()))).tolist()
    
    acc_array = df_acc.to_numpy().astype(float) if options["mode"] == 'percent' else df_acc.to_numpy().astype(
        int)
    cup_array = df_cup.to_numpy()
    for r in range(len(acc_array)):
        for c in range(len(acc_array[0])):
            case = f"{acc_array[r][c]}%\nCUP={cup_array[r][c]}" if options[
                                                                       "mode"] == 'percent' else f"{acc_array[r][c]}\nCUP={cup_array[r][c]}"
            mixed_labels_matrix[r][c] = case
    plt.close()
    
    # plotting
    fig, ax = plt.subplots(1, 1, figsize=(7 / 4 * len(options['testing_targets']), 6 / 4 * len(training_targets)))
    
    fig.suptitle("")
    sns.heatmap(ax=ax, data=acc_array, annot=mixed_labels_matrix, fmt='', cmap="Blues", square=True, )
    ax.xaxis.tick_top()
    ax.xaxis.set_label_position('top')
    ax.set_ylabel("The input is classified as")
    ax.set_xlabel("The test input is")
    ax.set_xticks([TEST_CORRESPONDENCE[x] + 0.5 for x in options['testing_targets']], options['testing_targets'])
    ax.set_yticks([TRAIN_CORRESPONDENCE[x] + 0.5 for x in training_targets], training_targets)
    plt.tight_layout()
    
    if options['savepath']:
        plt.savefig(os.path.join(options['savepath'], options["title"] + ".png"))
    if options['show']:
        plt.show()
    plt.close()


def test_sequential_by_confusion(model_path, dataset, training_targets, **kwargs):
    """
    Test an already trained keras Sequential model,
    resulting in a confusion matrix. The test can be done
    on targets_labels different from the targets_labels used for training
    the model.
        Parameters
        ----------
        model_path: str
            the absolute path to the trained model, with extension (to open).
        dataset:  list of lists, shape (n, (2, (ndarray(m,m)))
            list of n pictures of size m*m, coupled with its
            int-like label.
        training_targets: list of int
            the targets on which the model has been trained.
        **kwargs: keyword arguments
            savepath: str, optional, default: ""
                If not empty, path where le result will be saved.
            verbose: Bool, optional. Default: False
                Whether to display more information when computing
                or not.
            show: Bool, optional. Default: True
                Whether to show the resulting confusion matrix or not.
            iterations: int, optional. Default: 10
                Number of iterations the test will be computed.
            commentary: str, optional. Default: ""
                If any specification to add to the file name.
            testing_targets: list of int
                the targets on which the model will be tested.
                Can be different from the training targets.
            target_rename: dict, optional, default: {}
                the keys are the actual targets, the values are
                how you want to rename them on the confusion matrix.
    """
    model = load_model(model_path)
    options = {"verbose": False, "show": True,
               "testing_targets": (),
               "iterations": 10,
               "commentary": "",
               "savepath": "",
               "title": "",
               "target_rename": ""}
    options.update(**kwargs)
    if not options["testing_targets"]:
        options["testing_targets"] = training_targets
    CORRESPONDENCE = {}
    target_id = 0
    for t in training_targets:
        if t not in CORRESPONDENCE:
            CORRESPONDENCE[t] = target_id
            target_id += 1
    for t in options["testing_targets"]:
        if t not in CORRESPONDENCE:
            CORRESPONDENCE[t] = target_id
            target_id += 1
    x_train, x_val, y_train, y_val = train_test_split(dataset, train_size=0.1)
    
    x_val = np.array(x_val)
    y_val = np.array(y_val)
    
    # get predictions and probabilities
    all_matrices = []
    all_probability_matrices = []
    for iters in range(options["iterations"]):
        matrix = np.zeros((len(training_targets), len(options['testing_targets'])))
        probabilities_matrix = np.empty((len(training_targets), len(options['testing_targets'])), dtype=object)
        
        # Initializing the matrix containing the probabilities
        for i in range(len(probabilities_matrix)):
            for j in range(len(probabilities_matrix[i])):
                probabilities_matrix[i][j] = []
        
        # Making predictions and storing the results in predictions[]
        predictions = []
        for x in x_val:
            y_pred = model.predict(x[None, ...])[0]
            predictions.append((np.where(y_pred == max(y_pred))[0][0], list(y_pred)))
        
        targets = []
        for i in y_val:
            targets.append(np.where(i == max(i))[0][0])
        # Building the confusion matrix
        
        for i in range(len(targets)):
            y_true = targets[i]
            y_pred = predictions[i][0]
            y_proba = max(predictions[i][1])
            
            matrix[CORRESPONDENCE[y_pred]][CORRESPONDENCE[y_true]] += 1
            
            probabilities_matrix[CORRESPONDENCE[y_pred]][CORRESPONDENCE[y_true]].append(y_proba)
        mean_probabilities = np.zeros((len(training_targets), len(options['testing_targets'])))
        for i in range(len(probabilities_matrix)):
            for j in range(len(probabilities_matrix[i])):
                mean_probabilities[i][j] = np.mean(probabilities_matrix[i][j])
        all_matrices.append(matrix)
        all_probability_matrices.append(mean_probabilities)
    
    mixed_labels_matrix = np.empty((len(training_targets), len(options['testing_targets']))).tolist()
    mean_probabilities_matrix = np.empty((len(training_targets), len(options['testing_targets'])))
    overall_matrix = np.mean(np.array([i for i in all_matrices]), axis=0)
    overall_probabilities = np.mean(np.array([i for i in all_probability_matrices]), axis=0)
    
    # averaging the probabilities
    for i in range(len(overall_probabilities)):
        for j in range(len(overall_probabilities[i])):
            mean_probabilities_matrix[i][j] = np.mean(overall_probabilities[i][j])
    
    # mixing count and probabilities for displaying
    for i in range(len(overall_probabilities)):
        for j in range(len(overall_probabilities[i])):
            np.nan_to_num(overall_matrix[i][j])
            np.nan_to_num(mean_probabilities_matrix[i][j])
            mixed_labels_matrix[i][j] = str(int(overall_matrix[i][j])) + "\nCUP=" + str(
                round(mean_probabilities_matrix[i][j], 3))
    
    # plotting
    fig, ax = plt.subplots(1, 1, figsize=(7 / 4 * len(options['testing_targets']), 6 / 4 * len(training_targets)))
    
    fig.suptitle("")
    sns.heatmap(ax=ax, data=overall_matrix, annot=mixed_labels_matrix, fmt='', cmap="Blues")
    ax.xaxis.tick_top()
    ax.xaxis.set_label_position('top')
    ax.set_ylabel("The input is classified as")
    ax.set_xlabel("The input is")
    
    ax.set_xticks([CORRESPONDENCE[x] + 0.5 for x in options['testing_targets']],
                  [options["target_rename"][x] for x in options['testing_targets']])
    ax.set_yticks([CORRESPONDENCE[x] + 0.5 for x in training_targets],
                  [options["target_rename"][x] for x in training_targets])
    plt.tight_layout()
    
    if options['savepath']:
        plt.savefig(os.path.join(options['savepath'], options["title"] + ".png"))
    if options['show']:
        plt.show()
    plt.close()


def model_history_plot(history_path, savepath=""):
    """
    Save in a fancy way the history logs of a
    trained keras model, saved in the form of a
    csv file.

        Parameters
        ----------
        history_path: str
            the absolute path to the .log file,
            containing the history in csv format.
        savepath: str, optional, default: ""
            If not empty, the directory where the plot will be saved.
            If empty, the plot is shown.
    """
    data = pd.read_csv(history_path, index_col=False)
    plt.figure(figsize=(6, 5))
    plt.plot(data["accuracy"], linestyle="dashed", color="blue", label="training accuracy")
    plt.plot(data["val_accuracy"], linestyle="solid", color="blue", label="validation accuracy")
    plt.plot(data["loss"], linestyle="dashed", color="red", label="training loss")
    plt.plot(data["val_loss"], linestyle="solid", color="red", label="training loss")
    
    plt.xlabel("epochs", fontsize=15)
    plt.ylabel("score", fontsize=15)
    plt.xticks(fontsize=13)
    plt.yticks(fontsize=13)
    plt.legend(fontsize=13)
    title = "history " + os.path.basename(history_path).replace("history", "").split(".")[0] + ".png"
    if savepath:
        plt.savefig(os.path.join(savepath, title))
    else:
        plt.show()
    plt.close()


def split_train_test_deprecated(data, train_size: float = 0.7):
    """
    Split a dataset into train and validation sets for features and labels.

        Parameters
        ----------
        data: ndarray, shape((n, 2), m)
            The numpy array containing the data.
            Each entry is coupled within a tuple with its
            corresponding label
        train_size: float, optional, default: 0.7
            The proportion, between 0 and 1, that the train
            set will take on the whole dataset.

        Returns
        -------
        out: tuple of length 4
            The first element is the train set for features.
            The second is the validation set for features.
            The third is the train set for the labels.
            The fourth is the validation set for labels.
    """
    img_size = 224
    train = data[:int(len(data) * train_size)]
    val = data[int(len(data) * train_size):]
    
    x_train = []
    y_train = []
    x_val = []
    y_val = []
    
    for feature, label in train:
        x_train.append(feature)
        y_train.append(label)
    
    for feature, label in val:
        x_val.append(feature)
        y_val.append(label)
    
    x_train = np.array(x_train) / 255
    x_val = np.array(x_val) / 255
    
    x_train.reshape(-1, img_size, img_size, 1)
    y_train = np.array(y_train)
    
    x_val.reshape(-1, img_size, img_size, 1)
    y_val = np.array(y_val)
    
    y_train = to_categorical(y_train, 2)
    y_val = to_categorical(y_val, 2)
    return x_train, x_val, y_train, y_val

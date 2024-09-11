import numpy as np

from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
import ml_insights as mli
from venn_abers import VennAbers

n_features = 10
rand_seed = 7
n_samples = 100000

X, y = make_classification(
    n_classes=3,
    n_samples=n_samples,
    n_clusters_per_class=2,
    n_features=n_features,
    n_informative=int(n_features / 2),
    n_redundant=int(n_features / 4),
    random_state=rand_seed)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=rand_seed)

clf = RandomForestClassifier(random_state=0)
clf = GaussianNB()

X_train_proper, X_cal, y_train_proper, y_cal = train_test_split(
    X_train, y_train, test_size=0.2, shuffle=False
)

clf.fit(X_train_proper, y_train_proper)
p_cal = clf.predict_proba(X_cal)
p_test = clf.predict_proba(X_test)


va = VennAbers()
# va = VennAbersCalibrator(clf)
# va.fit(X_train_proper, y_train_proper)
# p = va.predict_proba(p_test)

va.fit(p_cal=p_cal, y_cal=y_cal)
p, probs = va.predict_proba(p_test)
print()

mli.plot_reliability_diagram(y_test, np.array(p[:,1]),marker_color='k',marker_edge_color='k', ci_ref='point')
mli.plot_reliability_diagram(y_test, p_test[:,1],marker_color='r', marker_edge_color='r', ci_ref='point')
print()
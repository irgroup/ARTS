from scipy import stats
import numpy as np
import glob
import re
from sklearn import preprocessing
import rbo
from sklearn.metrics import cohen_kappa_score
import krippendorff
from statsmodels.stats.inter_rater import fleiss_kappa, aggregate_raters

class Text:
    def __init__(self, t_id, text):
        self.rating = 1200
        self.num_matches = 0
        self.t_id = t_id
        self.text = text
        
    def set_rating(self, rating):
        self.rating = rating
    
    def get_rating(self):
        return self.rating

    def increment_num_matches(self):
        self.num_matches +=1
    
    def get_num_matches(self):
        return self.num_matches

    def get_t_id(self):
        return self.t_id

    def get_text(self):
        return self.text

    def __str__(self):
        return f"ID:\t{self.t_id} \n RATING:\t{self.rating}\n MATCHES:\t{self.num_matches}\n TEXT:\t {self.text}"


def _exspected_score(rating_1, rating_2):
    e_1 = 1 / (1 + 10**((rating_2-rating_1)/400))
    return e_1

def _update_score(rating, s, e, k=32):
    rating_p = rating + k*(s-e)
    return rating_p

def handle_scores(t1, t2):
    #t1 is expected to be the winner

    t1.increment_num_matches()
    t2.increment_num_matches()

    e1 = _exspected_score(t1.get_rating(), t2.get_rating())
    e2 = 1-e1

    t1.set_rating(_update_score(t1.get_rating(), 1, e1))
    t2.set_rating(_update_score(t2.get_rating(), 0, e2))

def apply_history(history, texts):

    for key, val in history.items():
        cands = val[0]
        winner = val[1]
        loser = sum(cands)-winner
        
        handle_scores(texts[winner], texts[loser])

#based on history
def calc_percentage_agreement(hist_a, hist_b):
    assert len(hist_a) == len(hist_b)

    total_agree = 0

    for i in range(len(hist_a)):
        judgment_a = hist_a[i][1]
        judgment_b = hist_b[i][1]

        if judgment_a == judgment_b:
            total_agree += 1

    return total_agree/len(hist_a)

#based on history
def calc_cohen_kappa_old(hist_a, hist_b):
    dec_a = []
    dec_b = []

    for key in hist_a.keys():
        dec_a.append(hist_a[key][1])
        dec_b.append(hist_b[key][1])
    
    return cohen_kappa_score(dec_a, dec_b)

def calc_cohen_kappa(hist_a, hist_b):
    dec_a = []
    dec_b = []

    for key in hist_a.keys():
        dec_a.append(hist_a[key][0].index(hist_a[key][1]))
        dec_b.append(hist_b[key][0].index(hist_b[key][1]))
    
    return cohen_kappa_score(dec_a, dec_b)

#def calc_cohens_kappa(hist_a, hist_b, verbose=False):
    #k = (p_0 - p_e) / (1 - p_e)
    #
    #0 = agreement equivalent to chance.
    #0.1 – 0.20 = slight agreement.
    #0.21 – 0.40 = fair agreement.
    #0.41 – 0.60 = moderate agreement.
    #0.61 – 0.80 = substantial agreement.
    #0.81 – 0.99 = near perfect agreement
    #1 = perfect agreement.

    '''p_0 = calc_percentage_agreement(hist_a, hist_b)

    prob_a_a = sum([1 for k, entry in hist_a.items() if entry[1] == entry[0][0]])/len(hist_a)
    prob_a_b = sum([1 for k, entry in hist_a.items() if entry[1] == entry[0][1]])/len(hist_a)

    prob_b_a = sum([1 for k, entry in hist_b.items() if entry[1] == entry[0][0]])/len(hist_b)
    prob_b_b = sum([1 for k, entry in hist_b.items() if entry[1] == entry[0][1]])/len(hist_b)

    p_e = prob_a_a*prob_a_b + prob_b_a*prob_b_b

    k = (p_0 - p_e) / (1 - p_e)
    
    if verbose:
        print()
        print(f"p_0={p_0}")
        print(f"p_e={p_e}")
        print()
        print(f"prob_a_a={prob_a_a}")
        print(f"prob_a_b={prob_a_b}")
        print(f"prob_b_a={prob_b_a}")
        print(f"prob_b_b={prob_b_b}")
        print()

    return k'''

#based on rank
def calc_rank_correlation(texts_a, texts_b):
    assert len(texts_a) == len(texts_b)

    scores_a = []
    scores_b = []

   
    #we need to ensure correct order
    for i in range(len(texts_a)):
        scores_a.append(texts_a[i].get_rating())
        scores_b.append(texts_b[i].get_rating())

    res = stats.spearmanr(scores_a, scores_b)

    stat = np.round(res.statistic, 5)
    p_val = np.round(res.pvalue, 5)
    return stat, p_val

#based on rank
def calc_rbo(texts_a, texts_b, rev=False):
    t1_ratings = np.argsort([texts_a[i].get_rating() for i in texts_a.keys()])
    t2_ratings = np.argsort([texts_b[i].get_rating() for i in texts_b.keys()])
    if rev:
        t1_ratings = np.flip(t1_ratings)
        t2_ratings = np.flip(t2_ratings)

    return rbo.RankingSimilarity(t2_ratings, t1_ratings).rbo()

#based on score
def calc_kendallstau(texts_a, texts_b):
    t1_ratings = [texts_a[i].get_rating() for i in texts_a.keys()]
    t2_ratings = [texts_b[i].get_rating() for i in texts_b.keys()]

    tau, p_val = stats.kendalltau(t1_ratings, t2_ratings)
    tau = np.round(tau, 5)
    p_val = np.round(p_val, 5)
    
    return tau, p_val


def get_all_users(root_path = "/workspace/Histories/*history*"):
    users = [re.search(r'/([^/]+)_history\.pkl$', path).group(1) for path in glob.glob(root_path)]
    return users

def apply_ranking_to_scores(ranking, texts):
    score_diff = 1/len(ranking)
    for _, text in texts.items():
        if text.get_t_id() in ranking:
            t_score = ranking.index(text.get_t_id()) * score_diff
        else:
            #if ranking doesn't contain the id, fill with avg dummy
            t_score = 0.5
        text.set_rating(t_score)


def apply_scores(history, texts):
    for text in texts.items():
        for _, text in texts.items():
            text.set_rating(history[text.get_t_id()][1])

def scale_scores(texts, return_new_texts = False, data=None):
    elo_scores = np.array([texts[key].get_rating() for key in sorted(texts.keys())]).reshape(-1, 1)
    scaler = preprocessing.MinMaxScaler()
    d = scaler.fit_transform(elo_scores)
    scaled_scores = np.round(d, 5).squeeze().tolist()

    scaled_res = {i: (scaled_scores[i], texts[i].get_text()) for i in sorted(texts.keys())}
    
    if return_new_texts:
        scaled_score_texts = {t_id : Text(t_id, text[0]) for t_id, text in data.iterrows()}
        for key, val in scaled_res.items():
            scaled_score_texts[key].set_rating(val[0])

        return scaled_res, scaled_score_texts

    return scaled_res

def scale_ranked_scores(texts, return_new_texts = False, data=None):
    simp_pos = np.argsort(np.array([texts[key].get_rating() for key in sorted(texts.keys())]))

    equis = np.round(np.linspace(0, 1, len(simp_pos)), 5)
    scaled_res = dict(sorted({key: (val, texts[key].get_text()) for key, val in dict(zip(simp_pos, equis)).items()}.items()))

    if return_new_texts:
        scaled_score_texts = {t_id : Text(t_id, text[0]) for t_id, text in data.iterrows()}
        for key, val in scaled_res.items():
            scaled_score_texts[key].set_rating(val[0])

        return scaled_res, scaled_score_texts

    return scaled_res


def calc_cat_mat(histories, determined_pairs):
    rat_mat = np.array([[histories[user][key][1] for key in sorted(histories[user].keys())] for user in sorted(histories.keys())])
    rat_mat = np.array([[determined_pairs[i].index(rat_mat.T[i][j]) for j in range(len(rat_mat.T[i]))] for i in range(len(determined_pairs))])

    cat_mat = aggregate_raters(rat_mat)[0]
    return cat_mat


def calc_fleiss_kappa(histories, determined_pairs):
    return fleiss_kappa(calc_cat_mat(histories, determined_pairs))

def calc_krippendorfs_alpha(histories, determined_pairs):
    return krippendorff.alpha(value_counts = calc_cat_mat(histories, determined_pairs), level_of_measurement="nominal")
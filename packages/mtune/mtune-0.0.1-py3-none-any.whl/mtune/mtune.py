import numpy as np
import pandas as pd

class mtune:
    def __init__(self, base_model, method='ensemble', n_ensemble=11, random_state=None):
        self.base_model = base_model
        self.method = method
        self.n_ensemble = n_ensemble
        self.threshold = None
        self.majority_class = None
        self.minority_class = None
        self.merged_data = None
        self.random_state = None
        self.thres_to_model_mapping = dict()

    def fit(self, X, y, verbose='off'):
        class_col_name = y.name
        val_counts = y.value_counts()

        self.majority_class = (val_counts.idxmax(), val_counts.max())
        self.minority_class = (val_counts.idxmin(), val_counts.min())  

        if self.method == 'direct':
            self.base_model.fit(X, y)
            pred_prob = self.base_model.predict_proba(X)
            pred_prob_minority = pred_prob[:, self.minority_class[0]]
            mean_value = np.mean(pred_prob_minority)
            self.threshold = mean_value
            
            if verbose == 'on':
                print('method =', self.method)
                print('threshold :', mean_value)
        
        elif self.method == 'ensemble':
            print('method =', self.method)
            merged_data_df = pd.concat([X, y], axis=1)
            majority_class_df = merged_data_df[merged_data_df[class_col_name] == self.majority_class[0]]
            minority_class_df = merged_data_df[merged_data_df[class_col_name] == self.minority_class[0]]
            n_subsets = self.n_ensemble
            majority_class_df_split = np.array_split(majority_class_df, n_subsets)
            for i, majority_class_subset in enumerate(majority_class_df_split, 1):
                paired_dataset = pd.concat([majority_class_subset, minority_class_df], axis=0)
                paired_dataset = paired_dataset.sample(frac=1, random_state=self.random_state)
                X_train = paired_dataset.drop(class_col_name, axis=1)
                y_train = paired_dataset[class_col_name]
                self.base_model.fit(X_train, y_train)
                pred_prob = self.base_model.predict_proba(X_train)
                pred_prob_minority = pred_prob[:, self.minority_class[0]]
                mean_value = np.mean(pred_prob_minority)
                self.thres_to_model_mapping[mean_value] = self.base_model
            
        else:
            print('Choose a valid method')
            pass

    def predict(self, X):
        if self.method == 'direct':
            pred_prob_minority = self.base_model.predict_proba(X)[:, self.minority_class[0]].tolist()
            y_pred = [self.minority_class[0] if p >= self.threshold else self.majority_class[0] for p in pred_prob_minority]
            return y_pred

        elif self.method == 'ensemble':
            pred_df = pd.DataFrame() 
            for threshold, model in self.thres_to_model_mapping.items():
                pred_prob = model.predict_proba(X)
                pred_prob_minority = pred_prob[:, self.minority_class[0]].tolist()
                y_pred = [self.minority_class[0] if p >= threshold else self.majority_class[0] for p in pred_prob_minority]
                pred_df[str(threshold) + '_pred_label'] = y_pred

            columns_to_check = [c for c in list(pred_df.columns) if 'pred_label' in c]
            pred_df['Final Prediction'] = pred_df[columns_to_check].apply(
                lambda row: self.minority_class[0] if (row == self.minority_class[0]).sum() > (row == self.majority_class[0]).sum()
                else self.majority_class[0], axis=1)
            output = pred_df['Final Prediction']
            output.name = None
            return output

        else:
            print('Please pass either "ensemble" or "direct" in "method" parameter ')
            pass

    def predict_proba(self, X):
        if self.method == 'direct':
            pred_probs = self.base_model.predict_proba(X)
            return pred_probs
        elif self.method == 'ensemble':
            pred_df = pd.DataFrame() 
            for threshold, model in self.thres_to_model_mapping.items():
                pred_prob = model.predict_proba(X)
                pred_prob_minority = pred_prob[:, self.minority_class[0]].tolist()
                pred_prob_majority = pred_prob[:, self.majority_class[0]].tolist()
                pred_df[str(threshold) + '_pred_prob_minority'] = pred_prob_minority
                pred_df[str(threshold) + '_pred_prob_majority'] = pred_prob_majority

            if self.minority_class[0] < self.majority_class[0]:
                columns_to_check = [c for c in list(pred_df.columns) if '_pred_prob_minority' in c]
                pred_df['Final_Pred_Prob_minority'] = pred_df[columns_to_check].mean(axis=1)
                columns_to_check = [c for c in list(pred_df.columns) if '_pred_prob_majority' in c]
                pred_df['Final_Pred_Prob_majority'] = pred_df[columns_to_check].mean(axis=1) 
                return pred_df[['Final_Pred_Prob_minority', 'Final_Pred_Prob_majority']].to_numpy()
            else:
                columns_to_check = [c for c in list(pred_df.columns) if '_pred_prob_majority' in c]
                pred_df['Final_Pred_Prob_majority'] = pred_df[columns_to_check].mean(axis=1)
                columns_to_check = [c for c in list(pred_df.columns) if '_pred_prob_minority' in c]
                pred_df['Final_Pred_Prob_minority'] = pred_df[columns_to_check].mean(axis=1)
                return pred_df[['Final_Pred_Prob_majority', 'Final_Pred_Prob_minority']].to_numpy()
        else:
            print('Please pass either "ensemble" or "direct" in "method" parameter ')
            pass

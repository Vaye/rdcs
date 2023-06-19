
from sklearn.cluster import DBSCAN
import pandas as pd
    
class Clustor():
    def __init__(self, eps, min_samples) -> None:
        self.eps = eps
        self.min_samples = min_samples

    def clustering(self, df_clean, df_cl, ne_list):
        merged_df = pd.DataFrame()

        xcode_dict = dict()
        label_dict = dict()
        anomaly_time_dict = dict()

        for ne in ne_list:
            ne_xcode_df = df_cl[df_cl['ne']==ne].reset_index(drop=True)
            ne_kpi_df = df_clean[df_clean['neName']==ne].reset_index(drop=True)
            
            ne_xcode_data = ne_xcode_df[['x0','x1','x2']].values
            db = DBSCAN(eps = self.eps, min_samples = self.min_samples).fit(ne_xcode_data)
            ne_labels = db.labels_
            ne_anomaly_index_list = [i for i,l in enumerate(ne_labels) if l<0]
            ne_anomaly_time_list = ne_kpi_df['time'][ne_anomaly_index_list].values.tolist()
            
            xcode_dict[ne] = ne_xcode_df
            label_dict[ne] = ne_labels
            anomaly_time_dict[ne] = ne_anomaly_time_list
            
            anomaly_rows = ne_kpi_df.iloc[ne_anomaly_index_list]
            merged_df = merged_df.append(anomaly_rows, ignore_index=True)
    
        return merged_df, xcode_dict, label_dict, anomaly_time_dict

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import io

class DataVisualizer:
    def __init__(self, xcode_dict, label_dict):
        """Initialize the DataVisualizer with xcode_dict and label_dict"""
        self.xcode_dict = xcode_dict
        self.label_dict = label_dict

    def _plot(self, data, labels, title=None, angle=(30,30)):
        """Plot the data with labels and return the Figure object"""
        unique_labels = set(labels)
        colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))

        fig, ax = plt.subplots(1, 1, subplot_kw={'projection': '3d'}, figsize=(20, 20))

        for k, col in zip(unique_labels, colors):
            if k == -1:
                # Black used for noise.
                col = [0, 0, 1, 1]
                m='x'
            else:
                m='.'
    
            class_member_mask = (labels == k)
            xy = data[class_member_mask]
            ax.scatter(xy[:,0], xy[:,1], xy[:,2], c=col,marker=m)
    
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")
        ax.view_init(*angle)
        if title:
            plt.title(title, fontsize=20)
        # plt.show() # test code

        return fig

    def plot_and_get(self, ne, xcode_df):
        """Plot the data for ne and return the BytesIO object of the image"""
        if ne not in self.xcode_dict or ne not in self.label_dict:
            return None

        # xcode_df = self.xcode_dict[ne]
        data = xcode_df[['x0','x1','x2']].values
        labels = self.label_dict[ne]

        if np.any(labels != 0):
            fig = self._plot(data, labels, title=ne, angle=(30,330))
            output = io.BytesIO()
            FigureCanvas(fig).print_png(output)
            return output
        else:
            print(f"{ne} is normal")
            return None
        
    def plot_and_show(self, ne, xcode_df):
        """Plot the data for ne and return the BytesIO object of the image"""
        if ne not in self.xcode_dict or ne not in self.label_dict:
            return None

        # xcode_df = self.xcode_dict[ne]
        data = xcode_df[['x0','x1','x2']].values
        labels = self.label_dict[ne]

        if np.any(labels != 0):
            fig = self._plot(data, labels, title=ne, angle=(30,330))
            plt.show()
        else:
            print(f"{ne} is normal")
            return None
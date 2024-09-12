import os
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
from kevin_toolbox.patches.for_os.path import replace_illegal_chars


def plot_confusion_matrix(data_s, title, gt_name, pd_name, label_to_value_s=None, output_dir=None, **kwargs):
    paras = {
        "dpi": 200,
        "normalize": None,  # "true", "pred", "all",
        "b_return_cfm": False,  # 是否输出混淆矩阵
    }
    paras.update(kwargs)

    value_set = set(data_s[gt_name]).union(set(data_s[pd_name]))
    if label_to_value_s is None:
        label_to_value_s = dict()
    for i in value_set.difference(set(label_to_value_s.values())):
        label_to_value_s[f'{i}'] = i

    assert set(label_to_value_s.values()).issuperset(value_set)
    # 计算混淆矩阵
    cfm = confusion_matrix(y_true=data_s[gt_name], y_pred=data_s[pd_name], labels=list(label_to_value_s.values()),
                           normalize=paras["normalize"])
    # 绘制混淆矩阵热力图
    plt.clf()
    plt.figure(figsize=(8, 6))
    sns.heatmap(cfm, annot=True, fmt='.2%' if paras["normalize"] is not None else 'd',
                xticklabels=list(label_to_value_s.keys()), yticklabels=list(label_to_value_s.keys()),
                cmap='viridis')

    plt.xlabel(f'{pd_name}')
    plt.ylabel(f'{gt_name}')
    plt.title(f'{title}')

    if output_dir is None:
        plt.show()
        output_path = None
    else:
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, f'{replace_illegal_chars(title)}.png')
        plt.savefig(output_path, dpi=paras["dpi"])

    if paras["b_return_cfm"]:
        return output_path, cfm
    else:
        return output_path


if __name__ == '__main__':
    import numpy as np

    # 示例真实标签和预测标签
    y_true = np.array([0, 1, 2, 0, 1, 2, 0, 1, 2, 5])
    y_pred = np.array([0, 2, 1, 0, 2, 1, 0, 1, 1, 5])

    plot_confusion_matrix(data_s={'a': y_true, 'b': y_pred},
                          title='test', gt_name='a', pd_name='b',
                          label_to_value_s={"A": 5, "B": 0, "C": 1, "D": 2},
                          # output_dir=os.path.join(os.path.dirname(__file__), "temp"),
                          normalize="true")

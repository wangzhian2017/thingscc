# 引入python库
import os
import mne
from mne.datasets import sample
import matplotlib.pyplot as plt

def show_nobad_10_20(raw):
    """
    案例：
    获取10-20秒内的良好的MEG数据
    # 根据type来选择 那些良好的MEG信号(良好的MEG信号，通过设置exclude="bads") channel,
    结果为 channels所对应的的索引
    """
    picks = mne.pick_types(raw.info, meg=True, exclude='bads')
    t_idx = raw.time_as_index([10., 20.])
    data, times = raw[picks, t_idx[0]:t_idx[1]]
    plt.plot(times,data.T)
    plt.title("Sample channels")

def show_plot_psd(raw):
    """
    绘制各通道的功率谱密度
    """
    raw.plot_psd()
    plt.show()

def show_plot_psd_topo(raw):
    """
    绘制通道频谱图作为topography
    """
    raw.plot_psd_topo()
    plt.show()

def show_plot_sensors(raw):
    """
    绘制电极位置
    """
    raw.plot_sensors()
    plt.show()

def main():
    # sample的存放地址
    data_path = sample.data_path()
    # 该fif文件存放地址
    fname =os.path.join(data_path, 'MEG', 'sample', 'sample_audvis_filt-0-40_raw.fif') #data_path + '/MEG/sample/sample_audvis_raw.fif'

    """
    如果上述给定的地址中存在该文件，则直接加载本地文件，
    如果不存在则在网上下载改数据
    """
    raw = mne.io.read_raw_fif(fname)
    print(raw)
    print(raw.info)


    # show_nobad_10_20(raw)
    # show_plot_psd(raw)
    # show_plot_psd_topo(raw)
    show_plot_sensors(raw)
    

    


if __name__ == '__main__':
    main()
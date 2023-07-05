import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
# epoch,acc,loss,val_acc,val_loss
from matplotlib import rcParams

x_axis_data = [1, 2, 3, 4, 5, 6, 7, 8, 9]
TD_3 =[16,12,3,3,3,3,3,3,3]
TD_4 =[22,12,16,4,4,4,4,4,4]
TD_6 =[28,21,16,19,21,6,6,6,6]
TD_8 =[34,27,25,19,21,24,26,8,8]
TD_9 =[40,33,25,28,21,24,26,28,9]
TD_10 =[40,33,31,28,21,24,26,28,30]

# y_axis_data1 = [68.72, 69.17, 69.26, 69.63, 69.35, 70.3, 66.8]
# y_axis_data2 = [71, 73, 52, 66, 74, 82, 71]
# y_axis_data3 = [82, 83, 82, 76, 84, 92, 81]
#############################TD#####################################
#导入数据（读者可忽略）
pre_lp=TD_3#组合模型
true=TD_4#真实值
pre_ph=TD_6#prophet
pre_lstm=TD_8#lstm
pre_ari=TD_9#arima
#设置中文字体
rcParams['font.sans-serif'] = 'kaiti'

# 生成一个时间序列 （读者可根据情况进行修改或删除）
time =pd.to_datetime(np.arange(0,21), unit='D',
                    origin=pd.Timestamp('2021-10-19'))
#创建画布
fig=plt.figure(figsize=(20,16))#figsize为画布大小
# 1
ax1=fig.add_subplot(221)
ax1.plot(time,pre_lp,color='#1bb9f6',marker='^',linestyle='-',label='1')
ax1.plot(time,true,color='#fd5749',marker='s',linestyle='-',label='true')
ax1.set_title('1',fontsize=15)#设置标题
ax1.set_xlabel('日期/天',fontsize=15)#设置横坐标名称
ax1.set_ylabel('感染人数/人',fontsize=15)#设置纵坐标名称
ax1.xaxis.set_major_formatter(mdate.DateFormatter('%m-%d'))#设置横坐标刻度（读者可忽略）
plt.xticks(pd.date_range(time[0],time[-1],freq='D'),rotation=45)#设置横坐标刻度（读者可忽略）

# 2
ax2=fig.add_subplot(222)
ax2.plot(time,pre_ph,color='#739b06',marker='o',linestyle='-',label='2')
ax2.plot(time,true,color='#fd5749',marker='s',linestyle='-',label='true')
ax2.set_title('2',fontsize=15)
ax2.set_xlabel('日期/天',fontsize=15)
ax2.set_ylabel('感染人数/人',fontsize=15)
ax2.xaxis.set_major_formatter(mdate.DateFormatter('%m-%d'))
plt.xticks(pd.date_range(time[0],time[-1],freq='D'),rotation=45)
# 3
ax3=fig.add_subplot(223)
ax3.plot(time,pre_lstm,color='#38d9a9',marker='*',linestyle='-',label='3')
ax3.plot(time,true,color='#fd5749',marker='s',linestyle='-',label='true')
ax3.set_title('3',fontsize=15)
ax3.set_xlabel('日期/天',fontsize=15)
ax3.set_ylabel('感染人数/人',fontsize=15)
ax3.xaxis.set_major_formatter(mdate.DateFormatter('%m-%d'))
plt.xticks(pd.date_range(time[0],time[-1],freq='D'),rotation=45)

# 4
ax4=fig.add_subplot(224)
ax4.plot(time,pre_ari,color='#e666ff',marker='x',linestyle='-',label='4')
ax4.plot(time,true,color='#fd5749',marker='s',linestyle='-',label='true')
ax4.set_title('4',fontsize=15)
ax4.set_xlabel('日期/天',fontsize=15)
ax4.set_ylabel('感染人数/人',fontsize=15)
ax4.xaxis.set_major_formatter(mdate.DateFormatter('%m-%d'))
plt.xticks(pd.date_range(time[0],time[-1],freq='D'),rotation=45)

#初始化labels和线型数组
# lines=[]
# labels=[]
#通过循环获取线型和labels
# for ax in fig.axes:
#  	 axLine, axLabel = ax.get_legend_handles_labels()
#    lines.extend(axLine)
#    labels.extend(axLabel)
#设置图例和调整图例位置
fig.legend(loc='lower center',
           ncol=5,framealpha=False,fontsize=25)



# 制作兼容 Python matplotlib库的气象、海洋绘图色标


## Dependencies

+ Python >= 3.5
+ numpy
+ matplotlib
+ jinja2


## Install

```
pip install geo_colormaps
```


## 色标使用方法

E.g.

```python

# 注意：须先 import geo_colormaps !!!
import geo_colormaps
from geo_colormaps import CMA_COLORMAPS

# prepare your data ...
XX, YY = ...
data = ...

# plot data
fig, ax = plt.subplots()
ax.pcolormesh(XX, YY, data,
              cmap=CMA_COLORMAPS.TEMP_CMAP.cmap,
              norm=CMA_COLORMAPS.TEMP_CMAP.norm,
              extend=CMA_COLORMAPS.TEMP_CMAP.extend)

# plot colorbar
cbar = CMA_COLORMAPS.TEMP_CMAP.plot_colorbar(ax, orientation='horizontal', spacing='uniform')
fig.show()
```

+ `orientation`: 色标方向，`'vertical'` (default) or `'horizontal'`
+ `spacing`: 色标中色块尺寸分布，`'uniform'` (default) or `'proportional'`


## 运行示例代码


```python

python examples/demo_sst_plot.py
```

其中， `examples/demo_sst_plot.py` 为本 repo 根目录下同名文件。


## 包含的默认色标

### 中国气象局《气象预报服务产品色标标准》色标实现

#### 参考文件

《中国气象局气象预报服务产品色标标准》（征求意见稿, 2009-11-23）。


#### 包含色标


| 色标描述                                              | 变量名                                 | 定义文件位置                                      | 示例图位置               |
| ---------------------------------                     | -------------------------------------- | -------------------------------------             | ------------------------ |
| 预报（警报）等级分布图配色表                          | `CMA_COLORMAPS.ALARM_LEVEL_CMAP`       | `colormap_defs/cma_colormaps/alarm_level.csv`     | `images/cma_colormaps/`  |
| 气象干旱等级分布图配色表                              | `CMA_COLORMAPS.DRAUGHT_LEVEL_CMAP`     | `colormap_defs/cma_colormaps/draught_level.csv`   | ~                        |
| 变温分布图配色表                                      | `CMA_COLORMAPS.DTEMP_CMAP`             | `colormap_defs/cma_colormaps/dtemp.csv`           | ~                        |
| 洪涝等级分布图配色表                                  | `CMA_COLORMAPS.FLOOD_LEVEL_CMAP`       | `colormap_defs/cma_colormaps/flood_level.csv`     | ~                        |
| 雾区分布图配色表                                      | `CMA_COLORMAPS.FOG_CMAP`               | `colormap_defs/cma_colormaps/fog.csv`             | ~                        |
| 降水量距平百分率分布图配色表                          | `CMA_COLORMAPS.PRE_ANO_CMAP`           | `colormap_defs/cma_colormaps/pre_ano.csv`         | ~                        |
| 降雨量等级分布图配色表                                | `CMA_COLORMAPS.PRE_LEVEL_CMAP`         | `colormap_defs/cma_colormaps/pre_level.csv`       | ~                        |
| 累计降雨量分布图配色表                                | `CMA_COLORMAPS.PRE_TOTAL_CMAP`         | `colormap_defs/cma_colormaps/pre_total.csv`       | ~                        |
| 相对湿度分布图配色表                                  | `CMA_COLORMAPS.RH_CMAP`                | `colormap_defs/cma_colormaps/rh.csv`              | ~                        |
| 沙尘天气等级分布图配色表                              | `CMA_COLORMAPS.SANDSTORM_LEVEL_CMAP`   | `colormap_defs/cma_colormaps/sandstorm_level.csv` | ~                        |
| 积雪分布图配色表                                      | `CMA_COLORMAPS.SNOW_DEPTH_CMAP`        | `colormap_defs/cma_colormaps/snow_depth.csv`      | ~                        |
| 降雪量等级分布图配色表                                | `CMA_COLORMAPS.SNOW_LEVEL_CMAP`        | `colormap_defs/cma_colormaps/snow_level.csv`      | ~                        |
| 气温距平分布图配色表                                  | `CMA_COLORMAPS.TEMP_ANO_CMAP`          | `colormap_defs/cma_colormaps/temp_ano.csv`        | ~                        |
| 气温分布图配色表                                      | `CMA_COLORMAPS.TEMP_CMAP`              | `colormap_defs/cma_colormaps/temp.csv`            | ~                        |
| 风力等级（6级以上）分布图配色表                       | `CMA_COLORMAPS.WIND_LEVEL_CMAP`        | `colormap_defs/cma_colormaps/wind_level.csv`      | ~                        |
| 1h累积降水量实况色标(采自国家气象信息中心)            | `CMA_COLORMAPS.RAIN_1H_CMAP`           | `colormap_defs/cma_colormaps/rain_1h.csv`         | ~                        |
| 3h累积降水量实况色标(采自国家气象信息中心)            | `CMA_COLORMAPS.RAIN_3H_CMAP`           | `colormap_defs/cma_colormaps/rain_3h.csv`         | ~                        |
| 气温实况色标(采自国家气象信息中心)                    | `CMA_COLORMAPS.TEMP_RT_CMAP`           | `colormap_defs/cma_colormaps/temp_rt.csv`         | ~                        |
| 10m风速色标(6.25km 1h 采自国家气象信息中心)           | `CMA_COLORMAPS.WS10_CMAP`              | `colormap_defs/cma_colormaps/ws10.csv`            | ~                        |
| 海平面气压色标(台风动力诊断 采自国家气象信息中心)     | `CMA_COLORMAPS.SLP_CMAP`               | `colormap_defs/cma_colormaps/slp.csv`             | ~                        |
| 10m风速色标(台风动力诊断 采自国家气象信息中心)        | `CMA_COLORMAPS.WS_TYPHOON_CMAP`        | `colormap_defs/cma_colormaps/ws10_typhoon.csv`    | ~                        |
| 850hPa相对湿度色标(台风湿度诊断 采自国家气象信息中心) | `CMA_COLORMAPS.RH850_CMAP`             | `colormap_defs/cma_colormaps/rh850.csv`           | ~                        |
| 海表温度色标(采自国家气象信息中心)                    | `CMA_COLORMAPS.SST_CMAP`               | `colormap_defs/cma_colormaps/sst.csv`             | ~                        |
| 最低能见度色标(采自国家气象信息中心)                  | `CMA_COLORMAPS.VIS_CMAP`               | `colormap_defs/cma_colormaps/vis.csv`             | ~                        |


#### 色标样例


![气温分布图配色表](images/cma_colormaps/气温分布图配色表_demo.png)


![降雨量等级分布图配色表](images/cma_colormaps/降雨量等级分布图配色表_demo.png)


![风力等级（6级以上）分布图配色表](images/cma_colormaps/风力等级（6级以上）分布图配色表_demo.png)




### 《多普勒天气雷达观测产品色标规范》色标实现

#### 参考文件

  《多普勒天气雷达观测产品色标规范》



#### 包含色标


| 色标描述         | 变量名                           | 定义文件位置                                  | 示例图位置                |
| ---------------- | ------------------------------   | ----------------------------                  | ------------------------  |
| 反射率色标       | `RADAR_COLORMAPS.REFL_CMAP`      | `colormap_defs/radar_colormaps/refl.csv`      | `images/radar_colormaps/` |
| 组合反射率色标   | `RADAR_COLORMAPS.CR_CMAP`        | `colormap_defs/radar_colormaps/cr.csv`        | ~                         |
| 多普勒速度色标   | `RADAR_COLORMAPS.V_CMAP`         | `colormap_defs/radar_colormaps/v.csv`         | ~                         |
| 回波顶高色标     | `RADAR_COLORMAPS.ET_CMAP`        | `colormap_defs/radar_colormaps/et.csv`        | ~                         |
| 液态含水量色标   | `RADAR_COLORMAPS.VIL_CMAP`       | `colormap_defs/radar_colormaps/vil.csv`       | ~                         |
| 降水累积量色标   | `RADAR_COLORMAPS.PRE_TOTAL_CMAP` | `colormap_defs/radar_colormaps/pre_total.csv` | ~                         |
| 谱宽色标         | `RADAR_COLORMAPS.SW_CMAP`        | `colormap_defs/radar_colormaps/sw.csv`        | ~                         |


#### 色标样例


![反射率色标](images/radar_colormaps/反射率色标_demo.png)

![组合反射率色标](images/radar_colormaps/组合反射率色标_demo.png)

![回波顶高色标](images/radar_colormaps/回波顶高色标_demo.png)

![液态含水量色标](images/radar_colormaps/液态含水量色标_demo.png)




### 其它色标


#### 包含色标


| 色标描述         | 变量名                         | 定义文件位置                                | 示例图位置                |
| ---------------- | ------------------------------ | ----------------------------                | ------------------------  |
| 1h降水量色标     | `OTHER_COLORMAPS.RAIN_1H_CMAP` | `colormap_defs/other_colormaps/rain_1h.csv` | `images/other_colormaps/` |



#### 色标样例


![降水累积量色标](images/other_colormaps/1h降水量色标_demo.png)


## 完整色标列表

默认色标列表见 [colormap_list.md](geo_colormaps/colormap_list.md).

默认色标+用户自定义色标列表，见

+ Linux 或 MacOS 系统下： `~/.config/geo_colormaps/colormap_list.md`
+ Windows 系统下：`%appdata%\geo_colormaps\colormap_list.md`



## 添加自定义色标


新色标建议在**用户默认配置目录**下新建一个文件夹，例如

+ Linux 或 MacOS 系统下： `~/.config/geo_colormaps/my_colormaps`。
+ Windows 系统下：`%appdata%\geo_colormaps\my_colormaps`

注意： `~/.config/geo_colormaps` (或 `%appdata%\geo_colormaps`) 是本软件包指定的用户自定义色标存放位置，须严格匹配。
`my_colormaps`是用户为自定义色标系列起的名称，可自选名称（不要带空格或其他非法字符即可）。

之后，在 `my_colormaps` 内以`csv`文件格式新增色标。如新建`my_colormaps/pre_total.csv` , 其中：


```
description=累计降雨量分布图配色表
unit=mm
vmin , vmax , r   , g   , b   , label
0.1  , 9.9  , 165 , 243 , 141 ,
10   , 24.9 , 153 , 210 , 202 ,
25   , 49.9 , 155 , 188 , 232 ,
50   , 99.9 , 107 , 157 , 225 ,
100  , 200  , 59  , 126 , 219 ,
200  , 250  , 43  , 92  , 194 ,
250  , 300  , 28  , 59  , 169 ,
300  , 400  , 17  , 44  , 144 ,
400  , 600  , 7   , 30  , 120 ,
600  , 800  , 70  , 25  , 129 ,
800  , 1000 , 134 , 21  , 138 ,
1000 , 2000 , 200 , 17  , 169 ,
2000 , None , 129 , 0   , 64  ,
```

定义后的新色标使用方法：


```python
# 注意：须先 import geo_colormaps !!!
import geo_colormaps
from geo_colormaps import MY_COLORMAPS

print(MY_COLORMAPS.PRE_TOTAL_CMAP)
```

更多csv示例见 `colormap_defs/cma_colormaps`, `colormap_defs/radar_colormaps`。

{# templates/colormaps.md #}

# 包含色标

{% for group in colormap_groups %}
## {{ group.name }}

+ 色标定义文件夹：`base_folder = {{ group.base_folder }}`
+ 色标示例图文件夹: `img_folder = {{ group.img_folder }}`

| 色标描述      | 变量名        | 定义文件位置        | 示例图位置      |
| --------------| ------------- | --------------------| --------------- |
{% for cmap_key, cmap in group.collection.items() -%}
| {{ cmap.description }}     | `{{ group.name.upper() }}.{{ cmap_key.upper()}}` | `<base_folder>/{{ group.name }}/{{ cmap_key }}.csv` | `<img_folder>/{{ cmap.description }}_demo.png` |
{% endfor %}


### 色标样例

{% for cmap_key, cmap in group.collection.items() %}
![{{ cmap.description }}](<{{ group.img_folder }}/{{ cmap.description }}_demo.png>)

{% endfor %}

{% endfor %}


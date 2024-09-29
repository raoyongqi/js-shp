import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import cartopy.crs as ccrs
import pandas as pd

# 读取第一个 GeoJSON 数据
geojson_file_path_1 = '中华人民共和国.json'
gdf_geojson_1 = gpd.read_file(geojson_file_path_1)

# 读取第二个 GeoJSON 数据
geojson_file_path_2 = '第二个文件.json'
gdf_geojson_2 = gpd.read_file(geojson_file_path_2)

# 设置 Pandas 显示选项
pd.set_option('display.max_columns', None)  # 显示所有列
pd.set_option('display.max_colwidth', None)  # 显示完整列宽
print(gdf_geojson_1)
print(gdf_geojson_2)

# 定义 Albers 投影坐标系
albers_proj = ccrs.AlbersEqualArea(
    central_longitude=105,
    central_latitude=35,
    standard_parallels=(25, 47)
)

# 创建绘图对象
fig, ax = plt.subplots(figsize=(12, 12), subplot_kw={'projection': albers_proj})

# 转换 GeoJSON 数据的坐标系到自定义投影坐标系
if gdf_geojson_1.crs is not None and gdf_geojson_1.crs != albers_proj:
    gdf_geojson_1 = gdf_geojson_1.to_crs(albers_proj)

if gdf_geojson_2.crs is not None and gdf_geojson_2.crs != albers_proj:
    gdf_geojson_2 = gdf_geojson_2.to_crs(albers_proj)

# 绘制转换后的 GeoJSON 数据
gdf_geojson_1.plot(ax=ax, edgecolor='black', facecolor='white', alpha=0.5, label='GeoJSON Data 1')
gdf_geojson_2.plot(ax=ax, edgecolor='red', facecolor='none', linewidth=2, alpha=0.5, label='GeoJSON Data 2')

# 添加标题
plt.title('Overlay of Two GeoJSON Datasets')

# 设置图例
plt.legend()

# 设置坐标轴标签
ax.set_xlabel('Easting (meters)')
ax.set_ylabel('Northing (meters)')

# 添加经纬度网格线
gridlines = ax.gridlines(draw_labels=True, color='gray', linestyle='--', alpha=0.5)
gridlines.xlabel_style = {'size': 10}
gridlines.ylabel_style = {'size': 10}
# 隐藏右边和上边的网格线标签
gridlines.top_labels = False
gridlines.right_labels = False

# 保存图形到文件
output_file_path = 'pic/geojson_overlay.png'  # 确保 pic 文件夹已存在
plt.savefig(output_file_path, dpi=300, bbox_inches='tight')

# 显示图形
plt.show()

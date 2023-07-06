import matplotlib.pyplot as plt
import numpy as np
from lxml import html


url = "D:\\Projects\\OpenStudioDev\\BoxModel\\reports\\eplustbl.html"
try:
    with open(url, "r") as f:
        page = f.read()
    tree = html.fromstring(page)
except ValueError:
    raise ValueError("Invalid url for file path.")

tables = tree.xpath('/html/body/table')
bolds = tree.xpath('/html/body/b')[2:]

row = tables[0].xpath('.//tr')
data = row[0].xpath('.//td')[0].text
# for table in tables:
#     rows = table.xpath('//tr')
#     for row in rows:
#         data = row.xpath('//td')
#         print(data[0].text)

print(len(tables))
print(bolds[0].text)
# print(html.tostring(tree))


cases = ("case 1", "case 2", "case 3")
end_use_values = {
    'Cooling': np.array([40, 30, 15]),
    'Heating': np.array([20, 40, 25]),
    'Lighting': np.array([10, 12, 14]),
    'Equipment': np.array([23, 22, 25]),
}
width = 0.6

fig, ax = plt.subplots()
bottom = np.zeros(3)

for category, end_use in end_use_values.items():
    p = ax.bar(cases, end_use, width, label=category, bottom=bottom)
    bottom += end_use

    ax.bar_label(p, label_type='center')

ax.set_title("Energy By End Use")
ax.legend(loc="right")
plt.show()


# fig, ax = plt.subplots(subplot_kw=dict(projection="polar"))
#
# size = 0.3
# vals = np.array([[60., 32.], [37., 40.], [29., 10.]])
# # Normalize vals to 2 pi
# valsnorm = vals/np.sum(vals)*2*np.pi
# # Obtain the ordinates of the bar edges
# valsleft = np.cumsum(np.append(0, valsnorm.flatten()[:-1])).reshape(vals.shape)
#
# cmap = plt.colormaps["tab20c"]
# outer_colors = cmap(np.arange(3)*4)
# inner_colors = cmap([1, 2, 5, 6, 9, 10])
#
# ax.bar(x=valsleft[:, 0],
#        width=valsnorm.sum(axis=1), bottom=1-size, height=size,
#        color=outer_colors, edgecolor='w', linewidth=1, align="edge")
#
# ax.bar(x=valsleft.flatten(),
#        width=valsnorm.flatten(), bottom=1-2*size, height=size,
#        color=inner_colors, edgecolor='w', linewidth=1, align="edge")
#
# ax.set(title="Pie plot with `ax.bar` and polar coordinates")
# ax.set_axis_off()
# plt.show()

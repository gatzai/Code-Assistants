from paddleocr import PaddleOCR, draw_ocr
from PIL import Image
from itertools import product
import cv2
import numpy as np

# TODO：这个测试用例 table.png 顶部和下部交叉部分没有标记出来
# TODO：获取表格区域

'''
	说明： 轮廓转为直线
	输入的 shape 是二维的，点的数量 n 和点的坐标，即 nx2
	输出起点和终点，即 2x2
'''
def contour2line(contours):
	x_min = min(contours[:,0])
	x_max = max(contours[:,0])
	y_min = min(contours[:,1])
	y_max = max(contours[:,1])
	del_x = abs(x_min-x_max)
	del_y = abs(y_min-y_max)

	if del_x < del_y: # vertical line
		x = (x_min + x_max)//2
		return [[x, y_min],[x, y_max]]
	else: #horizontal line
		y = (y_min + y_max)//2
		return [[x_min, y],[x_max, y]]

'''
	说明： 所有横线和竖线轮廓转为直线，并且进行相应的延长，从而避免 “交点误差”
	交点误差： 如果要求交点，还有一个潜在的问题就是有些线差一点点相交，但是却没有相交，
	这种情况就需要对所有线做延长，横线延长最小宽度的一半，纵线延长最小高度的一半
	输入：横线和纵线轮廓
	输出：
'''
def extende2lines(hors, vers):
	# 可能是多个 array 对象作为数组元素，所以只能看第一维度，剩余的维度需要每个元素再 shape 一下
	# 估计是每个元素不一定一样吧
	# 上面的猜想确实是正确的，不一定所有轮廓都是矩形，所以还要进一步将奇奇怪怪的形状转为线条
	
	if len(hors) < 2 or len(vers) < 2:
		print('[Error]Too Less Contour')
		return None
	# Contour 转为线条
	hor_lines, ver_lines = [], []
	for h in hors:
		contour = h.squeeze()
		if len(contour.shape) > 2:
			print('[Error]Horizontal Shape Error:', contour.shape)
		# 所有轮廓点转为直线
		line = contour2line(contour)
		hor_lines.append(line)
	for v in vers:
		contour = v.squeeze()
		if len(contour.shape) > 2:
			print('[Error]Vertical Shape Error:', contour.shape)
		# 所有轮廓点转为直线
		line = contour2line(contour)
		ver_lines.append(line)

	# 获取表格最小间距
	min_height_gap, min_width_gap = float('inf'), float('inf')
	for i in range(1, len(hor_lines)):
		min_height_gap = min(min_height_gap, abs(hor_lines[i][0][1] - hor_lines[i - 1][0][1]))
	for i in range(1, len(ver_lines)):
		min_width_gap = min(min_width_gap, abs(ver_lines[i][0][0] - ver_lines[i - 1][0][0]))
	
	print("Min Gap Height:",min_height_gap)
	print("Min Gap Width:",min_width_gap)

	# 延长
	for i in range(len(hor_lines)):
		hor_lines[i][0][0] -= min_width_gap//3
		hor_lines[i][1][0] += min_width_gap//3
	for i in range(len(ver_lines)):
		ver_lines[i][0][1] -= min_height_gap//3
		ver_lines[i][1][1] += min_height_gap//3
	return [hor_lines, ver_lines]

# 获取横纵线交点，每条横线的交点为一个批次
def get_cross_points(hors, vers):
	points =[]
	for h in hors:
		p = []
		for v in vers:
			if v[0][1] < h[0][1] < v[1][1]:
				p.append([ v[0][0], h[0][1]])
		points.append(p)
	return points

# TODO：按照横向来获取表格区域
def get_hor_area():
	pass

# 获取表格横纵线交点坐标
# TODO： 获取每个矩形的区域
def get_table():
	img = cv2.imread(r'table.png')
	#1.二值化处理
	# 灰度化
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	# 阈值分割
	#retval, dst = cv2.threshold(gray, 110, 255, cv2.THRESH_BINARY)
	retval, dst = cv2.threshold(~gray, 127, 255, cv2.THRESH_BINARY)

	print(dst.shape)

	res = img.copy()
	res *= 0

	#2.提取表格
	height = dst.shape[0]
	width = dst.shape[1]
	horizontal_size = height//16
	vertical_size = width//16

	#横向
	horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (horizontal_size,1))
	remove_horizontal = cv2.morphologyEx(dst, cv2.MORPH_OPEN, horizontal_kernel, iterations=1)
	cnts = cv2.findContours(remove_horizontal, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	cnts_h = cnts[0] if len(cnts) == 2 else cnts[1]
	print("横线数量：", len(cnts_h))
	#for c in cnts_h:
	#	cv2.drawContours(res, [c], -1, (255,255,255), 2)

	#纵向
	vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,vertical_size))
	remove_vertical = cv2.morphologyEx(dst, cv2.MORPH_OPEN, vertical_kernel, iterations=1)
	cnts = cv2.findContours(remove_vertical, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	cnts_v = cnts[0] if len(cnts) == 2 else cnts[1]
	print("竖线数量：", len(cnts_v))
	#for c in cnts_v:
	#	cv2.drawContours(res, [c], -1, (255,255,255), 2)

	hor_ver_lines = extende2lines(cnts_h, cnts_v)
	points = get_cross_points(hor_ver_lines[0], hor_ver_lines[1])
	# 绘制
	for hor_ver in hor_ver_lines:
		for line in hor_ver:
			cv2.drawContours(res, [np.array(line)], -1, (255,255,255), 2)
	for hp in points:
		for p in hp:
			p = [p[0],p[1]],[p[0]+10,p[1]+10]
			cv2.drawContours(res, [np.array(p)], -1, (0,255,0), 2)
	cv2.imwrite('table_res.png',res)

# 去除水印
def erase_mark():
	img = Image.open(r'test.png')
	width, height = img.size
	for pos in product(range(width), range(height)):
		if sum(img.getpixel(pos)[:3]) > 580:
			img.putpixel(pos, (255,255,255))
	img.show()
	#img.save('clean_test.png')

# 测试 OCR
def run():
	ocr = PaddleOCR(use_angle_cls=True, lang="ch")
	# 输入待识别图片路径
	img_path = r"clean_test.png"
	# 输出结果保存路径
	result = ocr.ocr(img_path, cls=True)
	for line in result:
		print(line)

	image = Image.open(img_path).convert('RGB')
	#box 是左上，右上，右下，左下
	boxes = [line[0] for line in result]
	txts = [line[1][0] for line in result]
	scores = [line[1][1] for line in result]
	im_show = draw_ocr(image, boxes, txts, scores)
	im_show = Image.fromarray(im_show)
	im_show.show()
	im_show.save()

if __name__ == "__main__":
	get_table()
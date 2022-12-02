import PyPDF3 as pdf
import os

#custom startpage implementing

input = pdf.PdfFileReader(open("course.pdf", "rb"))
output = pdf.PdfFileWriter()

pages = []
currentPage = -1

x1_A4 = 612
y1_A4 = 792

std_offset_x = 30
std_offset_y = 17
padding = 25

offsetX = x1_A4 - std_offset_x
offsetY = y1_A4 - std_offset_y

def getPageSize(page):
	x0 = page['/MediaBox'][0]
	y0 = page['/MediaBox'][1]
	x1 = page['/MediaBox'][2]
	y1 = page['/MediaBox'][3]

	return x0, y0, x1, y1

def getScaling(pdf_input, pagenumber):
	inputPage = pdf_input.getPage(pageNumber)

	x0, y0, x1, y1 = getPageSize(inputPage)

	scaling_factor = (x1_A4 - 2*std_offset_x)/(3*y1 + 2*padding)
	x1_scaled = x1*scaling_factor
	y1_scaled = y1*scaling_factor

	return scaling_factor, x1_scaled, y1_scaled

for pageNumber in range(input.getNumPages()):
	if pageNumber%6 == 0:
		pages.append(pdf.PdfFileWriter().addBlankPage(x1_A4, y1_A4))

		currentPage += 1
		secondRow = 0

	inputPage = input.getPage(pageNumber)
	scaling_factor, x1_scaled, y1_scaled = getScaling(input, pageNumber)

	if pageNumber%3 == 0 and pageNumber != 0 and pageNumber%6 != 0:
		secondRow = y1_A4/2

	pages[currentPage].mergeRotatedScaledTranslatedPage(inputPage, -90, scaling_factor, offsetX - (pageNumber%3 + 1)*y1_scaled - (pageNumber%3)*(padding-10) + 5, offsetY - secondRow)

for p in pages:
	output.addPage(p.rotateCounterClockwise(90))

output.write(open("MPT_SlidesPER6.pdf", "wb"))

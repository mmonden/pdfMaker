import PyPDF3 as pdf

#custom startpage implementing

input = pdf.PdfFileReader(open("MPT_Slides.pdf", "rb"))
output = pdf.PdfFileWriter()

pages = []
currentPage = -1

# for MPT
offsetX = 35 + 2*195
offsetY = 325 + 450

# for DIAC
# offsetX = 35 + 2*195 - 5
# offsetY = 325 + 450

# for NBM
# offsetX = 2*195
# offsetY = 325+450

# for SSC
# offsetX = 35 + 2*195 - 25
# offsetY = 325 + 450

for pageNumber in range(input.getNumPages()):
	if pageNumber%6 == 0:
		pages.append(pdf.PdfFileWriter().addBlankPage(8.5*72, 11*72))

		currentPage += 1
		secondRow = 0

	inputPage = input.getPage(pageNumber)

	if pageNumber%3 == 0 and pageNumber != 0 and pageNumber%6 != 0:
		secondRow = -offsetY + 385

	# For MPT and DIAC
	pages[currentPage].mergeRotatedScaledTranslatedPage(inputPage, -90, 0.3, offsetX - (pageNumber%3)*200, offsetY + secondRow)

	# For NBM
	# if pageNumber < 394:
	# 	pages[currentPage].mergeRotatedScaledTranslatedPage(inputPage, -90, 0.39, offsetX - 10 - (pageNumber%3)*200, offsetY + secondRow)
	# else:
	# 	pages[currentPage].mergeRotatedScaledTranslatedPage(inputPage, -90, 0.24, offsetX - 20 - (pageNumber%3)*190, offsetY + secondRow)

	# For SSC
	# pages[currentPage].mergeRotatedScaledTranslatedPage(inputPage, -90, 0.35, offsetX - (pageNumber%3)*190, offsetY + secondRow)

for p in pages:
	output.addPage(p)

output.write(open("MPT_SlidesPER6.pdf", "wb"))
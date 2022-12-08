import PyPDF3 as pdf
import typing

#custom startpage implementing

class PDFMaker():
	currentPage = -1

	x1_A4 = 612
	y1_A4 = 792

	std_offset_x = 30
	std_offset_y = 17
	padding = 25

	offsetX = x1_A4 - std_offset_x
	offsetY = y1_A4 - std_offset_y

	pdf_name = "semi.pdf"

	def getPageSize(self, page : pdf.pdf.PageObject) -> typing.Union[int, int, int, int]:
		x0 = page['/MediaBox'][0]
		y0 = page['/MediaBox'][1]
		x1 = page['/MediaBox'][2]
		y1 = page['/MediaBox'][3]

		return x0, y0, x1, y1

	def getScaling(self, pdf_page : pdf.pdf.PageObject, pagenumber : int) -> list[int]:
		inputPage = pdf_page.getPage(pagenumber)

		x0, y0, x1, y1 = self.getPageSize(inputPage)

		scaling_factor = (self.x1_A4 - 2*self.std_offset_x)/(3*y1 + 2*self.padding)
		x1_scaled = x1*scaling_factor
		y1_scaled = y1*scaling_factor

		return scaling_factor, x1_scaled, y1_scaled

	def constructPages(self, pdf_input : pdf.PdfFileReader) -> list[pdf.pdf.PageObject]:
		pages = []

		for pageNumber in range(pdf_input.getNumPages()):
			if pageNumber%6 == 0:
				pages.append(pdf.PdfFileWriter().addBlankPage(self.x1_A4, self.y1_A4))

				self.currentPage += 1
				secondRow = 0

			inputPage = pdf_input.getPage(pageNumber)
			scaling_factor, x1_scaled, y1_scaled = self.getScaling(pdf_input, pageNumber)

			if pageNumber%3 == 0 and pageNumber != 0 and pageNumber%6 != 0:
				secondRow = self.y1_A4/2

			pages[self.currentPage].mergeRotatedScaledTranslatedPage(inputPage, -90, scaling_factor, self.offsetX - (pageNumber%3 + 1)*y1_scaled - (pageNumber%3)*(self.padding-10) + 5, self.offsetY - secondRow)

		return pages

	def rotateAllPages(self, pages : list[pdf.pdf.PageObject], output : pdf.PdfFileWriter) -> pdf.PdfFileWriter:
		for p in pages:
			output.addPage(p.rotateCounterClockwise(90))

		return output

	def writeOutput(self, pdf_input : pdf.PdfFileReader, output : pdf.PdfFileWriter) -> None:
		output.write(open(self.pdf_name[:-4] + "PER6.pdf", "wb"))

	def __init__(self):
		pdf_input = pdf.PdfFileReader(open(input(), "rb")) if not self.pdf_name else pdf.PdfFileReader(open(self.pdf_name, "rb"))
		output = pdf.PdfFileWriter()

		pages = self.constructPages(pdf_input)
		output = self.rotateAllPages(pages, output)

		self.writeOutput(pdf_input, output)

PDFMaker()

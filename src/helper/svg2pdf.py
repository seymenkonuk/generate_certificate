from os import system

# SVG'yi PDF'e DÖNÜŞTÜR VE SVG'Yİ SİL
def svg2pdf(svg_path, pdf_path, text2path):
	if text2path:
		system(f"inkscape {svg_path} --export-filename={pdf_path} --export-text-to-path")
	else:
		system(f"inkscape {svg_path} --export-filename={pdf_path}")

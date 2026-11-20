// Prepara la tarjeta para imprimir a partir de los dos PDF exportados de Figma.
//
//   swift tools/imprimir.swift
//
// Escribe en tarjeta/:
//   eventually-tarjeta-copisteria.pdf  2 páginas (anverso y reverso), con 3 mm de
//                                      sangrado y marcas de corte: para la copistería.
//   eventually-tarjeta-casa-A4.pdf     una hoja A4 con las dos caras juntas, para
//                                      recortar, doblar y pegar: para imprimir en casa.

import CoreGraphics
import CoreText
import Foundation

let mm: CGFloat = 72.0 / 25.4
let root = URL(fileURLWithPath: #filePath).deletingLastPathComponent().deletingLastPathComponent()
let dir = root.appendingPathComponent("tarjeta")

func load(_ name: String) -> CGPDFPage {
    guard let doc = CGPDFDocument(dir.appendingPathComponent(name) as CFURL), let page = doc.page(at: 1) else {
        fatalError("No encuentro \(name) en tarjeta/")
    }
    return page
}

let front = load("eventually-tarjeta-anverso.pdf")
let back = load("eventually-tarjeta-reverso.pdf")
let trim = front.getBoxRect(.mediaBox).size            // 241 x 156 pt = 85 x 55 mm
let paper = CGColor(srgbRed: 0xF7 / 255.0, green: 0xF6 / 255.0, blue: 0xF2 / 255.0, alpha: 1)
let black = CGColor(gray: 0, alpha: 1)

func boxData(_ rect: CGRect) -> CFData {
    var r = rect
    return Data(bytes: &r, count: MemoryLayout<CGRect>.size) as CFData
}

func draw(_ page: CGPDFPage, in ctx: CGContext, at origin: CGPoint) {
    ctx.saveGState()
    ctx.translateBy(x: origin.x, y: origin.y)
    ctx.drawPDFPage(page)
    ctx.restoreGState()
}

/// Marcas de corte en las cuatro esquinas de `rect`, separadas `gap` del borde.
func cropMarks(_ ctx: CGContext, around rect: CGRect, gap: CGFloat, length: CGFloat) {
    ctx.setStrokeColor(black)
    ctx.setLineWidth(0.3)
    for x in [rect.minX, rect.maxX] {
        for y in [rect.minY, rect.maxY] {
            let dx: CGFloat = x == rect.minX ? -1 : 1
            let dy: CGFloat = y == rect.minY ? -1 : 1
            ctx.move(to: CGPoint(x: x + dx * gap, y: y))
            ctx.addLine(to: CGPoint(x: x + dx * (gap + length), y: y))
            ctx.move(to: CGPoint(x: x, y: y + dy * gap))
            ctx.addLine(to: CGPoint(x: x, y: y + dy * (gap + length)))
        }
    }
    ctx.strokePath()
}

func text(_ ctx: CGContext, _ string: String, x: CGFloat, y: CGFloat, size: CGFloat, gray: CGFloat = 0.35, bold: Bool = false) {
    let font = CTFontCreateWithName((bold ? "Helvetica-Bold" : "Helvetica") as CFString, size, nil)
    let attrs: [NSAttributedString.Key: Any] = [
        NSAttributedString.Key(kCTFontAttributeName as String): font,
        NSAttributedString.Key(kCTForegroundColorAttributeName as String): CGColor(gray: gray, alpha: 1),
    ]
    let line = CTLineCreateWithAttributedString(NSAttributedString(string: string, attributes: attrs))
    ctx.textPosition = CGPoint(x: x, y: y)
    CTLineDraw(line, ctx)
}

// ---------- 1. Para la copistería: una cara por página, con sangrado y marcas ----------

do {
    let bleed = 3 * mm
    let slug = 10 * mm                                   // margen donde van las marcas
    var media = CGRect(x: 0, y: 0, width: trim.width + 2 * slug, height: trim.height + 2 * slug)
    let trimBox = CGRect(x: slug, y: slug, width: trim.width, height: trim.height)
    let bleedBox = trimBox.insetBy(dx: -bleed, dy: -bleed)
    let url = dir.appendingPathComponent("eventually-tarjeta-copisteria.pdf")
    let ctx = CGContext(url as CFURL, mediaBox: &media, nil)!
    let info: [String: Any] = [
        kCGPDFContextMediaBox as String: boxData(media),
        kCGPDFContextBleedBox as String: boxData(bleedBox),
        kCGPDFContextTrimBox as String: boxData(trimBox),
    ]
    for page in [front, back] {
        ctx.beginPDFPage(info as CFDictionary)
        ctx.setFillColor(paper)
        ctx.fill(bleedBox)                               // el fondo se alarga 3 mm por cada lado
        draw(page, in: ctx, at: trimBox.origin)
        cropMarks(ctx, around: trimBox, gap: bleed, length: 5 * mm)
        ctx.endPDFPage()
    }
    ctx.closePDF()
    print("copistería:", url.lastPathComponent, "— página \(Int((media.width / mm).rounded())) × \(Int((media.height / mm).rounded())) mm, corte 85 × 55 mm")
}

// ---------- 2. Para casa: A4 con las dos caras juntas, para doblar y pegar ----------

do {
    var media = CGRect(x: 0, y: 0, width: 210 * mm, height: 297 * mm)
    let url = dir.appendingPathComponent("eventually-tarjeta-casa-A4.pdf")
    let ctx = CGContext(url as CFURL, mediaBox: &media, nil)!
    ctx.beginPDFPage(nil)

    let left: CGFloat = 22 * mm
    var y = media.height - 24 * mm
    text(ctx, "Eventually — tarjeta de autenticidad · para imprimir en casa", x: left, y: y, size: 11, gray: 0.1, bold: true)
    let steps = [
        "1.  Imprime esta hoja al 100 % (desmarca «Ajustar al tamaño del papel»). Mejor en el papel más grueso que admita tu impresora.",
        "2.  Recorta el rectángulo por las marcas de las cuatro esquinas.",
        "3.  Dobla por las dos marcas centrales, con lo impreso hacia fuera.",
        "4.  Pon pegamento de barra por dentro y aprieta. Tamaño final: 85 × 55 mm.",
        "Hay dos copias, por si una sale mal.",
    ]
    for step in steps {
        y -= 15
        text(ctx, step, x: left, y: y, size: 8.5)
    }

    let pairWidth = trim.width * 2
    let x0 = (media.width - pairWidth) / 2
    let extra = 2 * mm                                   // un poco de fondo de más, para que el corte no deje blanco
    var top = y - 26 * mm
    for _ in 0..<2 {
        let pair = CGRect(x: x0, y: top - trim.height, width: pairWidth, height: trim.height)
        ctx.setFillColor(paper)
        ctx.fill(pair.insetBy(dx: -extra, dy: -extra))
        draw(back, in: ctx, at: CGPoint(x: pair.minX, y: pair.minY))            // izquierda: reverso
        draw(front, in: ctx, at: CGPoint(x: pair.midX, y: pair.minY))           // derecha: anverso
        cropMarks(ctx, around: pair, gap: extra + 1 * mm, length: 6 * mm)
        // marcas de doblez, arriba y abajo de la línea central
        ctx.setStrokeColor(black)
        ctx.setLineWidth(0.3)
        ctx.setLineDash(phase: 0, lengths: [2, 2])
        for (a, b) in [(pair.maxY + extra + 1 * mm, pair.maxY + extra + 7 * mm), (pair.minY - extra - 7 * mm, pair.minY - extra - 1 * mm)] {
            ctx.move(to: CGPoint(x: pair.midX, y: a))
            ctx.addLine(to: CGPoint(x: pair.midX, y: b))
        }
        ctx.strokePath()
        ctx.setLineDash(phase: 0, lengths: [])
        text(ctx, "doblar", x: pair.midX + 3, y: pair.maxY + extra + 3 * mm, size: 6.5, gray: 0.5)
        top -= trim.height + 34 * mm
    }

    ctx.endPDFPage()
    ctx.closePDF()
    print("casa:", url.lastPathComponent, "— A4, dos copias")
}

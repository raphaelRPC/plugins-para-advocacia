// Recorte da pessoa (macOS, framework Vision, sem instalação): salva uma máscara PNG em que branco = pessoa.
// Uso único:   swift recortar.swift <quadro.png> <mascara.png>
// Uso contínuo (o motor usa assim): recortar --servico   e, em cada linha da entrada, "<quadro.png>\t<mascara.png>";
//              responde "ok" ou "erro: ..." por linha.
import Foundation
import Vision
import CoreImage
import ImageIO
import UniformTypeIdentifiers

let contexto = CIContext()

func recortar(_ entrada: String, _ saida: String) throws {
    guard let src = CGImageSourceCreateWithURL(URL(fileURLWithPath: entrada) as CFURL, nil),
          let img = CGImageSourceCreateImageAtIndex(src, 0, nil) else { throw NSError(domain: "imagem", code: 1) }
    let pedido = VNGeneratePersonSegmentationRequest()
    pedido.qualityLevel = .accurate
    pedido.outputPixelFormat = kCVPixelFormatType_OneComponent8
    try VNImageRequestHandler(cgImage: img, options: [:]).perform([pedido])
    guard let buf = pedido.results?.first?.pixelBuffer else { throw NSError(domain: "sem pessoa", code: 2) }
    var ci = CIImage(cvPixelBuffer: buf)
    ci = ci.transformed(by: CGAffineTransform(scaleX: CGFloat(img.width) / ci.extent.width, y: CGFloat(img.height) / ci.extent.height))
    guard let out = contexto.createCGImage(ci, from: CGRect(x: 0, y: 0, width: img.width, height: img.height)),
          let dest = CGImageDestinationCreateWithURL(URL(fileURLWithPath: saida) as CFURL, UTType.png.identifier as CFString, 1, nil)
    else { throw NSError(domain: "saida", code: 3) }
    CGImageDestinationAddImage(dest, out, nil)
    CGImageDestinationFinalize(dest)
}

let args = CommandLine.arguments
if args.count > 1 && args[1] == "--servico" {
    setvbuf(stdout, nil, _IOLBF, 0)
    while let linha = readLine() {
        let p = linha.components(separatedBy: "\t")
        guard p.count == 2 else { print("erro: linha inválida"); continue }
        do { try recortar(p[0], p[1]); print("ok") } catch { print("erro: \(error)") }
    }
} else if args.count == 3 {
    try recortar(args[1], args[2]); print("ok")
} else {
    print("uso: recortar <quadro.png> <mascara.png> | recortar --servico")
}

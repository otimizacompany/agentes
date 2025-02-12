// fileProcessing.ts
import mammoth from "mammoth";
import pdfParse from "pdf-parse";
import XLSX from "xlsx";
import { Document, Packer, Paragraph, HeadingLevel } from "docx";

/**
 * Processa o arquivo enviado e retorna o texto extraído.
 * Suporta: .docx, .txt, .pdf, .csv e .xlsx.
 */
export async function processFile(file: File): Promise<string | null> {
  const fileName = file.name.toLowerCase();
  try {
    if (fileName.endsWith(".docx")) {
      const arrayBuffer = await file.arrayBuffer();
      const result = await mammoth.extractRawText({ buffer: Buffer.from(arrayBuffer) });
      return result.value;
    } else if (fileName.endsWith(".txt")) {
      return await file.text();
    } else if (fileName.endsWith(".pdf")) {
      const arrayBuffer = await file.arrayBuffer();
      const buffer = Buffer.from(arrayBuffer);
      const data = await pdfParse(buffer);
      return data.text;
    } else if (fileName.endsWith(".csv")) {
      return await file.text();
    } else if (fileName.endsWith(".xlsx")) {
      const arrayBuffer = await file.arrayBuffer();
      const workbook = XLSX.read(arrayBuffer, { type: "array" });
      const firstSheetName = workbook.SheetNames[0];
      const worksheet = workbook.Sheets[firstSheetName];
      return XLSX.utils.sheet_to_csv(worksheet);
    } else {
      console.error("Tipo de arquivo não suportado. Envie .docx, .txt, .pdf, .csv ou .xlsx.");
      return null;
    }
  } catch (error) {
    console.error("Erro ao processar arquivo:", error);
    return null;
  }
}

/**
 * Gera um arquivo DOCX a partir do conteúdo e título informados.
 */
export async function generateDocx(content: string, title: string): Promise<Blob> {
  const doc = new Document({
    sections: [
      {
        children: [
          new Paragraph({
            text: title,
            heading: HeadingLevel.HEADING_1,
          }),
          new Paragraph({
            text: content,
          }),
        ],
      },
    ],
  });
  // Chama toBlob sem o segundo parâmetro para satisfazer a tipagem esperada
  const blob = await Packer.toBlob(doc);
  return blob;
}

// openaiHelper.ts
import OpenAI from "openai";
import { encoding_for_model } from "tiktoken";

/**
 * Configura e retorna o cliente do OpenAI usando a chave de API fornecida.
 */
export function getOpenaiClient(apiKey: string): OpenAI {
  return new OpenAI({ apiKey });
}

/**
 * Conta os tokens de um texto utilizando o encoder apropriado para o modelo.
 */
export function countTokens(
  text: string,
  model: "gpt-3.5-turbo" = "gpt-3.5-turbo"
): number {
  try {
    // Forçamos o modelo como literal para satisfazer o tipo TiktokenModel
    const encoder = encoding_for_model(model as "gpt-3.5-turbo");
    const tokens = encoder.encode(text);
    return tokens.length;
  } catch (error) {
    console.error("Erro ao contar tokens:", error);
    return text.split(/\s+/).length;
  }
}

/**
 * Realiza a chamada à API de chat do OpenAI, registra o uso de tokens e retorna a resposta.
 */
export async function callOpenaiChat(
  apiKey: string,
  model: "gpt-3.5-turbo",
  messages: { role: "system" | "user" | "assistant"; content: string }[],
  options: Record<string, any> = {}
): Promise<any> {
  const client = getOpenaiClient(apiKey);
  try {
    const response = await client.chat.completions.create({
      model,
      messages,
      ...options,
    });
    const usage = response.usage; // Use a propriedade diretamente, pois não há .data
    console.info("Uso de tokens:", usage);
    return response;
  } catch (error) {
    console.error("Erro ao chamar OpenAI Chat:", error);
    throw error;
  }
}

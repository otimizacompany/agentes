// openaiFunctions.ts
import OpenAI from "openai";
import { encoding_for_model } from "tiktoken";

// Defina uma interface para as mensagens, se necessário:
export interface ChatMessage {
  role: "system" | "user" | "assistant";
  content: string;
}

/**
 * Conta os tokens de um texto utilizando o encoder apropriado para o modelo.
 */
export function countTokens(
  text: string,
  model: "gpt-3.5-turbo" = "gpt-3.5-turbo"
): number {
  try {
    // Garanta que o modelo seja do tipo literal esperado
    const encoder = encoding_for_model(model as "gpt-3.5-turbo");
    const tokens = encoder.encode(text);
    return tokens.length;
  } catch (error) {
    console.error("Erro ao contar tokens:", error);
    return text.split(/\s+/).length;
  }
}

/**
 * Retorna uma instância do cliente OpenAI.
 * Use variáveis de ambiente para a API key em produção.
 */
export function getOpenaiClient(apiKey: string): OpenAI {
  return new OpenAI({ apiKey });
}

/**
 * Gera questões com base nos parâmetros informados.
 */
export async function gerarQuestoes(
  ano: string,
  componente: string,
  assunto: string,
  dificuldade: string,
  numero_questoes: number,
  tipo: string,
  contexto?: string,
  apiKey?: string
): Promise<string | null> {
  const tipo_texto = tipo === "Dissertativas" ? "dissertativas" : "objetivas";
  const contexto_texto = contexto ? `Utilize o seguinte contexto: \n${contexto}\n\n` : "";
  const prompt = `
${contexto_texto}
Crie um conjunto de ${numero_questoes} questões ${tipo_texto} sobre o seguinte assunto:
- Ano/Série: ${ano}
- Componente Curricular: ${componente}
- Assunto: ${assunto ? assunto : "N/A"}
- Dificuldade: ${dificuldade}

Certifique-se de que as questões sejam claras e adequadas ao nível de ensino informado.
`;
  const prompt_tokens = countTokens(prompt, "gpt-3.5-turbo");
  console.log(`Tokens do prompt: ${prompt_tokens}`);

  const max_total_tokens = 4096;
  const max_response_tokens = max_total_tokens - prompt_tokens;
  if (max_response_tokens < 50) {
    console.error("O prompt está muito extenso e não há tokens suficientes disponíveis para a resposta.");
    return null;
  }
  if (!apiKey) {
    console.error("API Key não fornecida.");
    return null;
  }
  const client = getOpenaiClient(apiKey);
  try {
    const response = await client.chat.completions.create({
      model: "gpt-3.5-turbo",
      messages: [
        { role: "system", content: "Você é um assistente especializado na criação de questões educacionais." },
        { role: "user", content: prompt },
      ],
      max_tokens: max_response_tokens,
    });
    // Use as propriedades do objeto de resposta diretamente (sem .data)
    const output_text = response.choices[0].message?.content || "";
    const output_tokens = countTokens(output_text, "gpt-3.5-turbo");
    console.log(`Tokens do output: ${output_tokens}`);
    console.log("Output:", output_text);
    return output_text;
  } catch (error) {
    console.error("Erro ao gerar questões:", error);
    return null;
  }
}

/**
 * Gera um plano de aula com base nos parâmetros informados.
 */
export async function gerarPlanoAula(
  ano: string,
  componente: string,
  capitulo: string,
  modulo: string,
  duracao: number,
  metodologia: string,
  caracteristicas: string,
  assunto?: string,
  contexto?: string,
  apiKey?: string
): Promise<string | null> {
  const contexto_texto = contexto ? `Utilize o seguinte contexto: \n${contexto}\n\n` : "";
  const prompt = `
${contexto_texto}
Crie um plano de aula com as seguintes características:
- Ano/Série: ${ano}
- Componente Curricular: ${componente}
- Capítulo do livro: ${capitulo}
- Módulo do capítulo: ${modulo}
- Assunto: ${assunto}
- Duração: ${duracao} minutos
- Metodologia: ${metodologia}
- Características da Turma: ${caracteristicas ? caracteristicas : "N/A"}
`;
  const prompt_tokens = countTokens(prompt, "gpt-3.5-turbo");
  console.log(`Tokens do prompt: ${prompt_tokens}`);
  const max_total_tokens = 4096;
  const max_response_tokens = max_total_tokens - prompt_tokens;
  if (max_response_tokens < 50) {
    console.error("O prompt está muito extenso e não há tokens suficientes disponíveis para a resposta.");
    return null;
  }
  if (!apiKey) {
    console.error("API Key não fornecida.");
    return null;
  }
  const client = getOpenaiClient(apiKey);
  try {
    const response = await client.chat.completions.create({
      model: "gpt-3.5-turbo",
      messages: [
        { role: "system", content: "Você é um assistente especializado em geração de planejamento educacional para os professores." },
        { role: "user", content: prompt },
      ],
      max_tokens: max_response_tokens,
    });
    const output_text = response.choices[0].message?.content || "";
    const output_tokens = countTokens(output_text, "gpt-3.5-turbo");
    console.log(`Tokens do output: ${output_tokens}`);
    console.log("Output:", output_text);
    return output_text;
  } catch (error) {
    console.error("Erro ao gerar plano de aula:", error);
    return null;
  }
}

/**
 * Gera um conteúdo contextualizado com base nos parâmetros informados.
 */
export async function gerarAssuntoContextualizado(
  ano: string,
  componente: string,
  assunto: string,
  interesse: string,
  contexto?: string,
  apiKey?: string
): Promise<string | null> {
  const contexto_texto = contexto ? `Utilize o seguinte contexto: \n${contexto}\n\n` : "";
  const prompt = `
${contexto_texto}
Crie um conteúdo contextualizado com as seguintes informações:
- Ano/Série: ${ano}
- Componente Curricular: ${componente}
- Assunto: ${assunto ? assunto : "N/A"}
- Tema de Interesse: ${interesse ? interesse : "N/A"}
`;
  const prompt_tokens = countTokens(prompt, "gpt-3.5-turbo");
  console.log(`Tokens do prompt: ${prompt_tokens}`);
  const max_total_tokens = 4096;
  const max_response_tokens = max_total_tokens - prompt_tokens;
  if (max_response_tokens < 50) {
    console.error("O prompt está muito extenso e não há tokens suficientes disponíveis para a resposta.");
    return null;
  }
  if (!apiKey) {
    console.error("API Key não fornecida.");
    return null;
  }
  const client = getOpenaiClient(apiKey);
  try {
    const response = await client.chat.completions.create({
      model: "gpt-3.5-turbo",
      messages: [
        { role: "system", content: "Você é um assistente especializado em gerar contextualização educacional." },
        { role: "user", content: prompt },
      ],
      max_tokens: max_response_tokens,
    });
    const output_text = response.choices[0].message?.content || "";
    const output_tokens = countTokens(output_text, "gpt-3.5-turbo");
    console.log(`Tokens do output: ${output_tokens}`);
    console.log("Output:", output_text);
    return output_text;
  } catch (error) {
    console.error("Erro ao gerar assunto contextualizado:", error);
    return null;
  }
}

/**
 * Corrige as questões com base nas respostas do aluno, gabarito e demais parâmetros.
 */
export async function corrigirQuestoes(
  respostas_aluno: string,
  gabarito: string,
  tipo: string,
  contexto?: string,
  apiKey?: string
): Promise<string> {
  const tipo_texto = tipo === "Dissertativas" ? "dissertativas" : "objetivas";
  const contexto_texto = contexto ? `Utilize o seguinte contexto: \n${contexto}\n\n` : "";
  const prompt = `
${contexto_texto}
Corrija as seguintes questões ${tipo_texto} respondidas por um aluno. Baseie-se no gabarito fornecido e forneça uma análise detalhada de cada resposta:

Respostas do Aluno:
${respostas_aluno}

Gabarito:
${gabarito}

Para cada questão, avalie:
1. Se a resposta está correta ou não.
2. Para questões incorretas, explique o erro e forneça a resposta correta.
3. Para questões dissertativas, avalie a qualidade da resposta e sugira melhorias.
`;
  if (!apiKey) {
    console.error("API Key não fornecida.");
    return "";
  }
  const client = getOpenaiClient(apiKey);
  try {
    const response = await client.chat.completions.create({
      model: "gpt-3.5-turbo",
      messages: [
        { role: "system", content: "Você é um assistente especializado em correção de questões educacionais." },
        { role: "user", content: prompt },
      ],
    });
    return response.choices[0].message?.content || "";
  } catch (error) {
    console.error("Erro ao corrigir questões:", error);
    return "";
  }
}

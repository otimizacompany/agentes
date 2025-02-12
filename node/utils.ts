// utils.ts

/**
 * Redireciona o navegador para a URL atual com os parâmetros de query informados.
 * 
 * @param params - Objeto contendo os parâmetros a serem adicionados à query string.
 */
export function redirectWithQueryParams(params: Record<string, any>): void {
    const queryString = Object.keys(params)
      .map(key => `${encodeURIComponent(key)}=${encodeURIComponent(params[key])}`)
      .join("&");
    const newUrl = `${window.location.origin}${window.location.pathname}?${queryString}`;
    window.location.href = newUrl;
  }
  
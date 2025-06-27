// utils/api.ts

export async function apiFetch(url: string, options: any = {}) {
  const config = useRuntimeConfig()
  const baseUrl = config.public.apiBaseUrl || 'http://backend:8000'
  const fullUrl = url.startsWith('/') ? `${baseUrl}${url}` : url

  try {
    console.log(`[apiFetch] URL: ${fullUrl}`, options)

    const response = await fetch(fullUrl, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
    })

    if (!response.ok && response.status !== 204) {
      const errorText = await response.text().catch(() => 'Неизвестная ошибка')
      throw new Error(`HTTP error! Status: ${response.status}, Detail: ${errorText}`)
    }

    return response.status === 204 ? response : await response.json()
  } catch (err) {
    console.error(`Ошибка в apiFetch для ${url}:`, err)
    throw err
  }
}

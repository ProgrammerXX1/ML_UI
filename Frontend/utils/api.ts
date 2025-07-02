// utils/api.ts

export async function apiFetch(url: string, options: any = {}) {
  const config = useRuntimeConfig()
  const baseUrl = config.public.apiUrl
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
// utils/api.ts
export function authCheck(): string {
  const token = localStorage.getItem('access_token')
  if (!token) throw new Error('NO_TOKEN')
  return token
}

export async function fetchWithToken<T>(url: string, options: RequestInit = {}): Promise<T> {
  const token = authCheck()
  return await apiFetch(url, {
    ...options,
    headers: {
      Authorization: `Bearer ${token}`,
      ...(options.headers || {})
    }
  })
}

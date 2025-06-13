export default defineNuxtPlugin((nuxtApp) => {
    const baseUrl = 'http://localhost:3000'
    const route = useRoute()

    useHead({
        link: [
            {
                rel: 'canonical',
                href: `${baseUrl}${route.path}`
            }
        ]
    })
})

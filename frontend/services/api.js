import axios from "axios";

const baseUrl = process.env.NEXT_PUBLIC_API_URL;

const urls = {
    SHORTEN_URL_ENDPOINT: `${baseUrl}/shorten`,
    STATS_ENDPOINT: `${baseUrl}/stats`,
    REDIRECT_URL_ENDPOINT: `${baseUrl}/`,
    HEALTH_CHECK_ENDPOINT: `${baseUrl}/_healthcheck`,
};

const apiService = (() => {
    const httpInstance = axios.create();

    return {
        setHttpHeaders: (token) => {
            httpInstance.defaults.headers.Authorization = `${token}`;
        },
        removeHttpHeaders: () => {
            httpInstance.defaults.headers.Authorization = "";
        },
        shortenUrl: (url) =>
            httpInstance
                .post(urls.SHORTEN_URL_ENDPOINT, { url })
                .then((response) => response.data),
        getStats: () =>
            httpInstance
                .get(urls.STATS_ENDPOINT)
                .then((response) => response.data),
        getStat: (hash) =>
            httpInstance
                .get(`${urls.STATS_ENDPOINT}/${hash}`)
                .then((response) => response.data),
        getStatByOriginalUrl: (url) =>
            httpInstance.post(`${urls.STATS_ENDPOINT}/find`, { url }),
        redirectByHash: (hash) =>
            httpInstance
                .get(`${urls.REDIRECT_URL_ENDPOINT}/${hash}`)
                .then((response) => response),
        getApiHealthCheck: () => httpInstance.get(urls.HEALTH_CHECK_ENDPOINT),
        post: httpInstance.post,
        get: httpInstance.get,
        delete: httpInstance.delete,
        put: httpInstance.put,
    };
})();

export default apiService;

import Head from "next/head";
import apiService from "services/api";
import { useState, useEffect } from "react";

const StatsPage = () => {
    const [stats, setStats] = useState([]);
    const [hashInput, setHashInput] = useState("");
    const [loading, setLoading] = useState(false);
    const [urlStat, setUrlStat] = useState({});

    const getStatByHash = () => {
        setLoading(true);
        apiService.getStat(hashInput).then((response) => {
            setUrlStat(response.data);
            setLoading(false);
        });
    };

    useEffect(() => {
        const getStats = async () => {
            const response = await apiService.getStats();
            setStats(response.data);
        };

        getStats();
    }, []);

    return (
        <>
            <Head>
                <title>Url Shortener</title>
            </Head>

            <main>
                <div className="m-5">
                    <div className="flex rounded-lg border-2 border-gray-200">
                        <table className="table-auto divide-y divide-gray-200 w-full">
                            <thead class="bg-gray-50">
                                <tr>
                                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                        Date Created
                                    </th>
                                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                        URL
                                    </th>
                                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                        Shortened URL
                                    </th>
                                </tr>
                            </thead>
                            <tbody className="bg-white divide-y divide-gray-200">
                                {stats.map((stat, index) => (
                                    <tr key={index}>
                                        <td className="px-6 py-4 whitespace-nowrap">
                                            {stat.datetime_created}
                                        </td>
                                        <td className="px-6 py-4 whitespace-nowrap">
                                            {stat.url}
                                        </td>
                                        <td className="px-6 py-4 whitespace-nowrap">
                                            {stat.shortened_url}
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </div>
                <div className="flex flex-col items-center m-5">
                    <div className="text-xl">Search url statistics by hash</div>
                    <div className="flex">
                        <input
                            className="bg-gray-100 px-4 py-2 border-2 border-purple-300 focus:outline-purple-500 text-center text-lg rounded-l-lg rounded-r-none"
                            placeholder="URL Hash"
                            value={hashInput}
                            onChange={(e) => setHashInput(e.target.value)}
                        />
                        <button
                            className="bg-purple-600 hover:bg-purple-700 text-gray-50 rounded-r-lg px-5 font-semibold -ml-1"
                            onClick={getStatByHash}
                        >
                            {loading ? (
                                <svg
                                    role="status"
                                    className="h-6 w-6 animate-spin mr-2 text-purple-300 fill-gray-50"
                                    viewBox="0 0 100 101"
                                    fill="none"
                                    xmlns="http://www.w3.org/2000/svg"
                                >
                                    <path
                                        d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z"
                                        fill="currentColor"
                                    />
                                    <path
                                        d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z"
                                        fill="currentFill"
                                    />
                                </svg>
                            ) : (
                                "Go"
                            )}
                        </button>
                    </div>
                    {Boolean(Object.keys(urlStat).length) && (
                        <div className="bg-gray-100 rounded-lg px-10 py-5 flex flex-col items-center relative mt-5">
                            <div className="flex flex-col items-center">
                                <div className="flex space-x-5">
                                    <div className="flex flex-col">
                                        <div className="flex justify-between space-x-3">
                                            <span>Shortened URL</span>
                                            <span>:</span>
                                        </div>
                                        <div className="flex justify-between space-x-3">
                                            <span>Times clicked</span>
                                            <span>:</span>
                                        </div>
                                        <div className="flex justify-between space-x-3">
                                            <span>Datetime created</span>
                                            <span>:</span>
                                        </div>
                                        <div className="flex justify-between space-x-3">
                                            <span>Original URL</span>
                                            <span>:</span>
                                        </div>
                                    </div>
                                    <div className="flex flex-col">
                                        <span>{urlStat.shortened_url}</span>
                                        <span>{urlStat.number_of_clicks}</span>
                                        <span>{urlStat.datetime_created}</span>
                                        <span>{urlStat.url}</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    )}
                </div>
            </main>
        </>
    );
};

export default StatsPage;

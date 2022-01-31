import Head from "next/head";
import { useState } from "react";

import { HiOutlineClipboard } from "react-icons/hi";

import apiService from "services/api";

export default function Home() {
    const [urlInput, setUrlInput] = useState("");
    const [hash, setHash] = useState("");
    const [loading, setLoading] = useState(false);

    const shortenUrl = () => {
        setLoading(true);
        apiService
            .shortenUrl(urlInput)
            .then((response) => {
                setHash(response.data.shortened_url);
                setLoading(false);
            })
            .catch(() => setLoading(false));
        // convert to try catch finally (setloading(false))
    };

    return (
        <>
            <Head>
                <title>Url Shortener</title>
            </Head>

            <main>
                <div className="h-screen flex items-center justify-center">
                    <div className="flex flex-col space-y-5 items-center">
                        <div className="flex">
                            <input
                                className="bg-gray-100 px-4 py-2 border-2 border-purple-300 focus:outline-purple-500 text-center text-lg rounded-l-lg rounded-r-none"
                                placeholder="URL to shorten"
                                value={urlInput}
                                onChange={(e) => setUrlInput(e.target.value)}
                            />
                            <button
                                className="bg-purple-600 hover:bg-purple-700 text-gray-50 rounded-r-lg px-5 font-semibold -ml-1"
                                onClick={shortenUrl}
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

                        {hash && (
                            <div className="bg-gray-100 rounded-lg px-10 py-5 flex flex-col items-center relative">
                                <button
                                    className="hover:bg-gray-200 rounded p-1 absolute top-1 right-1"
                                    {...(!hash ? { disabled: true } : {})}
                                    onClick={() => {
                                        navigator.clipboard.writeText(hash);
                                    }}
                                >
                                    <HiOutlineClipboard className="text-purple-500 w-6 h-6" />
                                </button>
                                <div>
                                    Shortened URL:{" "}
                                    <a
                                        className="text-purple-500"
                                        target="_blank"
                                        href={hash}
                                        rel="noreferrer"
                                    >
                                        {hash}
                                    </a>
                                </div>
                            </div>
                        )}
                    </div>
                </div>
            </main>
        </>
    );
}

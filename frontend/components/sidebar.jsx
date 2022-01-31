import Link from "next/link";
import { useRouter } from "next/router";

import { toast } from "react-toastify";
import { BsGraphDown } from "react-icons/bs";
import { HiOutlineHome } from "react-icons/hi";
import { RiHeartAddFill } from "react-icons/ri";

import apiService from "services/api";

const Sidebar = () => {
    const { pathname } = useRouter();

    const sidebarItemClassName = (targetPath) => {
        return `p-3 relative ${
            pathname === targetPath ? "bg-purple-500" : "bg-gray-100"
        } group hover:bg-purple-500 rounded-lg`;
    };

    const sidebarIconClassName = (targetPath) => {
        return `w-6 h-6 group-hover:text-gray-50 ${
            pathname === targetPath ? "text-gray-100" : "text-purple-500"
        }`;
    };

    const sidebarItemTextClassName =
        "group-hover:flex hidden absolute top-1/2 -translate-y-1/2 left-20 bg-gray-100 px-5 py-2 rounded-lg text-purple-500 font-semibold ";

    const checkHealth = () =>
        apiService
            .getApiHealthCheck()
            .then(() => toast.success("API is healthy"))
            .catch(() => toast.error("API is dead"));

    return (
        <div className="h-screen left-0 top-0 shadow-lg bg-gray-200 py-20">
            <div className="flex-col flex items-center space-y-5 px-5">
                <Link href="/">
                    <a className={sidebarItemClassName("/")}>
                        <HiOutlineHome className={sidebarIconClassName("/")} />
                        <span className={sidebarItemTextClassName}>Home</span>
                    </a>
                </Link>

                <Link href="/stats">
                    <a className={sidebarItemClassName("/stats")}>
                        <BsGraphDown
                            className={sidebarIconClassName("/stats")}
                        />
                        <span className={sidebarItemTextClassName}>
                            Statistics
                        </span>
                    </a>
                </Link>
                <button
                    className={sidebarItemClassName()}
                    onClick={checkHealth}
                >
                    <RiHeartAddFill className={sidebarIconClassName()} />
                    <span
                        className={
                            sidebarItemTextClassName + "whitespace-nowrap"
                        }
                    >
                        Health Check
                    </span>
                </button>
            </div>
        </div>
    );
};

export default Sidebar;

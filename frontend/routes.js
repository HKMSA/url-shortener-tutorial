import { BsGraphDown } from "react-icons/bs";
import { HiOutlineHome } from "react-icons/hi";
import { RiHeartAddFill } from "react-icons/ri";

export const routes = [
    {
        urlPath: "/",
        name: "Home",
        exact: true,
        icon: HiOutlineHome,
    },
    {
        urlPath: "stats",
        name: "Stats",
        icon: BsGraphDown,
    },
    {
        urlPath: "/health-check",
        name: "Health Check",
        icon: RiHeartAddFill,
    },
];

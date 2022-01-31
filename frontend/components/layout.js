import Sidebar from "./sidebar";

const Layout = ({ children }) => (
    <div className="flex">
        <Sidebar />
        <div className="flex-grow">{children}</div>
    </div>
);

export default Layout;

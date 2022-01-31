import '../styles/globals.css'
import { Layout } from "components";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

function MyApp({ Component, pageProps }) {
    return (
        <Layout>
            <ToastContainer />
            <Component {...pageProps} />
        </Layout>
    );
}

export default MyApp

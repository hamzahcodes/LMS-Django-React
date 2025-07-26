import { Navigate } from "react-router-dom";
import { useAuthStore } from "../store/auth";

export default function PrivateRoute({ children }) {
    const isLoggedIn = useAuthStore.getState().isLoggedIn()

    return isLoggedIn ? <>{children} </> : <Navigate to={'/login'} />
}
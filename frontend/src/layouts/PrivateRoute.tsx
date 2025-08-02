import type { ReactNode } from "react";
import { Navigate } from "react-router-dom";
import { useAuthStore } from "../store/auth";

type PrivateProps = {
    children: ReactNode
}
export default function PrivateRoute({ children }: PrivateProps) {
    const isLoggedIn = useAuthStore.getState().isLoggedIn()

    return isLoggedIn ? <>{children} </> : <Navigate to={'/login'} />
}
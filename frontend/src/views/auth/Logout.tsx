import { useEffect } from "react";
import { logout } from "../../utils/auth";
import { Link } from "react-router-dom";

export default function Logout() {
    useEffect(() => {
        logout()
    }, [])

    return (
        <div className="min-h-screen flex items-center justify-center bg-gray-100">
            <div className="bg-white p-8 rounded-xl shadow-md text-center w-80">
                <h2 className="text-xl font-semibold mb-6">You have been logged out</h2>
                <div className="flex flex-col gap-4">
                    <Link to="/login">
                        <button className="w-full bg-blue-500 hover:bg-blue-600 text-white py-2 px-4 rounded">
                        Login
                        </button>
                    </Link>
                    <Link to="/register">
                        <button className="w-full bg-gray-300 hover:bg-gray-400 text-gray-800 py-2 px-4 rounded">
                        Register
                        </button>
                    </Link>
                </div>
            </div>
        </div>
    );
}
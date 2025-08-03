import { useState } from "react"
import apiInstance from "../../utils/axios";

export default function ForgotPassword() {
    const [ email, setEmail ] = useState<string>('');
    const [ emailSent, setEmailSent ] = useState<string>('');
    const [ isLoading, setIsLoading ] = useState<boolean>(false);

    async function handleSubmit(e: { preventDefault: () => void; }) {
        e.preventDefault()
        setIsLoading(true)

        try {
            const response = await apiInstance.get(`user/password-reset/${email}/`)
            console.log(response.data)
            setEmailSent('Password Reset E-mail sent')
        } catch (error) {
            console.log(error)
        } finally {
            setIsLoading(false)
        }
    }

    return (
        <div className="flex items-center justify-center min-h-screen bg-gray-100">
            <div className="w-full max-w-md p-6 bg-white rounded-2xl shadow-lg">
                <h2 className="text-2xl font-bold text-center text-gray-800 mb-6">Forgot Password</h2>
                <form onSubmit={handleSubmit} className="space-y-4">

                    {/* Email */}
                    <div>
                        <label className="block text-gray-700 mb-1">Email</label>
                        <input
                            type="email"
                            name="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400"
                            placeholder="Enter your email"
                        />
                        {emailSent && (
                            <p className="text-blue-900 text-sm mt-1">{emailSent}</p>
                        )}
                    </div>

                    {/* Submit Button */}
                    <button
                        type="submit"
                        disabled={isLoading}
                        className={`w-full py-2 text-white rounded-lg transition cursor-pointer ${isLoading ? "bg-gray-400 cursor-not-allowed" : "bg-blue-500 hover:bg-blue-600"}`}
                    >
                        {isLoading ? "Submitting..." : "Reset Password"}
                    </button>

                </form>
            </div>
        </div>
    )
}
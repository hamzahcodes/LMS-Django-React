import { useState } from "react"
import { useSearchParams, useNavigate } from "react-router-dom";
import apiInstance from "../../utils/axios";

type passwordReset = {
    password: string,
    confirmPassword: string,
}

export default function CreateNewPassword() {
    const navigate = useNavigate()
    const [ formData, setFormData ] = useState<passwordReset>({
        password: "",
        confirmPassword: ""
    });

    type passwordResetErrors = {
        [K in keyof passwordReset] ?: string
    }
    const [ errors, setErrors ] = useState<passwordResetErrors>({
        password: "",
        confirmPassword: ""
    });

    const [ isLoading, setIsLoading ] = useState<boolean>(false);

    function handleChange(e: { target: { name: string, value: string } }) {
        setFormData({
            ...formData,
            [e.target.name] : e.target.value
        })
    }

    const [ searchParams ] = useSearchParams()
    const otp = searchParams.get('otp')
    const uuidb64 = searchParams.get('uuidb64')
    const refresh_token = searchParams.get('refresh_token')

    async function handleSubmit(e: { preventDefault: () => void }) {
        e.preventDefault()
        
        if (formData.password.length < 6) {
            setErrors({
                password: 'Password length should at least be 6',
                confirmPassword: ''
            })
            return
        }
        if (formData.password !== formData.confirmPassword) {
            setErrors({
                password: "",
                confirmPassword: "Passwords do not match"
            })
            return
        }

        setIsLoading(true)
        try {
            const formData = new FormData()
            formData.append('otp', otp!);
            formData.append('uuidb64', uuidb64!)
            formData.append('refresh_token', refresh_token!)

            const response = await apiInstance.post('user/password-change/', formData)
            console.log(response.data)
            navigate('/login')
        } catch (error) {
            console.log(error)
        } finally {
            setIsLoading(false)
        }
    }

    return (
         <div className="flex items-center justify-center min-h-screen bg-gray-100">
            <div className="w-full max-w-md p-6 bg-white rounded-2xl shadow-lg">
                <h2 className="text-2xl font-bold text-gray-800 mb-6">Create New Password</h2>
                <form onSubmit={handleSubmit} className="space-y-4">

                    {/* Password */}
                    <div>
                        <label className="block text-gray-700 mb-1">Enter New Password</label>
                        <input
                            type="password"
                            name="password"
                            value={formData.password}
                            onChange={handleChange}
                            className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400"
                            placeholder="Enter your password"
                        />
                        {errors && errors.password && (
                            <p className="text-red-500 text-sm mt-1">{errors.password}</p>
                        )}
                    </div>

                    {/* Confirm Password */}
                    <div>
                        <label className="block text-gray-700 mb-1">Confirm New Password</label>
                        <input
                            type="password"
                            name="confirmPassword"
                            value={formData.confirmPassword}
                            onChange={handleChange}
                            className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400"
                            placeholder="Confirm Your Password"
                        />
                        {errors && errors.confirmPassword && (
                            <p className="text-red-500 text-sm mt-1">{errors.confirmPassword}</p>
                        )}
                    </div>

                    {/* Submit Button */}
                    <button
                        type="submit"
                        disabled={isLoading}
                        className={`w-full py-2 text-white rounded-lg transition cursor-pointer ${isLoading ? "bg-gray-400 cursor-not-allowed" : "bg-blue-500 hover:bg-blue-600"}`}
                    >
                        {isLoading ? "Submitting..." : "Change Password"}
                    </button>

                </form>
            </div>
        </div>
    )
}
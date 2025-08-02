import { useState } from "react";
import { login, type ApiResponse, type LoginResponse, type UserLoginModel } from "../../utils/auth";
import { Link, useNavigate } from "react-router-dom";

export default function Login() {
    const navigate = useNavigate();
    const [formData, setFormData] = useState<UserLoginModel>({
        email: "",
        password: "",
    });
    type UserLoginErrors = {
        [K in keyof UserLoginModel]?: string;
    };
    const [errors, setErrors] = useState<UserLoginErrors>({});

    const [ isLoading, setIsLoading ] = useState<boolean>(false);

    const handleChange = (e: { target: { name: string; value: string }; }) => {
        console.log(e.target.name, e.target.value)
        setFormData({
            ...formData,
            [e.target.name]: e.target.value,
        });
    };

    const validate = () => {
        const newErrors: UserLoginErrors = {};

        if (!formData.email) newErrors.email = "Email is required";
        if (formData.password.length < 6) newErrors.password = "Password must be at least 6 characters";
        
        return newErrors;
    };

    const handleSubmit = async (e: { preventDefault: () => void; }) => {
        e.preventDefault();
        const validationErrors = validate();
        console.log(validationErrors)
        if (Object.keys(validationErrors).length > 0) {
            setErrors(validationErrors);
        } else {
            setErrors({});
            console.log("Form submitted:", formData);
            setIsLoading(true) 
            try {
                const response: ApiResponse<LoginResponse> = await login(formData)
                
                if(response.data) {
                    console.log(response.data.access)
                    setFormData({ email: "", password: "" })
                    alert('User Created Successfully!')
                    navigate('/')
                } else {
                    const error = response.error?.response?.data
                    console.log(response.error?.response)
                    setErrors({
                        email: error.detail,
                        password: '',
                    })
                }
            } catch (error) {
                console.log(error)
            } finally {
                setIsLoading(false)
            } 
        }
    };

    return (
        <div className="flex items-center justify-center min-h-screen bg-gray-100">
            <div className="w-full max-w-md p-6 bg-white rounded-2xl shadow-lg">
                <h2 className="text-2xl font-bold text-center text-gray-800 mb-6">Sign in</h2>
                <form onSubmit={handleSubmit} className="space-y-4">

                    {/* Email */}
                    <div>
                        <label className="block text-gray-700 mb-1">Email</label>
                        <input
                            type="email"
                            name="email"
                            value={formData.email}
                            onChange={handleChange}
                            className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400"
                            placeholder="Enter your email"
                        />
                        {errors && errors.email && (
                            <p className="text-red-500 text-sm mt-1">{errors.email}</p>
                        )}
                    </div>

                    {/* Password */}
                    <div>
                        <label className="block text-gray-700 mb-1">Password</label>
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


                    {/* Submit Button */}
                    <button
                        type="submit"
                        disabled={isLoading}
                        className={`w-full py-2 text-white rounded-lg transition cursor-pointer ${isLoading ? "bg-gray-400 cursor-not-allowed" : "bg-blue-500 hover:bg-blue-600"}`}
                    >
                        {isLoading ? "Submitting..." : "Login"}
                    </button>

                    <p className="text-center">Don't have an account? <Link to={'/register'} className="text-blue-500">Register</Link></p>
                </form>
            </div>
        </div>
    );
}

import { useState } from "react";
import type { ApiResponse, RegisterResponse, UserRegisterModel } from "../../utils/auth";
import { useNavigate, Link } from "react-router-dom";
import { register } from "../../utils/auth";

export default function Register() {

    const navigate = useNavigate()
    const [formData, setFormData] = useState<UserRegisterModel>({
        email: "",
        full_name: "",
        password: "",
        password2: "",
    });
    type UserRegisterErrors = {
        [K in keyof UserRegisterModel]?: string;
    };
    const [errors, setErrors] = useState<UserRegisterErrors>({});

    const [ isLoading, setIsLoading ] = useState<boolean>(false);

    const handleChange = (e: { target: { name: string; value: string }; }) => {
        console.log(e.target.name, e.target.value)
        setFormData({
            ...formData,
            [e.target.name]: e.target.value,
        });
    };

    const validate = () => {
        const newErrors: UserRegisterErrors = {};

        if (!formData.email) newErrors.email = "Email is required";
        if (!formData.full_name) newErrors.full_name = "Username is required";
        if (formData.password.length < 6) newErrors.password = "Password must be at least 6 characters";
        if (formData.password !== formData.password2) newErrors.password2 = "Passwords do not match";
        
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
                const response: ApiResponse<RegisterResponse> = await register(formData)
                // console.log(response.error?.response?.data)
                
                if(response.data) {
                    console.log(response.data.email)
                    setFormData({full_name: "", email: "", password: "", password2: ""})
                    alert('User Created Successfully!')
                    navigate('/login')
                } else {
                    const error: UserRegisterErrors = response.error?.response?.data
                    console.log(error.email)
                    setErrors({
                        full_name: error.full_name,
                        email: error.email,
                        password: error.password,
                        password2: error.password2
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
                <h2 className="text-2xl font-bold text-center text-gray-800 mb-6">Create an Account</h2>
                <form onSubmit={handleSubmit} className="space-y-4">

                    {/* Fullname */}
                    <div>
                        <label className="block text-gray-700 mb-1">Full Name</label>
                        <input
                            type="text"
                            name="full_name"
                            value={formData.full_name}
                            onChange={handleChange}
                            className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400"
                            placeholder="Enter your Full Name"
                        />
                        {errors && errors.full_name && (
                            <p className="text-red-500 text-sm mt-1">{errors.full_name}</p>
                        )}
                    </div>
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

                    {/* Confirm Password */}
                    <div>
                        <label className="block text-gray-700 mb-1">Confirm Password</label>
                        <input
                            type="password"
                            name="password2"
                            value={formData.password2}
                            onChange={handleChange}
                            className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400"
                            placeholder="Re-enter your password"
                        />
                        {errors && errors.password2 && (
                        <p className="text-red-500 text-sm mt-1">
                            {errors.password2}
                        </p>
                        )}
                    </div>

                    {/* Submit Button */}
                    <button
                        type="submit"
                        disabled={isLoading}
                        className={`w-full py-2 text-white rounded-lg transition cursor-pointer ${isLoading ? "bg-gray-400 cursor-not-allowed" : "bg-blue-500 hover:bg-blue-600"}`}
                    >
                        {isLoading ? "Submitting..." : "Register"}
                    </button>

                    <p className="text-center">Already have an account? <Link to={'/login'} className="text-blue-500">Login</Link></p>
                </form>
            </div>
        </div>
    );
}

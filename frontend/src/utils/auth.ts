// import { useAuthStore } from "../store/auth";
import { jwtDecode } from "jwt-decode";
import { useAuthStore, type AllUserData } from "../store/auth";
import apiInstance from "./axios";
// import { jwtDecode } from "jwt-decode";
import Cookie from "js-cookie";

export interface UserLoginModel {
    email: string;
    password: string;
}

export interface UserRegisterModel {
    full_name: string,
    email: string,
    password: string,
    password2: string
}

type RegisterResponse = UserRegisterModel

export type LoginResponse = {
    access: string,
    refresh: string
}

type ApiResponse<T> = {
    data: T | null,
    error: string
}

export async function login(user:UserLoginModel): Promise<ApiResponse<LoginResponse>> {
    try {
        const { data, status } = await apiInstance.post<LoginResponse>('user/token', user)
        if (status === 200) {
            console.log(data.access)
            alert('Login Successfull')
        }
        const result: ApiResponse<LoginResponse> = {
            data: data,
            error: ''
        }
        return result
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    } catch (error: any) {
        console.log(error)
        const result: ApiResponse<LoginResponse> = {
            data: null,
            error: error.response.data?.detail || 'Something went wrong'
        }
        return result
    }
}

export async function register(newUser:UserRegisterModel): Promise<ApiResponse<RegisterResponse>> {
    try {
        const { data } = await apiInstance.post<RegisterResponse>('user/register', newUser)
        
        const loginCred: UserLoginModel = {
            email: data.email,
            password: data.password
        }
        await login( loginCred )
        alert('Registration Successfull')

        const result: ApiResponse<RegisterResponse> = {
            data: data,
            error: ''
        }
        return result
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    } catch (error) {
        const result: ApiResponse<RegisterResponse> = {
            data: null,
            error: 'Something went wrong'
        }
        return result
    }
}

export async function logout() {
    Cookie.remove("accessToken")
    Cookie.remove("refreshToken")

    useAuthStore.getState().setUser(null)
    alert('You have been logged out')
}

export async function setUser() {
    const accessToken = Cookie.get("accessToken")
    const refreshToken = Cookie.get("refreshToken")

    if(!accessToken || !refreshToken) {
        alert('Token does not exist')
        return
    }

    if(isAccessTokenExpired(accessToken)) {
        const response = await getRefreshedToken(refreshToken)
        setAuthUser(response.access, response.refresh)
    } else {
        setAuthUser(accessToken, refreshToken)
    }
}

export function setAuthUser(accessToken: string, refreshToken: string) {
    Cookie.set("accessToken", accessToken, {
        expires: 1,
        secure: true
    })

    Cookie.set("refreshToken", refreshToken, {
        expires: 7,
        secure: true
    })

    const user = jwtDecode(accessToken) ?? null
    if(user) {
        const userDetails: AllUserData = {
            user_id: user?.user_id || '',
            username: user?.username || ''
        }
        useAuthStore.getState().setUser(userDetails)
    }
    useAuthStore.getState().setLoading(false)
}

export async function getRefreshedToken(refreshToken:string) {
    try {
        const response = await apiInstance.post('user/token/refresh', {
            refresh: refreshToken
        })
        return response.data.refresh
    } catch (error) {
        console.log(error)
    }
}

export function isAccessTokenExpired(accessToken:string): boolean {
    try {
        const decodedToken = jwtDecode(accessToken)
        if (decodedToken.exp) {
            return decodedToken.exp < Date.now() / 1000 || true
        }
        return true
    } catch (error) {
        console.log(error)
        return true
    }   
}
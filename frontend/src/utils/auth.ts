// import { useAuthStore } from "../store/auth";
import { jwtDecode } from "jwt-decode";
import { useAuthStore, type AllUserData } from "../store/auth";
import apiInstance from "./axios";
import Cookies from "js-cookie";
import type { AxiosError } from "axios";

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

export type RegisterResponse = UserRegisterModel

export type LoginResponse = {
    access: string,
    refresh: string
}

export type ApiResponse<T> = {
    data: T | null,
    error: AxiosError | null
}

export async function login(user:UserLoginModel): Promise<ApiResponse<LoginResponse>> {
    try {
        const { data, status } = await apiInstance.post<LoginResponse>('user/token', user)
        if (status === 200) {
            console.log(data.access)
            setAuthUser(data.access, data.refresh)
            alert('Login Successfull')
        }
        const result: ApiResponse<LoginResponse> = {
            data: data,
            error: null
        }
        return result
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    } catch (error: any) {
        console.log(error)
        const result: ApiResponse<LoginResponse> = {
            data: null,
            error: error || null
        }
        return result
    }
}

export async function register(newUser:UserRegisterModel): Promise<ApiResponse<RegisterResponse>> {
    try {
        const { data } = await apiInstance.post<RegisterResponse>('user/register/', newUser)
        
        // const loginCred: UserLoginModel = {
        //     email: data.email,
        //     password: data.password
        // }
        // console.log(loginCred)
        // await login( loginCred )

        const result: ApiResponse<RegisterResponse> = {
            data: data,
            error: null
        }
        return result
    } catch (error) {
        console.log((error as AxiosError).message)
        const result: ApiResponse<RegisterResponse> = {
            data: null,
            error: (error as AxiosError)
        }
        return result
    }
}

export async function logout() {
    Cookies.remove("accessToken", { secure: true })
    Cookies.remove("refreshToken", { secure: true })

    useAuthStore.getState().setUser(null)
    alert('You have been logged out')
}

export async function setUser() {
    const accessToken = Cookies.get("accessToken") || ''
    const refreshToken = Cookies.get("refreshToken") || ''

    if(accessToken?.length === 0 || refreshToken === 'undefined') {
        // alert('Token does not exist')
        return
    }

    if(typeof accessToken === 'string' && isAccessTokenExpired(accessToken)) {
        const response = await getRefreshedToken(refreshToken)
        setAuthUser(response?.data.access, response?.data.refresh)
    } else {
        setAuthUser(accessToken, refreshToken)
    }
}

export function setAuthUser(accessToken: string, refreshToken: string) {
    Cookies.set("accessToken", accessToken, {
        expires: 1,
        secure: true
    })

    Cookies.set("refreshToken", refreshToken, {
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
        const response = await apiInstance.post('user/token/refresh/', {
            refresh: refreshToken
        })
        return response
    } catch (error) {
        console.log(error)
    }
}

export function isAccessTokenExpired(accessToken:string): boolean {
    try {
        const decodedToken = jwtDecode(accessToken)
        if (decodedToken.exp) {
            return decodedToken.exp < Date.now() / 1000
        }
        return true
    } catch (error) {
        console.log(error)
        return true
    }   
}
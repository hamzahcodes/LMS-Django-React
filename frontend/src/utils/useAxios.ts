import axios, { type InternalAxiosRequestConfig } from "axios";
import { getRefreshedToken, isAccessTokenExpired, setAuthUser, type LoginResponse } from "./auth";
import Cookie from "js-cookie";
import { API_BASE_URL } from "./constants";

export async function useAxios() {
    const accessToken = Cookie.get('accessToken')!
    const refreshToken = Cookie.get('refreshToken')!

    const axiosInstance = axios.create({
        baseURL: API_BASE_URL,
        headers: {
            Authorization: `Bearer ${accessToken}`
        }
    })

    axiosInstance.interceptors.request.use(async (req: InternalAxiosRequestConfig) => {
        if(!isAccessTokenExpired(accessToken)) {
            return req
        }

        const response: LoginResponse = await getRefreshedToken(refreshToken)
        setAuthUser(response.access, response.refresh)
        req.headers['Authorization'] = `Bearer ${response.access}}`
        return req
    })

    return axiosInstance
}

export default useAxios
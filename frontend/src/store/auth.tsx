import { create } from "zustand";
import { mountStoreDevtool } from "simple-zustand-devtools";

export type AllUserData = {
    user_id: string;
    username?: string;
}

type AuthStore = {
    allUserData: AllUserData | null,
    loading: boolean,
    user: () => {
        user_id: string | null;
        username: string | null;
    },
    setUser: (user: AllUserData | null) => void,
    setLoading: (loading: boolean) => void,
    isLoggedIn: () => boolean
}

const useAuthStore = create<AuthStore>((set, get) => ({
    allUserData: null,
    loading: false,

    user: () => ({
        user_id: get().allUserData?.user_id || null,
        username: get().allUserData?.username || null,
    }),

    setUser: (user) => set({ allUserData: user }),

    setLoading: (loading) => set({ loading }),

    isLoggedIn: () => get().allUserData !== null,
}))

if (import.meta.env.DEV) {
    mountStoreDevtool("Store", useAuthStore);
}

export { useAuthStore }
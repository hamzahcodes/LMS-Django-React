import { useState, useEffect } from 'react'
import { setUser } from '../utils/auth'

export default function MainWrapper({ children }) {
    const [ loading, setLoading ] = useState(true)

    useEffect(() => {
        async function handler() {
            setLoading(true)

            await setUser()

            setLoading(false)
        }
        handler()
    }, [])

    return <>
        {loading ? null : children}
    </>
}
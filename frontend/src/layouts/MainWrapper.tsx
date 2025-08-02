import type { ReactNode } from 'react'
import { useState, useEffect } from 'react'
import { setUser } from '../utils/auth'

type WrapperProps = {
    children : ReactNode
}

export default function MainWrapper({ children }: WrapperProps) {
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
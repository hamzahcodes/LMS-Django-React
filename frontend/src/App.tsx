import { BrowserRouter, Routes, Route } from "react-router-dom"
import MainWrapper from "./layouts/MainWrapper"
// import PrivateRoute from "./layouts/PrivateRoute"
import Register from "./views/auth/Register"
import Login from "./views/auth/Login"
import Logout from "./views/auth/Logout"


export default function App() {
  return(
    <BrowserRouter>
      <MainWrapper>
        <Routes>
          <Route path="/register" element={<Register />}/>
          <Route path="/login" element={<Login />} />
          <Route path="/logout" element={<Logout />} />
        </Routes>
      </MainWrapper>
    </BrowserRouter>
  )  
}
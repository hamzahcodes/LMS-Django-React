import { BrowserRouter, Routes, Route } from "react-router-dom"
import MainWrapper from "./layouts/MainWrapper"
// import PrivateRoute from "./layouts/PrivateRoute"
import Register from "./views/auth/Register"
import Login from "./views/auth/Login"
import Logout from "./views/auth/Logout"
import ForgotPassword from "./views/auth/ForgotPassword"
import CreateNewPassword from "./views/auth/CreateNewPassword"


export default function App() {
  return(
    <BrowserRouter>
      <MainWrapper>
        <Routes>
          <Route path="/register" element={<Register />}/>
          <Route path="/login" element={<Login />} />
          <Route path="/logout" element={<Logout />} />
          <Route path="/forgot-password" element={<ForgotPassword />} />
          <Route path="/create-new-password" element={<CreateNewPassword />}/>
        </Routes>
      </MainWrapper>
    </BrowserRouter>
  )  
}
import React from 'react';
import { Layout, Menu } from 'antd';
import { Outlet, useNavigate, useLocation } from "react-router-dom";
import Chat from './pages/Chat';
import Prompt from './pages/Prompt';
import DragDrop from './pages/DragDrop';
import Home from './pages/Home'
const { Header, Footer, Content } = Layout;

export const loader = () => {
  return fetch("/session", {
    method: "POST",
    headers: {
      'Content-Type': 'application/json'
    }
  })
}

export const CHAT_ROUTE = "/chat"
export const CONTEXT_ROUTE = "/context"
export const PROMPT_ROUTE = "/prompt"


export const MenuItems = [
  { key: "/", label: "Home", element: <Home /> },
  { key: CHAT_ROUTE, label: "Chat", element: <Chat /> },
  { key: CONTEXT_ROUTE, label: "Add context", element: <DragDrop /> },
  { key: PROMPT_ROUTE, label: "Prompt", element: <Prompt /> },
]

const App: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation()
  return (
    <Layout className="layout" style={{ minHeight: "100vh" }}>
      <Header style={{ display: 'flex', alignItems: 'center' }}>
        <div className="demo-logo" />
        <Menu
          theme="dark"
          mode="horizontal"
          onClick={({ key }) => navigate(key)}
          selectedKeys={[location.pathname]}
          items={MenuItems.map(({ key, label }) => ({ key, label }))}
        />
      </Header>
      <Content style={{ padding: '0 50px' }}>
        <Outlet />
      </Content>
      <Footer style={{ textAlign: 'center' }}>GPT Playground</Footer>
    </Layout>
  );
};


export default App
import React from 'react'
import { Link } from 'react-router-dom'
import { CHAT_ROUTE, CONTEXT_ROUTE, PROMPT_ROUTE } from "./App"
const Home = () => {
    return <>
        <h3>Welcome to the GPT playground!</h3>
        <p>Go {<Link to={CHAT_ROUTE}>chat</Link>} with the model!
            If the model lacks context, {<Link to={CONTEXT_ROUTE}>add context</Link>} by uploading relevant documents.
            Prompts seem too restrictive? Head over to the {<Link to={PROMPT_ROUTE}>prompt manager</Link>} to create your own! </p>
    </>
}

export default Home
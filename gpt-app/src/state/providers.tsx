import React, { useState, PropsWithChildren } from "react"

type Source = {
    filename: string
    content: string
}
type Question = {
    question: string
    answer: string
    sources: Source[]
}
const initQuestions: Question[] = []
const chatContext = { questions: initQuestions, addQuestion: (update: Question) => { } }

export const ChatContext = React.createContext(chatContext)

export const ChatProviderComponent = ({ children }: PropsWithChildren) => {

    const updateContext = (contextUpdates: Question) =>
        setContext(currentContext => ({
            ...currentContext,
            questions: [contextUpdates, ...currentContext.questions], //show in reverse order
        })
        )

    const initState = {
        questions: initQuestions,
        addQuestion: updateContext
    }
    const [context, setContext] = useState(initState)

    return (
        <ChatContext.Provider value={context}>
            {children}
        </ChatContext.Provider>
    )
}

type Prompt = {
    prompt: string
    isEnabled: boolean
}

const initPrompt: Prompt[] = [{
    prompt: `Answer the question from the following context.
    
    {context}
    
    Question: {question}`,
    isEnabled: true
}]

const promptContext = {
    prompts: initPrompt,
    addPrompt: (update: Prompt) => { },
    updatePromptEnable: (value: boolean, index: number) => { }
}


export const PromptContext = React.createContext(promptContext)

export const PromptProviderComponent = ({ children }: PropsWithChildren) => {
    const addPrompt = (contextUpdates: Prompt) => {
        setContext(currentContext => ({
            ...currentContext,
            prompts: [...currentContext.prompts, contextUpdates]
        })
        )
    }

    const updatePromptEnable = (value: boolean, index: number) =>
        setContext(currentContext => ({
            ...currentContext,
            prompts: currentContext.prompts.map((v, i) => i === index ? { ...v, isEnabled: value } : { ...v, isEnabled: false })
        })
        )

    const initState = {
        prompts: initPrompt,
        addPrompt,
        updatePromptEnable
    }
    const [context, setContext] = useState(initState)
    return (
        <PromptContext.Provider value={context}>
            {children}
        </PromptContext.Provider>
    )
}
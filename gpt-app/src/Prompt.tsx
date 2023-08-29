import React, { useState } from 'react';
import { message, Button, Input, Switch, Row, Col, Modal } from 'antd';
import { useLoaderData } from "react-router-dom";

const { TextArea } = Input;

const submitPrompt = (sessionId: string, text: string) => {
    return fetch(`/session?existing_uid=${sessionId}`, {
        method: "POST", headers: {
            'Content-Type': 'application/json'
        }, body: JSON.stringify({ prompt: text })
    })
}
type Prompt = {
    prompt: string
    isEnabled: boolean
}

type ModalProps = {
    modalOpen: boolean,
    onOk: (a: string) => void,
    onCancel: () => void
}
const SubmitPromptModal: React.FC<ModalProps> = ({ modalOpen, onOk, onCancel }: ModalProps) => {
    const [text, setText] = useState("")
    return <Modal title="Create prompt" open={modalOpen} onOk={() => onOk(text)} onCancel={onCancel} >
        <p>Requires {"{question}"} to be put in the prompt</p>
        <TextArea value={text} onChange={v => setText(v.target.value)} />
    </Modal>
}

//type Props = { uid: string }
const ListPrompt: React.FC = () => {
    const uid = useLoaderData() as string;
    const [messageApi] = message.useMessage();
    const [modalOpen, setIsModalOpen] = useState(false)
    //const [isWaiting, setIsWaiting] = useState(false)
    const [prompts, setPrompts] = useState<Prompt[]>([{
        prompt: `Answer the question from the following context.
        
        {context}
        
        Question: {question}`,
        isEnabled: true
    }]) //append previous questions and answers
    const updateSwitch = (value: boolean, index: number) => {
        setPrompts(prompts => prompts.map((v, i) => i === index ? { ...v, isEnabled: value } : v))
        if (value) {
            submitPrompt(uid, prompts[index].prompt).then(() => {
                messageApi.open({
                    type: 'success',
                    content: 'Prompt instantiated',
                });
            }).catch(e => {
                messageApi.open({
                    type: 'error',
                    content: e,
                });
            })
        }
    }

    const handleOk = (text: string) => {
        setPrompts(prompts => [...prompts, { prompt: text, isEnabled: false }])
        setIsModalOpen(false)
    }
    const handleCancel = () => setIsModalOpen(false)
    return <><h3>Select prompts</h3>{prompts.map(({ prompt, isEnabled }, index) => (
        <Row key={index}>
            <Col span={4}>
                <Switch checked={isEnabled} onChange={v => updateSwitch(v, index)} />
            </Col>
            <Col span={20}>
                <p>{prompt}</p>
            </Col>
        </Row>
    ))}
        <Button onClick={() => setIsModalOpen(true)}>Create new Prompt</Button>
        <SubmitPromptModal modalOpen={modalOpen} onOk={handleOk} onCancel={handleCancel} />
    </>
}

export default ListPrompt;
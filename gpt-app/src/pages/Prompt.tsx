import React, { useState, useContext } from 'react';
import { message, Button, Input, Switch, Row, Col, Modal } from 'antd';
import { useRouteLoaderData } from "react-router-dom";
import { ROOT_ID } from '../utils/constants'
import { PromptContext } from '../state/providers';
const { TextArea } = Input;

const submitPrompt = (sessionId: string, text: string) => {
    return fetch(`/session?existing_uid=${sessionId}`, {
        method: "POST", headers: {
            'Content-Type': 'application/json'
        }, body: JSON.stringify({ prompt: text })
    })
}

type ModalProps = {
    modalOpen: boolean,
    onOk: (a: string) => void,
    onCancel: () => void
}
const SubmitPromptModal: React.FC<ModalProps> = ({ modalOpen, onOk, onCancel }: ModalProps) => {
    const [text, setText] = useState("")
    return <Modal title="Create prompt" open={modalOpen} onOk={() => onOk(text)} onCancel={onCancel} >
        <p>Requires {"{context}"} and {"{question}"} to be put in the prompt</p>
        <TextArea value={text} onChange={v => setText(v.target.value)} />
    </Modal>
}

const ListPrompt: React.FC = () => {
    const uid = useRouteLoaderData(ROOT_ID) as string;
    const [messageApi] = message.useMessage();
    const [modalOpen, setIsModalOpen] = useState(false)
    const { prompts, updatePromptEnable, addPrompt } = useContext(PromptContext)
    const updateSwitch = (value: boolean, index: number) => {
        updatePromptEnable(value, index)
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
        addPrompt({ prompt: text, isEnabled: false })
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